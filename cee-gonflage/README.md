# Stations de gonflage financées par les CEE — outil interne

Application web interne pour l'activité « stations de gonflage des pneumatiques »
financées par les Certificats d'Économies d'Énergie, fiche d'opération standardisée
**TRA-SE-104** (version A14), 6e période CEE (2026-2030).

> **Montants indicatifs.** Les volumes en kWh cumac sont fixés par l'État dans la fiche.
> Le prix du CEE, lui, **n'est pas réglementé** : il dépend du marché (registre national
> EMMY) et varie chaque mois. Aucun prix n'est figé dans le code : les valeurs livrées ne
> sont que des valeurs par défaut modifiables. Tout chiffrage doit être validé avec un
> délégataire CEE et avec la version de la fiche en vigueur à la date de signature.

## Lancer le projet

L'application utilise les modules ES natifs : elle doit être servie par un serveur HTTP
(l'ouvrir par double-clic en `file://` est bloqué par le navigateur).

```bash
cd cee-gonflage
python3 -m http.server 8000
# puis ouvrir http://localhost:8000
```

Alternative avec Node :

```bash
npx serve cee-gonflage
```

Aucune dépendance, aucune étape de build, aucun backend.

## Lancer les tests

```bash
cd cee-gonflage
node --test
```

22 tests couvrent les calculs (dont le cas de référence 10 stations B + 5 stations C),
la classification A/B/C et les échéances de dossier.

## Déploiement

Le dossier `cee-gonflage/` est un site statique : il se publie tel quel sur GitHub Pages,
Netlify, Vercel ou n'importe quel hébergement classique. Les données restant dans le
navigateur, il n'y a rien à configurer côté serveur.

## Les cinq modules

| Onglet | Rôle |
|---|---|
| **Simulateur** | Rentabilité : kWh cumac, montant brut/net, marge par station, point mort, projection 3 ans. |
| **Classification** | 3 questions → type A, B ou C + montant estimé, puis checklist d'éligibilité. |
| **Prospection** | Mini-CRM : sites, statuts, relances, filtres, export CSV, sauvegarde JSON. |
| **E-mails** | 3 modèles (premier contact, détaillé, relance) avec variables remplies depuis le CRM. |
| **Dossiers CEE** | Pour chaque site signé : pièces justificatives + alerte avant la date anniversaire. |

## Rappels métier codés dans l'application

**Volumes officiels (kWh cumac par station et par an)**

| Type | Implantation | kWh cumac |
|---|---|---|
| A | Autoroutes et voies de type autoroutier avec aires de repos | 534 200 |
| B | Zones urbaines, ZI, zones d'activité, parkings grand public — hors parkings privés d'entreprises/collectivités | 148 400 |
| C | Parkings privés d'entreprises ou de collectivités (salariés / flotte) | 39 600 |

`Total kWh cumac = 534 200 × NA + 148 400 × NB + 39 600 × NC`
`Montant € = (Total kWh cumac / 1000) × prix €/MWh cumac`
`Prix net = prix brut × (1 − marge délégataire %)`

**Règle B vs C** : un site privé mais ouvert au grand public (supermarché, centre
commercial) relève du **type B** ; un parking réservé aux salariés ou à la flotte relève
du **type C**.

**Conditions bloquantes** : gonflage gratuit pour les usagers, accès facile (M1/N1),
panneau TNPF visible, gonflage en sécurité, entretien conforme au cahier des charges TNPF,
remplacement des pièces défectueuses sous 15 jours maximum.

**Dates** : engagement = signature du contrat d'entretien ; achèvement = date anniversaire ;
durée de vie conventionnelle d'un an, valorisable chaque année si le contrat est actif et
**expressément** renouvelé (la reconduction tacite n'ouvre pas droit à une nouvelle
valorisation).

## Cas de référence vérifié par les tests

10 stations B + 5 stations C, prix brut 8,70 €/MWhc, marge délégataire 20 % :

| Indicateur | Valeur |
|---|---|
| Volume | 1 682 000 kWh cumac |
| Prix net | 6,96 €/MWhc |
| Montant CEE brut | 14 633,40 € |
| Montant CEE net | 11 706,72 € |
| Par station B | 1 032,86 €/an |
| Par station C | 275,62 €/an |

## Structure du code

```
cee-gonflage/
├── index.html              coquille + navigation
├── css/styles.css
├── js/
│   ├── config.js           constantes de la fiche + valeurs par défaut modifiables
│   ├── calc.js             moteur de calcul pur (testé)
│   ├── classify.js         arbre de décision A/B/C + éligibilité (testé)
│   ├── dossier.js          pièces et échéances du dossier CEE (testé)
│   ├── emails.js           modèles d'e-mails + substitution des variables
│   ├── storage.js          persistance localStorage + export/import JSON
│   ├── csv.js              export CSV (séparateur « ; », BOM Excel)
│   ├── ui.js               helpers DOM et formatage fr-FR
│   ├── app.js              routage par ancre (#/vue)
│   └── views/              une vue par module
└── tests/                  tests Node natifs
```

## Règles de rédaction des e-mails

À respecter pour toute modification de `js/emails.js` :

- ne jamais écrire « gratuit », « 100 % financé » ou « offert » **pour le site** :
  on écrit « **en grande partie financé par les CEE** » ;
- le mot « gratuit » ne s'applique qu'au **gonflage pour les usagers**, qui est une
  condition du dispositif ;
- les montants annoncés sont indicatifs et dépendent du cours du CEE ;
- une seule demande par e-mail, ton professionnel, phrases courtes.

## Données personnelles (RGPD)

Les données restent dans le navigateur (`localStorage`), aucun serveur, aucun transfert,
aucun scraping. Seules sont collectées les données professionnelles nécessaires au suivi
commercial : prénom, fonction et e-mail professionnel du contact. Exporter une sauvegarde
JSON régulièrement : vider les données du navigateur efface le CRM.

## Limites connues

- Les coûts réels (borne, installation, pièces, déplacements) ne sont pas chiffrés :
  ils valent 0 par défaut et l'interface signale que la marge affichée est alors un
  plafond théorique.
- La fiche TRA-SE-104 est ancienne : elle peut être révisée ou abrogée. Vérifier la version
  en vigueur avant chaque campagne.
- Un dossier non conforme peut entraîner l'annulation des CEE lors d'un contrôle du PNCEE.

## Gabarit d'e-mail HTML (dossier `emails/`)

| Fichier | Rôle |
|---|---|
| `email-gonflage.html` | Gabarit HTML de l'e-mail de premier contact (tableaux, styles en ligne, 600 px). |
| `build-email.mjs` | Remplit les variables et produit la version texte : `node emails/build-email.mjs --nom "Carrefour Bron" --prenom Sophie > sortie.html`. |
| `illustration-borne.svg` / `.png` | Illustration de la borne, seul élément en image. |
| `banniere-gonflage.svg` / `.png` | Bandeau complet avec texte, pour la plaquette ou les réseaux sociaux. |
| `build-banniere.mjs` | Régénère les PNG depuis les SVG (`npm i playwright-core` au préalable). |

**Parti pris :** le texte de l'en-tête est en HTML, pas dans l'image. En prospection à froid,
la plupart des messageries bloquent les images par défaut : le message doit rester entièrement
lisible sans elles. Seule l'illustration est une image, et elle porte un `alt` vide pour ne pas
polluer la lecture quand elle ne se charge pas.

Les visuels sont des tracés originaux : aucune photo tierce, aucun droit à acquérir.
