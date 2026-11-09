# Pilotage SEO de NOXEM GROUP (noxemgroup.com)

Dossier de travail du référencement de noxemgroup.com. Premier bilan au 9 novembre 2026.

**Le site public n'est pas dans ce dépôt.** noxemgroup.com est un WordPress (thème Tombuild, Elementor, Yoast SEO, Polylang) hébergé chez SiteGround et relié à Jetpack. Ce dépôt GitHub publie un autre site, sur `dgjmfrbv4k-lab.github.io/NOXEM-GROUP/`, qui présente des panneaux composites aluminium. Le point 10 du fichier `03-top10-actions.md` traite de ce sujet.

## Fichiers

| Fichier | Contenu |
|---|---|
| `01-acces.md` | Accès disponibles, accès manquants, et comment les ouvrir |
| `02-audit.md` | Audit public et technique, avec les chiffres mesurés |
| `03-top10-actions.md` | Les dix actions prioritaires : impact, urgence, effort |
| `04-meta-produits.csv` | Titres et descriptions SEO à coller dans Yoast pour les 18 fiches produits |
| `05-strategie-contenu.md` | Recherches visées, pages à créer ou refondre, contenus rédigés |
| `06-netlinking.md` | Opportunités de liens, page à pousser, messages de prise de contact |
| `07-plan-90-jours.md` | Plan d'action sur 90 jours |
| `suivi-seo.csv` | Tableau de suivi : action, priorité, statut, coût, résultat attendu, résultat mesuré |
| `data/crawl-2026-11-09.csv` | Données brutes du crawl, une ligne par URL (309 URL) |
| `data/recherche-concurrents-netlinking-2026-11-09.md` | Recherche documentaire brute sur les concurrents et les liens |

## Bilan au 9 novembre 2026

### Réalisé
- Inventaire complet du WordPress via le connecteur : 138 pages, 150 articles, 22 extensions, réglages SEO, statistiques Jetpack sur 90 jours.
- Crawl des 309 URL des sitemaps Yoast, puis vérification de 369 liens internes supplémentaires.
- Une correction appliquée en ligne : la page vide « Avis clients » (`/avis-clients/`) est passée **en brouillon**. Elle ne contenait qu'un formulaire de commentaire, aucun avis, et aucune page n'y renvoyait. Pour annuler : WordPress, Pages, Avis clients, Publier.

### Préparé, en attente de votre validation
- Titres et descriptions des 18 fiches produits françaises (`04-meta-produits.csv`).
- Nouveau contenu pour `/produits/`, `/qui-sommes-nous/` et `/contact/`, qui sont aujourd'hui des copies de la page d'accueil (`05-strategie-contenu.md`).
- Page à créer « Verre pour serres professionnelles » et page « Fournisseur de verre plat en France », rédigées (`05-strategie-contenu.md`).
- 30 opportunités de liens et 4 modèles de message (`06-netlinking.md`). **Rien n'a été envoyé.**

### Bloqué
- **Search Console et Analytics** : aucune donnée lisible ici. Site Kit et Google Tag Manager (GTM-58BX5677) sont installés, mais je n'ai pas accès aux comptes Google. Voir `01-acces.md`.
- **Fiches produits françaises** (type de contenu « service ») : le connecteur WordPress ne les expose pas, et les champs Yoast ne sont pas modifiables par l'API. Il faut les coller à la main (10 minutes) ou me donner un autre accès.
- **Backlinks** : aucun outil de backlinks n'est connecté (ni Ahrefs, ni Semrush, ni Majestic). L'export « Liens » de la Search Console suffit pour commencer.
- **Performance mobile** : l'API PageSpeed publique a refusé les requêtes (quota épuisé). À relancer avec une clé, ou à lire dans la Search Console.

### À décider par vous
1. Les 24 pages de langue (`/de/`, `/zh/`, `/sw/`, etc.), les 26 versions de « Nos réalisations » et les 150 articles d'actualité publiés en trois langues en dix jours : garder, regrouper ou désindexer ? Ma recommandation figure dans `03-top10-actions.md`, action 4.
2. Les affirmations commerciales à confirmer avant qu'on s'appuie dessus : paiement à 30 ou 60 jours, « prix usine / direct usine », « certificats fournis avec chaque commande », « 600+ références », livraison J+3, « plus de 50 ports », partenariat FFPV.
3. Le budget de netlinking : des annuaires et une presse spécialisée gratuits sont prévus d'abord ; les options payantes sont listées avec un coût « à confirmer ».
4. Le sort du site GitHub Pages consacré aux panneaux composites.

## Règles de travail
- Aucune donnée inventée. Quand un volume ou un coût n'est pas connu, il est écrit « à mesurer » ou « à confirmer ».
- Aucun message externe envoyé et aucune dépense engagée sans votre accord écrit.
- Aucune automatisation n'est configurée. Je ne travaille pas en arrière-plan entre deux sessions : chaque bilan est fait quand vous relancez le travail.
