/** Tests de l'estimation ADVENIR (bornes de recharge). */
import test from 'node:test';
import assert from 'node:assert/strict';
import { estimerPrimeRecharge } from '../js/recharge.js';

const proche = (a, b, tol = 0.01) => assert.ok(Math.abs(a - b) < tol, `${a} != ${b}`);

test('prime plafonnée : 4 points à 3 500 € HT, 30 %, plafond 2 100 €', () => {
  const r = estimerPrimeRecharge({ nbPoints: 4, coutHtParPoint: 3500, tauxPriseEnChargePct: 30, plafondParPoint: 2100 });
  proche(r.primeParPoint, 1050);      // 30 % de 3 500 = 1 050 < plafond
  assert.equal(r.plafondAtteint, false);
  proche(r.primeTotale, 4200);
  proche(r.coutTotal, 14000);
  proche(r.resteACharge, 9800);
  proche(r.tauxReelPct, 30);
});

test('le plafond écrête la prime', () => {
  const r = estimerPrimeRecharge({ nbPoints: 2, coutHtParPoint: 12000, tauxPriseEnChargePct: 50, plafondParPoint: 2100 });
  proche(r.primeParPoint, 2100);      // 50 % = 6 000, écrêté à 2 100
  assert.equal(r.plafondAtteint, true);
  proche(r.primeTotale, 4200);
  proche(r.tauxReelPct, 17.5);        // taux réel très inférieur au taux affiché
});

test('aucun point de charge : tout est neutre', () => {
  const r = estimerPrimeRecharge({ nbPoints: 0, coutHtParPoint: 3500, tauxPriseEnChargePct: 30, plafondParPoint: 2100 });
  proche(r.primeTotale, 0);
  proche(r.resteACharge, 0);
  proche(r.resteAChargeParPoint, 0);
  proche(r.tauxReelPct, 0);
});

test('entrées invalides bornées', () => {
  const r = estimerPrimeRecharge({ nbPoints: -3, coutHtParPoint: '3 500', tauxPriseEnChargePct: 150, plafondParPoint: 2100 });
  assert.equal(r.nbPoints, 0);
  assert.equal(r.tauxReelPct, 0);
});
