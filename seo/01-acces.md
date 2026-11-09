# Accès : ce qui est disponible et ce qui manque

État au 9 novembre 2026.

| Outil | État | Ce que je peux faire | Ce qu'il faut faire |
|---|---|---|---|
| **WordPress noxemgroup.com** (via Jetpack et le connecteur WordPress.com) | ✅ Connecté | Lire et modifier les pages et articles, les menus, les réglages ; lire les extensions et les statistiques Jetpack | Rien. **Limites** : (1) les fiches produits françaises `/service/...` (type « service » du thème) ne sont pas exposées ; (2) les champs Yoast (titre SEO, méta-description, noindex) ne sont pas modifiables par l'API. |
| **Site public** (crawl) | ✅ Ouvert | Crawler les pages, lire les balises, robots.txt, sitemaps, liens | Rien. L'environnement « NOXEM-GROUP » autorise noxemgroup.com. |
| **Statistiques Jetpack** | ✅ Lisibles | Vues, pays, pages vues, référents | Rien. Jetpack ne donne **pas** les requêtes Google : la ligne « termes de recherche » est vide. |
| **Google Search Console** | ❌ Non accessible | — | Voir la procédure A ci-dessous. **C'est l'accès le plus important.** |
| **Google Analytics 4 / Tag Manager** | ❌ Non accessible | — | Voir la procédure B. GTM-58BX5677 est présent sur toutes les pages ; on ne sait pas si une balise GA4 et des conversions y sont configurées. |
| **Bing Webmaster Tools** | ❌ Non vérifié | — | Champ de vérification Bing vide dans les réglages. Importer la propriété depuis la Search Console (2 minutes). |
| **Outil de backlinks** (Ahrefs, Semrush, Majestic) | ❌ Aucun | — | Pas indispensable au départ : l'export « Liens » de la Search Console suffit. Ahrefs Webmaster Tools est gratuit pour son propre site vérifié. |
| **PageSpeed / Core Web Vitals** | ⚠️ Bloqué | — | L'API publique répond « quota dépassé ». Lire le rapport « Signaux Web essentiels » dans la Search Console, ou me fournir une clé API Google gratuite. |
| **Gmail** | Connecteur présent | — | **Je ne l'utiliserai pas** pour des prises de contact sans votre accord explicite, campagne par campagne. |
| **Google Drive** | Connecteur présent | Pourrait recevoir les exports et le tableau de suivi | Dites-moi si vous voulez le suivi dans un Google Sheet. |

## Procédure A : donner accès à la Search Console

Il n'existe pas aujourd'hui de connecteur Search Console dans cette session. Deux possibilités, de la plus simple à la plus complète :

**Option 1 : exports manuels (5 minutes par mois).** Dans la Search Console, propriété `noxemgroup.com` :
1. **Performances** → onglet « Requêtes » → période « 3 derniers mois » → cocher Clics, Impressions, CTR, Position → **Exporter** → CSV. Refaire l'export avec l'onglet « Pages », puis avec l'onglet « Pays ».
2. **Indexation → Pages** → **Exporter**. On y voit les pages indexées, exclues et pourquoi.
3. **Liens** → **Exporter les liens externes** (« Plus d'infos » → Exporter).
4. Déposer les fichiers dans `seo/data/` (ou dans un dossier Google Drive que vous me désignez).

**Option 2 : accès direct.** Ajouter un utilisateur en « Accès complet » dans Paramètres → Utilisateurs et autorisations, sur un compte Google que je pourrai lire via un futur connecteur. À n'activer que si un connecteur Search Console est ajouté à vos sessions Claude.

**Si la propriété n'existe pas encore** : WordPress → Site Kit → Connecter le service → Search Console. Site Kit vérifie automatiquement le domaine. Puis soumettre `https://noxemgroup.com/sitemap_index.xml` dans Sitemaps.

## Procédure B : mesurer les demandes de devis (indispensable pour piloter)

Objectif : savoir combien de demandes de devis viennent de Google (SEO), et depuis quelles pages.

1. **Vérifier que GA4 reçoit des données** : WordPress → Site Kit → Analytics. Si GA4 n'est pas connecté, le connecter depuis Site Kit.
2. **Créer les événements de conversion** dans GTM (GTM-58BX5677) :
   - `generate_lead_form` : envoi réussi d'un formulaire de devis (Contact Form 7 émet l'événement JavaScript `wpcf7mailsent` ; formulaires Jetpack : page de remerciement) ;
   - `click_whatsapp` : clic sur un lien `wa.me/33686131271` ;
   - `click_phone` : clic sur `tel:` ;
   - `click_email` : clic sur `mailto:` ;
   - `download_catalogue` : clic sur `NOXEM-GROUP-Catalogue-2026-*.pdf`.
3. Dans GA4 → Administration → Événements clés : marquer ces événements comme **événements clés**.
4. **Rapport mensuel** : événements clés par « Groupe de canaux par défaut = Recherche organique » et par page de destination.
5. **Côté commercial** (le plus fiable) : ajouter au formulaire de devis un champ caché « page d'origine », et noter dans votre CRM ou votre tableau de devis la source de chaque demande (Google, WhatsApp, salon, recommandation). Le tableau `suivi-seo.csv` a une ligne prévue pour reporter ces chiffres.

Je peux préparer la configuration GTM exacte (déclencheurs et balises) dès que vous me dites quel formulaire est réellement utilisé pour les devis : Contact Form 7, Jetpack ou le formulaire intégré à la page d'accueil.

## Point d'attention sécurité (hors SEO, mais trouvé pendant l'audit)
- Le réglage WordPress **« Tout le monde peut s'inscrire »** est activé (rôle par défaut : abonné). Sur un site vitrine, cela ouvre la porte aux comptes spam. Recommandation : le désactiver (Réglages → Général). Je ne l'ai pas modifié sans votre accord.
- 17 extensions ont une mise à jour en attente (dont Yoast, Elementor, Jetpack et les extensions de sécurité). À faire après une sauvegarde.
