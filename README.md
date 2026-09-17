# NOXEM GROUP FRANCE — site vitrine

Site statique d'une seule page présentant l'activité panneaux composites
aluminium (ACP / ACM) : produits, spécifications sur mesure, coloris avec
aperçu 3D, emballage et expédition, qualité, demande de devis.

## Hébergement gratuit (GitHub Pages)

Aucun hébergeur payant. Le site est publié par GitHub à chaque `push` sur la
branche configurée dans `.github/workflows/deploy-pages.yml`.

À faire une seule fois dans les réglages du dépôt : `Settings` → `Pages` →
**Source : GitHub Actions**. L'adresse publique devient alors
`https://dgjmfrbv4k-lab.github.io/NOXEM-GROUP/`, et c'est ce lien qui se
partage. Un nom de domaine (par ex. `panneaux.noxemgroup.com`) peut être
branché dessus plus tard, toujours sans frais d'hébergement.

## Fichiers

| Fichier      | Rôle                                                                    |
|--------------|-------------------------------------------------------------------------|
| `index.html` | Contenu et structure de la page                                          |
| `styles.css` | Mise en forme, charte graphique, scène 3D                                |
| `i18n.js`    | Toutes les traductions (8 langues)                                       |
| `app.js`     | Nuancier, scène 3D, changement de langue, formulaire                     |
| `assets/`    | Vos photos — voir `assets/README.md`                                     |

## Langues

Anglais (par défaut), français, arabe (affichage droite-à-gauche automatique),
espagnol, turc, polonais, croate, néerlandais. La langue du visiteur est
détectée automatiquement et son choix est mémorisé.

Ajouter une langue : copier un bloc dans `i18n.js`, traduire les valeurs, puis
ajouter la ligne correspondante dans le menu déroulant de `index.html`.

## Points à personnaliser

| Quoi                        | Où                                                        |
|-----------------------------|-----------------------------------------------------------|
| Adresse de réception        | `MAIL` en haut de `app.js` (`aaron.harfi@noxemgroup.com`)  |
| Téléphone / WhatsApp        | section `#quote` de `index.html`                           |
| Teintes du nuancier         | tableau `COLORS` dans `app.js` (référence, nom, code hex)  |
| Épaisseurs, formats, âmes   | tableau de la section `#specs` et menus de la section 3D   |
| Chiffres de chargement      | clés `pack_s3_d` de `i18n.js`                              |
| Photos                      | dossier `assets/` — voir `assets/README.md`                |

## Le formulaire de devis

Un site statique n'a pas de serveur : le formulaire ouvre la messagerie du
visiteur avec la demande déjà rédigée (nom, société, pays, port de destination,
coloris, épaisseur, tôle par face, âme, format, quantité), traduite dans la
langue affichée. Pour recevoir les demandes directement par email sans que le
visiteur ouvre son logiciel de mail, un service gratuit comme Formspree ou
Web3Forms se branche sans rien changer à l'hébergement.

## Aperçu 3D des coloris

La scène de la section « Colours & 3D » est construite en CSS pur : bardage
mural, pile de panneaux dont la tranche montre la structure alu / âme / alu,
tôle échantillon et caisse d'export. Cliquer une teinte repeint la scène,
l'épaisseur choisie change l'épaisseur des tranches, et la scène se tourne à la
souris ou au doigt. Le bouton « Request this specification » reporte le coloris
et la configuration dans le formulaire de devis.
