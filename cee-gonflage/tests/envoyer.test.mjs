/** Tests des garde-fous d'envoi : journal, suppression, répartition, rythme. */
import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import {
  CAP_PAR_BOITE, volumeConseille, chargerJournal, dejaTraite, chargerSuppression,
  filtrerEnvoyables, capacite, repartir, pause, messagePour, resumePlan,
} from '../outils/envoyer.mjs';

const dossier = () => mkdtempSync(join(tmpdir(), 'noxem-'));

test('la montée en volume se fait par paliers hebdomadaires', () => {
  assert.equal(volumeConseille(0), 0);
  assert.equal(volumeConseille(1), 10);   // semaine 1
  assert.equal(volumeConseille(7), 10);
  assert.equal(volumeConseille(8), 20);   // semaine 2
  assert.equal(volumeConseille(15), 30);  // semaine 3
  assert.equal(volumeConseille(22), CAP_PAR_BOITE);
  assert.equal(volumeConseille(400), CAP_PAR_BOITE); // plafond de croisière
});

test('le journal est vide quand le fichier n’existe pas', () => {
  const journal = chargerJournal(join(dossier(), 'journal.json'));
  assert.deepEqual(journal.envois, []);
});

test('une adresse déjà envoyée n’est jamais renvoyée, un échec reste rejouable', () => {
  const journal = {
    envois: [
      { email: 'Mairie@Dardilly.fr', statut: 'ok' },
      { email: 'mairie@ecully.fr', statut: 'echec' },
    ],
  };
  // La comparaison ignore la casse : une adresse est la même en majuscules.
  assert.ok(dejaTraite(journal, 'mairie@dardilly.fr'));
  assert.ok(!dejaTraite(journal, 'mairie@ecully.fr'));
  assert.ok(!dejaTraite(journal, 'inconnu@x.fr'));
});

test('la liste de suppression ignore les commentaires et les lignes vides', () => {
  const d = dossier();
  const f = join(d, 'suppression.txt');
  writeFileSync(f, '# réponses STOP\nStop@Mairie.fr\n\n   autre@x.fr  \n');
  const set = chargerSuppression(f);
  assert.equal(set.size, 2);
  assert.ok(set.has('stop@mairie.fr'));
  assert.ok(set.has('autre@x.fr'));
  assert.ok(!set.has('# réponses stop'));
});

test('journal et suppression retirent bien les sites concernés', () => {
  const sites = [
    { nom: 'A', contactEmail: 'a@x.fr' },
    { nom: 'B', contactEmail: 'b@x.fr' },   // déjà contacté
    { nom: 'C', contactEmail: 'c@x.fr' },   // a répondu STOP
    { nom: 'D', contactEmail: '' },         // sans adresse
    { nom: 'E', contactEmail: 'e@x.fr' },
  ];
  const envoyables = filtrerEnvoyables(sites, {
    journal: { envois: [{ email: 'b@x.fr', statut: 'ok' }] },
    suppression: new Set(['c@x.fr']),
  });
  assert.deepEqual(envoyables.map((s) => s.nom), ['A', 'E']);
});

test('la répartition remplit les boîtes sans dépasser leur plafond', () => {
  const boites = [{ de: 'un@x.fr' }, { de: 'deux@x.fr' }, { de: 'trois@x.fr' }];
  const sites = Array.from({ length: 150 }, (_, i) => ({ contactEmail: `s${i}@x.fr` }));

  const lots = repartir(sites, boites, 40);
  assert.equal(capacite(boites, 40), 120);
  // 150 demandés, 120 de capacité : 30 ne partent pas aujourd'hui.
  assert.equal(lots.reduce((n, l) => n + l.sites.length, 0), 120);
  for (const lot of lots) assert.equal(lot.sites.length, 40);

  // Avec quatre boîtes, les 150 passent.
  const quatre = [...boites, { de: 'quatre@x.fr' }];
  assert.equal(repartir(sites, quatre, 40).reduce((n, l) => n + l.sites.length, 0), 150);

  // Aucune boîte déclarée : rien ne part, et surtout rien ne casse.
  assert.deepEqual(repartir(sites, [], 40), []);
});

test('la répartition alterne les boîtes au lieu de vider la première', () => {
  const boites = [{ de: 'un@x.fr' }, { de: 'deux@x.fr' }];
  const sites = Array.from({ length: 4 }, (_, i) => ({ contactEmail: `s${i}@x.fr` }));
  const lots = repartir(sites, boites, 40);
  assert.equal(lots[0].sites.length, 2);
  assert.equal(lots[1].sites.length, 2);
});

test('le rythme varie autour de l’intervalle demandé', () => {
  // Bornes de la variation : 40 % autour de 90 s, soit 72 s à 108 s.
  assert.equal(pause(90, 40, () => 0), 72000);
  assert.equal(pause(90, 40, () => 1), 108000);
  assert.equal(pause(90, 40, () => 0.5), 90000);
  // Une cadence parfaitement régulière est une signature d'automate :
  // deux appels consécutifs ne doivent pas donner la même valeur.
  assert.notEqual(pause(90, 40, () => 0.1), pause(90, 40, () => 0.9));
  assert.equal(pause(0), 0);
});

test('le message reprend la boîte expéditrice et le modèle demandé', () => {
  const boite = { nom: 'Aaron Harfi — NOXEM GROUP', de: 'aaron@noxemgroup.com' };
  const message = messagePour(
    { nom: 'Mairie de Dardilly', ville: 'Dardilly', contactEmail: 'mairie@dardilly.fr' },
    'mairie', boite,
  );
  assert.equal(message.from, 'Aaron Harfi — NOXEM GROUP <aaron@noxemgroup.com>');
  assert.equal(message.to, 'mairie@dardilly.fr');
  assert.match(message.subject, /commune/);
  assert.match(message.text, /transmettre ce message au service concerné/);
  assert.match(message.html, /Dardilly/);
});

test('le plan annonce le nombre de boîtes manquantes pour le volume demandé', () => {
  const boites = [{ de: 'un@x.fr' }];
  const sites = Array.from({ length: 150 }, (_, i) => ({ contactEmail: `s${i}@x.fr` }));
  const resume = resumePlan(repartir(sites, boites, 40), {
    demande: 150, disponibles: 150, capParBoite: 40, intervalle: 90,
  });
  assert.match(resume, /40 de capacité/);
  assert.match(resume, /il manque 3 boîte\(s\)/);
});
