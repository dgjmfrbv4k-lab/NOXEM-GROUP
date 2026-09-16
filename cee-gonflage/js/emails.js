/**
 * emails.js
 * ---------------------------------------------------------------------------
 * Modeles d'e-mails de prospection + substitution des variables.
 *
 * REGLES DE REDACTION (a respecter pour toute modification) :
 *  - Ne JAMAIS ecrire « gratuit », « 100 % finance » ou « offert » pour le site :
 *    on ecrit « en grande partie finance par les CEE ».
 *  - Le mot « gratuit » ne s'applique qu'a une chose : le gonflage pour
 *    les usagers, qui est une CONDITION du dispositif.
 *  - Les montants annonces sont indicatifs et dependent du prix du marche CEE.
 *  - Ton professionnel, phrases courtes, une seule demande par e-mail.
 * ---------------------------------------------------------------------------
 */

/**
 * Variables disponibles dans les modeles.
 * Cle = texte a remplacer dans le corps, valeur = description affichee.
 */
export const VARIABLES = {
  '[Prénom]': 'Prénom du contact',
  '[nom du site]': 'Nom du site (ex. : Intermarché Vaulx-en-Velin)',
  '[Société]': 'Raison sociale de l’exploitant',
  '[Ville]': 'Ville du site',
  '[Type CEE]': 'Type de station retenu (A, B ou C)',
  '[Montant estimé]': 'Montant CEE net estimé par an pour le site',
  '[Votre nom]': 'Votre nom (signature)',
  '[Votre société]': 'Votre structure (signature)',
  '[Votre téléphone]': 'Votre téléphone (signature)',
  '[Votre email]': 'Votre e-mail (signature)',
};

export const MODELES = [
  {
    id: 'court',
    nom: '1. Premier contact (court)',
    description: 'E-mail d\u2019accroche, 30 secondes de lecture. Objectif unique : obtenir un \u00E9change de 15 minutes.',
    objet: 'Station de gonflage pour vos clients, financée par les CEE',
    corps: `Bonjour [Prénom],

Je me permets de vous contacter au sujet de votre parking [nom du site].

Le dispositif des Certificats d'Économies d'Énergie (CEE), encadré par l'État, permet de financer une station de gonflage des pneus en libre accès pour vos clients, ainsi que son entretien (fiche officielle TRA-SE-104).

Pour vous, c'est :
- un service gratuit et visible pour vos clients ;
- une station entretenue et réparée sous 15 jours en cas de panne ;
- un coût en grande partie couvert par la prime CEE.

Seule condition : que le gonflage reste gratuit pour les usagers.

Auriez-vous 15 minutes cette semaine pour que je vous présente le fonctionnement et une estimation pour votre site ?

Bien cordialement,

[Votre nom]
[Votre société]
[Votre téléphone]`,
  },
  {
    id: 'detaille',
    nom: '2. Après échange (détaillé)',
    description: 'E-mail de confirmation après un premier échange téléphonique ou un RDV.',
    objet: 'Suite à notre échange – station de gonflage pour [nom du site]',
    corps: `Bonjour [Prénom],

Comme convenu, voici le détail du dispositif pour [nom du site] à [Ville].

1. Le principe
Les Certificats d'Économies d'Énergie (CEE) sont un dispositif réglementé par l'État : les fournisseurs d'énergie et de carburant doivent financer des actions d'économies d'énergie. La mise en place d'un contrat d'entretien de station de gonflage fait partie des opérations standardisées éligibles (fiche TRA-SE-104). Des pneus correctement gonflés réduisent la consommation de carburant : c'est ce gain qui est valorisé.

2. Ce que cela implique pour vous
- Le gonflage doit rester gratuit pour les usagers (véhicules légers et utilitaires).
- La station doit être facilement accessible et utilisable en toute sécurité.
- Un panneau d'information TNPF est apposé près de la borne.
- Un contrat d'entretien est signé, conforme au cahier des charges TNPF, avec remplacement des pièces défectueuses sous 15 jours maximum et un contrôle quotidien de l'équipement.
- Aucun critère de taille, de fréquentation ou de chiffre d'affaires n'est exigé.

3. Le financement
Votre site relève du type [Type CEE] au sens de la fiche, ce qui représente un financement CEE net estimé à environ [Montant estimé] par an et par station. Ce montant est indicatif : le volume (kWh cumac) est fixé par l'État, mais le prix du CEE dépend du marché et varie chaque mois. Il est confirmé par le délégataire CEE avant signature.
Le dispositif couvre une grande partie du coût de l'équipement et de son entretien ; le solde éventuel vous est présenté de façon transparente dans la proposition chiffrée.

4. Durée et renouvellement
Le contrat d'entretien est conclu pour un an. Il est valorisable chaque année tant qu'il est actif et expressément renouvelé (la reconduction tacite n'est pas admise par le dispositif). Nous assurons le suivi des échéances et des pièces justificatives.

5. Les prochaines étapes
- Vous me confirmez l'emplacement envisagé et le nombre de bornes.
- Je vous transmets la proposition chiffrée et le projet de contrat d'entretien.
- Après signature, l'installation et la mise en service sont planifiées.

Je reste à votre disposition pour toute question.

Bien cordialement,

[Votre nom]
[Votre société]
[Votre téléphone] — [Votre email]`,
  },
  {
    id: 'relance',
    nom: '3. Relance (sans réponse)',
    description: 'Relance courte, à envoyer 8 à 15 jours après le premier contact.',
    objet: 'Relance : station de gonflage pour [nom du site]',
    corps: `Bonjour [Prénom],

Je me permets de revenir vers vous au sujet de la station de gonflage pour [nom du site].

Pour résumer en trois lignes : équipement en accès libre sur votre parking, gonflage gratuit pour vos visiteurs, entretien assuré par un professionnel, et financement en grande partie couvert par le dispositif CEE de l'État.

Si le sujet n'est pas d'actualité, dites-le moi simplement, je n'insisterai pas. Sinon, je peux vous appeler cette semaine au moment qui vous convient.

Bien cordialement,

[Votre nom]
[Votre société]
[Votre téléphone] — [Votre email]`,
  },
];

/** Recupere un modele par son identifiant. */
export function modele(id) {
  return MODELES.find((m) => m.id === id) || MODELES[0];
}

/**
 * Remplace les variables d'un texte.
 * Les variables non renseignees sont laissees telles quelles (visibles),
 * afin de ne jamais envoyer un e-mail avec un trou silencieux.
 */
export function remplir(texte, valeurs = {}) {
  let resultat = texte;
  for (const [variable, valeur] of Object.entries(valeurs)) {
    if (valeur === undefined || valeur === null || valeur === '') continue;
    resultat = resultat.split(variable).join(String(valeur));
  }
  return resultat;
}

/** Liste des variables encore non remplies dans un texte. */
export function variablesManquantes(texte) {
  return Object.keys(VARIABLES).filter((v) => texte.includes(v));
}

/** Construit un lien mailto: pret a ouvrir dans le client de messagerie. */
export function lienMailto(destinataire, objet, corps) {
  const params = new URLSearchParams({ subject: objet, body: corps });
  // URLSearchParams encode les espaces en « + » : mailto attend « %20 ».
  return `mailto:${destinataire || ''}?${params.toString().replace(/\+/g, '%20')}`;
}
