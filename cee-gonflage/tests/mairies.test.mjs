/** Tests de la collecte des mairies (parsing de l'Annuaire de l'administration). */
import test from 'node:test';
import assert from 'node:assert/strict';
import { lireChamp, extraireCourriel, extraireTelephone, extraireAdresse, versSite, nettoyer, versCSV }
  from '../outils/collecte-mairies.mjs';

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
