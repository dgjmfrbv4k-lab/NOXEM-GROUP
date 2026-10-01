/**
 * csv.js — export CSV compatible Excel francais (separateur « ; », BOM UTF-8).
 */
import { STATUTS } from './config.js';

const COLONNES = [
  ['nom', 'Nom du site'],
  ['societe', 'Société'],
  ['typeSite', 'Type de site'],
  ['adresse', 'Adresse'],
  ['codePostal', 'Code postal'],
  ['ville', 'Ville'],
  ['typeCee', 'Type CEE'],
  ['nbStations', 'Nb stations'],
  ['contactPrenom', 'Contact (prénom)'],
  ['contactFonction', 'Fonction'],
  ['contactEmail', 'E-mail professionnel'],
  ['statut', 'Statut'],
  ['dateRelance', 'Date de relance'],
  ['dateSignature', 'Date de signature'],
  ['notes', 'Notes'],
];

/** Echappe une valeur pour le format CSV. */
function echapper(valeur) {
  const texte = String(valeur ?? '');
  return /[";\n\r]/.test(texte) ? `"${texte.replace(/"/g, '""')}"` : texte;
}

function libelleStatut(id) {
  return STATUTS.find((s) => s.id === id)?.label ?? id;
}

/** Construit le contenu CSV a partir d'une liste de sites. */
export function sitesVersCSV(sites) {
  const entetes = COLONNES.map(([, libelle]) => echapper(libelle)).join(';');
  const lignes = sites.map((site) => COLONNES
    .map(([cle]) => echapper(cle === 'statut' ? libelleStatut(site[cle]) : site[cle]))
    .join(';'));
  return [entetes, ...lignes].join('\r\n');
}

/** Declenche le telechargement d'un fichier texte depuis le navigateur. */
export function telecharger(nomFichier, contenu, type = 'text/csv;charset=utf-8') {
  // Le BOM force Excel a lire le fichier en UTF-8 (accents corrects).
  const bom = type.startsWith('text/csv') ? '﻿' : '';
  const blob = new Blob([bom + contenu], { type });
  const url = URL.createObjectURL(blob);
  const lien = document.createElement('a');
  lien.href = url;
  lien.download = nomFichier;
  document.body.appendChild(lien);
  lien.click();
  document.body.removeChild(lien);
  URL.revokeObjectURL(url);
}
