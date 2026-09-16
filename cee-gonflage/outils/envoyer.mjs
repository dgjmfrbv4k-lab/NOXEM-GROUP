/**
 * envoyer.mjs
 * ---------------------------------------------------------------------------
 * Envoie la série du jour depuis VOS boîtes d'envoi, en respectant un rythme
 * qui ne grille pas le domaine.
 *
 * Pourquoi cet outil en plus de preparer-envois.mjs : à 25 ou 50 messages par
 * jour, ouvrir les .eml un par un reste tenable et permet de relire chaque
 * message. À 150 par jour, ce n'est plus possible. Cet outil automatise
 * l'envoi — pas le ciblage, pas la rédaction, et pas la prudence.
 *
 *   # 1. Simulation (par défaut) : rien n'est envoyé, le plan est affiché
 *   node outils/envoyer.mjs --sites mairies-69.json --modele mairie --quota 150
 *
 *   # 2. Envoi réel
 *   node outils/envoyer.mjs --sites mairies-69.json --modele mairie --quota 150 --envoyer
 *
 * Trois garde-fous, tous actifs par défaut :
 *   - JOURNAL      envois/journal.json — un site déjà contacté ne l'est jamais
 *                  deux fois, même si la commande est relancée ;
 *   - SUPPRESSION  envois/suppression.txt — une adresse par ligne (réponses
 *                  « STOP », erreurs définitives). Jamais recontactée ;
 *   - RYTHME       un intervalle entre chaque message, et un plafond par boîte.
 *
 * Prérequis pour l'envoi réel : `npm i nodemailer`, et au moins une boîte
 * déclarée dans envois/boites.json (voir MODELE_BOITES ci-dessous).
 * ---------------------------------------------------------------------------
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'node:fs';
import { construire, versionTexte, modele } from '../emails/build-email.mjs';
import { valeursPour, selectionner } from './preparer-envois.mjs';

/**
 * Plafond quotidien par boîte d'envoi.
 *
 * Ce n'est pas la limite technique du fournisseur (Google Workspace accepte
 * 2 000 destinataires externes par jour) : c'est le seuil au-delà duquel une
 * boîte qui fait de la prospection à froid se fait repérer. Les plateformes
 * de cold e-mailing tournent toutes autour de 30-50 par boîte et par jour.
 * Le volume se gagne en ajoutant des boîtes, pas en poussant une seule.
 */
export const CAP_PAR_BOITE = 40;

/** Exemple de configuration, écrit sur disque à la première exécution. */
export const MODELE_BOITES = [
  {
    nom: 'Aaron Harfi — NOXEM GROUP',
    de: 'aaron.harfi@noxemgroup.com',
    hote: 'smtp.exemple.fr',
    port: 465,
    utilisateur: 'aaron.harfi@noxemgroup.com',
    // Le mot de passe n'est JAMAIS dans ce fichier : on nomme ici la variable
    // d'environnement qui le contient.
    motDePasseEnv: 'SMTP_MDP_1',
  },
];

/**
 * Volume quotidien conseillé par boîte, selon l'ancienneté de la campagne.
 *
 * Un domaine qui passe de 0 à 150 envois en une journée est signalé pour cela
 * seul, indépendamment du contenu. La montée se fait par paliers
 * hebdomadaires ; au-delà de quatre semaines, on est au plafond de croisière.
 *
 * @param {number} jour — jours écoulés depuis le premier envoi (1 = jour 1)
 */
export function volumeConseille(jour) {
  if (jour < 1) return 0;
  const semaine = Math.ceil(jour / 7);
  const paliers = [10, 20, 30, CAP_PAR_BOITE];
  return paliers[Math.min(semaine, paliers.length) - 1];
}

/**
 * Jour de campagne, à partir de la date de premier envoi (jour 1 = le jour
 * du démarrage). Sert à savoir sur quel palier on se trouve.
 */
export function jourDeCampagne(debut, aujourdhui = new Date()) {
  const d0 = new Date(`${debut}T00:00:00Z`);
  const d1 = new Date(`${aujourdhui.toISOString().slice(0, 10)}T00:00:00Z`);
  if (Number.isNaN(d0.getTime())) throw new Error(`Date de début illisible : « ${debut} ».`);
  return Math.floor((d1 - d0) / 86400000) + 1;
}

/**
 * Plafond du jour, imposé par le palier de montée en charge.
 *
 * C'est le cœur du « commencer doucement » : le volume autorisé ne dépend pas
 * de l'envie du jour mais de l'ancienneté de la campagne. Redemander 150 le
 * troisième jour ne les débloque pas.
 */
export function plafondDuJour(campagne, nbBoites, aujourdhui = new Date()) {
  const jour = jourDeCampagne(campagne.debut, aujourdhui);
  const parBoite = Math.min(volumeConseille(jour), campagne.capMax ?? CAP_PAR_BOITE);
  return { jour, parBoite, total: parBoite * nbBoites };
}

/** Journal des envois : la mémoire de ce qui est déjà parti. */
export function chargerJournal(fichier) {
  if (!existsSync(fichier)) return { version: 1, envois: [] };
  const data = JSON.parse(readFileSync(fichier, 'utf8'));
  return { version: 1, envois: data.envois || [] };
}

/** Une adresse déjà contactée avec succès ne repart jamais. */
export function dejaTraite(journal, email) {
  const cle = String(email || '').toLowerCase();
  return journal.envois.some((e) => e.email.toLowerCase() === cle && e.statut === 'ok');
}

/** Liste de suppression : une adresse par ligne, les vides et # ignorés. */
export function chargerSuppression(fichier) {
  if (!existsSync(fichier)) return new Set();
  return new Set(readFileSync(fichier, 'utf8')
    .split(/\r?\n/)
    .map((l) => l.trim().toLowerCase())
    .filter((l) => l && !l.startsWith('#')));
}

/** Retire les sites déjà contactés et ceux qui ont demandé à ne plus l'être. */
export function filtrerEnvoyables(sites, { journal, suppression }) {
  return sites.filter((s) => {
    const email = String(s.contactEmail || '').toLowerCase();
    if (!email.includes('@')) return false;
    if (suppression.has(email)) return false;
    if (dejaTraite(journal, email)) return false;
    return true;
  });
}

/** Capacité totale d'un jeu de boîtes pour la journée. */
export function capacite(boites, capParBoite = CAP_PAR_BOITE) {
  return boites.length * capParBoite;
}

/**
 * Répartit les sites entre les boîtes, en tourniquet et sans dépasser le
 * plafond de chacune. Ce qui dépasse la capacité du jour n'est pas envoyé :
 * c'est le point du plafond.
 */
export function repartir(sites, boites, capParBoite = CAP_PAR_BOITE) {
  if (!boites.length) return [];
  const lots = boites.map((boite) => ({ boite, sites: [] }));
  let place = 0;
  for (const site of sites) {
    let pose = false;
    // Tourniquet : on cherche la prochaine boîte qui n'est pas pleine.
    for (let essai = 0; essai < lots.length && !pose; essai += 1) {
      const lot = lots[(place + essai) % lots.length];
      if (lot.sites.length < capParBoite) {
        lot.sites.push(site);
        place = (place + essai + 1) % lots.length;
        pose = true;
      }
    }
    if (!pose) break; // toutes les boîtes sont pleines
  }
  return lots;
}

/**
 * Délai avant le message suivant, en millisecondes, avec une variation
 * aléatoire : une cadence parfaitement régulière est une signature d'automate.
 */
export function pause(intervalleSecondes, jitterPct = 40, alea = Math.random) {
  const base = Math.max(0, intervalleSecondes) * 1000;
  const variation = base * (jitterPct / 100);
  return Math.round(base - variation / 2 + alea() * variation);
}

/** Construit le message pour un site donné. */
export function messagePour(site, nomModele, boite) {
  const valeurs = valeursPour(site);
  const gabarit = modele(nomModele);
  return {
    from: `${boite.nom} <${boite.de}>`,
    to: site.contactEmail,
    subject: gabarit.objet,
    text: versionTexte(valeurs, nomModele),
    html: construire(valeurs, nomModele),
  };
}

/** Pièces jointes liées (images en cid:), communes à tous les messages. */
export function piecesJointes() {
  return ['email-borne.png', 'email-scene.png'].map((nom) => ({
    filename: nom,
    path: new URL(`../emails/${nom}`, import.meta.url).pathname,
    cid: nom,
  }));
}

/**
 * Ouvre une connexion SMTP pour une boîte.
 * nodemailer est chargé ici et pas en tête de fichier : la simulation doit
 * fonctionner sans aucune dépendance installée.
 */
export async function transport(boite) {
  let nodemailer;
  try {
    nodemailer = (await import('nodemailer')).default;
  } catch (e) {
    throw new Error('nodemailer n\'est pas installé. Lancez : npm i nodemailer');
  }
  const motDePasse = process.env[boite.motDePasseEnv];
  if (!motDePasse) {
    throw new Error(`Le mot de passe de ${boite.de} est attendu dans la variable `
      + `d'environnement ${boite.motDePasseEnv}, qui est vide.`);
  }
  return nodemailer.createTransport({
    host: boite.hote,
    port: boite.port,
    secure: boite.port === 465,
    auth: { user: boite.utilisateur, pass: motDePasse },
  });
}

/** Résumé lisible du plan de la journée. */
export function resumePlan(lots, { demande, disponibles, capParBoite, intervalle, palier }) {
  const prevus = lots.reduce((n, l) => n + l.sites.length, 0);
  const lignes = [];
  if (palier) {
    lignes.push(`Jour ${palier.jour} de la campagne — palier : ${palier.parBoite} par boîte.`);
    if (demande > palier.total) {
      lignes.push(`Vous avez demandé ${demande} : le palier prime, ce sera ${palier.total}.`);
    }
    lignes.push('');
  }
  lignes.push(
    `${disponibles} site(s) contactable(s) après journal et liste de suppression.`,
    `${lots.length} boîte(s) d'envoi × ${capParBoite} = ${capacite(lots.map((l) => l.boite), capParBoite)} de capacité aujourd'hui.`,
    `${prevus} message(s) au programme (${demande} demandé(s)).`,
  );
  if (demande > capacite(lots.map((l) => l.boite), capParBoite)) {
    const manque = Math.ceil((demande - capacite(lots.map((l) => l.boite), capParBoite)) / capParBoite);
    lignes.push('');
    lignes.push(`Pour tenir ${demande} par jour, il manque ${manque} boîte(s) d'envoi.`);
    lignes.push(`Le volume se gagne en ajoutant des boîtes, jamais en poussant une seule au-delà de ${capParBoite}.`);
  }
  const duree = Math.round((prevus * intervalle) / 60);
  lignes.push('');
  lignes.push(`Durée estimée de la série : environ ${duree} minute(s), étalée — c'est voulu.`);
  for (const lot of lots.filter((l) => l.sites.length)) {
    lignes.push(`  ${lot.boite.de} → ${lot.sites.length} message(s)`);
  }
  return lignes.join('\n');
}

async function principal() {
  const args = process.argv.slice(2);
  const lire = (cle, defaut) => {
    const i = args.indexOf(`--${cle}`);
    return i !== -1 && args[i + 1] ? args[i + 1] : defaut;
  };
  const drapeau = (cle) => args.includes(`--${cle}`);

  const fichierSites = lire('sites', '');
  if (!fichierSites) {
    console.error('Indiquez le fichier de sites : --sites mairies-69.json');
    process.exit(1);
  }

  const nomModele = lire('modele', 'gonflage');
  const quota = Number(lire('quota', 50));
  const statut = lire('statut', 'a_contacter');
  const intervalle = Number(lire('intervalle', 90));
  const capParBoite = Number(lire('cap', CAP_PAR_BOITE));
  const dossier = lire('dossier', 'envois');
  const envoiReel = drapeau('envoyer');

  try {
    modele(nomModele);
  } catch (e) {
    console.error(e.message);
    process.exit(1);
  }

  if (!existsSync(dossier)) mkdirSync(dossier, { recursive: true });

  const fichierBoites = `${dossier}/boites.json`;
  if (!existsSync(fichierBoites)) {
    writeFileSync(fichierBoites, JSON.stringify(MODELE_BOITES, null, 2));
    console.error(`Aucune boîte d'envoi déclarée. Un exemple vient d'être écrit dans ${fichierBoites}.`);
    console.error('Renseignez-le (hôte SMTP, port, identifiant), placez les mots de passe dans les');
    console.error('variables d\'environnement nommées, puis relancez.');
    console.error('\nCe fichier ne doit jamais être versionné : il est déjà dans .gitignore.');
    process.exit(1);
  }

  const boites = JSON.parse(readFileSync(fichierBoites, 'utf8'));

  // Mémoire du démarrage : c'est elle qui impose le palier, pas la ligne de commande.
  const fichierCampagne = `${dossier}/campagne.json`;
  if (!existsSync(fichierCampagne)) {
    writeFileSync(fichierCampagne, JSON.stringify(
      { debut: new Date().toISOString().slice(0, 10), capMax: CAP_PAR_BOITE }, null, 2,
    ));
    console.log(`Premier jour de campagne : ${fichierCampagne} vient d'être créé.\n`);
  }
  const campagne = JSON.parse(readFileSync(fichierCampagne, 'utf8'));
  const palier = plafondDuJour(campagne, boites.length);

  const fichierJournal = `${dossier}/journal.json`;
  const journal = chargerJournal(fichierJournal);
  const suppression = chargerSuppression(`${dossier}/suppression.txt`);

  const data = JSON.parse(readFileSync(fichierSites, 'utf8'));
  const tous = Array.isArray(data) ? data : data.sites || [];
  const candidats = filtrerEnvoyables(selectionner(tous, { statut, quota: Infinity }), { journal, suppression });
  // Le plus contraignant des deux gagne : ce qui est demandé, ou le palier du jour.
  const retenus = candidats.slice(0, Math.min(quota, palier.total));
  const lots = repartir(retenus, boites, Math.min(capParBoite, palier.parBoite));

  console.log(resumePlan(lots, {
    demande: quota, disponibles: candidats.length, capParBoite, intervalle, palier,
  }));

  if (!envoiReel) {
    console.log('\n--- SIMULATION : rien n\'a été envoyé. Ajoutez --envoyer pour lancer. ---');
    return;
  }

  const pieces = piecesJointes();
  let envoyes = 0;
  let echecs = 0;

  for (const lot of lots.filter((l) => l.sites.length)) {
    let connexion;
    try {
      connexion = await transport(lot.boite);
    } catch (e) {
      console.error(`\n${lot.boite.de} : ${e.message}`);
      echecs += lot.sites.length;
      continue;
    }

    for (const site of lot.sites) {
      const message = { ...messagePour(site, nomModele, lot.boite), attachments: pieces };
      try {
        await connexion.sendMail(message);
        journal.envois.push({
          email: site.contactEmail, nom: site.nom, boite: lot.boite.de,
          date: new Date().toISOString(), statut: 'ok',
        });
        envoyes += 1;
        console.log(`  ✓ ${site.contactEmail} (${site.nom || ''})`);
      } catch (e) {
        journal.envois.push({
          email: site.contactEmail, nom: site.nom, boite: lot.boite.de,
          date: new Date().toISOString(), statut: 'echec', erreur: e.message,
        });
        echecs += 1;
        console.error(`  ✗ ${site.contactEmail} — ${e.message}`);
      }
      // Le journal est réécrit à chaque message : une interruption ne fait
      // jamais perdre la trace de ce qui est déjà parti.
      writeFileSync(fichierJournal, JSON.stringify(journal, null, 2));
      await new Promise((r) => { setTimeout(r, pause(intervalle)); });
    }
    if (connexion.close) connexion.close();
  }

  console.log(`\n${envoyes} envoyé(s), ${echecs} en échec. Journal : ${fichierJournal}`);
  console.log('Relevez les erreurs définitives et ajoutez-les à suppression.txt.');
}

if (import.meta.url === `file://${process.argv[1]}`) {
  principal().catch((e) => { console.error(e.message); process.exit(1); });
}
