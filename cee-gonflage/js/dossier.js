/**
 * dossier.js
 * ---------------------------------------------------------------------------
 * Suivi du dossier CEE d'un site signe : pieces justificatives et echeances.
 *
 * Dates (fiche TRA-SE-104) :
 *  - Engagement  = date de signature du contrat d'entretien.
 *  - Achevement  = date anniversaire de la signature.
 *  - Duree de vie conventionnelle : 1 an, valorisable chaque annee tant que le
 *    contrat est actif ET expressement renouvele (la reconduction tacite
 *    n'ouvre pas droit a une nouvelle valorisation).
 * ---------------------------------------------------------------------------
 */

import { ALERTES_ANNIVERSAIRE } from './config.js';

/** Pieces a reunir pour un dossier controlable par le PNCEE. */
export const PIECES_DOSSIER = [
  {
    id: 'contrat',
    label: 'Contrat d’entretien signé et en cours de validité',
    aide: 'Doit mentionner le professionnel signataire, le bénéficiaire et la date de signature.',
    obligatoire: true,
  },
  {
    id: 'clause15j',
    label: 'Clause de remplacement des pièces défectueuses sous 15 jours',
    aide: 'Vérifier la présence explicite du délai dans le contrat.',
    obligatoire: true,
  },
  {
    id: 'avenants',
    label: 'Avenants éventuels au contrat',
    aide: 'Uniquement si le contrat a été modifié (périmètre, nombre de stations, durée).',
    obligatoire: false,
  },
  {
    id: 'procedureControle',
    label: 'Procédure de contrôle quotidien',
    aide: 'Document décrivant le contrôle quotidien de la station.',
    obligatoire: true,
  },
  {
    id: 'etatRecapitulatif',
    label: 'État récapitulatif des stations signé par le bénéficiaire',
    aide: 'Type (A/B/C), nom et adresse de chaque station.',
    obligatoire: true,
  },
  {
    id: 'panneauTnpf',
    label: 'Preuve de l’affichage du panneau TNPF',
    aide: 'Photo datée du panneau « Des pneus bien gonflés… » installé près de la borne.',
    obligatoire: true,
  },
  {
    id: 'gratuite',
    label: 'Confirmation écrite de la gratuité du gonflage',
    aide: 'Toute tarification rend l’opération inéligible.',
    obligatoire: true,
  },
];

/** Analyse une date ISO (AAAA-MM-JJ) en Date locale, ou null. */
export function parseDate(valeur) {
  if (!valeur) return null;
  const d = new Date(`${valeur}T00:00:00`);
  return Number.isNaN(d.getTime()) ? null : d;
}

/** Ajoute n annees a une date (gere le 29 fevrier en repliant sur le 28). */
export function ajouterAnnees(date, n) {
  const d = new Date(date.getTime());
  const jour = d.getDate();
  d.setFullYear(d.getFullYear() + n);
  if (d.getDate() !== jour) d.setDate(0); // repli sur le dernier jour du mois
  return d;
}

/** Nombre de jours entiers entre deux dates. */
export function joursEntre(debut, fin) {
  const MS_JOUR = 24 * 60 * 60 * 1000;
  const a = new Date(debut.getFullYear(), debut.getMonth(), debut.getDate());
  const b = new Date(fin.getFullYear(), fin.getMonth(), fin.getDate());
  return Math.round((b - a) / MS_JOUR);
}

/**
 * Calcule les echeances du dossier d'un site.
 * @param {string} dateSignature date ISO de signature du contrat
 * @param {Date} [aujourdhui] injectable pour les tests
 */
export function echeances(dateSignature, aujourdhui = new Date()) {
  const engagement = parseDate(dateSignature);
  if (!engagement) {
    return { engagement: null, achevement: null, prochaineEcheance: null, joursRestants: null, niveau: 'inconnu', anneeContrat: null };
  }

  // Achevement = premiere date anniversaire de la signature.
  const achevement = ajouterAnnees(engagement, 1);

  // Prochaine echeance = prochaine date anniversaire a venir (ou celle du jour).
  let anneeContrat = 1;
  let prochaineEcheance = achevement;
  while (joursEntre(aujourdhui, prochaineEcheance) < 0) {
    anneeContrat += 1;
    prochaineEcheance = ajouterAnnees(engagement, anneeContrat);
  }

  const joursRestants = joursEntre(aujourdhui, prochaineEcheance);
  let niveau = 'ok';
  if (joursRestants <= ALERTES_ANNIVERSAIRE.urgent) niveau = 'urgent';
  else if (joursRestants <= ALERTES_ANNIVERSAIRE.vigilance) niveau = 'vigilance';

  return { engagement, achevement, prochaineEcheance, joursRestants, niveau, anneeContrat };
}

/**
 * Etat d'avancement des pieces d'un dossier.
 * @param {Record<string, boolean>} pieces
 */
export function avancementPieces(pieces = {}) {
  const obligatoires = PIECES_DOSSIER.filter((p) => p.obligatoire);
  const manquantes = obligatoires.filter((p) => !pieces[p.id]);
  const fournies = PIECES_DOSSIER.filter((p) => pieces[p.id]).length;
  return {
    complet: manquantes.length === 0,
    manquantes,
    fournies,
    total: PIECES_DOSSIER.length,
    progression: fournies / PIECES_DOSSIER.length,
  };
}

/** Message d'alerte lisible pour l'interface. */
export function messageEcheance(ech) {
  if (!ech.engagement) return 'Date de signature non renseignée : échéances inconnues.';
  if (ech.joursRestants < 0) return 'Date anniversaire dépassée.';
  if (ech.joursRestants === 0) return 'Date anniversaire aujourd’hui : le renouvellement doit être formalisé.';
  if (ech.niveau === 'urgent') return `Renouvellement urgent : ${ech.joursRestants} jour(s) avant la date anniversaire.`;
  if (ech.niveau === 'vigilance') return `À préparer : ${ech.joursRestants} jour(s) avant la date anniversaire.`;
  return `${ech.joursRestants} jour(s) avant la prochaine date anniversaire.`;
}
