/** Tests du contrôle qualité d'une liste d'adresses achetée ou récupérée. */
import test from 'node:test';
import assert from 'node:assert/strict';
import { classer, analyser, verdict, estPersonnelle, estScolaire } from '../outils/analyser-liste.mjs';

test('une adresse personnelle est reconnue comme telle (RGPD)', () => {
  assert.ok(estPersonnelle('jean.dupont@ville-x.fr'));
  assert.ok(estPersonnelle('a-boullier@ville-x.fr'));   // initiale.nom
  // Un point de contact contenant un point n'est pas une personne.
  assert.ok(!estPersonnelle('accueil.unique@ville-givors.fr'));
  assert.ok(!estPersonnelle('affaires.generales@bourgoinjallieu.fr'));
  assert.ok(!estPersonnelle('mairie@ville-ecully.fr'));
});

test('les adresses scolaires sont repérées', () => {
  assert.ok(estScolaire('0120769w@ac-toulouse.fr'));
  assert.ok(!estScolaire('contact@meyzieu.fr'));
});

test('chaque adresse est classée avec son motif', () => {
  assert.deepEqual(classer('accueil-mairie@ville-bron.fr'), {
    email: 'accueil-mairie@ville-bron.fr', garde: true, motif: 'retenue',
  });
  assert.match(classer('mairie.xyz@wanadoo.fr').motif, /domaine mort/);
  assert.equal(classer('mairie@orange.fr').motif, 'messagerie grand public');
  assert.equal(classer('0271251n@ac-rouen.fr').motif, 'établissement scolaire');
  assert.equal(classer('j.pothin@ville-ecully.fr').motif, 'adresse personnelle (RGPD)');
  assert.equal(classer('cuisine.centrale@mairie-meyzieu.fr').motif, 'pas un point de contact identifiable');
  assert.equal(classer('pas-une-adresse').motif, 'adresse invalide');
  // La casse et les espaces ne doivent pas faire échouer le classement.
  assert.ok(classer('  CONTACT@Meyzieu.FR  ').garde);
});

test('le bilan compte doublons, écarts et taux de rebond', () => {
  const bilan = analyser([
    'contact@meyzieu.fr', 'CONTACT@meyzieu.fr',        // doublon (casse)
    'mairie.a@wanadoo.fr', 'mairie.b@wanadoo.fr',       // domaines morts
    'accueil@ville-roanne.fr',
    'jean.dupont@ville-x.fr',                            // personnelle
  ]);
  assert.equal(bilan.fournies, 6);
  assert.equal(bilan.uniques, 5);
  assert.equal(bilan.doublons, 1);
  assert.deepEqual(bilan.liste.sort(), ['accueil@ville-roanne.fr', 'contact@meyzieu.fr']);
  assert.equal(bilan.retenues, 2);
  assert.equal(bilan.ecartees, 3);
  // 2 domaines morts sur 5 uniques.
  assert.equal(bilan.tauxRebondEstime, 0.4);
});

test('le verdict bascule aux seuils de 5 % et 10 %', () => {
  const sain = analyser(['contact@a.fr', 'accueil@b.fr', 'mairie@c.fr']);
  assert.match(verdict(sain), /taux de rebond acceptable/);

  // 2 morts sur 20 = 10 % exactement : pas encore le seuil bloquant.
  const limite = analyser([
    ...Array.from({ length: 18 }, (_, i) => `contact@commune${i}.fr`),
    'mairie.x@voila.fr', 'mairie.y@tiscali.fr',
  ]);
  assert.match(verdict(limite), /au-dessus du seuil de 5/i);

  const grillee = analyser(['contact@a.fr', 'mairie.x@wanadoo.fr', 'mairie.y@wanadoo.fr']);
  assert.match(verdict(grillee), /inutilisable telle quelle/);
});

test('une liste vide ne fait pas diviser par zéro', () => {
  const bilan = analyser([]);
  assert.equal(bilan.tauxRebondEstime, 0);
  assert.match(verdict(bilan), /0 adresse/);
});

test('le nom de commune se déduit des domaines explicites, et se signale douteux ailleurs', async () => {
  const { communeDepuisDomaine } = await import('../outils/analyser-liste.mjs');

  // Domaines explicites : déduction fiable.
  assert.deepEqual(communeDepuisDomaine('mairie-montjean53.fr'), { nom: 'Montjean', sur: true });
  assert.deepEqual(communeDepuisDomaine('ville-antibes.fr'), { nom: 'Antibes', sur: true });
  assert.deepEqual(communeDepuisDomaine('villede-lyon.fr'), { nom: 'Lyon', sur: true });

  // Domaine nu : le nom est probable mais non garanti.
  assert.equal(communeDepuisDomaine('capbreton.fr').sur, false);
  assert.equal(communeDepuisDomaine('capbreton.fr').nom, 'Capbreton');

  // Capitalisation française : les particules restent en minuscules.
  assert.equal(communeDepuisDomaine('mairie-vern-sur-seiche.fr').nom, 'Vern-sur-Seiche');
  assert.equal(communeDepuisDomaine('ville-aix-en-provence.fr').nom, 'Aix-en-Provence');

  // Trop court ou vide : on ne devine pas.
  assert.deepEqual(communeDepuisDomaine('ab.fr'), { nom: '', sur: false });
  assert.deepEqual(communeDepuisDomaine(''), { nom: '', sur: false });
  assert.deepEqual(communeDepuisDomaine(null), { nom: '', sur: false });

  // LIMITE CONNUE, volontairement figée par ce test : un nom composé collé
  // ne peut pas être recoupé sans dictionnaire des communes. « Sainte-Foy-lès-Lyon »
  // ressort collé — donc impossible à envoyer sans relecture.
  assert.equal(communeDepuisDomaine('ville-saintefoyleslyon.fr').nom, 'Saintefoyleslyon');
});

test('les services sans rapport avec un parking sont écartés', async () => {
  const { estMauvaisService } = await import('../outils/analyser-liste.mjs');
  assert.ok(estMauvaisService('accueil_bij@ville-antibes.fr'));        // info jeunesse
  assert.ok(estMauvaisService('accueil.mdj@mairie-guipavas.fr'));      // maison des jeunes
  assert.ok(estMauvaisService('cuisine.centrale@mairie-meyzieu.fr'));
  assert.ok(estMauvaisService('etat-civil@ville-x.fr'));
  assert.ok(estMauvaisService('bibliotheque@ville-x.fr'));
  // Ceux qui décident d'un aménagement de parking passent.
  assert.ok(!estMauvaisService('accueil-mairie@ville-guise.fr'));
  assert.ok(!estMauvaisService('accueil.environnement@mairie-mandelieu.fr'));
  assert.ok(!estMauvaisService('cadredevie@mairie-francheville69.fr'));
  assert.ok(!estMauvaisService('services.techniques@ville-x.fr'));
});

test('un nom composé aplati bascule en version générique', async () => {
  const { nomProbablementColle } = await import('../outils/analyser-liste.mjs');
  assert.ok(nomProbablementColle('Sinlenoble'));     // Sin-le-Noble
  assert.ok(nomProbablementColle('Azaysurcher'));    // Azay-sur-Cher
  assert.ok(nomProbablementColle('Batzsurmer'));     // Batz-sur-Mer
  // Les noms simples passent.
  assert.ok(!nomProbablementColle('Montjean'));
  assert.ok(!nomProbablementColle('Albi'));
  assert.ok(!nomProbablementColle('Guipavas'));
  // Déjà décomposé : rien à signaler.
  assert.ok(!nomProbablementColle('Vern-sur-Seiche'));
  assert.ok(!nomProbablementColle(''));
});

test('les formes d’adresse qui ont rebondi à 100 % sont écartées', async () => {
  const { formeRisquee } = await import('../outils/analyser-liste.mjs');
  // Mesuré le 17/09 : 3 rebonds sur 3 pour accueil.mairie@, 1 sur 1 pour un préfixe numérique.
  assert.equal(formeRisquee('accueil.mairie@ville-renage.fr'), 'forme accueil.mairie');
  assert.equal(formeRisquee('05contact@mairie-montjean53.fr'), 'préfixe numérique');
  // Les formes qui ont tenu passent.
  assert.equal(formeRisquee('accueil@mairie-lherm.fr'), '');
  assert.equal(formeRisquee('contact@colmar.fr'), '');
  assert.equal(formeRisquee('accueil-mairie@ville-guise.fr'), '');
  assert.equal(formeRisquee('accueil.environnement@mairie-mandelieu.fr'), '');
});
