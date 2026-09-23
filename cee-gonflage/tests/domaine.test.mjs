/** Tests du diagnostic SPF / DKIM / DMARC (analyse pure, sans réseau). */
import test from 'node:test';
import assert from 'node:assert/strict';
import {
  identifierHebergeur, analyserSpf, tailleCleDkim, analyserDkim, analyserDmarc,
  plateformesIncompletes, rapport,
} from '../outils/verifier-domaine.mjs';

const gravites = (r) => r.problemes.map(([g]) => g);
const textes = (r) => r.problemes.map(([, t]) => t).join(' | ');

test('l’hébergeur se déduit des serveurs MX', () => {
  assert.match(identifierHebergeur([{ exchange: 'mx10.antispam.mailspamprotection.com' }]), /SiteGround/);
  assert.match(identifierHebergeur([{ exchange: 'aspmx.l.google.com' }]), /Google Workspace/);
  assert.match(identifierHebergeur([{ exchange: 'noxem-com.mail.protection.outlook.com' }]), /Microsoft 365/);
  assert.equal(identifierHebergeur([{ exchange: 'mail.inconnu.xyz' }]), 'inconnu');
  assert.equal(identifierHebergeur([]), 'inconnu');
});

test('SPF : absence, doublon et mécanisme all', () => {
  assert.equal(analyserSpf([]).present, false);
  assert.deepEqual(gravites(analyserSpf([])), ['grave']);

  // Deux enregistrements SPF invalident l'authentification entière.
  const double = analyserSpf(['v=spf1 include:a ~all', 'v=spf1 include:b -all']);
  assert.deepEqual(gravites(double), ['grave']);
  assert.match(textes(double), /n'en faut qu'un/);

  // « +all » autorise le monde entier : c'est le pire cas.
  assert.deepEqual(gravites(analyserSpf(['v=spf1 +all'])), ['grave']);

  const softfail = analyserSpf(['v=spf1 +a +mx include:exemple.net ~all']);
  assert.equal(softfail.all, '~');
  assert.deepEqual(softfail.includes, ['exemple.net']);
  assert.deepEqual(gravites(softfail), ['moyen']);

  // Le cas propre : hardfail, aucun reproche.
  assert.deepEqual(analyserSpf(['v=spf1 include:exemple.net -all']).problemes, []);
});

test('la taille de clé DKIM se lit dans le champ p=', () => {
  // 162 octets de DER ≈ 1024 bits, 294 ≈ 2048.
  const cle = (octets) => `v=DKIM1; p=${Buffer.alloc(octets, 1).toString('base64')}`;
  assert.equal(tailleCleDkim(cle(162)), 1024);
  assert.equal(tailleCleDkim(cle(294)), 2048);
  assert.equal(tailleCleDkim('v=DKIM1; p='), 0);
  assert.equal(tailleCleDkim('rien du tout'), 0);
});

test('DKIM : absence, clé faible, clé révoquée', () => {
  assert.equal(analyserDkim(null, null).present, false);
  assert.deepEqual(gravites(analyserDkim(null, null)), ['grave']);

  const faible = analyserDkim('default', `v=DKIM1; p=${Buffer.alloc(162, 1).toString('base64')}`);
  assert.equal(faible.bits, 1024);
  assert.deepEqual(gravites(faible), ['moyen']);
  assert.match(textes(faible), /2048/);

  const bonne = analyserDkim('default', `v=DKIM1; p=${Buffer.alloc(294, 1).toString('base64')}`);
  assert.deepEqual(bonne.problemes, []);

  assert.deepEqual(gravites(analyserDkim('default', 'v=DKIM1; p=')), ['grave']);
});

test('DMARC : absence, p=none, rapports manquants', () => {
  assert.deepEqual(gravites(analyserDmarc([])), ['grave']);

  const surveillance = analyserDmarc(['v=DMARC1; p=none; rua=mailto:rua@dmarc.brevo.com']);
  assert.equal(surveillance.politique, 'none');
  assert.equal(surveillance.rua, 'rua@dmarc.brevo.com');
  assert.deepEqual(gravites(surveillance), ['moyen']);

  // Sans rua, on ne voit jamais qui écrit en son nom.
  assert.deepEqual(gravites(analyserDmarc(['v=DMARC1; p=quarantine'])), ['moyen']);

  // Le cas propre.
  assert.deepEqual(analyserDmarc(['v=DMARC1; p=reject; rua=mailto:dmarc@x.fr']).problemes, []);
});

test('une plateforme validée mais absente du SPF est signalée', () => {
  const txts = ['brevo-code:c38ed6df63bb2e35c4782d5d54daaa45', 'v=spf1 include:autre.net ~all'];
  const spf = analyserSpf(txts);
  const manquantes = plateformesIncompletes(txts, spf);
  assert.equal(manquantes.length, 1);
  assert.equal(manquantes[0].nom, 'Brevo');
  assert.equal(manquantes[0].attendu, 'spf.brevo.com');

  // Une fois l'include posé, plus rien à signaler.
  const corrige = ['brevo-code:abc', 'v=spf1 include:spf.brevo.com -all'];
  assert.deepEqual(plateformesIncompletes(corrige, analyserSpf(corrige)), []);
});

test('le rapport classe les problèmes graves en premier', () => {
  const texte = rapport({
    domaine: 'exemple.fr',
    mx: [{ exchange: 'mx10.antispam.mailspamprotection.com' }],
    txts: ['brevo-code:abc', 'v=spf1 +a +mx ~all'],
    dmarcTxts: ['v=DMARC1; p=none; rua=mailto:x@y.fr'],
    dkim: { selecteur: 'default', enregistrement: `v=DKIM1; p=${Buffer.alloc(162, 1).toString('base64')}` },
  });
  assert.match(texte, /SiteGround/);
  // Le premier problème listé doit être le grave.
  const premier = texte.slice(texte.indexOf('point(s) à traiter'));
  assert.ok(premier.indexOf('[GRAVE]') < premier.indexOf('[moyen]'));
});

test('un domaine sain ne déclenche aucune alerte', () => {
  const texte = rapport({
    domaine: 'propre.fr',
    mx: [{ exchange: 'aspmx.l.google.com' }],
    txts: ['v=spf1 include:_spf.google.com -all'],
    dmarcTxts: ['v=DMARC1; p=reject; rua=mailto:dmarc@propre.fr'],
    dkim: { selecteur: 'google', enregistrement: `v=DKIM1; p=${Buffer.alloc(294, 1).toString('base64')}` },
  });
  assert.match(texte, /Aucun défaut détecté/);
});
