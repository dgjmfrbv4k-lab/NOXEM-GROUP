/**
 * analyser-liste.mjs
 * ---------------------------------------------------------------------------
 * Évalue une liste d'adresses e-mail AVANT de l'utiliser, et en extrait la
 * part exploitable.
 *
 * Pourquoi cet outil : une liste achetée ou récupérée coûte moins cher qu'une
 * collecte, mais une liste périmée coûte le domaine. Au-delà de 5 % de rebonds
 * durs, les fournisseurs dégradent la réputation de l'expéditeur ; au-delà de
 * 10 %, ils bloquent. Une liste à 40 % de rebonds ne se « nettoie pas en
 * envoyant » : elle grille l'expéditeur avant d'être nettoyée.
 *
 *   node outils/analyser-liste.mjs adresses.txt
 *   node outils/analyser-liste.mjs adresses.txt --sortie liste-propre.txt
 * ---------------------------------------------------------------------------
 */

import { readFileSync, writeFileSync } from 'node:fs';

/**
 * Fournisseurs fermés ou abandonnés. Une adresse qui y réside rebondit
 * presque à coup sûr.
 */
export const DOMAINES_MORTS = new Map([
  ['wanadoo.fr', 'marque abandonnée en 2006, boîtes largement inactives'],
  ['voila.fr', 'fermé par Orange en 2016'],
  ['club-internet.fr', 'fermé'],
  ['tiscali.fr', 'fermé'],
  ['libertysurf.fr', 'fermé'],
  ['worldonline.fr', 'fermé'],
  ['infonie.fr', 'fermé'],
  ['caramail.com', 'fermé'],
  ['9online.fr', 'fermé'],
  ['cegetel.net', 'très ancien, créations arrêtées'],
  ['neuf.fr', 'absorbé par SFR, très ancien'],
  ['numericable.fr', 'absorbé par SFR'],
  ['aol.com', 'quasi abandonné en France'],
]);

/** Messageries grand public : une administration n'y a pas d'adresse officielle. */
export const DOMAINES_GRAND_PUBLIC = new Set([
  'orange.fr', 'free.fr', 'laposte.net', 'yahoo.fr', 'yahoo.com', 'hotmail.fr',
  'hotmail.com', 'gmail.com', 'sfr.fr', 'outlook.fr', 'outlook.com', 'live.fr',
  'bbox.fr', 'msn.com', 'nordnet.fr',
]);

/**
 * Vocabulaire des points de contact d'établissement.
 * « affaires.generales » ou « services.techniques » sont des services, pas des
 * personnes : sans ce vocabulaire, la forme « mot.mot » les ferait passer pour
 * des noms propres et on écarterait de bonnes adresses.
 */
const INSTITUTIONNEL = new RegExp([
  'mairie', 'commune', 'ville', 'accueil', 'contact', 'secretariat', 'secrétariat',
  'affaires', 'generales', 'générales', 'direction', 'services?', 'techniques?',
  'urbanisme', 'cabinet', 'administration', 'dgs', 'courrier', 'info',
].join('|'));

/**
 * Prénoms les plus répandus dans l'administration française. Sert uniquement à
 * distinguer « jean.dupont » (une personne) de « cuisine.centrale » (un service).
 */
const PRENOMS = new Set(['jean', 'marie', 'pierre', 'michel', 'philippe', 'alain', 'nicolas',
  'christophe', 'patrick', 'daniel', 'bernard', 'claude', 'eric', 'laurent', 'sylvie',
  'catherine', 'nathalie', 'isabelle', 'christine', 'francoise', 'monique', 'martine',
  'anne', 'sophie', 'julie', 'celine', 'valerie', 'sandrine', 'veronique', 'david',
  'olivier', 'pascal', 'thierry', 'stephane', 'frederic', 'vincent', 'julien', 'sebastien',
  'antoine', 'francois', 'jacques', 'andre', 'robert', 'louis', 'paul', 'guy', 'serge',
  'gerard', 'didier', 'bruno', 'herve', 'yves', 'marc', 'denis', 'florence', 'caroline',
  'emilie', 'aurelie', 'chantal', 'brigitte', 'nadine', 'corinne', 'laurence', 'karine']);

/**
 * Une adresse qui désigne une personne : donnée personnelle au sens du RGPD,
 * et destinataire qu'on ne démarche pas sur une adresse d'établissement.
 *
 * Deux formes reconnues : « initiale.nom » (j.pothin) et « prénom.nom »
 * (jean.dupont). Tout le reste est considéré comme non personnel.
 */
export function estPersonnelle(email) {
  const local = email.split('@')[0];
  if (INSTITUTIONNEL.test(local)) return false;
  if (/^[a-z][.\-_][a-z]{2,}$/.test(local)) return true;          // j.pothin, a-boullier
  const parties = local.split(/[.\-_]/);
  return parties.length === 2 && PRENOMS.has(parties[0]);            // jean.dupont
}

/** Adresse d'établissement scolaire (code UAI @ac-<académie>). */
export function estScolaire(email) {
  return /@ac-|\.ac-/.test(email);
}

/** Classe une adresse et dit pourquoi elle est retenue ou écartée. */
export function classer(email) {
  const propre = String(email).trim().toLowerCase();
  const domaine = propre.split('@')[1] || '';
  const local = propre.split('@')[0] || '';

  if (!propre.includes('@') || !domaine.includes('.')) return { email: propre, garde: false, motif: 'adresse invalide' };
  if (estScolaire(propre)) return { email: propre, garde: false, motif: 'établissement scolaire' };
  if (DOMAINES_MORTS.has(domaine)) return { email: propre, garde: false, motif: `domaine mort (${DOMAINES_MORTS.get(domaine)})` };
  if (DOMAINES_GRAND_PUBLIC.has(domaine)) return { email: propre, garde: false, motif: 'messagerie grand public' };
  if (estPersonnelle(propre)) return { email: propre, garde: false, motif: 'adresse personnelle (RGPD)' };
  if (!INSTITUTIONNEL.test(local)) return { email: propre, garde: false, motif: 'pas un point de contact identifiable' };
  return { email: propre, garde: true, motif: 'retenue' };
}

/** Analyse complète : verdict, comptes par motif, liste retenue. */
export function analyser(adresses) {
  const uniques = [...new Set(adresses.map((a) => String(a).trim().toLowerCase()).filter(Boolean))];
  const classees = uniques.map(classer);
  const gardees = classees.filter((c) => c.garde).map((c) => c.email);

  const motifs = {};
  for (const c of classees) if (!c.garde) motifs[c.motif] = (motifs[c.motif] || 0) + 1;

  const mortes = classees.filter((c) => c.motif.startsWith('domaine mort')).length;
  return {
    fournies: adresses.length,
    uniques: uniques.length,
    doublons: adresses.length - uniques.length,
    retenues: gardees.length,
    ecartees: uniques.length - gardees.length,
    tauxRebondEstime: uniques.length ? mortes / uniques.length : 0,
    motifs,
    liste: gardees,
  };
}

/** Verdict lisible, avec le seuil qui décide. */
export function verdict(bilan) {
  const pct = (n) => `${(100 * n / (bilan.uniques || 1)).toFixed(1)} %`;
  const lignes = [
    `${bilan.fournies} adresse(s) fournie(s), ${bilan.uniques} unique(s) (${bilan.doublons} doublon(s)).`,
    '',
    'Écartées :',
    ...Object.entries(bilan.motifs).sort((a, b) => b[1] - a[1])
      .map(([motif, n]) => `  ${String(n).padStart(6)}  ${motif}  (${pct(n)})`),
    '',
    `RETENUES : ${bilan.retenues} (${pct(bilan.retenues)})`,
    '',
    `Rebond dur estimé sur la liste brute : ${(100 * bilan.tauxRebondEstime).toFixed(1)} %`,
  ];
  if (bilan.tauxRebondEstime > 0.10) {
    lignes.push('VERDICT : liste inutilisable telle quelle. Au-delà de 10 % de rebonds,');
    lignes.push('les fournisseurs bloquent l\'expéditeur — le domaine est perdu avant');
    lignes.push('que la liste ne soit nettoyée. N\'envoyer qu\'au sous-ensemble retenu.');
  } else if (bilan.tauxRebondEstime > 0.05) {
    lignes.push('VERDICT : au-dessus du seuil de 5 %. Réputation dégradée à prévoir.');
  } else {
    lignes.push('VERDICT : taux de rebond acceptable.');
  }
  return lignes.join('\n');
}

function principal() {
  const args = process.argv.slice(2);
  const fichier = args[0];
  if (!fichier) {
    console.error('Usage : node outils/analyser-liste.mjs adresses.txt [--sortie liste-propre.txt]');
    process.exit(1);
  }
  const i = args.indexOf('--sortie');
  const sortie = i !== -1 ? args[i + 1] : '';

  const adresses = readFileSync(fichier, 'utf8').split(/[\r\n,;]+/).map((l) => l.trim()).filter((l) => l.includes('@'));
  const bilan = analyser(adresses);
  console.log(verdict(bilan));

  if (sortie) {
    writeFileSync(sortie, bilan.liste.join('\n'));
    console.log(`\n${bilan.retenues} adresse(s) retenue(s) écrite(s) dans ${sortie}`);
  }
}

if (import.meta.url === `file://${process.argv[1]}`) principal();
