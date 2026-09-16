/** Tests de la simulation par profil de client. */
import test from 'node:test';
import assert from 'node:assert/strict';
import { PROFILS, chiffrer, classer, dossiersPourObjectif } from '../outils/simuler-profils.mjs';

const HYPOTHESES = {
  prixBrutEurMWhc: 8.7, margeDelegatairePct: 20,
  coutEntretienAnnuelParStation: 300, coutInstallationParStation: 900,
};
const proche = (a, b, tol = 1) => assert.ok(Math.abs(a - b) < tol, `${a} != ${b}`);

test('un supermarché indépendant : 1 station B', () => {
  const l = chiffrer(PROFILS.find((p) => p.nom.startsWith('Supermarché indépendant')), HYPOTHESES);
  assert.equal(l.stations, 1);
  assert.equal(l.kwhCumac, 148400);
  proche(l.ceeNet, 1032.86);
  proche(l.margeAnnuelle, 732.86);       // 1 032,86 − 300 d'entretien
  proche(l.investissement, 900);
  proche(l.resultatAnnee1, -167.14);     // l'installation n'est pas absorbée la première année
});

test('le dossier groupé d’une commune additionne B et C', () => {
  const l = chiffrer(PROFILS.find((p) => p.nom.startsWith('Commune')), HYPOTHESES);
  assert.equal(l.stations, 2);
  assert.equal(l.kwhCumac, 148400 + 39600);
});

test('une station de type C seule ne couvre pas son entretien', () => {
  const l = chiffrer(PROFILS.find((p) => p.nom.startsWith('Entreprise')), HYPOTHESES);
  assert.ok(l.margeAnnuelle < 0, 'la marge doit être négative avec 300 € d’entretien');
  assert.equal(dossiersPourObjectif(l, 50000), null);
});

test('le classement privilégie la marge rapportée à l’effort commercial', () => {
  const lignes = classer(HYPOTHESES);
  assert.equal(lignes[0].nom, 'Groupement de 10 supermarchés');
  // Un intégré rapporte autant qu'un indépendant, mais coûte quatre fois plus d'efforts.
  const independant = lignes.find((l) => l.nom.startsWith('Supermarché indépendant'));
  const integre = lignes.find((l) => l.nom.startsWith('Supermarché intégré'));
  proche(independant.margeAnnuelle, integre.margeAnnuelle);
  assert.ok(independant.margeParRendezVous > integre.margeParRendezVous);
});

test('nombre de dossiers pour atteindre un objectif', () => {
  const l = chiffrer(PROFILS.find((p) => p.nom.startsWith('Supermarché indépendant')), HYPOTHESES);
  assert.equal(dossiersPourObjectif(l, 50000), 69); // 50 000 / 732,86 = 68,2 -> 69
});
