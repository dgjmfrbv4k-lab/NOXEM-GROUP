# Le message de prospection export

| Fichier | Rôle |
|---|---|
| `modele-fr.html` | Le modèle de référence, en français, avec le vrai logo (`cid:noxem-logo.png`). |
| `modele-fr-sans-image.html` | Le même sans aucune image, logo compris, pour les plateformes qui filtrent les images. |
| `modele-fr.txt` | La version texte, à envoyer en alternative — elle évite le classement en spam. |
| `apercu-autonome.html` | Le modèle avec le logo intégré au fichier : s'ouvre dans un navigateur pour vérifier le rendu. |
| `noxem-logo.png` | Le logo, 181 × 60 px, 2 Ko. À joindre en pièce inline sous ce nom exact. |
| `banniere-image.png` | La bannière entière en une image, 1200 × 420 px, pour LinkedIn ou un en-tête de devis. |

**Les 47 autres langues ne sont pas des fichiers.** Elles vivent dans
`../data/emails.js` et la console `../prospection.html` assemble le HTML à la
demande, dans la langue du pays choisi, avec le port inséré au bon endroit.
C'est le même message, la même bannière, la même mise en page : seule la langue
change.

## Deux règles à ne jamais enfreindre

Le logo est une image, mais **rien d'autre ne l'est** : le bandeau, les filets et
les aplats sont faits de couleurs de fond et de texte. Deux raisons :

1. **Une bonne partie des messageries bloquent les images par défaut.** L'accroche
   doit rester lisible même dans ce cas — elle l'est, seul le logo manque alors.
2. **Certains chemins d'envoi filtrent le HTML.** Un envoi via l'API Gmail
   supprime *toutes* les balises `<img>` — pièce jointe, data URI ou URL
   distante — et efface le raccourci CSS `background:`. C'est pour ce cas
   qu'existe `modele-fr-sans-image.html`.

D'où les deux règles :

- **Jamais `background:`** — toujours l'attribut `bgcolor="#RRGGBB"` sur la cellule,
  doublé de `background-color:` dans le style. Ces deux-là passent partout.
- **Pas d'image indispensable à la lecture.**

Sont vérifiés comme passant sans dommage : `border`, `padding`, `font-family`,
`font-size`, `font-weight`, `letter-spacing`, `color`, `text-transform`,
`line-height`, et les attributs `width`, `height`, `align`, `valign`, `colspan`.

## Ce que le message détaille

Trois blocs : **la gamme** (float, trempé, feuilleté, Low-E, contrôle solaire,
vitrage isolant, miroirs, laqué, dépoli, imprimé, émaillé), **les formats** — le
3210 × 2550 mis en avant, les huit autres formats courants, et la découpe sur
plan — puis **caisses bois & livraison** : verre lavé et contrôlé, caisses
d'export traitées NIMP-15, chargement 20' ou 40', photos et numéro de conteneur
le jour de l'empotage, livraison au port avec les documents.

Les formats et les épaisseurs viennent du catalogue professionnel. Si le
catalogue évolue, corriger ici et dans `../data/emails.js` : un acheteur qui
compare les deux relève la moindre différence.

## Avant l'envoi en nombre

- Authentifier le domaine d'envoi (SPF, DKIM, DMARC) sinon les messages partent
  en indésirables.
- Monter en volume progressivement depuis une adresse neuve.
- Faire relire les langues marquées `"q":"check"` dans `../data/emails.js`.
- Tenir à jour la liste des sociétés qui ont répondu « STOP ».
