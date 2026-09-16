/**
 * collecte-mairies.mjs
 * ---------------------------------------------------------------------------
 * Constitue la liste des mairies d'un département, avec leur adresse de contact
 * officielle, à partir de l'Annuaire de l'administration (service-public.fr).
 *
 * Ces coordonnées sont institutionnelles et publiées par l'État : ce sont des
 * adresses d'établissement, pas des données personnelles. Aucun nom d'agent ni
 * d'élu n'est collecté — le nom de l'interlocuteur se demande au téléphone.
 *
 *   node outils/collecte-mairies.mjs --departement 69
 *   node outils/collecte-mairies.mjs --departement 69,01,38 --sortie mairies-lyon
 *
 * Produit `<sortie>.json`, importable dans l'onglet Prospection, et `<sortie>.csv`.
 *
 * À lancer depuis un poste disposant d'un accès Internet ordinaire : l'API est
 * publique mais inaccessible depuis certains environnements d'exécution.
 * ---------------------------------------------------------------------------
 */

import { writeFileSync } from 'node:fs';

const API = 'https://api-lannuaire.service-public.fr/api/explore/v2.1/catalog/datasets'
  + '/api-lannuaire-administration/records';

/**
 * Les champs de l'annuaire sont parfois sérialisés en JSON dans une chaîne,
 * parfois déjà structurés. Cette fonction accepte les deux formes.
 */
export function lireChamp(valeur) {
  if (valeur === null || valeur === undefined || valeur === '') return null;
  if (typeof valeur === 'object') return valeur;
  if (typeof valeur !== 'string') return valeur;
  const texte = valeur.trim();
  if (!texte.startsWith('[') && !texte.startsWith('{')) return texte;
  try {
    return JSON.parse(texte);
  } catch (e) {
    return texte;
  }
}

/** Première adresse e-mail exploitable d'un enregistrement. */
export function extraireCourriel(enregistrement) {
  const brut = lireChamp(enregistrement.adresse_courriel);
  const candidats = []
    .concat(brut ?? [])
    .map((c) => (typeof c === 'string' ? c : c?.valeur ?? c?.value ?? ''))
    .filter((c) => typeof c === 'string' && c.includes('@'));
  return candidats[0] || '';
}

/** Téléphone principal, en texte lisible. */
export function extraireTelephone(enregistrement) {
  const brut = lireChamp(enregistrement.telephone);
  const candidats = []
    .concat(brut ?? [])
    .map((t) => (typeof t === 'string' ? t : t?.valeur ?? t?.value ?? ''))
    .filter(Boolean);
  return candidats[0] || '';
}

/** Adresse postale : on retient l'adresse physique si plusieurs sont fournies. */
export function extraireAdresse(enregistrement) {
  const brut = lireChamp(enregistrement.adresse);
  const liste = [].concat(brut ?? []).filter((a) => a && typeof a === 'object');
  const choisie = liste.find((a) => a.type_adresse === 'Adresse') || liste[0] || {};
  return {
    voie: [choisie.numero_voie, choisie.complement1, choisie.complement2].filter(Boolean).join(' ').trim(),
    codePostal: choisie.code_postal || '',
    ville: choisie.nom_commune || '',
  };
}

/**
 * Un enregistrement de l'annuaire -> une fiche site du CRM.
 *
 * Le type CEE reste vide : une commune a le plus souvent un parking public
 * (type B) ET un parking d'agents (type C). C'est un dossier groupé, à
 * qualifier lors de l'échange.
 */
export function versSite(enregistrement) {
  const adresse = extraireAdresse(enregistrement);
  const courriel = extraireCourriel(enregistrement);
  const telephone = extraireTelephone(enregistrement);
  const nom = enregistrement.nom || `Mairie de ${adresse.ville}`;

  return {
    id: `mairie_${enregistrement.id || adresse.codePostal + adresse.ville}`.replace(/[^a-zA-Z0-9_]/g, '_'),
    nom,
    societe: 'Commune',
    typeSite: 'Collectivité',
    adresse: adresse.voie,
    codePostal: adresse.codePostal,
    ville: adresse.ville,
    typeCee: '',
    nbStations: 1,
    contactPrenom: '',
    contactFonction: 'Direction générale des services',
    contactEmail: courriel,
    statut: 'a_contacter',
    dateRelance: '',
    dateSignature: '',
    notes: [
      telephone ? `Standard : ${telephone}.` : '',
      'Parking public = type B, parking des agents = type C : dossier groupé à qualifier.',
      'Demander le DGS ou le service technique. Source : Annuaire de l’administration (service-public.fr).',
    ].filter(Boolean).join(' '),
    eligibilite: {},
    pieces: {},
    creeLe: new Date().toISOString(),
    majLe: new Date().toISOString(),
  };
}

/** Écarte les fiches sans adresse e-mail et les doublons de commune. */
export function nettoyer(sites) {
  const vues = new Set();
  return sites.filter((s) => {
    if (!s.contactEmail) return false;
    const cle = s.contactEmail.toLowerCase();
    if (vues.has(cle)) return false;
    vues.add(cle);
    return true;
  });
}

/** Requête paginée sur l'annuaire, pour un département. */
export async function collecterDepartement(departement, { pageMax = 100 } = {}) {
  const resultats = [];
  let offset = 0;

  for (;;) {
    const parametres = new URLSearchParams({
      where: `pivot LIKE "mairie" AND code_insee_commune LIKE "${departement}%"`,
      limit: String(pageMax),
      offset: String(offset),
    });
    const reponse = await fetch(`${API}?${parametres}`);
    if (!reponse.ok) {
      throw new Error(`L'annuaire a répondu ${reponse.status}. Réessayez dans quelques minutes.`);
    }
    const data = await reponse.json();
    const lot = data.results || [];
    resultats.push(...lot);
    if (lot.length < pageMax) break;
    offset += pageMax;
    if (offset > 10000) break; // garde-fou
  }

  return resultats;
}

/** CSV au format Excel français. */
export function versCSV(sites) {
  const colonnes = [['nom', 'Commune'], ['adresse', 'Adresse'], ['codePostal', 'Code postal'],
    ['ville', 'Ville'], ['contactEmail', 'E-mail officiel'], ['notes', 'Notes']];
  const echapper = (v) => (/[";\n\r]/.test(String(v ?? '')) ? `"${String(v).replace(/"/g, '""')}"` : String(v ?? ''));
  return `﻿${[colonnes.map(([, l]) => l).join(';'),
    ...sites.map((s) => colonnes.map(([c]) => echapper(s[c])).join(';'))].join('\r\n')}`;
}

async function principal() {
  const args = process.argv.slice(2);
  const lire = (cle, defaut) => {
    const i = args.indexOf(`--${cle}`);
    return i !== -1 && args[i + 1] ? args[i + 1] : defaut;
  };

  const departements = lire('departement', '').split(',').map((d) => d.trim()).filter(Boolean);
  const sortie = lire('sortie', 'mairies');

  if (!departements.length) {
    console.error('Indiquez au moins un département : --departement 69');
    console.error('Plusieurs départements : --departement 69,01,38,42');
    process.exit(1);
  }

  const tous = [];
  for (const departement of departements) {
    console.log(`Interrogation de l'annuaire pour le département ${departement}…`);
    const enregistrements = await collecterDepartement(departement);
    console.log(`  ${enregistrements.length} mairie(s) trouvée(s)`);
    tous.push(...enregistrements.map(versSite));
  }

  const sites = nettoyer(tous);
  writeFileSync(`${sortie}.json`, JSON.stringify({ version: 1, exporteLe: new Date().toISOString(), sites }, null, 2));
  writeFileSync(`${sortie}.csv`, versCSV(sites));

  console.log(`\n${sites.length} mairie(s) avec une adresse e-mail officielle, sur ${tous.length} au total.`);
  console.log(`Fichiers écrits : ${sortie}.json (à importer dans Prospection) et ${sortie}.csv`);
  console.log('\nEnchaînez avec :');
  console.log(`  node outils/preparer-envois.mjs --sites ${sortie}.json --quota 50 --modele mairie`);
}

if (import.meta.url === `file://${process.argv[1]}`) {
  principal().catch((e) => { console.error(e.message); process.exit(1); });
}
