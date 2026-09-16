/** Tests de la préparation des e-mails (format RFC 5322 et sélection). */
import test from 'node:test';
import assert from 'node:assert/strict';
import {
  encoderEntete, plierBase64, construireEml, nomFichier, selectionner, valeursPour,
} from '../outils/preparer-envois.mjs';

test('les en-têtes non ASCII sont encodés (RFC 2047)', () => {
  assert.equal(encoderEntete('Hello'), 'Hello');
  const encode = encoderEntete('Financé par l’État');
  assert.match(encode, /^=\?UTF-8\?B\?/);
  assert.equal(Buffer.from(encode.slice(10, -2), 'base64').toString('utf8'), 'Financé par l’État');
});

test('le base64 est plié à 76 caractères', () => {
  const lignes = plierBase64('a'.repeat(200)).split('\r\n');
  assert.equal(lignes[0].length, 76);
  assert.equal(lignes.length, 3);
});

test('le message respecte la structure multipart attendue', () => {
  const eml = construireEml({
    de: 'aaron.harfi@noxemgroup.com',
    nomExpediteur: 'Aaron Harfi — NOXEM GROUP',
    a: 'contact@exemple.fr',
    objet: 'Le gonflage gratuit, financé par l’État',
    texte: 'Bonjour,',
    html: '<html><body><img src="cid:email-borne.png"></body></html>',
    images: [{ nom: 'email-borne.png', donnees: Buffer.from('faux-png') }],
  });

  assert.match(eml, /^From: =\?UTF-8\?B\?[^<]+<aaron\.harfi@noxemgroup\.com>/m);
  assert.match(eml, /^To: contact@exemple\.fr$/m);
  assert.match(eml, /^MIME-Version: 1\.0$/m);
  assert.match(eml, /Content-Type: multipart\/related; type="multipart\/alternative"/);
  assert.match(eml, /Content-Type: multipart\/alternative/);
  assert.match(eml, /Content-Type: text\/plain; charset=UTF-8/);
  assert.match(eml, /Content-Type: text\/html; charset=UTF-8/);
  // L'image est liée par son Content-ID, celui utilisé dans le HTML.
  assert.match(eml, /Content-ID: <email-borne\.png>/);
  assert.match(eml, /Content-Disposition: inline; filename="email-borne\.png"/);
  // Les frontières sont ouvertes puis refermées.
  const racine = eml.match(/boundary="([^"]+_racine)"/)[1];
  assert.ok(eml.includes(`--${racine}--`), 'la frontière racine doit être refermée');
  // Les sauts de ligne sont bien en CRLF.
  assert.ok(eml.includes('\r\n'));
});

test('le nom de fichier est sûr et numéroté', () => {
  const nom = nomFichier(7, { nom: 'Intermarché Vaulx-en-Velin', ville: 'Vaulx-en-Velin' });
  assert.equal(nom, '007-Intermarche-Vaulx-en-Velin-Vaulx-en-Velin.eml');
  assert.equal(nomFichier(1, { nom: '', ville: '' }), '001-site.eml');
});

test('la sélection respecte le quota, le statut et l’adresse renseignée', () => {
  const sites = [
    { nom: 'A', contactEmail: 'a@x.fr', statut: 'a_contacter' },
    { nom: 'B', contactEmail: '', statut: 'a_contacter' },          // sans adresse
    { nom: 'C', contactEmail: 'c@x.fr', statut: 'signe' },          // déjà signé
    { nom: 'D', contactEmail: 'd@x.fr', statut: 'a_contacter' },
    { nom: 'E', contactEmail: 'e@x.fr', statut: 'a_contacter' },
  ];
  const retenus = selectionner(sites, { quota: 2 });
  assert.deepEqual(retenus.map((s) => s.nom), ['A', 'D']);
  assert.equal(selectionner(sites, { quota: 99 }).length, 3);
});

test('les variables reprennent la fiche, avec un repli générique', () => {
  const v = valeursPour({ nom: 'Carrefour Bron', contactPrenom: 'Sophie' });
  assert.equal(v['[Prénom]'], 'Sophie');
  assert.equal(v['[nom du site]'], 'Carrefour Bron');
  const generique = valeursPour({});
  assert.equal(generique['[Prénom]'], 'Madame, Monsieur');
  assert.equal(generique['[nom du site]'], 'votre établissement');
});
