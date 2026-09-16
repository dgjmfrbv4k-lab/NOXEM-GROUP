/** Tests des echeances et des pieces du dossier CEE. */
import test from 'node:test';
import assert from 'node:assert/strict';
import { echeances, ajouterAnnees, joursEntre, avancementPieces, PIECES_DOSSIER } from '../js/dossier.js';

test('achevement = date anniversaire de la signature', () => {
  const e = echeances('2026-03-15', new Date('2026-04-01T12:00:00'));
  assert.equal(e.achevement.getFullYear(), 2027);
  assert.equal(e.achevement.getMonth(), 2); // mars
  assert.equal(e.achevement.getDate(), 15);
  assert.equal(e.anneeContrat, 1);
});

test('annee de contrat suivante une fois l’anniversaire passe', () => {
  const e = echeances('2026-03-15', new Date('2027-06-01T12:00:00'));
  assert.equal(e.anneeContrat, 2);
  assert.equal(e.prochaineEcheance.getFullYear(), 2028);
});

test('niveaux d’alerte avant la date anniversaire', () => {
  assert.equal(echeances('2026-03-15', new Date('2027-03-01T12:00:00')).niveau, 'urgent');    // J-14
  assert.equal(echeances('2026-03-15', new Date('2027-01-15T12:00:00')).niveau, 'vigilance'); // J-59
  assert.equal(echeances('2026-03-15', new Date('2026-06-15T12:00:00')).niveau, 'ok');
  assert.equal(echeances('', new Date()).niveau, 'inconnu');
});

test('29 fevrier replie sur le 28 fevrier', () => {
  const d = ajouterAnnees(new Date('2028-02-29T00:00:00'), 1);
  assert.equal(d.getMonth(), 1);
  assert.equal(d.getDate(), 28);
});

test('joursEntre ignore l’heure', () => {
  assert.equal(joursEntre(new Date('2026-01-01T23:00:00'), new Date('2026-01-02T01:00:00')), 1);
});

test('avancement des pieces du dossier', () => {
  assert.equal(avancementPieces({}).complet, false);
  const toutes = Object.fromEntries(PIECES_DOSSIER.filter((p) => p.obligatoire).map((p) => [p.id, true]));
  assert.equal(avancementPieces(toutes).complet, true);
});
