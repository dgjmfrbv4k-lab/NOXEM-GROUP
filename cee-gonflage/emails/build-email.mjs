/**
 * build-email.mjs — remplit un gabarit HTML avec les variables d'une fiche site.
 *
 *   node emails/build-email.mjs --nom "Carrefour Bron" --prenom Sophie > sortie.html
 *   node emails/build-email.mjs --modele mairie --commune "Dardilly" > sortie.html
 *
 * Deux modèles sont disponibles (voir MODELES plus bas) :
 *   - « gonflage » : commerces, parkings privés ouverts au public, aires ;
 *   - « mairie »   : collectivités, message destiné à être transmis en interne.
 *
 * Sans argument, produit la version de démonstration servant aux tests
 * d'affichage dans les différents clients de messagerie.
 */
import { readFileSync } from 'node:fs';

const args = process.argv.slice(2);
const lire = (cle, defaut) => {
  const i = args.indexOf(`--${cle}`);
  return i !== -1 && args[i + 1] ? args[i + 1] : defaut;
};

/** Signature Noxem Group (valeurs réelles, surchargeables en ligne de commande). */
export const SIGNATURE = {
  '[Votre nom]': lire('signataire', 'Aaron Harfi'),
  '[Votre fonction]': lire('fonction', 'Président'),
  '[Votre société]': lire('societe', 'NOXEM GROUP'),
  '[Votre téléphone]': lire('telephone', '02 59 50 84 59'),
  '[Votre email]': lire('email', 'aaron.harfi@noxemgroup.com'),
  '[Votre adresse]': lire('adresse', '5 chemin du Jubin – 69570 Dardilly'),
};

/**
 * Valeurs par défaut : version GÉNÉRIQUE, envoyable telle quelle à n'importe
 * quel établissement. Les options --prenom et --nom produisent la version
 * personnalisée, qui obtient de bien meilleurs taux de réponse quand le nom
 * du contact et celui du site sont connus (fiche CRM renseignée).
 */
export const VALEURS_GENERIQUES = {
  '[Prénom]': 'Madame, Monsieur',
  '[nom du site]': 'votre établissement',
  '[commune]': 'votre commune',
  ...SIGNATURE,
};

/**
 * Lien du bouton « Réserver 15 minutes ».
 * Tant qu'aucun agenda en ligne n'est branché (Calendly, plages de rendez-vous
 * Google Agenda...), on retombe sur un message pré-rempli : le prospect envoie
 * ses disponibilités en un clic. Passer --rdv <url> pour brancher l'agenda.
 */
export function lienReservation(valeurs = SIGNATURE) {
  const url = lire('rdv', '');
  if (url) return url;
  const objet = encodeURIComponent('Réservation d’un créneau de 15 minutes');
  const corps = encodeURIComponent(
    'Bonjour,\n\nJe souhaite réserver un créneau de 15 minutes au sujet de la station de gonflage.\n\n'
    + 'Mes disponibilités :\n- \n- \n\nÉtablissement :\nVille :\nTéléphone :\n',
  );
  return `mailto:${valeurs['[Votre email]']}?subject=${objet}&body=${corps}`;
}

export const VALEURS_DEMO = {
  '[Prénom]': lire('prenom', VALEURS_GENERIQUES['[Prénom]']),
  '[nom du site]': lire('nom', VALEURS_GENERIQUES['[nom du site]']),
  '[commune]': lire('commune', VALEURS_GENERIQUES['[commune]']),
  ...SIGNATURE,
};

/**
 * Élision devant voyelle ou h muet : « de Dardilly » mais « d'Écully ».
 *
 * Sans cela le message écrit « un parking de Écully », et c'est exactement
 * le détail qui signale un envoi automatique à la lecture.
 */
export function deCommune(nom) {
  const texte = String(nom || '').trim();
  if (!texte) return 'de votre commune';
  // On compare sans accent : « Écully » commence bien par une voyelle.
  const premiere = texte.normalize('NFD').replace(/[\u0300-\u036f]/g, '')[0].toLowerCase();
  return /[aeiouy]/.test(premiere) ? `d’${texte}` : `de ${texte}`;
}

/** Version texte du modèle « gonflage » (commerces, parkings, aires). */
function texteGonflage(valeurs) {
  return `Bonjour ${valeurs['[Prénom]']},

1 véhicule sur 3 roule aujourd'hui avec des pneus mal gonflés. Vos clients peuvent y remédier sur votre parking, gratuitement - et l'État en finance l'essentiel.

Je me permets de vous contacter au sujet du parking de ${valeurs['[nom du site]']}.

Le dispositif des Certificats d'Économies d'Énergie, encadré par l'État, permet de financer en grande partie l'installation d'une station de gonflage en libre accès sur votre parking, ainsi que son entretien (fiche officielle TRA-SE-104).

- Un service visible et gratuit pour vos clients, sur votre parking
- Entretien assuré par un professionnel, pièces défectueuses remplacées sous 15 jours
- Aucune gestion de votre côté, aucun changement dans votre activité
- Aucun critère de surface, de chiffre d'affaires ni d'ancienneté

Une seule condition : que le gonflage reste gratuit pour les usagers. C'est la règle du dispositif, et c'est tout.

15 minutes suffisent pour que je vous présente le fonctionnement et le montant pris en charge pour ${valeurs['[nom du site]']}. Seriez-vous disponible cette semaine ou la suivante ?

Cordialement,

${valeurs['[Votre nom]']}
${valeurs['[Votre fonction]']} – ${valeurs['[Votre société]']}

Tél. : ${valeurs['[Votre téléphone]']}
E-mail : ${valeurs['[Votre email]']}
Adresse : ${valeurs['[Votre adresse]']}

--
Sources : ADEME (véhicules mal gonflés), Michelin (surconsommation liée au sous-gonflage).
Montants indicatifs, confirmés avec le délégataire CEE avant signature.
Pour ne plus être contacté, répondez « STOP » à ce message.`;
}

/**
 * Version texte du modèle « mairie ».
 * Le message arrive sur un accueil : la demande de transmission est la
 * première ligne du corps, avant même l'argumentaire.
 */
function texteMairie(valeurs) {
  return `Bonjour ${valeurs['[Prénom]']},

Merci de transmettre ce message au service concerné : direction générale des services, services techniques ou service voirie / stationnement selon votre organisation.

Une station de gonflage en libre accès sur un parking ${deCommune(valeurs['[commune]'])}, gratuite pour les usagers, sans dépense pour la commune.

Le dispositif des Certificats d'Économies d'Énergie, encadré par l'État, finance en grande partie l'installation d'une station de gonflage en libre accès ainsi que son entretien (fiche officielle TRA-SE-104). Un véhicule sur trois roule avec des pneus sous-gonflés : c'est de la surconsommation de carburant, de l'usure prématurée et un risque routier.

Concrètement pour ${valeurs['[commune]']} :

- Aucune dépense communale : ni investissement, ni budget d'entretien
- Un service gratuit et permanent pour vos administrés, en libre accès
- Entretien assuré par un professionnel, pièces remplacées sous 15 jours
- Deux emplacements possibles dans le même dossier : un parking ouvert au public, et le parking des agents
- Aucun critère de taille de commune, de fréquentation ni d'ancienneté

Côté formalisme, l'implantation se règle par une convention d'occupation du domaine public à durée déterminée, et la commune reste propriétaire de son emplacement. Nous fournissons le dossier technique, l'implantation proposée et les pièces attendues par le délégataire CEE.

Une seule condition : que le gonflage reste gratuit pour les usagers. C'est la règle du dispositif, et c'est tout.

15 minutes suffisent pour présenter le dispositif, le cadre juridique et le montant pris en charge pour vos parkings. Je suis disponible tous les jours, en visioconférence ou sur place.

Je vous prie d'agréer, Madame, Monsieur, l'expression de mes salutations distinguées.

${valeurs['[Votre nom]']}
${valeurs['[Votre fonction]']} – ${valeurs['[Votre société]']}

Tél. : ${valeurs['[Votre téléphone]']}
E-mail : ${valeurs['[Votre email]']}
Adresse : ${valeurs['[Votre adresse]']}

--
Sources : ADEME (véhicules mal gonflés), Michelin (surconsommation liée au sous-gonflage).
Montants indicatifs, confirmés avec le délégataire CEE avant signature.
Message adressé à une adresse institutionnelle publiée par l'Annuaire de l'administration.
Pour ne plus être contacté, répondez « STOP » à ce message.`;
}

/**
 * Version texte de la relance.
 * Même parti pris que le gabarit HTML : court, une seule information nouvelle,
 * et une porte de sortie explicite.
 */
function texteRelance(valeurs) {
  return `Bonjour ${valeurs['[Prénom]']},

Je me permets de revenir vers vous au sujet de mon message concernant l'installation d'une station de gonflage en libre accès sur un parking ${deCommune(valeurs['[commune]'])}.

Ce type de dossier passe rarement en tête des priorités, et c'est normal. Une précision qui lève souvent la question principale : le dispositif ne demande aucune dépense communale, et l'instruction du dossier CEE se fait de notre côté. Il n'y a pas de budget à trouver, pas de ligne à voter.

Si le sujet n'est pas d'actualité, répondez-moi simplement en un mot : je ne vous solliciterai plus.

S'il vous intéresse, 15 minutes au téléphone suffisent pour que je vous présente le fonctionnement et le montant pris en charge - au ${valeurs['[Votre téléphone]']}, ou en réponse à ce message.

Bien cordialement,

${valeurs['[Votre nom]']}
${valeurs['[Votre fonction]']} - ${valeurs['[Votre société]']}
Tél. : ${valeurs['[Votre téléphone]']}
E-mail : ${valeurs['[Votre email]']}

--
Fiche CEE TRA-SE-104. Montants indicatifs, confirmés avec le délégataire CEE avant signature.
Pour ne plus être contacté, répondez « STOP » à ce message.`;
}

/**
 * Les modèles disponibles. Chacun associe un gabarit HTML, l'objet du message
 * et la version texte brut envoyée en alternative.
 */
export const MODELES = {
  gonflage: {
    libelle: 'Commerces, parkings et aires',
    fichier: 'email-gonflage.html',
    objet: 'Le gonflage gratuit pour vos clients, financé par l’État',
    texte: texteGonflage,
  },
  mairie: {
    libelle: 'Collectivités (mairies)',
    fichier: 'email-mairie.html',
    objet: 'Station de gonflage en libre accès pour votre commune, financée par les CEE',
    texte: texteMairie,
  },
  relance: {
    libelle: 'Relance (tous destinataires)',
    fichier: 'email-relance.html',
    // L'objet réel est « Re: » + celui du premier message, repris du journal :
    // la relance doit s'afficher dans le fil de l'original, pas à côté.
    objet: 'Re: votre parking',
    texte: texteRelance,
    // Aucune image : une relance ne doit pas ressembler à une seconde publicité.
    sansImages: true,
    relance: true,
  },
};

/** Retourne un modèle, ou échoue avec la liste des noms acceptés. */
export function modele(nom = 'gonflage') {
  const choisi = MODELES[nom];
  if (!choisi) {
    throw new Error(`Modèle inconnu : « ${nom} ». Modèles disponibles : ${Object.keys(MODELES).join(', ')}.`);
  }
  return choisi;
}

/** Remplit le gabarit HTML du modèle demandé. */
export function construire(valeurs = VALEURS_DEMO, nomModele = 'gonflage') {
  let html = readFileSync(new URL(`./${modele(nomModele).fichier}`, import.meta.url), 'utf8');
  // Variable dérivée : « de Dardilly » / « d'Écully ».
  html = html.split('[de commune]').join(deCommune(valeurs['[commune]']));
  // Le lien « tel: » ne doit pas contenir d'espaces.
  html = html.split('[Votre téléphone sans espaces]')
    .join((valeurs['[Votre téléphone]'] || '').replace(/[^0-9+]/g, ''));
  html = html.split('[lien de réservation]').join(lienReservation(valeurs));
  for (const [variable, valeur] of Object.entries(valeurs)) {
    html = html.split(variable).join(valeur);
  }
  return html;
}

/** Version texte brut, envoyée en alternative au HTML (clients sans images ni styles). */
export function versionTexte(valeurs = VALEURS_DEMO, nomModele = 'gonflage') {
  return modele(nomModele).texte(valeurs);
}

if (import.meta.url === `file://${process.argv[1]}`) {
  process.stdout.write(construire(VALEURS_DEMO, lire('modele', 'gonflage')));
}
