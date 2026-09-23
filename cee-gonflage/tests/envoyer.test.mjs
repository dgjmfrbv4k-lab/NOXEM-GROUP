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

test('le jour de campagne se compte depuis le démarrage', async () => {
  const { jourDeCampagne } = await import('../outils/envoyer.mjs');
  assert.equal(jourDeCampagne('2026-09-17', new Date('2026-09-17T23:00:00Z')), 1);
  assert.equal(jourDeCampagne('2026-09-17', new Date('2026-09-18T06:00:00Z')), 2);
  assert.equal(jourDeCampagne('2026-09-17', new Date('2026-10-08T12:00:00Z')), 22);
  assert.throws(() => jourDeCampagne('pas-une-date'), /illisible/);
});

test('le palier du jour prime sur le volume demandé', async () => {
  const { plafondDuJour } = await import('../outils/envoyer.mjs');
  const campagne = { debut: '2026-09-17', capMax: 40 };

  // Jour 1 avec 4 boîtes : 10 par boîte, donc 40 — pas 150.
  const j1 = plafondDuJour(campagne, 4, new Date('2026-09-17T10:00:00Z'));
  assert.deepEqual(j1, { jour: 1, parBoite: 10, total: 40 });

  // Semaine 2, puis 3, puis le régime de croisière.
  assert.equal(plafondDuJour(campagne, 4, new Date('2026-09-25T10:00:00Z')).parBoite, 20);
  assert.equal(plafondDuJour(campagne, 4, new Date('2026-10-02T10:00:00Z')).parBoite, 30);
  const croisiere = plafondDuJour(campagne, 4, new Date('2026-10-10T10:00:00Z'));
  assert.equal(croisiere.parBoite, 40);
  assert.equal(croisiere.total, 160); // les 150 deviennent atteignables ici, pas avant

  // capMax abaissé volontairement : il plafonne le palier.
  assert.equal(plafondDuJour({ debut: '2026-09-17', capMax: 15 }, 2, new Date('2026-10-10T10:00:00Z')).parBoite, 15);
});

test('le plan annonce le palier et le fait primer sur la demande', async () => {
  const { plafondDuJour: p, repartir: r, resumePlan: rp } = await import('../outils/envoyer.mjs');
  const boites = [{ de: 'un@x.fr' }, { de: 'deux@x.fr' }];
  const palier = p({ debut: '2026-09-17', capMax: 40 }, boites.length, new Date('2026-09-17T10:00:00Z'));
  const sites = Array.from({ length: 150 }, (_, i) => ({ contactEmail: `s${i}@x.fr` }));
  const texte = rp(r(sites.slice(0, palier.total), boites, palier.parBoite), {
    demande: 150, disponibles: 150, capParBoite: palier.parBoite, intervalle: 90, palier,
  });
  assert.match(texte, /Jour 1 de la campagne — palier : 10 par boîte/);
  assert.match(texte, /le palier prime, ce sera 20/);
});

test('la relance ne part qu’après le délai, une seule fois, et jamais aux désinscrits', async () => {
  const { candidatsRelance } = await import('../outils/envoyer.mjs');
  const maintenant = new Date('2026-10-01T10:00:00Z');
  const ilYA = (jours) => new Date(maintenant - jours * 86400000).toISOString();

  const sites = [
    { nom: 'Mûr', contactEmail: 'mur@x.fr' },          // contacté il y a 12 jours
    { nom: 'Trop tôt', contactEmail: 'tot@x.fr' },     // contacté il y a 3 jours
    { nom: 'Déjà relancé', contactEmail: 'deja@x.fr' },
    { nom: 'Jamais contacté', contactEmail: 'rien@x.fr' },
    { nom: 'Désinscrit', contactEmail: 'stop@x.fr' },  // mûr, mais a dit STOP
    { nom: 'Échec', contactEmail: 'echec@x.fr' },      // le premier envoi a échoué
  ];
  const journal = {
    envois: [
      { email: 'mur@x.fr', statut: 'ok', type: 'premier', date: ilYA(12), messageId: '<a@noxem>', objet: 'Station de gonflage' },
      { email: 'tot@x.fr', statut: 'ok', type: 'premier', date: ilYA(3) },
      { email: 'deja@x.fr', statut: 'ok', type: 'premier', date: ilYA(30) },
      { email: 'deja@x.fr', statut: 'ok', type: 'relance', date: ilYA(20) },
      { email: 'stop@x.fr', statut: 'ok', type: 'premier', date: ilYA(15) },
      { email: 'echec@x.fr', statut: 'echec', type: 'premier', date: ilYA(15) },
    ],
  };

  const retenus = candidatsRelance(sites, {
    journal, suppression: new Set(['stop@x.fr']), joursMin: 10, aujourdhui: maintenant,
  });
  assert.deepEqual(retenus.map((s) => s.nom), ['Mûr']);
  // Le fil du premier message est conservé pour rattacher la relance.
  assert.equal(retenus[0]._fil.messageId, '<a@noxem>');
  assert.equal(retenus[0]._fil.jours, 12);
});

test('un journal ancien sans champ type reste interprétable', async () => {
  const { dejaTraite, envoisReussis } = await import('../outils/envoyer.mjs');
  const journal = { envois: [{ email: 'vieux@x.fr', statut: 'ok', date: '2026-01-01T00:00:00Z' }] };
  assert.equal(envoisReussis(journal, 'vieux@x.fr')[0].type, 'premier');
  assert.ok(dejaTraite(journal, 'vieux@x.fr'));
});

test('la relance reprend le fil et préfixe l’objet', async () => {
  const { messagePour } = await import('../outils/envoyer.mjs');
  const boite = { nom: 'Aaron Harfi', de: 'aaron@noxem-group.com' };
  const site = {
    nom: 'Mairie de Dardilly', ville: 'Dardilly', contactEmail: 'mairie@dardilly.fr',
    _fil: { messageId: '<abc@noxem>', objet: 'Station de gonflage en libre accès', jours: 12 },
  };

  const m = messagePour(site, 'relance', boite);
  assert.equal(m.subject, 'Re: Station de gonflage en libre accès');
  assert.equal(m.inReplyTo, '<abc@noxem>');
  assert.deepEqual(m.references, ['<abc@noxem>']);
  assert.match(m.text, /revenir vers vous/);
  assert.match(m.text, /Dardilly/);
  // La porte de sortie doit être explicite : un « non » vaut mieux qu'un signalement.
  assert.match(m.text, /je ne vous solliciterai plus/);

  // Un objet déjà préfixé ne le devient pas deux fois.
  const dejaRe = messagePour({ ...site, _fil: { ...site._fil, objet: 'Re: Déjà' } }, 'relance', boite);
  assert.equal(dejaRe.subject, 'Re: Déjà');

  // Sans fil connu, la relance part quand même, avec son objet par défaut.
  const sansFil = messagePour({ ...site, _fil: undefined }, 'relance', boite);
  assert.equal(sansFil.subject, 'Re: votre parking');
  assert.equal(sansFil.inReplyTo, undefined);

  // Un premier envoi n'est jamais rattaché à un fil.
  const premier = messagePour(site, 'mairie', boite);
  assert.equal(premier.inReplyTo, undefined);
  assert.match(premier.subject, /commune/);
});
