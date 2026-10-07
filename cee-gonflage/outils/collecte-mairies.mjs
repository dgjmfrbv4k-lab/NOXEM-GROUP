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
import { collecterDepartement, versSite, nettoyer } from '../js/annuaire.js';

// La logique de lecture de l'annuaire vit dans js/annuaire.js : elle est
// partagée avec l'application, qui fait la même collecte depuis le navigateur.
export { collecterDepartement, versSite, nettoyer };
export {
  lireChamp, extraireCourriel, extraireTelephone, extraireAdresse, urlRequete,
} from '../js/annuaire.js';

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
