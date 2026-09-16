/** Tests de la collecte de cibles (classification OSM -> fiche TRA-SE-104). */
import test from 'node:test';
import assert from 'node:assert/strict';
import { classifierOsm, versSite, nettoyer, versCSV, requeteParZone } from '../outils/collecte-cibles.mjs';

test('aire de service autoroutière -> type A', () => {
  assert.equal(classifierOsm({ highway: 'services' }).type, 'A');
  assert.equal(classifierOsm({ highway: 'rest_area' }).type, 'A');
});

test('commerces ouverts au public -> type B', () => {
  assert.equal(classifierOsm({ shop: 'supermarket' }).type, 'B');
  assert.equal(classifierOsm({ shop: 'mall' }).type, 'B');
  assert.equal(classifierOsm({ amenity: 'fuel' }).type, 'B');
});

test('parking : public -> B, réservé -> C', () => {
  assert.equal(classifierOsm({ amenity: 'parking' }).type, 'B');
  assert.equal(classifierOsm({ amenity: 'parking', access: 'customers' }).type, 'B');
  assert.equal(classifierOsm({ amenity: 'parking', access: 'private' }).type, 'C');
  assert.equal(classifierOsm({ amenity: 'parking', parking: 'staff' }).type, 'C');
});

test('élément inconnu : type à qualifier', () => {
  assert.equal(classifierOsm({ amenity: 'bench' }).type, '');
});

test('conversion en fiche site', () => {
  const site = versSite({
    type: 'way', id: 42,
    tags: {
      name: 'Intermarché Vaulx-en-Velin', shop: 'supermarket', operator: 'SAS Beaulieu',
      'addr:housenumber': '12', 'addr:street': 'rue des Peupliers',
      'addr:postcode': '69120', 'addr:city': 'Vaulx-en-Velin',
    },
  });
  assert.equal(site.nom, 'Intermarché Vaulx-en-Velin');
  assert.equal(site.societe, 'SAS Beaulieu');
  assert.equal(site.typeCee, 'B');
  assert.equal(site.adresse, '12 rue des Peupliers');
  assert.equal(site.ville, 'Vaulx-en-Velin');
  assert.equal(site.statut, 'a_contacter');
  assert.match(site.notes, /OpenStreetMap/);
  // Aucune donnée personnelle n'est reprise.
  assert.equal(site.contactPrenom, '');
  assert.equal(site.contactEmail, '');
});

test('les doublons et les fiches vides sont écartés', () => {
  const brut = [
    { type: 'node', id: 1, tags: { name: 'Carrefour Bron', shop: 'supermarket', 'addr:city': 'Bron' } },
    { type: 'way', id: 2, tags: { name: 'Carrefour Bron', shop: 'supermarket', 'addr:city': 'Bron' } },
    { type: 'node', id: 3, tags: { amenity: 'parking' } },
  ].map(versSite);
  assert.equal(nettoyer(brut).length, 1);
});

test('export CSV : en-têtes et séparateur français', () => {
  const csv = versCSV([versSite({ type: 'node', id: 7, tags: { name: 'Test; virgule', shop: 'supermarket' } })]);
  assert.ok(csv.startsWith('﻿Nom du site;Société;'));
  assert.match(csv, /"Test; virgule"/);
});

test('la requête Overpass cible bien la zone demandée', () => {
  const r = requeteParZone('Métropole de Lyon');
  assert.match(r, /area\["name"="Métropole de Lyon"\]/);
  assert.match(r, /\["shop"="supermarket"\]\(area\.zone\)/);
  assert.match(r, /out center tags;/);
});
