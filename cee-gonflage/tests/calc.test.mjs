/**
 * Tests du moteur de calcul (Node natif : `node --test tests/`).
 * Cas de reference demande par le porteur de projet :
 *   10 stations B + 5 stations C, prix brut 8,7 EUR/MWhc, marge delegataire 20 %.
 */
import test from 'node:test';
import assert from 'node:assert/strict';
import { simuler, volumeCumac, prixNetEurMWhc, montantEuros, calculPointMort } from '../js/calc.js';

/** Egalite a 1 centime pres. */
const proche = (a, b, tol = 0.01) => assert.ok(Math.abs(a - b) < tol, `${a} != ${b}`);

test('volumes officiels TRA-SE-104', () => {
  assert.equal(volumeCumac({ nbA: 1 }).total, 534200);
  assert.equal(volumeCumac({ nbB: 1 }).total, 148400);
  assert.equal(volumeCumac({ nbC: 1 }).total, 39600);
  // 10 B + 5 C = 1 484 000 + 198 000
  assert.equal(volumeCumac({ nbB: 10, nbC: 5 }).total, 1682000);
});

test('prix net apres marge delegataire', () => {
  proche(prixNetEurMWhc(8.7, 20), 6.96);
  proche(prixNetEurMWhc(9, 0), 9);
  proche(prixNetEurMWhc(8.5, 100), 0);
});

test('conversion kWh cumac -> euros', () => {
  proche(montantEuros(1000, 7), 7);
  proche(montantEuros(148400, 7), 1038.8); // ~1 040 EUR/an pour une station B
  proche(montantEuros(534200, 7), 3739.4); // ~3 700 EUR/an pour une station A
  proche(montantEuros(39600, 7), 277.2);   // ~280 EUR/an pour une station C
});

test('cas de reference : 10 B + 5 C a 8,7 EUR/MWhc brut, 20 % de marge', () => {
  const r = simuler({ nbA: 0, nbB: 10, nbC: 5, prixBrutEurMWhc: 8.7, margeDelegatairePct: 20 });

  assert.equal(r.stations.total, 15);
  assert.equal(r.volume.total, 1682000);         // kWh cumac
  proche(r.prix.net, 6.96);                      // EUR/MWhc net
  proche(r.cee.brut, 14633.4);                   // 1 682 MWhc x 8,7
  proche(r.cee.net, 11706.72);                   // 1 682 MWhc x 6,96
  proche(r.margeParStation.B, 1032.864);         // 148,4 MWhc x 6,96
  proche(r.margeParStation.C, 275.616);          //  39,6 MWhc x 6,96
  proche(r.margeParStation.moyenne, 780.448);    // 11 706,72 / 15
  proche(r.margeRecurrenteAnnuelle, 11706.72);   // aucun cout renseigne
  assert.equal(r.coutsNonRenseignes, true);
});

test('cas de reference avec couts : entretien 300 EUR, installation 900 EUR, frais fixes 6 000 EUR', () => {
  const r = simuler({
    nbB: 10, nbC: 5, prixBrutEurMWhc: 8.7, margeDelegatairePct: 20,
    coutEntretienAnnuelParStation: 300, coutInstallationParStation: 900, fraisFixesAnnuels: 6000,
  });
  proche(r.charges.entretien, 4500);
  proche(r.charges.total, 10500);
  proche(r.margeRecurrenteAnnuelle, 11706.72 - 10500);
  proche(r.investissementInitial, 13500);
  proche(r.resultatAnnee1, 11706.72 - 10500 - 13500);
  proche(r.margeParStation.B, 1032.864 - 300);
  // Point mort recurrent en stations B : 6 000 / 732,864 = 8,19 -> 9
  assert.equal(r.pointMort.B, 9);
  // Une station C ne couvre pas son entretien : marge negative -> jamais rentable
  assert.equal(r.pointMort.C, null);
});

test('projection sur 3 ans', () => {
  const r = simuler({
    nbB: 10, prixBrutEurMWhc: 8.7, margeDelegatairePct: 20,
    coutInstallationParStation: 900, variationAnnuellePrixPct: 0,
  });
  const ceeAnnuel = montantEuros(1484000, 6.96);
  proche(r.projection[0].resultat, ceeAnnuel - 9000); // installation en annee 1
  proche(r.projection[1].resultat, ceeAnnuel);
  proche(r.projection[2].cumule, 3 * ceeAnnuel - 9000);
});

test('projection avec variation annuelle du prix CEE', () => {
  const r = simuler({ nbB: 1, prixBrutEurMWhc: 10, margeDelegatairePct: 0, variationAnnuellePrixPct: 10 });
  proche(r.projection[0].prixNetEurMWhc, 10);
  proche(r.projection[1].prixNetEurMWhc, 11);
  proche(r.projection[2].prixNetEurMWhc, 12.1);
});

test('point mort', () => {
  assert.equal(calculPointMort(1000, 0), 1);       // pas de frais fixes
  assert.equal(calculPointMort(1000, 5000), 5);
  assert.equal(calculPointMort(1000, 5001), 6);    // arrondi a l'entier superieur
  assert.equal(calculPointMort(-10, 5000), null);  // marge unitaire negative
  assert.equal(calculPointMort(null, 5000), null);
});

test('robustesse des entrees', () => {
  const r = simuler({ nbB: '3,4', prixBrutEurMWhc: '8,7', margeDelegatairePct: -5 });
  assert.equal(r.stations.B, 3);          // arrondi, jamais negatif
  proche(r.prix.brut, 8.7);               // virgule decimale acceptee
  assert.equal(r.prix.margeDelegatairePct, 0); // marge bornee a [0 ; 100]
});
