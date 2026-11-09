# Les dix actions prioritaires

Classement par impact sur les **demandes de devis qualifiées**, puis par urgence, puis par effort.
Échelles : impact et urgence de 1 à 3 (3 = maximal) ; effort en S (moins de 2 h), M (une demi-journée à 2 jours) ou L (plus de 2 jours).

| # | Action | Impact | Urgence | Effort | Qui | Statut |
|---|---|---|---|---|---|---|
| 1 | Brancher la mesure : Search Console, GA4, événements « devis » | 3 | 3 | S | Vous (accès) + moi (configuration) | Bloqué : accès |
| 2 | Unifier les coordonnées et vérifier l'adresse `aaronharfi@noxem-group.com` | 3 | 3 | S | Vous (choix du numéro) + moi | À décider |
| 3 | Donner un contenu propre à `/produits/`, `/qui-sommes-nous/` et `/contact/` | 3 | 3 | M | Moi | Contenu préparé |
| 4 | Faire le ménage dans le multilingue et le contenu produit en masse | 3 | 2 | M | Vous (décision) + moi | À décider |
| 5 | Fiches produits : titres, descriptions, liens internes, hreflang | 3 | 2 | S/M | Vous (collage Yoast) + moi | Préparé |
| 6 | Créer les pages France et métiers : serres, menuiseries et façades, miroiteries, transformateurs | 3 | 2 | M/L | Moi (rédaction) + vous (validation des faits) | 2 pages rédigées |
| 7 | Une seule navigation, un seul message | 2 | 2 | M | Moi + intégrateur Elementor | Préparé |
| 8 | Alléger les pages (de 433 Ko vers moins de 150 Ko de HTML) | 2 | 2 | M | Intégrateur, ou moi avec accès admin | À planifier |
| 9 | Netlinking : premiers liens gratuits et pertinents | 2 | 1 | M | Moi (préparation) + vous (accord, envoi) | Préparé, rien envoyé |
| 10 | Nettoyage technique, et décision sur le site GitHub Pages « panneaux composites » | 1 | 1 | S | Moi | Préparé |

---

## 1. Brancher la mesure (indispensable)
**Pourquoi.** Sans mesure, impossible de relier le SEO à des demandes de devis, ni même de savoir quelles requêtes vous montrent déjà dans Google.
**Comment.** Voir `01-acces.md`, procédures A et B. Il faut au minimum : la Search Console vérifiée avec le sitemap soumis, GA4 relié, les événements clés (formulaire, WhatsApp, téléphone, e-mail, catalogue), et un champ « source » dans votre suivi commercial.
**Résultat attendu.** Premier relevé de référence (requêtes, pages, devis) sous 7 jours.

## 2. Unifier les coordonnées
**Pourquoi.** Trois téléphones différents et une adresse e-mail sur un autre domaine que celui du site : c'est un risque direct de **demandes perdues**, et un signal de confiance négatif.
**Comment.**
1. Envoyez un e-mail de test à `aaronharfi@noxem-group.com`. S'il n'arrive pas, je remplace le lien par `contact@noxemgroup.com` dans le bloc HTML de l'accueil et des pages du nouveau gabarit.
2. Choisissez un numéro principal (02 59 50 84 59 ou 04 22 91 55 80). Je le reporte dans l'en-tête de l'ancien gabarit (Tombuild : Apparence → Personnaliser → En-tête), dans les pages Elementor, les mentions légales et le schéma Organization de Yoast (Yoast → Réglages → Représentation du site).
3. Alignez la fiche Europages et les annuaires sur les mêmes coordonnées.

## 3. Un contenu propre pour `/produits/`, `/qui-sommes-nous/` et `/contact/`
**Pourquoi.** Ces trois pages sont des copies de l'accueil (similarité de 96 %, même H1). Ce sont pourtant les pages les plus consultées après l'accueil (Produits : 18 vues sur 90 jours).
**Comment.** Les structures et les textes complets sont dans `05-strategie-contenu.md`, sections B1 à B3. Pour `/produits/` : H1 « Verre plat en gros pour professionnels : float, feuilleté, trempé, miroir, Low-E », une carte par famille avec un lien vers la fiche, un tableau des épaisseurs et formats repris des fiches, et l'appel à demander un prix.
**Mise en ligne.** Possible directement par le connecteur. Comme les pages sont construites avec Elementor, je propose de créer chaque nouvelle version **en brouillon**, de vous la faire valider, puis d'échanger.

## 4. Faire le ménage dans le multilingue et le contenu produit en masse
**Pourquoi.** 24 pages de langue déclarées en français, aucun hreflang sur les articles, environ 100 articles d'actualité en trois langues publiés en trois jours, des pages « stock vendu » en 26 langues. C'est exactement le schéma que Google traite comme du contenu produit en masse. Ce contenu ne vise pas les acheteurs français, et il dilue le site.

**Ma recommandation** (à valider) :
- **Garder** le français (marché prioritaire) et l'anglais (export), tous deux gérés par Polylang avec hreflang. Ajouter **l'arabe et l'espagnol** plus tard, en vraies traductions des pages commerciales et non de l'actualité, si les demandes de devis le justifient (voir `05-strategie-contenu.md`, section D).
- **Passer en noindex et retirer du sitemap** les pages de langue sans marché actif aujourd'hui : sw, ha, am, bn, ur, hi, id, vi, ja, ko, fa, zh, el, uk, ro, ru, ainsi que leurs pages « Nos réalisations » et « Export ». C'est réversible. Si vous préférez les supprimer : redirection 301 vers `/en/home/`.
- **Pages « stock vendu »** (10 langues) : redirection 301 vers `/livraison-monde/` ou vers la page Déstockage actuelle.
- **Articles d'actualité géopolitique** (Ormuz, pétrole, gaz, Ukraine, Koweït, etc.) : passer en noindex ceux qui ne serviront plus dans trois mois. **Garder et renforcer** les articles utiles dans la durée, qui ont une vraie intention d'achat : « Combien de m² de verre dans un conteneur 20 et 40 pieds », « Verre feuilleté 33.1, 44.2, 55.2 », « CIF, CFR ou FOB », « Low-E ou réfléchissant », les guides pays (Maroc, Algérie, Outre-mer). Les relier aux fiches produits.
- Pour l'avenir : **au plus 2 à 4 articles par mois**, chacun relu, sourcé, et relié à une page commerciale.

**Comment.** Les réglages noindex se font dans Yoast (colonne SEO, avancé → « Autoriser les moteurs à afficher… : Non »). L'API n'y donne pas accès. Je peux fournir la liste exacte des URL. Avec un accès administrateur, une seule règle suffit.

## 5. Fiches produits : titres, descriptions, liens internes, hreflang
**Pourquoi.** Ce sont les pages qui doivent capter « fournisseur verre feuilleté », « verre float en gros », « miroir argenté en plateaux », etc. Aujourd'hui elles sont isolées et n'ont pas de description.
**Comment.**
1. Coller titres et descriptions depuis `04-meta-produits.csv` (Yoast, champ par champ : environ 20 minutes au total).
2. Relier les fiches : depuis l'accueil (remplacer l'ancre `#produits` par des liens vers chaque fiche), depuis `/produits/` (action 3), depuis les articles techniques (par exemple, l'article « Verre feuilleté 33.1 / 44.2 » doit renvoyer vers `/service/verre-feuillete/`), et depuis le menu.
3. Dans Polylang, associer chaque fiche FR à sa fiche EN (`/service/verre-float/` ↔ `/en/float-glass/`), pour que le hreflang soit généré automatiquement.
4. Ajouter à chaque fiche un bloc « Pour qui » (transformateurs, miroitiers, menuisiers, etc.) et un bloc « Conditionnement et livraison » repris des informations déjà publiées.

## 6. Créer les pages France et métiers
**Pourquoi.** Vos clients cherchent par métier et par besoin, pas par port. Aucune page ne vise les fabricants de menuiseries, les façadiers ni les constructeurs de serres.
**Pages proposées, par ordre :**
1. « Fournisseur de verre plat en France » : livraison en France, stock en Belgique, conteneur complet ou panaché. ✅ Rédigée.
2. « Verre pour serres professionnelles » : aucun concurrent négociant visible, et c'est le préalable aux liens Hortidaily et SIVAL. ✅ Rédigée.
3. « Verre pour fabricants de menuiseries et façadiers » (feuilleté, Low-E, trempable, double vitrage).
4. « Verre pour miroiteries » (miroirs, laqués, extra-clair, panachage).
5. « Verre pour transformateurs et trempeurs » (float en plateaux jumbo, conteneur complet).
**Attention.** Chaque fait (épaisseurs, délais, certifications) doit venir de vous ou d'une fiche existante. Les zones « à confirmer » sont signalées dans les textes.

## 7. Une seule navigation, un seul message
Menu cible, identique sur toutes les pages :
`Produits ▾` (float, feuilleté, trempé, miroirs, Low-E et contrôle solaire, double vitrage, tous les produits) · `Votre métier ▾` (transformateurs, miroiteries, menuiseries et façades, serres) · `Livraison` (France et Belgique, Export) · `À propos` · `Guides` · **`Demander un prix`**
Retirer « tous les verres industriels au prix le plus bas du marché » de l'en-tête Tombuild.

## 8. Alléger les pages
- Sortir le gros bloc HTML, CSS et JS intégré à chaque page Elementor (environ 580 Ko sur l'accueil) vers un fichier CSS et un fichier JS communs, mis en cache.
- Activer dans SiteGround Speed Optimizer la minification et le report du JS, le lazy-load et la conversion WebP ; supprimer l'extension en double (WP-Optimize et Speed Optimizer font la même chose ; garder Speed Optimizer, qui est l'outil de l'hébergeur).
- Objectif : HTML de moins de 150 Ko, LCP mobile sous 2,5 s, à vérifier dans la Search Console.

## 9. Netlinking : premiers liens gratuits et pertinents
Le détail et les messages sont dans `06-netlinking.md`. Premières actions, sans coût connu :
1. UDTVP : vérifier que le logo Noxem pointe vers le site.
2. Europages : compléter la fiche existante.
3. Lyon Entreprises : proposer une suite à l'article déjà publié.
4. Windoorexpert : article d'expert gratuit.
5. Glassonweb : fiche annuaire de base.
**Rien ne sera envoyé sans votre accord.**

## 10. Nettoyage technique, et site GitHub Pages
- Corriger les H1 manquants ou multiples, les liens vers des URL qui redirigent et les liens en `http://` (liste dans `02-audit.md`, tableau M).
- Passer en noindex les archives `uncategorized`, `non-classe-en`, `eng` et `/blog-grid/` ; choisir une seule page blog (`/actualites/` ou `/blog/`).
- **Site GitHub Pages** (`dgjmfrbv4k-lab.github.io/NOXEM-GROUP/`, ce dépôt) : il est indexable, se présente comme « NOXEM GROUP FRANCE… Manufacturer & Exporter » de panneaux composites aluminium, et il contient aussi une page déstockage de verre et un site PIWA. Cela brouille la marque et contredit le positionnement de fournisseur non fabricant. Trois options : (a) le passer en `noindex` si c'est un essai ; (b) le déplacer sur un sous-domaine dédié s'il s'agit d'une vraie activité distincte, avec un vocabulaire juste (« fabricant » seulement si c'est exact) ; (c) le supprimer. **À décider.**
