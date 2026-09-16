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

## Cibler les bons clients

`outils/simuler-profils.mjs` chiffre chaque profil de client avec le moteur de calcul
et les classe par marge rapportée à l'effort commercial :

```bash
node outils/simuler-profils.mjs
node outils/simuler-profils.mjs --prix 9 --entretien 250 --md > docs/simulations.md
```

Le tableau produit est dans `docs/simulations.md`. Il répond à une question de
prospection : à temps commercial égal, quel type de client rapporte le plus ?

## Constituer la liste de prospects

`outils/collecte-cibles.mjs` interroge OpenStreetMap et produit la liste des sites
d'une zone, déjà classés A / B / C au sens de la fiche :

```bash
node outils/collecte-cibles.mjs --zone "Métropole de Lyon" --sortie cibles-lyon
```

Sortie : `cibles-lyon.json` (à importer dans l'onglet Prospection) et `cibles-lyon.csv`.
Aucune donnée personnelle n'est collectée : OpenStreetMap décrit des établissements,
pas des personnes.

`docs/cibles.md` détaille, pour chaque type A / B / C, les catégories de sites,
**qui signe** dans chaque cas et l'ordre d'attaque conseillé.

### Les communes

> La séquence complète pour couvrir la France — l'ordre des départements, les commandes
> de chaque vague et la boucle quotidienne — est dans **`docs/plan-france.md`**.


`outils/collecte-mairies.mjs` constitue la liste des mairies d'un département à partir
de l'**Annuaire de l'administration** (service-public.fr), avec leur adresse de contact
officielle :

```bash
node outils/collecte-mairies.mjs --departement 69
node outils/collecte-mairies.mjs --departement 69,01,38,42 --sortie mairies-lyon
```

Ces adresses sont **institutionnelles et publiées par l'État** : ce sont des adresses
d'établissement, pas des données personnelles. Aucun nom d'agent ni d'élu n'est collecté
— le nom de l'interlocuteur se demande au téléphone.

Le type CEE reste vide dans les fiches produites : une commune a le plus souvent un parking
ouvert au public (**type B**) *et* un parking d'agents (**type C**). C'est un dossier groupé,
à qualifier lors de l'échange.

> L'API est publique mais bloquée depuis certains environnements d'exécution : lancer
> cette commande depuis un poste avec un accès Internet ordinaire.

## Préparer les envois

`outils/preparer-envois.mjs` transforme la liste de prospects en messages prêts à
envoyer **depuis votre messagerie** :

```bash
node outils/preparer-envois.mjs --sites cibles-lyon.json --quota 25
node outils/preparer-envois.mjs --sites mairies-lyon.json --quota 50 --modele mairie
```

`--modele` choisit le gabarit (voir le dossier `emails/`) :

| Modèle | Pour qui | Angle |
|---|---|---|
| `gonflage` *(défaut)* | Commerces, parkings privés ouverts au public, aires | Service gratuit et visible pour **vos clients**. |
| `mairie` | Communes | **Aucune dépense communale**, service aux administrés, convention d'occupation du domaine public, parking public + parking des agents dans le même dossier. Le message demande explicitement sa **transmission au service concerné** — il arrive sur un accueil, pas chez le décideur. |
| `relance` | Ceux déjà contactés | Deuxième message, à J+10. Voir « La relance » plus bas. |

Il écrit un dossier `envois/` avec un fichier `.eml` par site — double-clic ou
glisser-déposer dans le client de messagerie, le message s'ouvre rédigé, images
comprises — et un `index.html` pour suivre les envois du jour.

**Pourquoi pas un envoi automatique en masse :** une boîte professionnelle plafonne
à quelques centaines d'envois par jour, et un domaine récent qui dépasse ce seuil est
classé en spam en quelques jours. Un domaine grillé ne se répare pas. L'outil fait
gagner le temps de rédaction, pas celui de l'envoi : vous restez l'expéditeur, à un
rythme que les filtres acceptent.

## Envoyer la série du jour (volume élevé)

À 25 ou 50 messages par jour, les `.eml` de `preparer-envois.mjs` restent tenables :
on relit chaque message avant de l'envoyer. **À 150 par jour, ce n'est plus possible.**
`outils/envoyer.mjs` prend le relais :

```bash
# 1. Simulation (comportement par défaut) : rien n'est envoyé, le plan s'affiche
node outils/envoyer.mjs --sites mairies-69.json --modele mairie --quota 150

# 2. Envoi réel
node outils/envoyer.mjs --sites mairies-69.json --modele mairie --quota 150 --envoyer
```

Prérequis : `npm i nodemailer`, et au moins une boîte déclarée dans `envois/boites.json`
(un exemple est écrit automatiquement à la première exécution). **Les mots de passe ne
sont jamais dans ce fichier** : il nomme la variable d'environnement qui les contient.
Le dossier `envois/` est dans `.gitignore`.

### Les trois garde-fous

| Garde-fou | Fichier | Effet |
|---|---|---|
| **Journal** | `envois/journal.json` | Réécrit après *chaque* message. Une adresse déjà contactée ne repart jamais, même si la commande est relancée ou interrompue. |
| **Suppression** | `envois/suppression.txt` | Une adresse par ligne (réponses « STOP », erreurs définitives). Jamais recontactée. |
| **Rythme** | `--intervalle` (90 s par défaut) | Délai variable entre deux messages. Une cadence parfaitement régulière est une signature d'automate. |

### 150 par jour : ajouter des boîtes, pas pousser une seule

`CAP_PAR_BOITE` vaut **40**. Ce n'est pas la limite du fournisseur (Google Workspace
accepte 2 000 destinataires externes par jour) : c'est le seuil au-delà duquel une boîte
qui fait de la prospection à froid se fait repérer. Toutes les plateformes de cold
e-mailing tournent entre 30 et 50 par boîte et par jour.

**150 par jour = 4 boîtes à ~38.** L'outil le dit lui-même :

```
1 boîte(s) d'envoi × 40 = 40 de capacité aujourd'hui.
40 message(s) au programme (150 demandé(s)).

Pour tenir 150 par jour, il manque 3 boîte(s) d'envoi.
```

Il répartit en tourniquet et ne dépasse jamais le plafond d'une boîte. Ce qui excède la
capacité du jour n'est pas envoyé — c'est le principe du plafond.

### La relance — c'est elle qui rapporte

En prospection à froid, **l'essentiel des réponses arrive après le deuxième message**,
pas après le premier. Un premier envoi sans relance gaspille la majeure partie du travail
de collecte.

```bash
node outils/envoyer.mjs --sites mairies-01-rhone.json --modele relance --quota 150 --envoyer
```

L'outil sélectionne tout seul : contactés il y a **au moins 10 jours** (`--jours` pour
changer le délai), **jamais relancés**, **pas sur la liste de suppression**. Quand il n'y
a rien à relancer, il le dit et s'arrête.

Trois partis pris dans le gabarit `emails/email-relance.html` :

- **Le message est rattaché au fil du premier** (en-têtes `In-Reply-To` / `References`,
  objet préfixé `Re:`). Il s'affiche sous l'original dans la boîte du destinataire :
  une conversation reprise, pas une deuxième sollicitation isolée. C'est pour cela que
  le journal conserve le `messageId` de chaque envoi.
- **Aucune image, aucun bandeau, aucun bouton.** Une relance qui ressemble à une
  deuxième publicité est supprimée ; une relance qui ressemble à quelqu'un qui reprend
  contact est lue.
- **Une porte de sortie explicite** (« répondez-moi en un mot, je ne vous solliciterai
  plus »). Un « non » franc vaut mieux qu'un signalement en spam, et il nettoie la liste.

**Une seule relance par destinataire.** Au-delà, on fabrique des plaintes, pas des
rendez-vous — et le journal l'empêche.

### Vérifier le domaine avant d'envoyer

```bash
node outils/verifier-domaine.mjs noxemgroup.com
```

Relève SPF, DKIM, DMARC et MX dans le DNS public, identifie l'hébergeur mail et classe
les défauts du plus grave au plus bénin. À passer **avant le premier envoi** et après
chaque modification DNS. Il détecte notamment le défaut le plus coûteux : une plateforme
d'envoi validée dans le DNS mais absente du SPF — la plateforme affiche le domaine comme
validé, l'envoi part, et il échoue à l'authentification.

L'état relevé pour `noxemgroup.com` et les correctifs exacts sont dans
`docs/delivrabilite.md`.

### La montée en volume est automatique

`envois/campagne.json` retient la date du premier envoi. À chaque exécution, l'outil en
déduit le palier du jour : **10 par boîte la première semaine, 20 la deuxième, 30 la
troisième, 40 ensuite.**

`--quota` est une demande, pas un ordre — **le palier prime** :

```
Jour 1 de la campagne — palier : 10 par boîte.
Vous avez demandé 150 : le palier prime, ce sera 40.
```

C'est voulu : un domaine qui passe de 0 à 150 en une journée est signalé pour cela seul,
indépendamment du contenu. La commande reste la même tous les jours, et le volume monte
tout seul. SPF, DKIM et DMARC doivent être en place **avant** le premier envoi — voir
`docs/delivrabilite.md`.

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
| `email-mairie.html` | Même gabarit, version **collectivités** : demande de transmission en interne, cadre juridique, aucune dépense communale. |
| `build-email.mjs` | Remplit les variables et produit la version texte : `node emails/build-email.mjs --nom "Carrefour Bron" --prenom Sophie > sortie.html`, ou `--modele mairie --commune Dardilly`. Les modèles sont déclarés dans `MODELES`. |
| `illustration-borne.svg` / `.png` | Illustration de la borne, seul élément en image. |
| `banniere-gonflage.svg` / `.png` | Bandeau complet avec texte, pour la plaquette ou les réseaux sociaux. |
| `build-banniere.mjs` | Régénère les PNG depuis les SVG (`npm i playwright-core` au préalable). |

**Parti pris :** le texte de l'en-tête est en HTML, pas dans l'image. En prospection à froid,
la plupart des messageries bloquent les images par défaut : le message doit rester entièrement
lisible sans elles. Seule l'illustration est une image, et elle porte un `alt` vide pour ne pas
polluer la lecture quand elle ne se charge pas.

Les visuels sont des tracés originaux : aucune photo tierce, aucun droit à acquérir.
