/**
 * verifier-domaine.mjs
 * ---------------------------------------------------------------------------
 * Diagnostic d'authentification e-mail d'un domaine : SPF, DKIM, DMARC, MX.
 *
 * C'est le contrôle à passer AVANT le premier envoi, et à repasser après
 * chaque modification DNS. Un domaine mal authentifié part en spam quel que
 * soit le contenu du message — et la réputation perdue ne se rachète pas.
 *
 *   node outils/verifier-domaine.mjs noxemgroup.com
 *
 * Les fonctions d'analyse sont séparées des appels DNS : elles prennent des
 * chaînes en entrée, ce qui les rend testables sans réseau.
 * ---------------------------------------------------------------------------
 */

import { promises as dns } from 'node:dns';

/** Hébergeurs reconnus à leur MX — utile pour savoir à qui demander quoi. */
export const HEBERGEURS = [
  [/mailspamprotection\.com$/i, 'SiteGround (souvent via un revendeur)'],
  [/aspmx.*google\.com$|googlemail\.com$/i, 'Google Workspace'],
  [/protection\.outlook\.com$/i, 'Microsoft 365'],
  [/mail\.ovh\.net$|mx\d+\.ovh\.net$/i, 'OVH'],
  [/gandi\.net$/i, 'Gandi'],
  [/ionos|1and1/i, 'IONOS'],
  [/zoho/i, 'Zoho Mail'],
  [/infomaniak/i, 'Infomaniak'],
  [/lws\.fr$|dnssmarthost/i, 'LWS'],
];

/** Déduit l'hébergeur mail à partir des serveurs MX. */
export function identifierHebergeur(mx) {
  for (const enregistrement of mx) {
    for (const [motif, nom] of HEBERGEURS) {
      if (motif.test(enregistrement.exchange || enregistrement)) return nom;
    }
  }
  return 'inconnu';
}

/**
 * Analyse un enregistrement SPF.
 * Le point qui compte en prospection : le mécanisme « all » final, et le
 * nombre de résolutions DNS (la limite est de 10, au-delà l'enregistrement
 * est invalide et SPF échoue silencieusement).
 */
export function analyserSpf(txts) {
  const spf = txts.filter((t) => /^v=spf1\b/i.test(t));
  if (!spf.length) {
    return { present: false, problemes: [['grave', 'Aucun enregistrement SPF. Les messages seront rejetés ou classés en spam.']] };
  }
  if (spf.length > 1) {
    return { present: true, brut: spf, problemes: [['grave', `${spf.length} enregistrements SPF : c'est invalide, SPF échoue entièrement. Il n'en faut qu'un.`]] };
  }
  const brut = spf[0];
  const all = (brut.match(/([-~+?])all\s*$/) || [])[1] || null;
  const includes = [...brut.matchAll(/include:(\S+)/g)].map((m) => m[1]);
  const problemes = [];

  if (all === '+') problemes.push(['grave', '« +all » autorise le monde entier à écrire en votre nom. À corriger immédiatement.']);
  else if (all === '~') problemes.push(['moyen', '« ~all » (softfail) : toléré au démarrage, à passer en « -all » une fois la liste des expéditeurs stabilisée.']);
  else if (!all) problemes.push(['moyen', 'Pas de mécanisme « all » final : le comportement par défaut est permissif.']);

  return { present: true, brut, all, includes, problemes };
}

/** Taille approximative d'une clé RSA DKIM, en bits, depuis son champ p=. */
export function tailleCleDkim(enregistrement) {
  const p = (String(enregistrement).match(/p=([A-Za-z0-9+/=]+)/) || [])[1];
  if (!p) return 0;
  const octets = Buffer.from(p, 'base64').length;
  // SubjectPublicKeyInfo : ~162 octets pour 1024 bits, ~294 pour 2048.
  if (octets < 100) return 0;
  return octets < 200 ? 1024 : 2048;
}

/** Analyse un enregistrement DKIM trouvé sur un sélecteur. */
export function analyserDkim(selecteur, enregistrement) {
  if (!enregistrement) {
    return { present: false, problemes: [['grave', 'Aucune clé DKIM trouvée sur les sélecteurs courants.']] };
  }
  const bits = tailleCleDkim(enregistrement);
  const problemes = [];
  // Une clé révoquée (p= vide) est un cas précis : ne pas la confondre avec
  // un enregistrement illisible, sinon le même défaut est signalé deux fois.
  if (/p=\s*(;|$)/.test(enregistrement)) {
    problemes.push(['grave', `Clé révoquée sur « ${selecteur} » (p= vide) : DKIM ne signe plus rien.`]);
  } else if (bits === 0) {
    problemes.push(['grave', `Le sélecteur « ${selecteur} » existe mais ne contient pas de clé publique exploitable.`]);
  } else if (bits === 1024) {
    problemes.push(['moyen', `Clé DKIM de 1024 bits sur le sélecteur « ${selecteur} ». Le standard actuel est 2048 bits : demandez la régénération à votre hébergeur.`]);
  }
  return { present: true, selecteur, bits, problemes };
}

/** Analyse l'enregistrement DMARC. */
export function analyserDmarc(txts) {
  const dmarc = txts.filter((t) => /^v=DMARC1\b/i.test(t));
  if (!dmarc.length) {
    return { present: false, problemes: [['grave', 'Aucun enregistrement DMARC. Sans lui, SPF et DKIM ne sont pas mis en application.']] };
  }
  const brut = dmarc[0];
  const politique = (brut.match(/\bp=(\w+)/) || [])[1] || 'none';
  const rua = (brut.match(/rua=mailto:([^;,\s]+)/) || [])[1] || '';
  const problemes = [];

  if (politique === 'none') {
    problemes.push(['moyen', '« p=none » : surveillance seule, aucune mise en application. Correct pour démarrer, à passer en « quarantine » après quelques semaines de rapports propres.']);
  }
  if (!rua) {
    problemes.push(['moyen', 'Pas d\'adresse de rapports (rua=) : vous ne voyez pas qui écrit en votre nom.']);
  }
  return { present: true, brut, politique, rua, problemes };
}

/**
 * Détecte les plateformes d'envoi déclarées dans le DNS (code de validation)
 * mais absentes du SPF. C'est le défaut le plus coûteux : la plateforme est
 * validée côté interface, l'envoi part, et il échoue à l'authentification.
 */
export function plateformesIncompletes(txts, spf) {
  const signatures = [
    [/^brevo-code:/i, 'Brevo', 'spf.brevo.com'],
    [/^sendinblue-code:/i, 'Brevo (ex-Sendinblue)', 'spf.brevo.com'],
    [/^google-site-verification=/i, 'Google', '_spf.google.com'],
    [/^MS=/i, 'Microsoft 365', 'spf.protection.outlook.com'],
    [/^mailgun-verification/i, 'Mailgun', 'mailgun.org'],
    [/^sendgrid/i, 'SendGrid', 'sendgrid.net'],
  ];
  const includes = (spf.includes || []).join(' ');
  const trouvees = [];
  for (const txt of txts) {
    for (const [motif, nom, attendu] of signatures) {
      if (motif.test(txt) && !includes.includes(attendu)) {
        trouvees.push({ nom, attendu });
      }
    }
  }
  return trouvees;
}

/** Interroge le DNS. Sélecteurs DKIM les plus répandus, dans l'ordre. */
export const SELECTEURS_DKIM = ['default', 'mail', 'dkim', 'brevo', 'selector1', 'selector2',
  'google', 'k1', 's1', 's2', 'smtp', 'zoho'];

export async function interroger(domaine) {
  const plat = (r) => r.map((x) => (Array.isArray(x) ? x.join('') : x));
  const sûr = async (promesse, repli) => { try { return await promesse; } catch (e) { return repli; } };

  const mx = await sûr(dns.resolveMx(domaine), []);
  const txts = plat(await sûr(dns.resolveTxt(domaine), []));
  const dmarcTxts = plat(await sûr(dns.resolveTxt(`_dmarc.${domaine}`), []));

  let dkim = { selecteur: null, enregistrement: null };
  for (const selecteur of SELECTEURS_DKIM) {
    const r = plat(await sûr(dns.resolveTxt(`${selecteur}._domainkey.${domaine}`), []));
    if (r.length) { dkim = { selecteur, enregistrement: r.join('') }; break; }
  }

  return { domaine, mx, txts, dmarcTxts, dkim };
}

/** Rapport lisible, problèmes classés du plus grave au plus bénin. */
export function rapport(brut) {
  const spf = analyserSpf(brut.txts);
  const dmarc = analyserDmarc(brut.dmarcTxts);
  const dkim = analyserDkim(brut.dkim.selecteur, brut.dkim.enregistrement);
  const incompletes = plateformesIncompletes(brut.txts, spf);

  const lignes = [`Domaine : ${brut.domaine}`,
    `Hébergeur mail : ${identifierHebergeur(brut.mx)}`,
    `MX : ${brut.mx.map((m) => m.exchange).join(', ') || 'aucun'}`,
    '',
    `SPF   : ${spf.present ? spf.brut : 'ABSENT'}`,
    `DKIM  : ${dkim.present ? `sélecteur « ${dkim.selecteur} », ${dkim.bits} bits` : 'ABSENT'}`,
    `DMARC : ${dmarc.present ? dmarc.brut : 'ABSENT'}`,
    ''];

  const tous = [...spf.problemes, ...dkim.problemes, ...dmarc.problemes];
  for (const { nom, attendu } of incompletes) {
    tous.push(['grave', `${nom} est validé dans le DNS mais absent du SPF. `
      + `Tout envoi via ${nom} échouera à l'authentification. Ajoutez « include:${attendu} » au SPF, ou retirez la validation si la plateforme n'est plus utilisée.`]);
  }

  const rang = { grave: 0, moyen: 1 };
  tous.sort((a, b) => rang[a[0]] - rang[b[0]]);

  if (!tous.length) lignes.push('Aucun défaut détecté. Le domaine est prêt.');
  else {
    lignes.push(`${tous.length} point(s) à traiter :`, '');
    for (const [gravite, texte] of tous) {
      lignes.push(`  [${gravite === 'grave' ? 'GRAVE' : 'moyen'}] ${texte}`);
    }
  }
  return lignes.join('\n');
}

async function principal() {
  const domaine = process.argv[2];
  if (!domaine) {
    console.error('Usage : node outils/verifier-domaine.mjs noxemgroup.com');
    process.exit(1);
  }
  console.log(rapport(await interroger(domaine)));
}

if (import.meta.url === `file://${process.argv[1]}`) {
  principal().catch((e) => { console.error(e.message); process.exit(1); });
}
