# Aurelis — Comptoir d'Or

Site vitrine d'un comptoir d'achat et de rachat d'or : grille de rachat publique,
simulateur d'estimation, explication du parcours client, FAQ et formulaire de contact.

Le site est entièrement statique (HTML, CSS, JavaScript, sans dépendance ni build).

## Fichiers

| Fichier      | Contenu                                                      |
|--------------|--------------------------------------------------------------|
| `index.html` | Toutes les sections de la page et les textes                 |
| `styles.css` | La charte graphique (couleurs, typographies, mise en page)   |
| `script.js`  | Les prix, la grille de rachat, le simulateur, les animations |

## Voir le site en local

Ouvrez `index.html` dans un navigateur, ou lancez un petit serveur :

```bash
python3 -m http.server 8000
# puis ouvrez http://localhost:8000
```

## Mettre à jour les prix

Tout est centralisé dans l'objet `TARIFS`, en haut de `script.js` :

- `miseAJour` : la date affichée sous la grille de rachat ;
- `alliages` : le prix de rachat au gramme, par titre d'or (24, 22, 18, 14, 9 carats) ;
- `pieces` : le prix de rachat à l'unité des pièces et lingots.

La grille affichée sur le site **et** le simulateur d'estimation lisent les mêmes
valeurs : une seule modification suffit, il n'y a rien à changer dans `index.html`.

> ⚠️ Les prix livrés sont des **valeurs d'exemple cohérentes entre elles**, pas un
> cours réel. Remplacez-les par votre propre grille avant toute mise en ligne.

## Changer le nom de la marque

Le nom « Aurelis » apparaît dans `index.html` : la balise `<title>`, les balises
`<meta>` de description, les deux blocs `.logo` (en-tête et pied de page), la section
« Pourquoi Aurelis », le lingot décoratif et la ligne de copyright.

## À compléter avant la mise en ligne

- [ ] Coordonnées réelles : téléphone, email, adresse, horaires (section `#contact`)
- [ ] Mentions légales, SIREN, politique de confidentialité (pied de page)
- [ ] Grille de rachat réelle et procédure de mise à jour du cours
- [ ] Traitement du formulaire : il est aujourd'hui purement visuel et n'envoie rien.
      Branchez-le sur un service de formulaire ou sur votre propre backend.
- [ ] Vérification des mentions réglementaires (identification du vendeur, registre
      des achats, délai de rétractation, fiscalité) avec votre conseil juridique.

## Mise en ligne

Le workflow `.github/workflows/deploy-pages.yml` publie automatiquement le site sur
GitHub Pages à chaque push sur les branches listées dans son déclencheur. GitHub Pages
doit être activé sur le dépôt, avec la source « GitHub Actions ».
