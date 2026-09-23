/**
 * recharge.js
 * ---------------------------------------------------------------------------
 * Estimation de la prime ADVENIR (bornes de recharge), calcul PUR.
 *
 * Règle appliquée : prime par point de charge =
 *     min( coût HT du point × taux de prise en charge, plafond par point )
 * puis multipliée par le nombre de points.
 *
 * Les taux et plafonds ne sont pas figés dans le code : ce sont des paramètres.
 * ---------------------------------------------------------------------------
 */

import { nombre, entierPositif } from './calc.js';

/**
 * @param {{nbPoints:number, coutHtParPoint:number, tauxPriseEnChargePct:number,
 *          plafondParPoint:number, prixFactureClientParPoint?:number}} params
 */
export function estimerPrimeRecharge(params = {}) {
  const nbPoints = entierPositif(params.nbPoints);
  const coutHtParPoint = Math.max(0, nombre(params.coutHtParPoint));
  const taux = Math.min(100, Math.max(0, nombre(params.tauxPriseEnChargePct)));
  const plafond = Math.max(0, nombre(params.plafondParPoint));
  const prixClient = Math.max(0, nombre(params.prixFactureClientParPoint));

  // La prime est le minimum entre le pourcentage du coût et le plafond.
  const primeTheoriqueParPoint = coutHtParPoint * (taux / 100);
  const primeParPoint = Math.min(primeTheoriqueParPoint, plafond);
  const plafondAtteint = primeTheoriqueParPoint > plafond;

  const coutTotal = coutHtParPoint * nbPoints;
  const primeTotale = primeParPoint * nbPoints;
  const resteACharge = coutTotal - primeTotale;

  return {
    nbPoints,
    coutHtParPoint,
    coutTotal,
    primeParPoint,
    primeTotale,
    plafondAtteint,
    resteACharge,
    resteAChargeParPoint: nbPoints > 0 ? resteACharge / nbPoints : 0,
    tauxReelPct: coutTotal > 0 ? (primeTotale / coutTotal) * 100 : 0,
    recettesContrats: prixClient * nbPoints,
  };
}
