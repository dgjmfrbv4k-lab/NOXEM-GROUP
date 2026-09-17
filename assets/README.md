# Photos du site

Déposer les photos dans ce dossier avec **exactement** ces noms de fichiers.
Le site les affiche automatiquement dès qu'elles sont présentes ; tant qu'un
fichier manque, une illustration de remplacement s'affiche à la place
(aucune image cassée n'apparaît jamais).

| Nom du fichier         | Où elle s'affiche                          | Photo conseillée                                   |
|------------------------|--------------------------------------------|----------------------------------------------------|
| `color-chart.jpg`      | Section « Colours & 3D », sous le sélecteur | Le nuancier physique, à plat, lumière naturelle     |
| `container-loading.jpg`| Section « Packing & shipping », 1re photo   | Le conteneur ouvert, caisses calées à l'intérieur   |
| `crates.jpg`           | Section « Packing & shipping », 2e photo    | Les caisses bois fermées, marquage visible          |
| `warehouse.jpg`        | Section « Packing & shipping », 3e photo    | L'entrepôt, panneaux ou caisses en stock            |

Conseils :

- Format paysage, minimum 1200 px de large, JPEG de qualité 80 (viser < 400 ko
  par photo pour que le site reste rapide sur mobile).
- Pas besoin de recadrer : le site ajuste automatiquement.
- Pour ajouter d'autres photos, dupliquer un bloc `<figure class="shot">`
  dans `index.html` et pointer `src` vers le nouveau fichier.
