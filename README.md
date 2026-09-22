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

## Référencement naturel (SEO)

Tout ce qui se joue dans le code est en place :

| Élément | Détail |
|---|---|
| Pages par langue | `/en/ /fr/ /ar/ /es/ /tr/ /pl/ /hr/ /nl/` — chaque page est **entièrement traduite dans le HTML**, donc indexable séparément par Google. C'est le point le plus important pour prospecter dans plusieurs pays. |
| `hreflang` | Chaque page déclare ses huit sœurs + `x-default`, pour que Google serve la bonne langue selon le pays du visiteur. |
| Balises `title` / `description` | Uniques et traduites par langue, calibrées pour l'affichage dans les résultats. |
| Canonique | Chaque page pointe vers elle-même, pas de contenu dupliqué. |
| Données structurées | JSON-LD `Organization`, `WebSite` et `Product` : nom, logo, email, langues parlées, 21 pays desservis, épaisseurs, âmes, revêtements, disponibilité. C'est ce qui alimente les fiches enrichies. |
| `sitemap.xml` | Les 9 URL avec leurs alternates, régénéré à chaque build. |
| `robots.txt` | Indexation autorisée + lien vers le sitemap. |
| Image de partage | `assets/og-image.png` (1200 × 630) : aperçu propre sur WhatsApp, LinkedIn, Facebook, Slack. |
| Vitesse | Aucune police ni bibliothèque externe, aucune requête tierce, logo en PNG transparent. Un site rapide est mieux classé. |
| Sémantique | Un seul `h1` par page, `h2` par section, texte alternatif sur les images, langue déclarée sur `<html>`. |
| Mots-clés | Vocabulaire métier réellement recherché : ACP, ACM, aluminium composite panel, PVDF, âme A2, B1, incoterms, plus 29 ports de destination nommés. |

### Regénérer les pages

Après toute modification de `index.html` ou de `i18n.js` :

```bash
node build.mjs
```

Le script réécrit les huit dossiers de langue, `sitemap.xml` et `robots.txt`.
**Ne jamais modifier à la main les fichiers dans `/en/`, `/fr/`, etc.** : ils sont
écrasés à chaque build. Le jour d'un nom de domaine, changer la constante `SITE`
en haut de `build.mjs` puis relancer le build.

### Ce qui ne peut pas se faire depuis le code

Le référencement se gagne autant en dehors du site :

1. **Un vrai nom de domaine.** `panneaux.noxemgroup.com` inspire confiance et se
   classe mieux qu'une adresse `github.io`. Se branche gratuitement sur GitHub Pages.
2. **Google Search Console** — déclarer le site et soumettre `sitemap.xml`.
   C'est ce qui déclenche l'indexation, sinon Google peut mettre des mois.
3. **Bing Webmaster Tools** — même chose, utile au Maghreb et en Turquie.
4. **Fiche Google Business Profile** au nom de l'entreprise, avec l'adresse réelle :
   c'est ce qui fait apparaître la société quand on tape son nom.
5. **Annuaires professionnels export** : Europages, Kompass, Alibaba, Made-in-China,
   les chambres de commerce. Chaque fiche est un lien entrant, et les acheteurs y cherchent.
6. **LinkedIn d'entreprise** pointant vers le site.
7. **Les photos réelles** dans `assets/` : Google Images amène des acheteurs du bâtiment.

## Campagne « conteneur direct » — verre plat

Dossier `campagne-conteneur-20-open-top/` : campagne d'export mondiale du verre plat
chargé en conteneur 20' / 40' Open Top, formats 3210 × 2250 et 3210 × 2550 mm.

| Page | Adresse | Rôle |
|---|---|---|
| Page de campagne | `/campagne-conteneur-20-open-top/` | Publique, 10 langues, avec calculateur de chargement par conteneur |
| Console de prospection | `/campagne-conteneur-20-open-top/prospection.html` | Interne, non indexée : 176 pays, 314 ports, messages sur mesure dans 48 langues |

Le détail — types de clients, alertes sanctions, ajout d'un pays ou d'une langue, règles
d'envoi et sources pour constituer les listes de sociétés — est dans
`campagne-conteneur-20-open-top/README.md`.

Ces deux pages sont autonomes : elles ne dépendent ni de `i18n.js` ni de `build.mjs`, et ne
sont pas réécrites par le build. Seule la page publique est déclarée dans `sitemap.xml` ;
la console est explicitement exclue dans `robots.txt`.

## Pages légales

Six pages, en français et en anglais, dans `legal/` :

| Français | English |
|---|---|
| `mentions-legales.html` | `legal-notice.html` |
| `politique-de-confidentialite.html` | `privacy-policy.html` |
| `conditions-generales-de-vente.html` | `terms-of-sale.html` |

Elles sont liées depuis le pied de page de toutes les pages du site : version
française sur `/fr/`, version anglaise partout ailleurs.

**Avant diffusion commerciale, il reste à faire deux choses :**

1. Remplacer les mentions surlignées en jaune (`<mark class="fill">`) par les
   informations officielles : forme juridique et capital, RCS, TVA
   intracommunautaire, directeur de la publication, délai de validité des offres,
   modalités de paiement, tolérance de quantité.
2. Faire relire les conditions générales de vente par votre conseil juridique,
   puis supprimer l'encadré orange `<div class="todo">` en haut de chaque page.

La politique de confidentialité décrit fidèlement le fonctionnement réel du site :
aucun cookie de suivi, aucun service tiers, formulaire qui ouvre la messagerie du
visiteur sans passer par un serveur, et mémorisation locale de la langue choisie.
Si le fonctionnement du formulaire change (branchement d'un service type
Formspree), cette page doit être mise à jour en conséquence.
