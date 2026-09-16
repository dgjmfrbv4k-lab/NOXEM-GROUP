/**
 * preparer-envois.mjs
 * ---------------------------------------------------------------------------
 * Prépare les e-mails de prospection, un par site, prêts à envoyer depuis
 * VOTRE messagerie.
 *
 * Pourquoi ce détour plutôt qu'un envoi automatique en masse : une boîte
 * professionnelle plafonne autour de quelques centaines d'envois par jour, et
 * un domaine récent qui dépasse ce seuil est classé en spam en quelques jours.
 * Un domaine grillé ne se répare pas. Cet outil vous fait gagner le temps de
 * rédaction, pas le temps d'envoi : vous restez l'expéditeur, à un rythme que
 * les filtres acceptent.
 *
 *   node outils/preparer-envois.mjs --sites cibles-lyon.json --quota 25
 *   node outils/preparer-envois.mjs --sites cibles-lyon.json --statut a_contacter
 *
 * Produit un dossier `envois/` contenant :
 *   - un fichier .eml par site : double-clic (ou glisser-déposer dans votre
 *     client de messagerie) ouvre le message déjà rédigé, images comprises ;
 *   - index.html : la console du jour, avec le suivi des envois.
 * ---------------------------------------------------------------------------
 */

import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { construire, versionTexte, SIGNATURE } from '../emails/build-email.mjs';

/** Encode un en-tête non ASCII selon la RFC 2047. */
export function encoderEntete(texte) {
  // eslint-disable-next-line no-control-regex
  if (/^[\x00-\x7F]*$/.test(texte)) return texte;
  return `=?UTF-8?B?${Buffer.from(texte, 'utf8').toString('base64')}?=`;
}

/** Découpe une chaîne base64 en lignes de 76 caractères (RFC 2045). */
export function plierBase64(base64) {
  return (base64.match(/.{1,76}/g) || []).join('\r\n');
}

/**
 * Construit un message complet au format RFC 5322, avec alternative texte,
 * version HTML et images liées.
 *
 * @param {{de:string, nomExpediteur:string, a:string, objet:string,
 *          texte:string, html:string, images:Array<{nom:string, donnees:Buffer}>}} message
 */
export function construireEml(message) {
  const limiteRacine = `noxem_${Date.now().toString(36)}_racine`;
  const limiteAlternative = `noxem_${Date.now().toString(36)}_alt`;
  const b64 = (t) => plierBase64(Buffer.from(t, 'utf8').toString('base64'));

  const lignes = [
    `From: ${encoderEntete(message.nomExpediteur)} <${message.de}>`,
    `To: ${message.a}`,
    `Subject: ${encoderEntete(message.objet)}`,
    `Date: ${new Date().toUTCString()}`,
    'MIME-Version: 1.0',
    // Ouvre le fichier comme un brouillon modifiable dans Outlook.
    'X-Unsent: 1',
    `Content-Type: multipart/related; type="multipart/alternative"; boundary="${limiteRacine}"`,
    '',
    `--${limiteRacine}`,
    `Content-Type: multipart/alternative; boundary="${limiteAlternative}"`,
    '',
    `--${limiteAlternative}`,
    'Content-Type: text/plain; charset=UTF-8',
    'Content-Transfer-Encoding: base64',
    '',
    b64(message.texte),
    '',
    `--${limiteAlternative}`,
    'Content-Type: text/html; charset=UTF-8',
    'Content-Transfer-Encoding: base64',
    '',
    b64(message.html),
    '',
    `--${limiteAlternative}--`,
    '',
  ];

  for (const image of message.images) {
    lignes.push(
      `--${limiteRacine}`,
      'Content-Type: image/png',
      'Content-Transfer-Encoding: base64',
      `Content-ID: <${image.nom}>`,
      `Content-Disposition: inline; filename="${image.nom}"`,
      '',
      plierBase64(image.donnees.toString('base64')),
      '',
    );
  }

  lignes.push(`--${limiteRacine}--`, '');
  return lignes.join('\r\n');
}

/** Nom de fichier sûr, sans accent ni caractère spécial. */
export function nomFichier(index, site) {
  const base = `${site.nom} ${site.ville}`
    .normalize('NFD').replace(/[̀-ͯ]/g, '')
    .replace(/[^a-zA-Z0-9]+/g, '-')
    .replace(/^-|-$/g, '')
    .slice(0, 60) || 'site';
  return `${String(index).padStart(3, '0')}-${base}.eml`;
}

/**
 * Sélectionne les sites à contacter : e-mail renseigné, statut voulu,
 * dans la limite du quota quotidien.
 */
export function selectionner(sites, { statut = 'a_contacter', quota = 25 } = {}) {
  return sites
    .filter((s) => s.contactEmail && s.contactEmail.includes('@'))
    .filter((s) => !statut || s.statut === statut)
    .slice(0, quota);
}

/** Valeurs de variables pour un site donné. */
export function valeursPour(site) {
  return {
    '[Prénom]': site.contactPrenom || 'Madame, Monsieur',
    '[nom du site]': site.nom || 'votre établissement',
    ...SIGNATURE,
  };
}

function principal() {
  const args = process.argv.slice(2);
  const lire = (cle, defaut) => {
    const i = args.indexOf(`--${cle}`);
    return i !== -1 && args[i + 1] ? args[i + 1] : defaut;
  };

  const fichierSites = lire('sites', '');
  if (!fichierSites) {
    console.error('Indiquez le fichier de sites : --sites cibles-lyon.json');
    console.error('(c\'est le fichier produit par outils/collecte-cibles.mjs, ou la sauvegarde JSON du CRM)');
    process.exit(1);
  }

  const quota = Number(lire('quota', 25));
  const statut = lire('statut', 'a_contacter');
  const dossier = lire('dossier', 'envois');

  const data = JSON.parse(readFileSync(fichierSites, 'utf8'));
  const tous = Array.isArray(data) ? data : data.sites || [];
  const retenus = selectionner(tous, { statut, quota });

  if (!retenus.length) {
    console.error(`Aucun site à contacter : ${tous.length} site(s) dans le fichier, mais aucun avec `
      + `une adresse e-mail et le statut « ${statut} ».`);
    console.error('Renseignez les adresses dans l\'onglet Prospection, puis réexportez la sauvegarde JSON.');
    process.exit(1);
  }

  if (!existsSync(dossier)) mkdirSync(dossier, { recursive: true });

  const images = ['email-borne.png', 'email-scene.png'].map((nom) => ({
    nom,
    donnees: readFileSync(new URL(`../emails/${nom}`, import.meta.url)),
  }));

  const prepares = [];
  retenus.forEach((site, i) => {
    const valeurs = valeursPour(site);
    const eml = construireEml({
      de: SIGNATURE['[Votre email]'],
      nomExpediteur: `${SIGNATURE['[Votre nom]']} — ${SIGNATURE['[Votre société]']}`,
      a: site.contactEmail,
      objet: 'Le gonflage gratuit pour vos clients, financé par l’État',
      texte: versionTexte(valeurs),
      html: construire(valeurs),
      images,
    });
    const fichier = nomFichier(i + 1, site);
    writeFileSync(`${dossier}/${fichier}`, eml);
    prepares.push({ fichier, site });
  });

  writeFileSync(`${dossier}/index.html`, consoleEnvoi(prepares, { quota, restants: tous.length }));

  console.log(`${prepares.length} e-mail(s) préparé(s) dans ${dossier}/`);
  console.log(`Ouvrez ${dossier}/index.html pour suivre vos envois du jour.`);
  console.log('\nChaque .eml s\'ouvre dans votre messagerie : vous relisez, vous envoyez.');
  console.log('Tenez-vous à ce quota quotidien : au-delà, votre domaine est classé en spam.');
}

/** Console de suivi : la liste du jour, cochable, avec le rappel du rythme. */
export function consoleEnvoi(prepares, { quota, restants }) {
  const lignes = prepares.map(({ fichier, site }, i) => `
      <tr>
        <td><input type="checkbox" id="c${i}"></td>
        <td><label for="c${i}"><strong>${site.nom || '(sans nom)'}</strong><br>
          <span class="doux">${[site.ville, site.typeSite].filter(Boolean).join(' — ')}</span></label></td>
        <td>${site.typeCee ? `<span class="type">${site.typeCee}</span>` : ''}</td>
        <td><a href="${fichier}">${fichier}</a></td>
      </tr>`).join('');

  return `<!DOCTYPE html>
<html lang="fr"><head><meta charset="UTF-8"><title>Envois du jour — Noxem Group</title>
<style>
 body{font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;color:#14202c;background:#f4f6f8;margin:0;padding:24px}
 .cadre{max-width:900px;margin:auto;background:#fff;border:1px solid #d9e0e7;border-radius:8px;padding:24px}
 h1{font-size:20px;margin:0 0 4px} .doux{color:#5b6b7b;font-size:13px}
 table{width:100%;border-collapse:collapse;margin-top:16px;font-size:14px}
 td,th{text-align:left;padding:9px 10px;border-bottom:1px solid #d9e0e7}
 .type{display:inline-block;background:#e6f5ee;color:#1b7f5a;font-weight:700;padding:2px 9px;border-radius:999px}
 .rappel{background:#fff8e8;border-left:4px solid #ffc24a;padding:12px 16px;border-radius:0 6px 6px 0;margin-top:20px;font-size:14px}
 a{color:#00868f}
</style></head><body><div class="cadre">
 <h1>Envois du jour</h1>
 <p class="doux">${prepares.length} e-mail(s) préparé(s) sur ${restants} site(s) au fichier. Quota retenu : ${quota} par jour.</p>
 <table><thead><tr><th></th><th>Site</th><th>Type</th><th>Message</th></tr></thead><tbody>${lignes}</tbody></table>
 <p class="rappel"><strong>Tenez le rythme.</strong> Chaque fichier s'ouvre dans votre messagerie :
 vous relisez, vous envoyez, vous cochez. Au-delà d'une trentaine d'envois par jour depuis un domaine
 récent, les filtres anti-spam classent le domaine entier — et cela ne se répare pas.
 Repassez les sites contactés au statut « Contacté » dans l'onglet Prospection avant la prochaine série.</p>
</div></body></html>`;
}

if (import.meta.url === `file://${process.argv[1]}`) principal();
