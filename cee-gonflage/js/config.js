/**
 * config.js
 * ---------------------------------------------------------------------------
 * Constantes de la fiche CEE et valeurs par defaut de l'application.
 *
 * REGLE IMPORTANTE :
 *  - Les VOLUMES (kWh cumac) sont fixes par l'Etat dans la fiche d'operation
 *    standardisee TRA-SE-104 : ils sont donc des constantes.
 *  - Le PRIX du CEE (EUR/MWh cumac) n'est PAS fixe par l'Etat : il depend du
 *    marche (registre national EMMY). Il ne doit JAMAIS etre traite comme une
 *    constante metier : il n'apparait ici que comme VALEUR PAR DEFAUT,
 *    modifiable dans l'interface et persistee dans le navigateur.
 * ---------------------------------------------------------------------------
 */

/** Identification de la fiche officielle utilisee par l'application. */
export const FICHE = {
  code: 'TRA-SE-104',
  libelle: 'Station de gonflage des pneumatiques',
  version: 'A14',
  secteur: 'Transport — véhicules de catégorie M1 (voitures) et N1 (utilitaires légers)',
  periode: '6e période CEE (2026-2030)',
  dureeVieConventionnelleAns: 1,
};

/**
 * Types de stations et volumes officiels, en kWh cumac par station et par an.
 * Source : fiche TRA-SE-104 (version A14).
 */
export const TYPES_STATION = {
  A: {
    code: 'A',
    kwhCumac: 534200,
    titre: 'Type A — autoroutier',
    implantation: 'Autoroutes et voies de type autoroutier disposant d’aires de repos',
    exemples: 'Aires de repos et de service autoroutières, voies express avec aires.',
  },
  B: {
    code: 'B',
    kwhCumac: 148400,
    titre: 'Type B — public / zones d’activité',
    implantation:
      'Zones urbaines, zones industrielles, zones d’activité, parkings ouverts au grand public, '
      + 'hors agglomération — HORS parkings privés d’entreprises ou de collectivités',
    exemples: 'Supermarchés, centres commerciaux, stations-service indépendantes, parkings municipaux.',
  },
  C: {
    code: 'C',
    kwhCumac: 39600,
    titre: 'Type C — parking privé',
    implantation: 'Parkings privés d’entreprises ou de collectivités (salariés / flotte professionnelle)',
    exemples: 'Parking réservé aux salariés, dépôt de flotte, parking technique d’une collectivité.',
  },
};

/** Ordre d'affichage stable des types. */
export const ORDRE_TYPES = ['A', 'B', 'C'];

/**
 * Conditions d'eligibilite listees par la fiche TRA-SE-104.
 * `bloquant: true` = sans cette condition, l'operation n'est pas valorisable.
 */
export const CONDITIONS_ELIGIBILITE = [
  {
    id: 'gratuit',
    label: 'Le gonflage est gratuit pour les usagers',
    aide: 'Toute tarification, même symbolique, rend l’opération inéligible.',
    bloquant: true,
  },
  {
    id: 'acces',
    label: 'Accès facile pour les usagers (véhicules M1 et N1)',
    aide: 'La station doit être accessible et utilisable simplement par les voitures et utilitaires légers.',
    bloquant: true,
  },
  {
    id: 'panneau',
    label: 'Panneau TNPF visible',
    aide: '« Des pneus bien gonflés : les 10 conseils pour rouler en toute sécurité ».',
    bloquant: true,
  },
  {
    id: 'securite',
    label: 'Gonflage réalisable en toute sécurité',
    aide: 'Implantation, éclairage et dégagement permettant une utilisation sûre.',
    bloquant: true,
  },
  {
    id: 'entretien',
    label: 'Entretien conforme au cahier des charges TNPF',
    aide: 'Contrat d’entretien signé avec un professionnel, conforme au cahier des charges.',
    bloquant: true,
  },
  {
    id: 'delai15j',
    label: 'Contrat garantissant le remplacement des pièces défectueuses sous 15 jours maximum',
    aide: 'Clause à vérifier explicitement dans le contrat d’entretien.',
    bloquant: true,
  },
  {
    id: 'controleQuotidien',
    label: 'Procédure de contrôle quotidien formalisée',
    aide: 'Pièce justificative exigée en cas de contrôle du PNCEE.',
    bloquant: false,
  },
  {
    id: 'etatRecap',
    label: 'État récapitulatif des stations signé par le bénéficiaire',
    aide: 'Doit mentionner le type (A/B/C), le nom et l’adresse de chaque station.',
    bloquant: false,
  },
];

/**
 * Valeurs par defaut du simulateur.
 * Toutes sont modifiables dans l'interface et sauvegardees localement.
 *
 * prixBrutEurMWhc : fourchette observee mi-2026 ~8,5 a 9 EUR/MWhc brut.
 * margeDelegatairePct : ~20 % correspond a un net de ~7 EUR/MWhc.
 * Les couts (entretien, installation) ne sont PAS encore chiffres dans le
 * projet : ils valent 0 par defaut et l'interface signale que la marge
 * affichee est alors un plafond theorique.
 */
export const DEFAUTS_SIMULATEUR = {
  nbA: 0,
  nbB: 10,
  nbC: 5,
  prixBrutEurMWhc: 8.7,
  margeDelegatairePct: 20,
  partCeeConserveePct: 100,
  coutEntretienAnnuelParStation: 0,
  coutInstallationParStation: 0,
  prixFactureClientParStation: 0,
  fraisFixesAnnuels: 0,
  variationAnnuellePrixPct: 0,
};

/** Statuts de prospection du mini-CRM (ordre = avancement commercial). */
export const STATUTS = [
  { id: 'a_contacter', label: 'À contacter' },
  { id: 'contacte', label: 'Contacté' },
  { id: 'rdv', label: 'RDV' },
  { id: 'devis', label: 'Devis' },
  { id: 'signe', label: 'Signé' },
  { id: 'refuse', label: 'Refusé' },
];

/** Typologies de sites proposees dans le CRM (aide a la qualification). */
export const TYPES_SITE = [
  'Supermarché / hypermarché',
  'Centre commercial',
  'Station-service indépendante',
  'Parking municipal',
  'Zone d’activité / zone industrielle',
  'Collectivité',
  'Entreprise (parking salariés / flotte)',
  'Aire autoroutière',
  'Autre',
];

/** Seuils d'alerte (en jours) avant la date anniversaire du contrat. */
export const ALERTES_ANNIVERSAIRE = { vigilance: 90, urgent: 30 };

/** Avertissement affiche dans l'interface (montants indicatifs). */
export const AVERTISSEMENT =
  'Montants indicatifs. Les volumes en kWh cumac proviennent de la fiche '
  + 'TRA-SE-104 ; le prix du CEE dépend du marché (EMMY) et varie chaque mois. '
  + 'Tout chiffrage doit être validé avec un délégataire CEE et la version de la '
  + 'fiche en vigueur à la date de signature du contrat.';

/* ---------------------------------------------------------------------------
   Identité Noxem Group : valeurs par défaut de la signature des e-mails.
   Modifiables dans l'onglet E-mails, puis conservées dans le navigateur.
   --------------------------------------------------------------------------- */
export const SIGNATURE_DEFAUT = {
  signatureNom: 'Aaron Harfi',
  signatureSociete: 'Noxem Group',
  signatureTelephone: '',
  signatureEmail: 'harfiaaron@icloud.com',
};

/* ---------------------------------------------------------------------------
   SECONDE OFFRE : bornes de recharge pour véhicules électriques (IRVE).

   ATTENTION — ce n'est PAS le même mécanisme que le gonflage :
   - le gonflage relève d'une FICHE d'opération standardisée (TRA-SE-104), avec
     un volume de kWh cumac fixé par l'État et revendu au prix du marché ;
   - la recharge relève du PROGRAMME ADVENIR, piloté par l'Avere-France et
     financé par les CEE. C'est une prime à l'investissement : un pourcentage du
     coût HT, plafonné par point de charge, avec dossier à déposer AVANT travaux
     et enveloppe budgétaire limitée.

   Conséquences commerciales, à ne jamais contourner dans les e-mails :
   - la prise en charge est PARTIELLE : on n'écrit jamais « borne gratuite » ;
   - les parkings privés d'entreprise (flotte et salariés) ne sont plus
     éligibles depuis le 1er janvier 2023 : la cible est le parking ouvert au
     public (commerce, centre commercial, hôtel, restaurant) ;
   - la recharge peut rester payante pour l'usager : c'est même une recette pour
     le site, à la différence du gonflage qui doit être gratuit ;
   - les barèmes changent : ils sont ici des valeurs par défaut modifiables, à
     revalider sur advenir.mobi / avere-france.org avant chaque proposition.
   --------------------------------------------------------------------------- */
export const PROGRAMME_RECHARGE = {
  nom: 'Programme ADVENIR',
  pilote: 'Avere-France',
  financement: 'Certificats d’Économies d’Énergie (CEE)',
  echeance: 'Programme prolongé jusqu’au 31 décembre 2027 (à revérifier).',
  sources: ['https://advenir.mobi', 'https://www.avere-france.org'],
  regles: [
    'Dossier à déposer et à faire valider AVANT le début des travaux.',
    'Prise en charge partielle : un pourcentage du coût HT, plafonné par point de charge.',
    'Parkings privés d’entreprise (flotte et salariés) exclus depuis le 1er janvier 2023.',
    'Cible éligible : parkings ouverts au public — commerces, centres commerciaux, hôtels, restaurants.',
    'Enveloppe budgétaire limitée : les barèmes et l’éligibilité peuvent évoluer en cours d’année.',
  ],
};

/** Barèmes ADVENIR par défaut — À REVALIDER avant toute proposition chiffrée. */
export const DEFAUTS_RECHARGE = {
  nbPoints: 4,
  coutHtParPoint: 3500,
  tauxPriseEnChargePct: 30,
  plafondParPoint: 2100,
  prixFactureClientParPoint: 0,
};
