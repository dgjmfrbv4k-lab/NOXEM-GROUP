/**
 * calc.js
 * ---------------------------------------------------------------------------
 * Module de calcul PUR (aucun acces au DOM, aucun etat global).
 * Il est importable tel quel par l'interface et par les tests Node.
 *
 * Formules de reference (fiche TRA-SE-104) :
 *   Total kWh cumac = 534 200 x NA + 148 400 x NB + 39 600 x NC
 *   Montant EUR      = (Total kWh cumac / 1000) x prix EUR/MWh cumac
 *
 * Le prix net percu par le beneficiaire est le prix brut du marche diminue de
 * la marge du delegataire :
 *   prix net = prix brut x (1 - marge% / 100)
 * ---------------------------------------------------------------------------
 */

import { TYPES_STATION, ORDRE_TYPES } from './config.js';

/**
 * Hypotheses neutres du moteur de calcul.
 * A ne pas confondre avec DEFAUTS_SIMULATEUR (config.js), qui ne sert qu'a
 * pre-remplir le formulaire : un parametre absent ici vaut 0, jamais une
 * valeur commerciale implicite.
 */
export const BASE_SIMULATION = {
  nbA: 0,
  nbB: 0,
  nbC: 0,
  prixBrutEurMWhc: 0,
  margeDelegatairePct: 0,
  partCeeConserveePct: 100,
  coutEntretienAnnuelParStation: 0,
  coutInstallationParStation: 0,
  prixFactureClientParStation: 0,
  fraisFixesAnnuels: 0,
  variationAnnuellePrixPct: 0,
};

/** Convertit une valeur saisie en nombre fini (0 par defaut). */
export function nombre(valeur, parDefaut = 0) {
  const n = typeof valeur === 'string' ? Number(valeur.replace(',', '.')) : Number(valeur);
  return Number.isFinite(n) ? n : parDefaut;
}

/** Entier positif ou nul (nombre de stations). */
export function entierPositif(valeur) {
  return Math.max(0, Math.round(nombre(valeur, 0)));
}

/**
 * Volume de CEE genere, en kWh cumac.
 * @param {{nbA:number, nbB:number, nbC:number}} stations
 * @returns {{A:number, B:number, C:number, total:number}}
 */
export function volumeCumac({ nbA = 0, nbB = 0, nbC = 0 } = {}) {
  const detail = {
    A: entierPositif(nbA) * TYPES_STATION.A.kwhCumac,
    B: entierPositif(nbB) * TYPES_STATION.B.kwhCumac,
    C: entierPositif(nbC) * TYPES_STATION.C.kwhCumac,
  };
  return { ...detail, total: detail.A + detail.B + detail.C };
}

/**
 * Prix net percu apres marge du delegataire.
 * @param {number} prixBrutEurMWhc prix marche brut, en EUR/MWh cumac
 * @param {number} margePct marge du delegataire, en %
 */
export function prixNetEurMWhc(prixBrutEurMWhc, margePct) {
  const brut = Math.max(0, nombre(prixBrutEurMWhc));
  const marge = Math.min(100, Math.max(0, nombre(margePct)));
  return brut * (1 - marge / 100);
}

/**
 * Conversion volume -> montant.
 * @param {number} kwhCumac volume en kWh cumac
 * @param {number} prixEurMWhc prix en EUR/MWh cumac (1 MWh cumac = 1000 kWh cumac)
 */
export function montantEuros(kwhCumac, prixEurMWhc) {
  return (nombre(kwhCumac) / 1000) * nombre(prixEurMWhc);
}

/**
 * Montant CEE net annuel pour UNE station d'un type donne.
 * @param {'A'|'B'|'C'} type
 * @param {number} prixNet prix net en EUR/MWh cumac
 */
export function montantNetParStation(type, prixNet) {
  const t = TYPES_STATION[type];
  if (!t) return 0;
  return montantEuros(t.kwhCumac, prixNet);
}

/**
 * Simulation complete de rentabilite.
 *
 * @param {object} params voir BASE_SIMULATION pour la liste et les unites
 *   (tout parametre omis vaut 0)
 * @returns {object} resultat detaille (valeurs brutes non arrondies)
 */
export function simuler(params = {}) {
  const p = { ...BASE_SIMULATION, ...params };

  // --- 1. Volumes ---------------------------------------------------------
  const stations = {
    A: entierPositif(p.nbA),
    B: entierPositif(p.nbB),
    C: entierPositif(p.nbC),
  };
  stations.total = stations.A + stations.B + stations.C;
  const volume = volumeCumac({ nbA: stations.A, nbB: stations.B, nbC: stations.C });

  // --- 2. Prix ------------------------------------------------------------
  const prix = {
    brut: Math.max(0, nombre(p.prixBrutEurMWhc)),
    margeDelegatairePct: Math.min(100, Math.max(0, nombre(p.margeDelegatairePct))),
  };
  prix.net = prixNetEurMWhc(prix.brut, prix.margeDelegatairePct);

  // --- 3. Montants CEE ----------------------------------------------------
  // `partConservee` = part du montant net qui revient a votre structure (%).
  // 100 % = vous percevez la totalite de la prime ; en dessous, le reste est
  // reverse au beneficiaire (exploitant du site) selon votre montage.
  const partConserveePct = Math.min(100, Math.max(0, nombre(p.partCeeConserveePct, 100)));
  const cee = {
    brut: montantEuros(volume.total, prix.brut),
    net: montantEuros(volume.total, prix.net),
    partConserveePct,
  };
  cee.conserve = cee.net * (partConserveePct / 100);

  // --- 4. Recettes et charges annuelles ----------------------------------
  const prixContratClient = Math.max(0, nombre(p.prixFactureClientParStation));
  const coutEntretien = Math.max(0, nombre(p.coutEntretienAnnuelParStation));
  const coutInstallation = Math.max(0, nombre(p.coutInstallationParStation));
  const fraisFixes = Math.max(0, nombre(p.fraisFixesAnnuels));

  const recettes = {
    cee: cee.conserve,
    contrats: prixContratClient * stations.total,
  };
  recettes.total = recettes.cee + recettes.contrats;

  const charges = {
    entretien: coutEntretien * stations.total,
    fraisFixes,
  };
  charges.total = charges.entretien + charges.fraisFixes;

  const margeRecurrenteAnnuelle = recettes.total - charges.total;
  const investissementInitial = coutInstallation * stations.total;
  const resultatAnnee1 = margeRecurrenteAnnuelle - investissementInitial;

  // --- 5. Marge par station (hors frais fixes de structure) ---------------
  // Marge annuelle recurrente apportee par UNE station supplementaire.
  const margeParStation = {};
  for (const type of ORDRE_TYPES) {
    const ceeStation = montantNetParStation(type, prix.net) * (partConserveePct / 100);
    margeParStation[type] = ceeStation + prixContratClient - coutEntretien;
  }
  margeParStation.moyenne = stations.total > 0
    ? (recettes.total - charges.entretien) / stations.total
    : null;

  // --- 6. Point mort ------------------------------------------------------
  // Nombre de stations necessaires pour couvrir les frais fixes annuels de
  // structure. Sans frais fixes, le point mort vaut 1 station des lors que la
  // marge unitaire est positive ; il est impossible si la marge est negative.
  const pointMort = {};
  for (const type of [...ORDRE_TYPES, 'moyenne']) {
    const marge = margeParStation[type];
    pointMort[type] = calculPointMort(marge, fraisFixes);
  }
  // Point mort de la premiere annee : la station doit aussi absorber son
  // cout d'installation la premiere annee.
  const pointMortAnnee1 = {};
  for (const type of [...ORDRE_TYPES, 'moyenne']) {
    const marge = margeParStation[type] === null ? null : margeParStation[type] - coutInstallation;
    pointMortAnnee1[type] = calculPointMort(marge, fraisFixes);
  }

  // Delai de retour sur l'investissement d'installation, en mois.
  const retourInvestissementMois = (coutInstallation > 0 && margeParStation.moyenne > 0)
    ? (coutInstallation / margeParStation.moyenne) * 12
    : (coutInstallation === 0 ? 0 : null);

  // --- 7. Projection sur 3 ans -------------------------------------------
  const variationPct = nombre(p.variationAnnuellePrixPct);
  const projection = [];
  let cumule = 0;
  for (let annee = 1; annee <= 3; annee += 1) {
    const facteur = (1 + variationPct / 100) ** (annee - 1);
    const prixNetAnnee = prix.net * facteur;
    const ceeAnnee = montantEuros(volume.total, prixNetAnnee) * (partConserveePct / 100);
    const recettesAnnee = ceeAnnee + recettes.contrats;
    const investAnnee = annee === 1 ? investissementInitial : 0;
    const resultat = recettesAnnee - charges.total - investAnnee;
    cumule += resultat;
    projection.push({
      annee,
      prixNetEurMWhc: prixNetAnnee,
      recettesCee: ceeAnnee,
      recettesContrats: recettes.contrats,
      charges: charges.total,
      investissement: investAnnee,
      resultat,
      cumule,
    });
  }

  return {
    parametres: p,
    stations,
    volume,
    prix,
    cee,
    recettes,
    charges,
    margeRecurrenteAnnuelle,
    investissementInitial,
    resultatAnnee1,
    margeParStation,
    pointMort,
    pointMortAnnee1,
    retourInvestissementMois,
    projection,
    // Signale a l'interface que les couts n'ont pas ete renseignes : la marge
    // affichee est alors un plafond theorique, pas un resultat realiste.
    coutsNonRenseignes: coutEntretien === 0 && coutInstallation === 0,
  };
}

/**
 * Nombre de stations necessaires pour couvrir des frais fixes annuels.
 * @returns {number|null} null = jamais rentable (marge unitaire <= 0)
 */
export function calculPointMort(margeParStation, fraisFixesAnnuels) {
  if (margeParStation === null || !Number.isFinite(margeParStation) || margeParStation <= 0) {
    return null;
  }
  if (fraisFixesAnnuels <= 0) return 1;
  return Math.ceil(fraisFixesAnnuels / margeParStation);
}
