/**
 * collecte-cibles.mjs
 * ---------------------------------------------------------------------------
 * Construit une liste de sites prospects à partir d'OpenStreetMap (API Overpass)
 * et la classe en type A / B / C au sens de la fiche TRA-SE-104.
 *
 * Pourquoi OpenStreetMap : les données y sont ouvertes (licence ODbL), elles
 * décrivent des ÉTABLISSEMENTS et des ÉQUIPEMENTS, jamais des personnes. On ne
 * collecte donc aucune donnée personnelle : pas de nom de dirigeant, pas
 * d'adresse e-mail nominative. Les interlocuteurs se trouvent ensuite un par
 * un, à l'accueil ou sur le site institutionnel de l'enseigne.
 *
 * Usage :
 *   node outils/collecte-cibles.mjs --zone "Métropole de Lyon"
 *   node outils/collecte-cibles.mjs --zone "Rhône" --sortie prospects
 *   node outils/collecte-cibles.mjs --bbox 45.65,4.72,45.85,4.95
 *
 * Produit deux fichiers :
 *   <sortie>.json  — à importer directement dans l'onglet Prospection (bouton « Importer JSON »)
 *   <sortie>.csv   — pour Excel / LibreOffice
 *
 * Remarques d'usage :
 *  - l'API Overpass est un service public gratuit : une requête à la fois,
 *    et on n'insiste pas si elle répond « too many requests » ;
 *  - la licence ODbL impose de citer OpenStreetMap si les données sont
 *    rediffusées ; pour un usage interne de prospection, rien à faire.
 * ---------------------------------------------------------------------------
 */

import { writeFileSync } from 'node:fs';

const OVERPASS = 'https://overpass-api.de/api/interpreter';

/* --------------------------------------------------------------------------
   1. Ce que l'on cherche, et comment cela se traduit au sens de la fiche
   -------------------------------------------------------------------------- */

/**
 * Catégories recherchées dans OpenStreetMap.
 * `filtre` est un filtre Overpass, `libelle` le type de site affiché dans le CRM.
 */
export const CATEGORIES = [
  { cle: 'supermarche', filtre: '["shop"="supermarket"]', libelle: 'Supermarché / hypermarché', type: 'B' },
  { cle: 'hypermarche', filtre: '["shop"="department_store"]', libelle: 'Supermarché / hypermarché', type: 'B' },
  { cle: 'centre_commercial', filtre: '["shop"="mall"]', libelle: 'Centre commercial', type: 'B' },
  { cle: 'station_service', filtre: '["amenity"="fuel"]', libelle: 'Station-service indépendante', type: 'B' },
  { cle: 'parking_public', filtre: '["amenity"="parking"]["access"!="private"]', libelle: 'Parking municipal', type: 'B' },
  { cle: 'aire_service', filtre: '["highway"="services"]', libelle: 'Aire autoroutière', type: 'A' },
  { cle: 'aire_repos', filtre: '["highway"="rest_area"]', libelle: 'Aire autoroutière', type: 'A' },
];

/**
 * Classification d'un élément OSM selon la fiche TRA-SE-104.
 *
 * Rappel de la règle : un site privé mais OUVERT AU GRAND PUBLIC est de type B ;
 * seul un parking réservé aux salariés ou à une flotte est de type C.
 *
 * @returns {{type:'A'|'B'|'C', libelle:string, motif:string}}
 */
export function classifierOsm(tags = {}) {
  if (tags.highway === 'services' || tags.highway === 'rest_area') {
    return { type: 'A', libelle: 'Aire autoroutière', motif: 'Aire de service ou de repos autoroutière.' };
  }

  if (tags.amenity === 'parking') {
    // Un parking explicitement réservé au personnel relève du type C.
    if (tags.access === 'private' || tags.parking === 'staff' || tags.access === 'employees') {
      return { type: 'C', libelle: 'Entreprise (parking salariés / flotte)', motif: 'Parking réservé : type C.' };
    }
    return { type: 'B', libelle: 'Parking municipal', motif: 'Parking accessible au public : type B.' };
  }

  if (tags.shop === 'mall') {
    return { type: 'B', libelle: 'Centre commercial', motif: 'Centre commercial ouvert au public : type B.' };
  }
  if (tags.shop === 'supermarket' || tags.shop === 'department_store') {
    return { type: 'B', libelle: 'Supermarché / hypermarché', motif: 'Commerce ouvert au public : type B.' };
  }
  if (tags.amenity === 'fuel') {
    return { type: 'B', libelle: 'Station-service indépendante', motif: 'Station-service ouverte au public : type B.' };
  }

  return { type: '', libelle: 'Autre', motif: 'Typologie à qualifier.' };
}

/* --------------------------------------------------------------------------
   2. Construction de la requête Overpass
   -------------------------------------------------------------------------- */

/** Requête Overpass pour une zone nommée (commune, département, métropole). */
export function requeteParZone(nomZone, categories = CATEGORIES) {
  const corps = categories
    .flatMap(({ filtre }) => [
      `  nwr${filtre}(area.zone);`,
    ])
    .join('\n');
  return `[out:json][timeout:240];
area["name"="${nomZone}"]["boundary"="administrative"]->.zone;
(
${corps}
);
out center tags;`;
}

/** Requête Overpass pour une emprise géographique (sud,ouest,nord,est). */
export function requeteParBbox(bbox, categories = CATEGORIES) {
  const corps = categories.map(({ filtre }) => `  nwr${filtre}(${bbox});`).join('\n');
  return `[out:json][timeout:240];
(
${corps}
);
out center tags;`;
}

/* --------------------------------------------------------------------------
   3. Conversion en fiches site du CRM
   -------------------------------------------------------------------------- */

/** Un élément OSM -> une fiche site, au format attendu par le CRM. */
export function versSite(element) {
  const tags = element.tags || {};
  const { type, libelle, motif } = classifierOsm(tags);
  const adresse = [tags['addr:housenumber'], tags['addr:street']].filter(Boolean).join(' ');

  return {
    id: `osm_${element.type}_${element.id}`,
    nom: tags.name || tags.brand || tags.operator || '(sans nom)',
    societe: tags.operator || tags.brand || '',
    typeSite: libelle,
    adresse,
    codePostal: tags['addr:postcode'] || '',
    ville: tags['addr:city'] || '',
    typeCee: type,
    nbStations: 1,
    contactPrenom: '',
    contactFonction: '',
    contactEmail: '',
    statut: 'a_contacter',
    dateRelance: '',
    dateSignature: '',
    notes: [
      motif,
      tags.website ? `Site : ${tags.website}` : '',
      tags.phone ? `Téléphone du site : ${tags.phone}` : '',
      `Source : OpenStreetMap (${element.type}/${element.id}).`,
    ].filter(Boolean).join(' '),
    eligibilite: {},
    pieces: {},
    creeLe: new Date().toISOString(),
    majLe: new Date().toISOString(),
  };
}

/** Écarte les doublons (même nom + même ville) et les fiches sans nom exploitable. */
export function nettoyer(sites) {
  const vus = new Set();
  return sites.filter((site) => {
    if (site.nom === '(sans nom)' && !site.adresse) return false;
    const cle = `${site.nom.toLowerCase()}|${site.ville.toLowerCase()}|${site.adresse.toLowerCase()}`;
    if (vus.has(cle)) return false;
    vus.add(cle);
    return true;
  });
}

/** Fichier de sauvegarde JSON, importable tel quel dans l'onglet Prospection. */
export function versSauvegarde(sites) {
  return JSON.stringify({ version: 1, exporteLe: new Date().toISOString(), sites }, null, 2);
}

/** CSV au format attendu par Excel français (séparateur « ; », BOM UTF-8). */
export function versCSV(sites) {
  const colonnes = [
    ['nom', 'Nom du site'], ['societe', 'Société'], ['typeSite', 'Type de site'],
    ['adresse', 'Adresse'], ['codePostal', 'Code postal'], ['ville', 'Ville'],
    ['typeCee', 'Type CEE'], ['nbStations', 'Nb stations'], ['statut', 'Statut'], ['notes', 'Notes'],
  ];
  const echapper = (v) => (/[";\n\r]/.test(String(v ?? '')) ? `"${String(v).replace(/"/g, '""')}"` : String(v ?? ''));
  const lignes = sites.map((s) => colonnes.map(([c]) => echapper(s[c])).join(';'));
  return `﻿${[colonnes.map(([, l]) => l).join(';'), ...lignes].join('\r\n')}`;
}

/* --------------------------------------------------------------------------
   4. Exécution
   -------------------------------------------------------------------------- */

async function principal() {
  const args = process.argv.slice(2);
  const lire = (cle, defaut) => {
    const i = args.indexOf(`--${cle}`);
    return i !== -1 && args[i + 1] ? args[i + 1] : defaut;
  };

  const zone = lire('zone', '');
  const bbox = lire('bbox', '');
  const sortie = lire('sortie', 'cibles');

  if (!zone && !bbox) {
    console.error('Indiquez une zone : --zone "Métropole de Lyon"  ou  --bbox sud,ouest,nord,est');
    process.exit(1);
  }

  const requete = zone ? requeteParZone(zone) : requeteParBbox(bbox);
  console.log(`Interrogation d'Overpass pour ${zone || bbox}… (cela peut prendre une minute)`);

  const reponse = await fetch(OVERPASS, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: `data=${encodeURIComponent(requete)}`,
  });

  if (!reponse.ok) {
    console.error(`Overpass a répondu ${reponse.status}. Réessayez dans quelques minutes (service public, usage partagé).`);
    process.exit(1);
  }

  const data = await reponse.json();
  const sites = nettoyer((data.elements || []).map(versSite));

  writeFileSync(`${sortie}.json`, versSauvegarde(sites));
  writeFileSync(`${sortie}.csv`, versCSV(sites));

  const parType = sites.reduce((acc, s) => { acc[s.typeCee || '?'] = (acc[s.typeCee || '?'] || 0) + 1; return acc; }, {});
  console.log(`\n${sites.length} site(s) retenu(s) :`);
  for (const [type, nb] of Object.entries(parType).sort()) {
    console.log(`  type ${type} : ${nb}`);
  }
  console.log(`\nFichiers écrits : ${sortie}.json (à importer dans l'onglet Prospection) et ${sortie}.csv`);
  console.log('Données OpenStreetMap, licence ODbL. Aucune donnée personnelle collectée.');
}

if (import.meta.url === `file://${process.argv[1]}`) {
  principal().catch((e) => { console.error(e.message); process.exit(1); });
}
