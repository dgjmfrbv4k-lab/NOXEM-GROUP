# NOXEM GROUP — site vitrine (panneaux composites aluminium)

Site statique d'une seule page présentant l'activité « panneaux composites aluminium
type Alucobond® » : produits, finitions, applications, méthode, FAQ et demande de devis.

## Hébergement : gratuit, via GitHub Pages

Aucun hébergeur payant, aucun nom de domaine obligatoire. Le site est publié
automatiquement par GitHub à chaque `push` sur la branche configurée dans
`.github/workflows/deploy-pages.yml`.

**À faire une seule fois, dans les réglages du dépôt :**

1. Ouvrir `Settings` → `Pages`
2. Dans **Source**, choisir **GitHub Actions**
3. Attendre la fin du workflow « Deploy static site to Pages » (onglet `Actions`)

L'adresse publique est ensuite :

```
https://dgjmfrbv4k-lab.github.io/NOXEM-GROUP/
```

C'est ce lien qui se partage (email, WhatsApp, carte de visite, QR code).

## Fichiers

| Fichier      | Rôle                                                        |
|--------------|-------------------------------------------------------------|
| `index.html` | Contenu et structure de la page                              |
| `styles.css` | Mise en forme complète (responsive, mobile inclus)           |
| `script.js`  | Menu mobile, animations, sélecteur de finitions, formulaire  |
| `montaugem/` | Ancien site de démonstration, conservé à part                |

## Ce qu'il reste à personnaliser

- **Coordonnées** : email et téléphone dans `index.html` (section `#contact` et pied de page)
- **Adresse de réception du devis** : constante `DESTINATAIRE` en haut de la partie
  formulaire dans `script.js`
- **Tarifs et références produits** : section `#produits`
- **Photos de chantiers** : les visuels sont actuellement générés en CSS ; il suffit de
  déposer des images dans le dépôt et de remplacer les blocs concernés

## Le formulaire

Un site statique n'a pas de serveur : le formulaire ouvre donc la messagerie du visiteur
avec la demande déjà rédigée. Pour recevoir les demandes directement par email sans que
le visiteur ait à ouvrir son logiciel de mail, un service gratuit comme Formspree ou
Web3Forms peut être branché en remplaçant l'action du formulaire — sans rien changer
à l'hébergement.

---

Alucobond® est une marque déposée de 3A Composites GmbH. Elle n'est citée qu'à titre de
référence produit.
