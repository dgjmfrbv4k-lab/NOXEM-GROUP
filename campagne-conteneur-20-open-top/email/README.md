# Modèle d'e-mail — campagne conteneur

| Fichier | Rôle |
|---|---|
| `modele-fr.html` | **Le modèle.** Le vrai logo en image (`cid:noxem-logo.png`), tout le reste en couleurs de fond et en texte. |
| `modele-fr-sans-image.html` | Le même sans aucune image, logo compris : à utiliser si la plateforme d'envoi filtre les images. |
| `modele-fr.txt` | La version texte, à envoyer en alternative — elle évite le classement en spam. |
| `apercu-autonome.html` | Le modèle avec le logo intégré au fichier : s'ouvre dans un navigateur pour vérifier le rendu. |
| `noxem-logo.png` | Le logo, 181 × 60 px, 2 Ko. À joindre en pièce inline sous ce nom exact. |
| `banniere-image.png` | La bannière entière en une image, 1200 × 420 px, pour LinkedIn ou un en-tête de devis. |

## Deux règles à ne jamais enfreindre

Le logo est une image, mais **rien d'autre ne l'est** : le bandeau, les filets et
les aplats sont faits de couleurs de fond et de texte. Deux raisons :

1. **Une bonne partie des messageries bloquent les images par défaut.** L'accroche
   « Votre livraison à votre port, en conteneur complet » doit rester lisible même
   dans ce cas — elle l'est, seul le logo manque alors.
2. **Certains chemins d'envoi filtrent le HTML.** Un envoi via l'API Gmail, par
   exemple, supprime *toutes* les balises `<img>` — pièce jointe, data URI ou URL
   distante — et efface le raccourci CSS `background:`. C'est pour ce cas qu'existe
   `modele-fr-sans-image.html`.

D'où les deux règles :

- **Jamais `background:`** — toujours l'attribut `bgcolor="#RRGGBB"` sur la cellule,
  doublé de `background-color:` dans le style. Ces deux-là passent partout.
- **Pas d'image indispensable à la lecture.** Le logo est redessiné en cellules
  colorées et en typographie ; le message se tient sans une seule image.

Sont également vérifiés comme passant sans dommage : `border`, `padding`,
`font-family`, `font-size`, `font-weight`, `letter-spacing`, `color`,
`text-transform`, `line-height`, et les attributs `width`, `height`, `align`,
`valign`, `colspan` des tableaux.

## Ce que le message détaille

Trois blocs, dans cet ordre : **la gamme** (float, trempé, feuilleté, Low-E,
contrôle solaire, vitrage isolant, miroirs, laqué, dépoli, imprimé, émaillé),
**les formats** — le 3210 × 2550 mis en avant, les huit autres formats courants
listés, et la découpe sur plan — puis **caisses bois & livraison** : verre lavé
et contrôlé, caisses d'export traitées NIMP-15, chargement 20' ou 40', photos et
numéro de conteneur le jour de l'empotage, livraison au port avec les documents.

Les formats et les épaisseurs viennent du catalogue professionnel. Si le
catalogue évolue, corriger ici aussi : un acheteur qui compare les deux relève
la moindre différence.

## Champs à remplacer pour chaque destinataire

Le modèle est volontairement sans nom de société : il s'envoie tel quel. Pour
le personnaliser, remplacer `Bonjour,` par la formule d'appel du pays et
insérer l'accroche métier — la console `../prospection.html` produit ces deux
éléments dans la langue du destinataire.

## Avant l'envoi en nombre

- Authentifier le domaine d'envoi (SPF, DKIM, DMARC) sinon les messages
  partent en indésirables.
- Monter en volume progressivement depuis une adresse neuve.
- Tenir à jour la liste des sociétés qui ont répondu « STOP ».
