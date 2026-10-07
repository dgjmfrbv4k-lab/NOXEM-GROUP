/** Tests de la collecte des mairies (parsing de l'Annuaire de l'administration). */
import test from 'node:test';
import assert from 'node:assert/strict';
import { lireChamp, extraireCourriel, extraireTelephone, extraireAdresse, versSite, nettoyer }
  from '../js/annuaire.js';
// versCSV reste côté outil : le navigateur importe directement dans le CRM.
import { versCSV } from '../outils/collecte-mairies.mjs';

// L'annuaire sérialise certains champs en JSON dans une chaîne : les deux
// formes doivent être acceptées, faute de quoi la collecte rend des fiches vides.
test('les champs JSON sérialisés sont lus comme les champs structurés', () => {
  assert.equal(lireChamp('texte simple'), 'texte simple');
  assert.deepEqual(lireChamp('["a@b.fr"]'), ['a@b.fr']);
  assert.deepEqual(lireChamp([{ valeur: 'x' }]), [{ valeur: 'x' }]);
  assert.equal(lireChamp(''), null);
  assert.equal(lireChamp('[cassé'), '[cassé'); // JSON invalide : on rend la chaîne telle quelle
});

test('extraction du courriel, quelle que soit la forme', () => {
  assert.equal(extraireCourriel({ adresse_courriel: '["mairie@ville.fr"]' }), 'mairie@ville.fr');
  assert.equal(extraireCourriel({ adresse_courriel: 'contact@ville.fr' }), 'contact@ville.fr');
  assert.equal(extraireCourriel({ adresse_courriel: [{ valeur: 'dgs@ville.fr' }] }), 'dgs@ville.fr');
  assert.equal(extraireCourriel({ adresse_courriel: '["pas-une-adresse"]' }), '');
  assert.equal(extraireCourriel({}), '');
});

test('extraction du téléphone', () => {
  assert.equal(extraireTelephone({ telephone: '[{"valeur":"04 72 00 00 00"}]' }), '04 72 00 00 00');
  assert.equal(extraireTelephone({}), '');
});

test('l’adresse physique est préférée aux autres types d’adresse', () => {
  const a = extraireAdresse({
    adresse: JSON.stringify([
      { type_adresse: 'Adresse postale', numero_voie: 'BP 12', code_postal: '69001', nom_commune: 'Lyon' },
      { type_adresse: 'Adresse', numero_voie: '1 place de la Mairie', code_postal: '69001', nom_commune: 'Lyon' },
    ]),
  });
  assert.equal(a.voie, '1 place de la Mairie');
  assert.equal(a.codePostal, '69001');
  assert.equal(a.ville, 'Lyon');
});

test('conversion en fiche site du CRM', () => {
  const site = versSite({
    id: 'mairie-69123',
    nom: 'Mairie de Vaulx-en-Velin',
    adresse: JSON.stringify([{ type_adresse: 'Adresse', numero_voie: 'place de la Nation', code_postal: '69120', nom_commune: 'Vaulx-en-Velin' }]),
    adresse_courriel: '["mairie@vaulx-en-velin.fr"]',
    telephone: '[{"valeur":"04 72 04 80 80"}]',
  });
  assert.equal(site.nom, 'Mairie de Vaulx-en-Velin');
  assert.equal(site.contactEmail, 'mairie@vaulx-en-velin.fr');
  assert.equal(site.typeSite, 'Collectivité');
  assert.equal(site.statut, 'a_contacter');
  assert.equal(site.typeCee, '', 'le type reste à qualifier : une commune a souvent du B et du C');
  assert.match(site.notes, /04 72 04 80 80/);
  assert.match(site.notes, /dossier groupé/);
  // Aucun nom de personne n'est repris.
  assert.equal(site.contactPrenom, '');
});

test('les fiches sans adresse et les doublons sont écartés', () => {
  const sites = [
    { nom: 'A', contactEmail: 'a@x.fr' },
    { nom: 'B', contactEmail: '' },
    { nom: 'C', contactEmail: 'A@X.FR' }, // même adresse, casse différente
  ];
  assert.equal(nettoyer(sites).length, 1);
});

test('export CSV', () => {
  const csv = versCSV([{ nom: 'Mairie de X', adresse: '1 rue; test', codePostal: '69000', ville: 'X', contactEmail: 'm@x.fr', notes: '' }]);
  assert.ok(csv.startsWith('﻿Commune;Adresse;'));
  assert.match(csv, /"1 rue; test"/);
});

test('l’URL de requête cible bien les mairies du département', async () => {
  const { urlRequete } = await import('../js/annuaire.js');
  const url = new URL(urlRequete('69', { limit: 100, offset: 200 }));
  assert.equal(url.searchParams.get('where'), 'pivot LIKE "mairie" AND code_insee_commune LIKE "69%"');
  assert.equal(url.searchParams.get('limit'), '100');
  assert.equal(url.searchParams.get('offset'), '200');
  // Un département corse ou d'outre-mer passe par le même chemin.
  assert.match(new URL(urlRequete('2A')).searchParams.get('where'), /"2A%"/);
});

test('la collecte pagine jusqu’au bout et remonte l’avancement', async () => {
  const { collecterDepartement } = await import('../js/annuaire.js');
  const appels = [];
  const avancements = [];
  const fetchFn = async (url) => {
    const offset = Number(new URL(url).searchParams.get('offset'));
    appels.push(offset);
    // Deux pages pleines, puis une partielle : la collecte doit s'arrêter là.
    const n = offset < 20 ? 10 : 4;
    return { ok: true, json: async () => ({ total_count: 24, results: Array.from({ length: n }, (_, i) => ({ id: offset + i })) }) };
  };

  const r = await collecterDepartement('69', {
    fetchFn, parPage: 10, surAvancement: (a) => avancements.push(a.recus),
  });
  assert.equal(r.length, 24);
  assert.deepEqual(appels, [0, 10, 20]);
  assert.deepEqual(avancements, [10, 20, 24]);
});

test('une erreur de l’annuaire est remontée en clair', async () => {
  const { collecterDepartement } = await import('../js/annuaire.js');
  const fetchFn = async () => ({ ok: false, status: 503 });
  await assert.rejects(
    () => collecterDepartement('69', { fetchFn }),
    /L'annuaire a répondu 503/,
  );
});
