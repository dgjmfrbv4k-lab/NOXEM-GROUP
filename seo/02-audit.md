# Audit SEO de noxemgroup.com, 9 novembre 2026

**Méthode.** Inventaire du WordPress via le connecteur Jetpack, puis crawl des 309 URL listées dans les sitemaps Yoast et contrôle de 369 liens internes supplémentaires. Chaque ligne du crawl est dans `data/crawl-2026-11-09.csv`.

**Ce qui n'a pas pu être mesuré** : l'indexation réelle et les requêtes Google (pas d'accès à la Search Console), les Core Web Vitals (API PageSpeed refusée) et les backlinks (aucun outil connecté). Les temps de réponse indiqués ont été mesurés depuis un serveur cloud, à travers un proxy : ils servent à comparer les pages entre elles, pas à donner une valeur absolue.

---

## 1. Situation de départ

| Indicateur | Valeur mesurée | Source |
|---|---|---|
| Vues sur 30 jours | **212** (136 sur 7 jours) | Jetpack |
| Visites venant des moteurs de recherche sur 90 jours | **70** | Jetpack, référents |
| Premier pays | France, 51 vues sur 90 jours ; tous les autres sont sous 15 | Jetpack |
| Pages les plus vues sur 90 jours | Accueil (48), Catalog EN (25), Produits (18), Home EN (10), Float glass EN (10), Contact (7) | Jetpack |
| URL dans les sitemaps | 309 : 151 articles, 135 pages, 18 fiches produits, 5 catégories | Sitemaps Yoast |
| Contenus publiés entre le 2 et le 4 novembre 2026 | Environ 100 articles et 60 pages | API WordPress |

**Lecture.** L'audience est encore très faible. Le site a grossi très vite en volume (langues, actualités) alors que les pages qui vendent (produits, France, métiers clients) sont faibles. Il n'y a pas encore de trafic à protéger : on peut restructurer sans risque.

---

## 2. Ce qui est déjà correct

- HTTPS actif ; `www` redirige en 301 vers `noxemgroup.com` ; `/sitemap.xml` redirige vers `sitemap_index.xml`.
- `robots.txt` propre : il n'interdit rien d'important et déclare le sitemap.
- Les 309 URL des sitemaps répondent en 200. Aucune n'est en noindex, et toutes ont une balise canonique qui pointe vers elles-mêmes.
- Une seule balise H1 sur 298 des 309 pages.
- Données structurées Yoast présentes : WebSite, WebPage, BreadcrumbList, Article. Organization n'apparaît que sur 32 pages.
- La vraie page 404 renvoie bien un code 404.
- Le titre et la description de l'accueil sont bons : « Fournisseur de verre plat en conteneur, prix usine | Noxem Group ».

---

## 3. Problèmes, classés par gravité

### 🔴 Critique

**C1. Trois pages clés sont des copies de la page d'accueil.**
`/produits/`, `/qui-sommes-nous/` et `/contact/` affichent le **même H1** que l'accueil (« Votre verre plat en direct usine, à prix extrêmement compétitifs. ») et un contenu **similaire à 96 %** à celui de l'accueil (mesure par comparaison de texte). Seuls le titre et la description diffèrent. Google les traitera comme du contenu dupliqué, et aucune ne pourra se positionner sur sa propre intention (« catalogue verre plat », « importateur de verre plat », « devis verre plat »).

**C2. Les fiches produits ne sont pas reliées au reste du site.**
Les 18 fiches françaises (`/service/verre-float/`, `/service/verre-feuillete/`, etc.) ne reçoivent que **17 liens internes, qui viennent toutes des autres fiches** (menu latéral). L'accueil, la page Produits, les articles et la navigation du nouveau gabarit ne pointent vers aucune d'elles : les liens « Produits » de l'accueil sont des ancres `#produits`. `/service/verre-trempe/` ne reçoit **aucun** lien depuis les pages des sitemaps.
Ce sont pourtant les pages qui devraient porter les recherches à intention d'achat (« fournisseur verre feuilleté », « verre float 4 mm en gros », etc.).

**C3. Les fiches produits françaises n'ont ni titre SEO travaillé ni méta-description.**
Les 18 fiches portent un titre générique (« Verre float - Noxem Group ») et **aucune méta-description**. Leurs équivalentes anglaises (`/en/float-glass/`) en ont une. Les titres et descriptions prêts à coller sont dans `04-meta-produits.csv`.

**C4. Les coordonnées ne sont pas les mêmes d'une page à l'autre (nom, adresse, téléphone).**
- Téléphone **02 59 50 84 59** sur l'accueil, la page Contact et la méta-description de Contact.
- Téléphone **04 22 91 55 80** dans l'en-tête de l'ancien gabarit (fiches produits, blog).
- Mobile et WhatsApp 06 86 13 12 71.
- Lien e-mail `mailto:aaronharfi@noxem-group.com` sur l'accueil et les pages du nouveau gabarit. Le domaine **noxem-group.com** (avec un tiret) n'est pas celui du site, alors que l'adresse d'administration est `aaron.harfi@noxemgroup.com`. **À vérifier tout de suite** : si cette adresse ne reçoit pas les messages, des demandes de devis sont perdues.
- Europages indique Dardilly (69).
Des coordonnées incohérentes affaiblissent la confiance des acheteurs et des moteurs. Il faut choisir un seul numéro principal et l'appliquer partout.

### 🟠 Important

**I1. Le multilingue est fait de deux systèmes qui se marchent dessus.**
- **Polylang** gère le français et l'anglais : `/en/float-glass/`, `/en/home/`, etc.
- **24 pages de langue construites à la main** (`/es/`, `/de/`, `/zh/`, `/sw/`, `/ha/`, `/am/`, etc.) déclarent `<html lang="fr-FR">` alors qu'elles sont en allemand, en chinois ou en arabe.
- Le hreflang de l'accueil liste ces 24 pages, mais **ni le français (`fr`) ni l'anglais Polylang**.
- Les fiches FR et EN ne sont pas reliées entre elles par hreflang (0 sur les fiches produits).
- Les 151 articles n'ont **aucun hreflang**. Les versions anglaise et arabe d'un même article sont publiées comme articles français (`lang="fr-FR"`).
Résultat : Google ne sait ni quelle version servir à quel pays, ni que les versions se correspondent.

**I2. Un gros volume de contenu à faible valeur commerciale, produit en masse.**
- Environ 100 articles publiés entre le 2 et le 4 novembre 2026, chacun en FR, EN et AR. Beaucoup portent sur l'actualité géopolitique ou économique (Ormuz, pétrole, gaz, Ukraine, Koweït) ; trois articles différents traitent de glasstec 2026 et trois de Big 5 Dubai.
- 26 versions linguistiques de « Nos réalisations », 26 de « Export en conteneur », 10 de « Stock en Belgique », dont plusieurs annoncent un stock **vendu**.
Google sanctionne le contenu produit en masse sans valeur propre (« scaled content abuse »). Ces articles d'actualité vieilliront vite, et leurs affirmations factuelles (attaques à Ormuz, prix du gaz) engagent la crédibilité de l'entreprise si elles sont inexactes. Ils n'attirent pas les acheteurs français ciblés.

**I3. Les pages sont très lourdes.**
Le HTML pèse en moyenne **433 Ko** par page, jusqu'à **1 Mo** pour l'accueil et les pages de langue (la norme se situe entre 50 et 150 Ko). La cause : un très gros bloc HTML, CSS et JavaScript intégré à chaque page Elementor (environ 580 Ko de contenu sur l'accueil), 61 scripts et 14 feuilles de style sur l'accueil. La page 404 pèse 404 Ko. Sur mobile et en 4G dans les pays visés (Maghreb, Afrique), le chargement sera lent. Le temps de réponse moyen mesuré est de 1,7 s.

**I4. Deux gabarits et deux navigations coexistent.**
L'ancien gabarit Tombuild (menu Accueil, À propos, Catalogue, Logistique, Sous-traitance, Actualités, slogan « tous les verres industriels au prix le plus bas du marché ») et le nouveau gabarit Elementor (menu Actualités, Livraison monde, Partenaires, Déstockage) n'ont ni les mêmes menus, ni le même téléphone, ni le même message. Les pages de chaque gabarit se lient très peu à celles de l'autre.

**I5. Les pages commerciales destinées au marché français manquent.**
Rien ne cible spécifiquement les **métiers clients** (transformateurs, miroiteries, fabricants de menuiseries, façadiers, serristes), ni une offre **France** (livraison en France, stock en Belgique, délai). La méta-description de l'accueil vise « importateurs et distributeurs… conteneur 20′ livrés CIF dans plus de 50 ports », c'est-à-dire l'export. Il n'y a **aucune page serres**.

### 🟡 À corriger, impact moindre

| # | Problème | Pages |
|---|---|---|
| M1 | H1 absent | `/conteneur/`, `/destockage/` (pages de moins de 300 mots, sans description) |
| M2 | Plusieurs H1 (titre du thème plus titre Elementor) | `/sous-traitance/`, `/logistique/`, `/en/logistics/`, `/en/outsourcing/`, `/galerie-logistique/`, `/en/catalog/`, `/service/catalogue/`, pages légales |
| M3 | Méta-description absente | 25 URL, dont les 18 fiches produits, `/conteneur/`, `/destockage/`, les catégories |
| M4 | Titre de plus de 65 caractères (coupé dans Google) | 107 URL, surtout des articles |
| M5 | Titres et descriptions en double | 3 paires d'articles FR et EN anciens (« Top 5 : choisir un fournisseur… », « Verre feuilleté ou trempé… », « Pourquoi choisir un négociant… ») |
| M6 | Liens internes vers des URL qui redirigent | `/en/` → `/en/home/` ; `/service/strengthening-practices/` → `/service/verre-trempe/` ; `/contact` et `/presse` sans « / » final ; `http://noxemgroup.com` (non sécurisé) depuis 33 pages |
| M7 | Page sans aucun lien interne entrant | `/qui-sommes-nous/`, `/edito/`, `/galerie-logistique/`, `/blog/`, `/destockage/`, `/service/verre-trempe/`, 5 catégories |
| M8 | Pages d'archives inutiles indexées | `/category/uncategorized/`, `/en/category/non-classe-en/`, `/en/category/eng/`, `/blog-grid/`, `/blog/` (en double avec `/actualites/`) |
| M9 | Images sans texte alternatif | 51 sur 2 115 |
| M10 | Page « Déstockage Mollem » contradictoire | Titre « Stock vendu », H1 « 8 230 m² de verre plat à reprendre », alors qu'elle reçoit des liens de 192 pages |
| M11 | Page vide « Avis clients » | ✅ **Corrigé** : passée en brouillon le 9 novembre 2026 |
| M12 | Inscription WordPress ouverte | Voir `01-acces.md` |

---

## 4. Affirmations du site à confirmer avant de s'en servir dans le SEO et les relations presse

Ces affirmations sont publiées aujourd'hui. Je ne les ai ni créées ni vérifiées. Ce sont des engagements commerciaux ou réglementaires, et chacune doit être exacte :

| Affirmation | Où |
|---|---|
| « Paiement 30 ou 60 jours après livraison, partout dans le monde et sans minimum, sous réserve d'acceptation » | Article dédié en 3 langues |
| « Direct usine », « prix usine sans intermédiaire » | Accueil, titre de l'accueil |
| « Certifié CE, certificats fournis avec chaque commande » | Accueil |
| « Plus de 600 références » | Accueil, `/produits/` |
| « Réponse sous 24 h, en 12 langues » | Accueil |
| « Livraison J+3 en France et en Belgique » | Article de mars 2026, `/logistique/` |
| « Livré CIF dans plus de 50 ports » | Méta-description de l'accueil |
| « Partenaire de la FFPV », « équipe formée par la FFPV » | `/partenaires/`, pied de page. La page partenaires publique de la FFPV, consultée via un outil de recherche, ne cite pas Noxem. Côté UDTVP, un logo Noxem semble présent. |
| « Le prix le plus bas du marché » | En-tête de l'ancien gabarit. Superlatif impossible à prouver : à retirer. |

Le texte de l'accueil présente bien NOXEM comme « importateur & négociant », ce qui est cohérent avec le positionnement de fournisseur direct. En revanche, « en direct usine » et « prix usine » peuvent laisser croire que vous êtes fabricant : à reformuler si nécessaire (« approvisionnement direct auprès des verriers »).

---

## 5. Concurrence (synthèse de la recherche documentaire)

Le détail est dans `data/recherche-concurrents-netlinking-2026-11-09.md`. Ce sont les résultats d'un outil de recherche, pas le classement Google exact.

- Les requêtes « fournisseur / grossiste / importateur verre plat » sont dominées par des **annuaires** (Batiproduits, Batiweb, Europages, Kompass, Archiexpo) et des **places de marché asiatiques**. Peu de négociants indépendants ont des pages commerciales qui se positionnent.
- noxemgroup.com ressort déjà sur « importateur verre plat ».
- Concurrent le plus proche en négoce multi-pays : **Glass Partners Solutions** (gps-glass.com, Anglet, France, Espagne et Portugal). Références fabricants : AGC Glass Distribution, Saint-Gobain, Şişecam. Sur les serres : Van Looveren (Belgique), Scheuten et Glascom (Pays-Bas).
- Sur « verre float en gros », l'outil n'a renvoyé aucun résultat pertinent (« float » y est compris comme « flottant ») : le terrain est libre pour une page bien ciblée.
