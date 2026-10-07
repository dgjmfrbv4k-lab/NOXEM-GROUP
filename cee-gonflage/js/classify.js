/**
 * classify.js
 * ---------------------------------------------------------------------------
 * Classification d'un site en type A / B / C au sens de la fiche TRA-SE-104,
 * et evaluation de la checklist d'eligibilite.
 *
 * Regle de lecture (dans cet ordre) :
 *   1. Autoroute ou voie de type autoroutier avec aire de repos        -> A
 *   2. Parking reserve aux salaries / a la flotte d'une entreprise
 *      ou d'une collectivite                                           -> C
 *   3. Site ouvert au grand public (zone urbaine, ZI, zone d'activite,
 *      parking grand public, hors agglomeration)                       -> B
 *   Sinon : a qualifier avec le delegataire.
 *
 * Point d'attention : un site PRIVE mais OUVERT AU GRAND PUBLIC
 * (supermarche, centre commercial) releve du type B, pas du type C.
 * ---------------------------------------------------------------------------
 */

import { TYPES_STATION, CONDITIONS_ELIGIBILITE } from './config.js';
import { montantNetParStation, prixNetEurMWhc } from './calc.js';

/** Questionnaire de classification (pose dans l'ordre du tableau). */
export const QUESTIONS = [
  {
    id: 'autoroute',
    question: 'La station est-elle implantée sur une autoroute ou une voie de type autoroutier disposant d’aires de repos ?',
    aide: 'Aire de repos ou de service autoroutière, voie express avec aires aménagées.',
  },
  {
    id: 'reserveSalaries',
    question: 'Le parking est-il réservé aux salariés ou à la flotte d’une entreprise ou d’une collectivité ?',
    aide: 'Accès limité au personnel ou aux véhicules professionnels (badge, barrière, règlement intérieur).',
  },
  {
    id: 'ouvertPublic',
    question: 'Le site est-il ouvert au grand public (zone urbaine, zone industrielle, zone d’activité, parking grand public) ?',
    aide: 'Un parking privé mais librement accessible au public (supermarché, centre commercial) compte comme ouvert au public.',
  },
];

/**
 * Determine le type de station a partir des reponses au questionnaire.
 * @param {{autoroute?:boolean, reserveSalaries?:boolean, ouvertPublic?:boolean}} reponses
 * @returns {{type:'A'|'B'|'C'|null, motif:string, alerte?:string}}
 */
export function classifier(reponses = {}) {
  const { autoroute, reserveSalaries, ouvertPublic } = reponses;

  if (autoroute === true) {
    return {
      type: 'A',
      motif: 'Implantation autoroutière avec aire de repos : type A.',
      alerte: 'Marché majoritairement verrouillé par les concessionnaires autoroutiers. '
        + 'Piste alternative : voies express et rocades non concédées (DIR, départements).',
    };
  }

  // Un site ouvert au grand public l'emporte sur le caractere prive du parking.
  if (ouvertPublic === true) {
    if (reserveSalaries === true) {
      return {
        type: 'B',
        motif: 'Site accessible au grand public : type B, même si une partie du parking est réservée au personnel.',
        alerte: 'Si la station de gonflage est installée dans la zone réservée au personnel, '
          + 'elle relève du type C. À trancher selon l’emplacement exact de la borne.',
      };
    }
    return {
      type: 'B',
      motif: 'Parking ouvert au grand public hors autoroute : type B.',
    };
  }

  if (reserveSalaries === true) {
    return {
      type: 'C',
      motif: 'Parking privé d’entreprise ou de collectivité réservé aux salariés ou à la flotte : type C.',
      alerte: 'Volume faible : rentable surtout en complément d’un parc de sites de type B.',
    };
  }

  if (autoroute === false && reserveSalaries === false && ouvertPublic === false) {
    return {
      type: null,
      motif: 'Site ni autoroutier, ni ouvert au public, ni réservé aux salariés : '
        + 'la typologie doit être qualifiée avec le délégataire CEE avant tout engagement.',
    };
  }

  return { type: null, motif: 'Répondez aux questions pour obtenir la typologie.' };
}

/**
 * Estimation annuelle pour un type et un nombre de stations donnes.
 * @param {'A'|'B'|'C'|null} type
 * @param {number} nbStations
 * @param {number} prixBrut prix marche brut en EUR/MWh cumac
 * @param {number} margePct marge du delegataire en %
 */
export function estimationPourType(type, nbStations, prixBrut, margePct) {
  if (!type || !TYPES_STATION[type]) return null;
  const nb = Math.max(0, Math.round(Number(nbStations) || 0));
  const prixNet = prixNetEurMWhc(prixBrut, margePct);
  const parStation = montantNetParStation(type, prixNet);
  return {
    type,
    nbStations: nb,
    kwhCumacParStation: TYPES_STATION[type].kwhCumac,
    kwhCumacTotal: TYPES_STATION[type].kwhCumac * nb,
    prixNetEurMWhc: prixNet,
    montantNetParStation: parStation,
    montantNetTotal: parStation * nb,
  };
}

/**
 * Evalue la checklist d'eligibilite.
 * @param {Record<string, boolean>} coches conditions cochees (id -> true)
 * @returns {{eligible:boolean, bloquantsManquants:Array, aCompleter:Array, progression:number}}
 */
export function evaluerEligibilite(coches = {}) {
  const bloquantsManquants = CONDITIONS_ELIGIBILITE.filter((c) => c.bloquant && !coches[c.id]);
  const aCompleter = CONDITIONS_ELIGIBILITE.filter((c) => !c.bloquant && !coches[c.id]);
  const nbCoches = CONDITIONS_ELIGIBILITE.filter((c) => coches[c.id]).length;
  return {
    eligible: bloquantsManquants.length === 0,
    bloquantsManquants,
    aCompleter,
    progression: nbCoches / CONDITIONS_ELIGIBILITE.length,
  };
}
