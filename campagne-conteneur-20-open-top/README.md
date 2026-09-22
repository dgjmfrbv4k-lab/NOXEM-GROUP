# Campagne « conteneur direct » — verre plat 20' / 40' Open Top

Campagne d'export mondiale pour le verre plat chargé en conteneur Open Top au départ
d'Anvers : float clair, Low-E, miroir argenté, feuilleté et verres teintés, formats
3210 × 2250 mm et 3210 × 2550 mm.

Elle tient en deux pages et trois fichiers de données, sans serveur ni abonnement.

| Fichier | Rôle |
|---|---|
| `index.html` | Page publique de campagne, 10 langues, avec calculateur de chargement |
| `prospection.html` | Console interne : choisir un pays, générer le message dans la bonne langue |
| `data/pays.js` | 176 pays, leurs ports, la langue de contact, le transit indicatif, les alertes |
| `data/messages.js` | Les modèles de message dans 48 langues, par type de client |
| `data/page.js` | Les textes de la page publique, 10 langues |

## La page publique

`index.html` — adresse publique :
`https://dgjmfrbv4k-lab.github.io/NOXEM-GROUP/campagne-conteneur-20-open-top/`

C'est le lien à mettre dans les messages, la signature e-mail et les annuaires. Elle contient :

- le produit, les épaisseurs et les formats ;
- **un calculateur de chargement** : épaisseur + format + conteneur + charge utile → nombre de
  feuilles, m², tonnage et longueur de pile. Il dit ce que tout acheteur de verre veut savoir
  avant de parler prix, et il explique pourquoi le 20' reste la norme (c'est le poids qui bloque,
  jamais le volume : 24 t sont atteintes à 2 400 m² en 4 mm, à 950 m² en 10 mm) ;
- pourquoi l'Open Top (chargement par le toit à la grue, hauteur des grands formats, calage mer) ;
- les incoterms, les documents et les modalités de paiement ;
- la liste des ports desservis, par région, avec un champ de recherche ;
- deux boutons de contact qui pré-remplissent WhatsApp et l'e-mail dans la langue affichée.

Langues : anglais, français, espagnol, portugais, **arabe (affichage droite-à-gauche)**,
roumain, russe, turc, italien, allemand. La langue du visiteur est détectée, son choix est
mémorisé dans son navigateur.

## La console de prospection

`prospection.html` — page **non indexée** (`robots: noindex`), pour un usage interne.
Elle est tout de même accessible à qui connaît l'adresse : ne la diffusez pas.

1. **Votre signature** — nom, e-mail, téléphone, WhatsApp, lien de campagne. Saisis une fois,
   conservés dans le navigateur, repris dans tous les messages.
2. **Le pays** — recherche par pays ou par port, filtre par région et par langue. Chaque ligne
   donne les ports, le transit indicatif depuis Anvers et ce qu'il faut savoir du marché.
3. **La société** — nom, interlocuteur, type de client, port de destination. Le message se
   réécrit à chaque frappe, dans la langue du pays, avec l'e-mail complet d'un côté et la
   version courte WhatsApp / LinkedIn de l'autre, plus un mémo pays à garder sous les yeux.
4. **La série** — collez une liste de sociétés, récupérez un CSV prêt pour le publipostage
   (colonnes `societe ; pays ; langue ; email ; objet ; message ; whatsapp ; alerte`).

### Les six types de client

Chaque type a sa propre accroche, traduite dans les 48 langues :

| Clé | Cible | Angle du message |
|---|---|---|
| `miroiterie` | Miroiterie, transformateur | le jumbo livré à l'atelier, sans grossiste local |
| `trempe` | Trempeur, verre de sécurité | la régularité du float pour la ligne de trempe |
| `vitrage` | Double vitrage, menuiserie alu-PVC | les formats qui limitent les chutes de découpe |
| `negoce` | Négociant, importateur | le prix départ Europe et les documents pris en charge |
| `miroir` | Miroiterie déco, mobilier | le miroir argenté et les références introuvables sur place |
| `chantier` | Façadier, promoteur | éviter la rupture et le prix local en pleine saison |

### Les alertes

- 🔴 **Sanctions** — Iran, Syrie, Russie, Biélorussie, Soudan, Venezuela, Cuba, Birmanie,
  Ukraine, Yémen, Afghanistan. Le message se génère quand même, mais la destination, le
  destinataire et le circuit bancaire doivent être validés avant tout envoi d'offre.
- 🟠 **Float local** — le pays produit son propre float (Turquie, Égypte, Inde, Chine,
  Pologne, Espagne, Brésil…). Inutile d'y vendre du float clair standard : viser le miroir,
  le Low-E, le feuilleté et les formats jumbo.
- ⚪ **Enclavé** — coter CFR le port de transit, annoncer l'acheminement terrestre à part.

## Ajouter un pays, un port, une langue

**Un port ou un pays** : ouvrez `data/pays.js` et ajoutez une entrée. Les champs sont
`c` (code ISO), `fr` / `en` (noms), `r` (région), `l` (langue du message), `p` (ports),
`t` (transit indicatif en jours), `f` (drapeaux `p`/`x`/`e`), `n` (note), `loc` (nom du pays
dans la langue du message, article et déclinaison compris — c'est ce qui évite les
« vers Maroc » et les « do Polska »).

**Une langue** : copiez un bloc de `data/messages.js`, traduisez les valeurs, gardez les
champs de fusion `{contact} {company} {country} {port} {transit} {sender} {site}` intacts,
puis mettez `l` à ce code dans les pays concernés.

## Avant un envoi en nombre

1. **Faire relire les traductions marquées `"q":"check"`** dans `data/messages.js` :
   amharique, azéri, bengali, danois, estonien, persan, finnois, hébreu, hindi, arménien,
   géorgien, lituanien, letton, macédonien, malais, norvégien, somali, suédois, swahili,
   thaï, ourdou. La console affiche un bandeau orange quand le modèle est dans ce cas.
   Les autres langues sont rédigées, pas traduites automatiquement, mais une relecture
   commerciale reste toujours utile.
2. **Vérifier les mentions de la page publique** : la campagne annonce des documents
   (EUR.1, certificat d'origine) et des délais de réponse à 24 h — tenez-les.
3. **Prospection B2B et RGPD** : l'intérêt légitime (art. 6.1.f) couvre la prospection
   professionnelle vers des adresses génériques de société, à condition d'indiquer qui vous
   êtes, d'où viennent les coordonnées si on le demande, et de traiter toute demande de
   retrait. Chaque message se termine par une ligne de désinscription : ne la supprimez pas,
   et tenez à jour la liste des sociétés qui ont répondu « STOP ».
4. **Rythme d'envoi** : une adresse d'expédition neuve qui envoie 500 messages le premier jour
   finit en spam. Montez progressivement et répondez depuis la même adresse.

## Où trouver les sociétés à contacter

Les fichiers de données contiennent les pays, les ports et les messages — pas de listes de
sociétés : elles se constituent à la main, marché par marché, et c'est là que se gagne la
campagne. Les sources qui fonctionnent pour ce métier :

- **Europages, Kompass** — recherche par code d'activité et par pays (miroiterie, verre plat).
- **Chambres de commerce et fédérations** — annuaires des adhérents ; pour le verre, les
  associations nationales de miroitiers et de fabricants de menuiserie.
- **Salons** — glasstec (Düsseldorf), Zak Glass (Inde), Glass Expo Middle East, Big 5 (Dubaï),
  Batimatec (Alger) : les listes d'exposants sont publiques et à jour.
- **LinkedIn Sales Navigator** — filtre par secteur « verre » et par pays, pour trouver
  l'interlocuteur plutôt que l'adresse générique.
- **Statistiques douanières d'importation** (code SH 7005 pour le float, 7007 pour le feuilleté,
  7009 pour les miroirs) : elles disent quels pays importent vraiment, et combien.

Remplissez ensuite l'onglet « série » avec `société ; pays ; type ; interlocuteur ; e-mail ; port`
et la campagne part.
