# Stratégie de contenu

**Principe.** Chaque page doit répondre à une recherche d'acheteur professionnel et déboucher sur une demande de prix. Pas d'article générique, pas de pages pays presque identiques.

**Volumes de recherche : non mesurés.** Aucun outil de mots-clés n'est connecté. Les requêtes ci-dessous sont classées par intention d'achat et par cohérence avec votre offre. Leurs volumes sont à mesurer dès que la Search Console est branchée (impressions réelles), ou via Google Keyword Planner avec votre compte Google Ads.

Convention : **[À CONFIRMER]** marque une information que je ne peux pas affirmer à votre place.

---

## A. Recherches visées (France d'abord)

| Groupe | Exemples de requêtes | Intention | Page cible |
|---|---|---|---|
| Fournisseur générique | fournisseur verre plat, grossiste verre plat, négociant verre plat, importateur verre plat, achat verre en gros professionnel | Achat | Accueil + page « Fournisseur de verre plat en France » (C1) |
| Produit et volume | verre float en gros, verre float 4 mm plateau, verre extra-clair fournisseur, verre feuilleté 44.2 fournisseur, plateau verre 3210 × 2550, miroir argenté en plateau, verre Low-E fournisseur | Achat | Fiches `/service/...` (voir `04-meta-produits.csv`) |
| Logistique et volume | conteneur verre plat, achat verre conteneur, combien de m² de verre dans un conteneur, verre plat livraison France Belgique | Achat / préparation | `/conteneur/`, article « m² par conteneur », `/logistique/` |
| Métier client | verre pour menuiserie PVC alu fournisseur, verre pour fabricant de fenêtres, fournisseur verre miroiterie, verre pour façade mur-rideau fournisseur, verre serre horticole, verre trempé 4 mm serre | Achat | Pages métiers (C2 à C5) |
| Technique avant achat | 33.1 44.2 55.2 différence, PVB ou EVA, float clair ou extra-clair, Low-E ou réfléchissant, EN 12150, garde-corps verre épaisseur | Information qui précède l'achat | Articles existants, à relier aux fiches |
| Export (phase 2) | flat glass supplier container, float glass supplier Morocco / Algeria / UAE, proveedor vidrio float contenedor | Achat | `/en/` + `/livraison-monde/` + guides pays existants |

---

## B. Pages existantes à refondre (priorité 1)

### B1. `/produits/`, aujourd'hui une copie de l'accueil
- **Titre SEO** : `Verre plat en gros : float, feuilleté, trempé, miroir | Noxem Group` (64 caractères)
- **Méta-description** : `Gamme de verre plat pour professionnels : float clair et extra-clair, feuilleté, trempé, miroirs, Low-E, double vitrage. Conteneur complet ou panaché. Demandez un prix.` (155 caractères)
- **H1** : Verre plat en gros pour les professionnels
- **Structure** :
  - Introduction (2 à 3 phrases) : importateur et négociant, approvisionnement auprès de verriers, livraison en France, en Belgique et à l'export, conteneur complet ou panaché.
  - **H2 Verres de base** : cartes Float clair et extra-clair → `/service/verre-float/` ; Verre teinté → `/service/verre-colore/` ; Verre à motifs ; Verre dépoli.
  - **H2 Verres de sécurité** : Feuilleté → `/service/verre-feuillete/` ; Trempé → `/service/verre-trempe/` ; Vitrages techniques.
  - **H2 Verres à couche et isolants** : Low-E ; Réfléchissant ; Double vitrage ; Triple vitrage.
  - **H2 Miroirs et verres décoratifs** : Miroirs professionnels ; Sans cuivre ni plomb ; Antique ; Laqué ; Émaillé ou imprimé.
  - **H2 Formats, épaisseurs et normes** : tableau repris des informations publiées (format standard 3210 × 2550 mm, épaisseurs de 3 à 19 mm pour le float, normes EN 572, EN 1096, EN 12150, EN 12600, EN ISO 12543, EN 14449, EN 1279).
  - **H2 Comment commander** : conteneur complet / panaché, liste Excel acceptée → lien `/contact/`.
  - Bouton « Télécharger le catalogue 2026 » et bouton « Demander un prix ».

### B2. `/qui-sommes-nous/`
- **Titre SEO** : `Qui sommes-nous : importateur et négociant de verre plat | Noxem Group`
- **Méta-description** : conserver la description actuelle, qui est bonne.
- **H1** : Noxem Group, importateur et négociant de verre plat
- **Structure** : H2 Notre métier (fournisseur direct, non fabricant : nous sélectionnons les verriers et organisons l'achat et le transport) · H2 Notre organisation (rattachement à MONTAUGEM, logistique de Mollem en Belgique) · H2 Pour qui nous travaillons (les 5 métiers, avec un lien vers chaque page métier) · H2 Nos engagements (uniquement ceux que vous confirmez : délai de réponse, contrôle avant départ, photos de chargement) · H2 Le mot du dirigeant (reprendre `/edito/`, aujourd'hui sans lien entrant) · H2 Partenaires de la filière (UDTVP ; FFPV **[À CONFIRMER]**).
- Photos réelles : entrepôt de Mollem, chargements (déjà publiées dans `/nos-realisations/`).

### B3. `/contact/`
- **Titre SEO** : conserver « Contact et demande de prix | Noxem Group ».
- **H1** : Demander un prix de verre plat
- **Contenu** : formulaire de devis en premier (produits, épaisseurs, quantités ou nombre de conteneurs, lieu de livraison, pièce jointe Excel) ; ensuite **un seul** téléphone principal, WhatsApp, `contact@noxemgroup.com`, l'adresse du siège (identique aux mentions légales), les horaires ; puis une FAQ courte de 4 questions (« Vendez-vous aux particuliers ? Non, uniquement aux professionnels. », « Quel volume minimum ? » **[À CONFIRMER]**, « Livrez-vous en France ? », « Quels documents fournissez-vous ? » **[À CONFIRMER]**).
- Mention claire : **« Réservé aux professionnels »**. Elle filtre les demandes de particuliers.

---

## C. Pages à créer

### C1. Fournisseur de verre plat en France ✅ rédigée (texte complet ci-dessous)
### C2. Verre pour serres professionnelles ✅ rédigée (texte complet ci-dessous)
### C3. Verre pour fabricants de menuiseries et façadiers
`/verre-menuiseries-facades/`. H1 « Verre pour fabricants de menuiseries et façadiers ». H2 : feuilleté et sécurité (33.1, 44.2, 44.6) · Low-E et contrôle solaire · trempable et trempé · double vitrage sur plan · conditionnement en plateaux et livraison · demander un prix. Liens vers les fiches et les articles « murs-rideaux » et « 6/10/44.2 argon ».
### C4. Verre pour miroiteries
`/verre-miroiteries/`. H2 : miroirs (argenté, sans cuivre ni plomb, antique) · laqués et dépolis · extra-clair · panachage de références dans un même camion · demander un prix.
### C5. Verre pour transformateurs et trempeurs
`/verre-transformateurs/`. H2 : float clair et extra-clair en plateaux jumbo · feuilleté pour découpe · verre trempable · conteneur complet au meilleur coût · régularité des approvisionnements · demander un prix.

Pour C3 à C5, la structure est fixée. Je rédige chaque texte complet après validation de C1 et C2, pour reprendre vos corrections.

---

### Texte complet : C1. Fournisseur de verre plat en France

- **URL** : `/fournisseur-verre-plat-france/`
- **Titre SEO** : `Fournisseur de verre plat en France pour professionnels | Noxem Group` (64 caractères)
- **Méta-description** : `Fournisseur direct de verre plat pour transformateurs, miroiteries, menuisiers et façadiers : float, feuilleté, miroir, Low-E. Conteneur complet ou panaché, livraison France.` (159 caractères)

> # Fournisseur de verre plat en France pour les professionnels du verre
>
> Noxem Group est un importateur et négociant de verre plat. Nous achetons auprès de verriers sélectionnés et nous livrons les professionnels en France et en Belgique : en conteneur complet pour les gros volumes, ou en livraison panachée quand vous avez besoin de plusieurs références sans remplir un conteneur.
>
> Nous ne vendons pas aux particuliers : nos clients sont des transformateurs, des miroiteries, des fabricants de menuiseries, des façadiers et des constructeurs de serres.
>
> ## Ce que nous livrons
> - **Verre float** clair, extra-clair et teinté, en plateaux → [Verre float](/service/verre-float/)
> - **Verre feuilleté** de sécurité → [Verre feuilleté](/service/verre-feuillete/)
> - **Verre trempé** et vitrages transformés sur plan → [Verre trempé](/service/verre-trempe/)
> - **Miroirs** et verres décoratifs → [Miroirs professionnels](/service/miroirs-professionnels/)
> - **Verres à couche** Low-E et contrôle solaire → [Verre Low-E](/service/verre-a-faible-emissivite/)
>
> Voir [toute la gamme](/produits/) ou [télécharger le catalogue 2026](/service/catalogue/).
>
> ## Deux façons d'acheter
> ### Conteneur complet
> Pour les transformateurs, négociants et stockistes qui achètent en volume : un conteneur d'une ou plusieurs références, en caisses bois, livré sur votre site. Pour estimer la quantité, voir [combien de m² de verre dans un conteneur 20 et 40 pieds](/combien-m2-verre-conteneur-20-40-pieds/).
> ### Livraison panachée
> Pour les miroiteries et les petits et moyens transformateurs : plusieurs références et épaisseurs dans un même transport.
>
> ## Une logistique en Belgique, à proximité du marché français
> Notre plateforme de Mollem (Belgique) reçoit, stocke et réexpédie le verre en grand volume. [Voir notre logistique](/logistique/).
> Délai de livraison en France : **[À CONFIRMER : délai réel à annoncer, J+3 ou autre]**.
>
> ## Normes et documents
> Nos verres sont conformes aux normes européennes applicables : EN 572 (verre float), EN 12150 (verre trempé), EN ISO 12543 et EN 14449 (verre feuilleté), EN 1096 (verre à couche), EN 1279 (vitrage isolant). **[À CONFIRMER : documents remis à chaque livraison (déclaration de performance, certificats)]**
>
> ## Comment se passe une commande
> 1. Vous nous envoyez vos références, épaisseurs, quantités et lieu de livraison (une liste Excel suffit).
> 2. Nous vous adressons un devis détaillé, rendu chez vous.
> 3. La commande est confirmée par écrit, puis contrôlée et mise en caisses.
> 4. Nous vous envoyons les photos du chargement avant le départ.
> 5. Le verre est livré sur votre site.
>
> ## Questions fréquentes
> **Vendez-vous à l'unité ?** Non. Nous fournissons des professionnels, en conteneur complet ou en livraison panachée.
> **Quel est le minimum de commande ?** **[À CONFIRMER]**
> **Pouvez-vous fournir une référence absente du catalogue ?** Oui, sur demande : nous la recherchons auprès de nos verriers.
>
> **[Demander un prix →](/contact/)**

Liens internes à ajouter **vers** cette page : accueil (bloc « Notre métier »), `/produits/`, `/logistique/`, et l'article « Comment choisir un fournisseur de verre plat ».

---

### Texte complet : C2. Verre pour serres professionnelles

- **URL** : `/verre-serres-professionnelles/`
- **Titre SEO** : `Verre pour serres professionnelles en conteneur | Noxem Group` (58 caractères)
- **Méta-description** : `Verre horticole pour constructeurs de serres professionnelles : verre trempé, float extra-clair, grands volumes livrés en conteneur en France et à l'export. Demandez un prix.` (158 caractères)

> # Verre pour serres professionnelles
>
> Les constructeurs de serres achètent le verre en très grande quantité, avec des dimensions répétitives et des délais liés aux chantiers. Noxem Group, importateur et négociant de verre plat, organise ces approvisionnements en conteneur, en France et à l'export.
>
> ## Les verres utilisés en serre
> - **Verre float extra-clair** : une faible teneur en fer donne une meilleure transmission lumineuse, l'un des premiers critères en production végétale. → [Verre float](/service/verre-float/)
> - **Verre trempé** : il résiste mieux aux chocs et à la grêle ; en cas de casse, il se fragmente en petits morceaux. → [Verre trempé](/service/verre-trempe/)
> - **Verre diffusant ou traité antireflet** : il répartit mieux la lumière dans la culture. **[À CONFIRMER : le proposez-vous ?]**
> - **Verre feuilleté** pour les toitures et les zones accessibles au public (jardineries, serres de vente). → [Verre feuilleté](/service/verre-feuillete/)
>
> ## Ce que nous demandons pour établir un prix
> - type de verre et épaisseur ;
> - dimensions des vitrages et nombre de pièces (ou surface totale) ;
> - finition des bords ;
> - lieu de livraison et calendrier du chantier.
>
> ## Volumes et transport
> Le verre de serre se livre en caisses ou en pupitres adaptés au chargement en conteneur. Pour estimer le nombre de conteneurs, voir [combien de m² de verre dans un conteneur 20 et 40 pieds](/combien-m2-verre-conteneur-20-40-pieds/).
> **[À CONFIRMER : dimensions maximales, épaisseurs, conditionnement réellement proposés pour les serres]**
>
> ## Pour qui
> Constructeurs et intégrateurs de serres professionnelles (maraîchage, horticulture, recherche), serres de vente et jardineries, entreprises de rénovation de serres.
>
> **[Demander un prix pour votre projet de serre →](/contact/)**

Note : cette page ne doit être publiée qu'après confirmation des produits proposés pour les serres. C'est le préalable aux actions de presse horticole (Hortidaily, SIVAL, Le Lien Horticole).

---

## D. Extension internationale, argumentée

**Constat.** 24 langues ont déjà été mises en ligne. Pourtant, en 90 jours, les visites hors de France se comptent par unités (Trinité-et-Tobago 14, Croatie 14, Italie 12…), et aucune donnée ne relie ces langues à des demandes de devis.

**Proposition : avancer par marché validé, pas par langue.**
1. **Phase 1 (mois 1 à 3) : France et Belgique francophone.** Toute la priorité.
2. **Phase 2 (mois 3 à 6) : anglais.** Il sert de langue d'export par défaut (Golfe, Afrique anglophone, Europe du Nord). Version anglaise propre des pages commerciales via Polylang, avec hreflang.
3. **Phase 3, selon vos ventes réelles** : **arabe** (Maghreb, Golfe), puis **espagnol** (Espagne, où un concurrent comme Glass Partners Solutions est présent). Déclencheur proposé : au moins 3 demandes de devis qualifiées par trimestre venant du marché, ou un commercial dédié.
4. **Une page par marché seulement si elle apporte une information propre** : ports, documents d'importation, réglementation (par exemple, les guides Algérie PPI, Nigeria SONCAP et Côte d'Ivoire VoC déjà publiés), et pas une page clonée avec le nom du pays changé.

**Ce qu'on évite** : traduire l'actualité dans 26 langues, ou publier des pages « stock vendu » multilingues.

---

## E. Rythme éditorial proposé (après les refontes)
- **2 contenus par mois au maximum**, chacun relié à une fiche produit ou à une page métier :
  - novembre et décembre : refonte B1 à B3, publication de C1, C3 ;
  - janvier : C4, C5, C2 (si les produits pour serres sont confirmés), avant SIVAL du 12 au 14 janvier 2027 ;
  - ensuite : un guide technique par mois, selon les questions réelles de vos clients (vos commerciaux sont la meilleure source de sujets).
