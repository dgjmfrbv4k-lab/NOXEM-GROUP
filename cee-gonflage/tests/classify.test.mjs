/** Tests de la classification A / B / C et de la checklist d'eligibilite. */
import test from 'node:test';
import assert from 'node:assert/strict';
import { classifier, estimationPourType, evaluerEligibilite } from '../js/classify.js';

test('autoroute -> type A', () => {
  assert.equal(classifier({ autoroute: true }).type, 'A');
});

test('supermarche (prive mais ouvert au public) -> type B', () => {
  const r = classifier({ autoroute: false, reserveSalaries: false, ouvertPublic: true });
  assert.equal(r.type, 'B');
});

test('parking reserve aux salaries -> type C', () => {
  const r = classifier({ autoroute: false, reserveSalaries: true, ouvertPublic: false });
  assert.equal(r.type, 'C');
});

test('site mixte public + zone salaries -> type B avec alerte', () => {
  const r = classifier({ autoroute: false, reserveSalaries: true, ouvertPublic: true });
  assert.equal(r.type, 'B');
  assert.match(r.alerte, /type C/);
});

test('cas non qualifiable -> aucun type', () => {
  assert.equal(classifier({ autoroute: false, reserveSalaries: false, ouvertPublic: false }).type, null);
  assert.equal(classifier({}).type, null);
});

test('estimation pour 3 stations B a 8,7 EUR/MWhc et 20 % de marge', () => {
  const e = estimationPourType('B', 3, 8.7, 20);
  assert.equal(e.kwhCumacTotal, 445200);
  assert.ok(Math.abs(e.montantNetParStation - 1032.864) < 0.01);
  assert.ok(Math.abs(e.montantNetTotal - 3098.592) < 0.01);
});

test('checklist : les conditions bloquantes conditionnent l’eligibilite', () => {
  assert.equal(evaluerEligibilite({}).eligible, false);
  const toutBloquant = {
    gratuit: true, acces: true, panneau: true, securite: true, entretien: true, delai15j: true,
  };
  const r = evaluerEligibilite(toutBloquant);
  assert.equal(r.eligible, true);
  assert.equal(r.aCompleter.length, 2); // procedure de controle + etat recapitulatif
  const sansGratuite = { ...toutBloquant, gratuit: false };
  assert.equal(evaluerEligibilite(sansGratuite).eligible, false);
});
