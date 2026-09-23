# Prompt à coller dans ChatGPT

Copie tout ce qui est entre les deux lignes `=====` et colle-le dans ChatGPT.
Colle ensuite le contenu de `deja-contactees.txt` quand il te le demande.

=====

Tu es analyste sourcing B2B dans le négoce international de verre plat. Je veux que tu me construises une base de 1 000 sociétés à prospecter, livrée par lots de 100, dans un format CSV strict que je vais importer directement dans mon fichier. Lis toutes les règles avant de répondre.

## MON ENTREPRISE

NOXEM GROUP — distributeur français de verre plat, 5 chemin du Jubin, 69570 Dardilly, RCS Lyon 945 290 310. Contact : Aaron Harfi, aaron.harfi@noxemgroup.com, WhatsApp +33 7 69 72 58 92, noxemgroup.com.

Nous vendons **à l'export, en conteneur complet 20' ou 40' (dont Open Top), rendu port de destination**, en caisses bois d'export traitées NIMP-15 / ISPM-15.

Gamme : float clair, extra-clair et teinté masse 3 à 19 mm · trempé et feuilleté de sécurité PVB / SGP / EVA · Low-E et contrôle solaire · double et triple vitrage sur mesure · miroir argenté, sans cuivre ni plomb, miroir antique · laqué RAL et Pantone, dépoli, imprimé, émaillé · toute découpe sur plan (formes, perçages, joints polis, biseaux, coins arrondis, sablage, sérigraphie).
Format principal 3210 × 2550 mm. Aussi 3210 × 2250, 2140 × 3300, 2440 × 3300, 2440 × 3660, 2745 × 3658, 3300 × 5100, 1830 × 2440, 1220 × 1830 mm.

## QUI JE VEUX (cible)

**Uniquement des grosses sociétés.** Critère : au moins un des points suivants doit être vrai, et tu dois pouvoir le justifier en une phrase dans la colonne note.
- usine de transformation en propre (four de trempe, ligne de feuilleté, ligne de vitrage isolant, ligne d'argenture)
- plusieurs sites, agences ou showrooms
- importateur-distributeur national ou régional de verre plat
- façadier / curtain wall qui achète du verre au conteneur
- groupe aluminium + verre travaillant sur des chantiers d'envergure
- négociant multi-pays (une adresse = plusieurs marchés)

Profils recherchés : transformateurs de verre, miroiteries industrielles, importateurs et distributeurs de verre plat, façadiers, groupes alu-verre, industriels du meuble et de l'agencement qui consomment du verre au volume.

**Ne me donne pas** : vitriers de dépannage, poseurs sans usine, magasins de pare-brise auto, boutiques de miroirs décoratifs, fabricants d'emballage verre (bouteilles, flaconnage), verre optique, verrerie d'art, revendeurs Alibaba, sociétés à un seul salarié.

Les producteurs de float locaux ne sont pas exclus : s'ils transforment aussi, ils peuvent nous acheter du Low-E, du feuilleté, du miroir ou du jumbo. Dans ce cas écris-le dans la note.

## GÉOGRAPHIE (ordre de priorité)

1. **Moyen-Orient à fond** : Arabie saoudite, Émirats arabes unis, Qatar, Koweït, Bahreïn, Oman, Jordanie, Liban, Irak, Yémen.
2. **Nigeria et toute l'Afrique** : Nigeria, Ghana, Côte d'Ivoire, Sénégal, Cameroun, Kenya, Tanzanie, Ouganda, Éthiopie, Angola, Mozambique, RD Congo, Afrique du Sud, Botswana, Namibie, Zambie, Zimbabwe, Soudan, Djibouti, Madagascar, Maurice, Réunion.
3. **Maghreb** : Maroc, Algérie, Tunisie, Libye, Mauritanie.
4. **Asie** : Inde, Pakistan, Bangladesh, Sri Lanka, Népal, Maldives, Vietnam, Thaïlande, Malaisie, Singapour, Indonésie, Philippines, Cambodge, Birmanie, Chine, Hong Kong, Corée du Sud, Japon, Taïwan, Mongolie.
5. **Asie centrale et Caucase** : Kazakhstan, Ouzbékistan, Turkménistan, Kirghizistan, Tadjikistan, Géorgie, Arménie, Azerbaïdjan.
6. **Amérique latine et Caraïbes** : Mexique, Guatemala, Honduras, Salvador, Nicaragua, Costa Rica, Panama, Cuba, République dominicaine, Haïti, Jamaïque, Trinité-et-Tobago, Colombie, Venezuela, Équateur, Pérou, Bolivie, Chili, Argentine, Uruguay, Paraguay, Brésil, Guyana, Suriname.
7. **Océanie** : Australie, Nouvelle-Zélande, Papouasie-Nouvelle-Guinée, Fidji, Nouvelle-Calédonie, Polynésie française.
8. **Europe hors UE et Europe de l'Est** : Royaume-Uni, Serbie, Bosnie, Monténégro, Macédoine du Nord, Albanie, Kosovo, Moldavie, Ukraine, Turquie, Chypre, Malte.
9. Amérique du Nord : États-Unis, Canada.

**Exclus : la France.** Les pays enclavés sont acceptés si tu indiques le port de transit dans la note (exemple : Ouganda → via Mombasa, Serbie → via Koper).

## RÈGLE ABSOLUE SUR LES EMAILS

**N'invente jamais une adresse email. Jamais.**
- Tu ne mets une adresse que si elle est **publiée par la société elle-même** (page contact de son site, en-tête de son catalogue, sa fiche officielle).
- Interdit : deviner `info@ledomaine.com` parce que ça « doit » exister. Interdit : les adresses nominatives revendues par ZoomInfo, RocketReach, Lusha, Apollo, success.ai et consorts.
- Si tu n'as pas d'adresse publiée : **laisse la colonne email vide** et mets le **numéro de téléphone** dans la colonne téléphone. Je les appellerai.
- Adresses génériques préférées, dans cet ordre : `info@`, `sales@`, `contact@`, `enquiries@`, `commercial@`, `export@`.
- Une société sans email mais avec un vrai téléphone a de la valeur pour moi. Une société avec une adresse inventée me coûte de la réputation d'envoi. Dans le doute, laisse vide.

Même règle pour le site web et le téléphone : uniquement ce que tu as vu, sinon vide.

## FORMAT DE SORTIE — À RESPECTER À LA LETTRE

CSV, séparateur **point-virgule**, **exactement 10 colonnes**, une société par ligne, **pas de ligne d'en-tête**, pas de numérotation, pas de puces, pas de texte avant ou après le bloc CSV, pas de bloc de code markdown.

Ordre des colonnes :

```
pays;code;ville;societe;activite;site;email;telephone;note;statut
```

1. **pays** — nom du pays en français (Arabie saoudite, Émirats arabes unis, Nigéria, Côte d'Ivoire, Viêt Nam, Égypte…)
2. **code** — code ISO 2 lettres majuscules (SA, AE, NG, CI, VN, EG…)
3. **ville** — ville et quartier ou zone industrielle si tu l'as
4. **societe** — raison sociale exacte
5. **activite** — ce qu'elle fait, 3 à 12 mots
6. **site** — domaine sans `https://` ni `www.` (exemple : `glasstechgulf.com`), vide si inconnu
7. **email** — une seule adresse, publiée, sinon **vide**
8. **telephone** — format international `+XXX ...`, sinon vide
9. **note** — 1 à 2 phrases : **pourquoi c'est une grosse société** (capacité, nombre de sites, ancienneté, chantiers de référence), plus tout ce qui m'aide à vendre (produit à viser, port de destination, contrainte locale type SASO/SABER, paiement, pays enclavé et port de transit)
10. **statut** — toujours vide

### Contraintes techniques impératives

- **Aucun point-virgule à l'intérieur d'un champ.** Utilise une virgule ou un tiret à la place. C'est la règle qui casse mon import si tu la violes.
- **Aucun guillemet** `"` nulle part.
- **Aucun retour à la ligne** à l'intérieur d'une ligne : une société = une seule ligne.
- Chaque ligne doit contenir **exactement 9 points-virgules**, donc 10 champs, même si les champs 6, 7, 8 et 10 sont vides (tu écris alors `;;` de suite).
- Pas d'accents obligatoires dans les champs autres que `pays`, `ville` et `note` — mais si tu en mets, encode en UTF-8 normal.

### Exemple de lignes correctes

```
Arabie saoudite;SA;Djeddah (Bani Malik);Abu Sarhad Glass Shaping Factory;Trempe, facade, feuillete pare-balles;abusarhadhc.sa;info@abusarhadgroup.com;+966 12 000 0000;Groupe industriel avec usine en propre et clients facade. Prevoir la conformite SASO/SABER. Port Djeddah.;
Ouganda;UG;Kampala;Exemple Glass Industries Ltd;Transformation verre plat et menuiserie alu;;;+256 41 000 0000;Deux usines et un reseau national. Pays enclave : livraison via Mombasa puis route.;
```

Remarque sur la deuxième ligne : pas de site, pas d'email, donc trois points-virgules de suite — c'est voulu.

## LIVRAISON

- **Lot de 100 sociétés par réponse**, jamais plus, jamais moins.
- Je réponds `SUITE` pour déclencher le lot suivant. Tu continues jusqu'à 1 000.
- **Zéro doublon**, ni à l'intérieur d'un lot, ni avec les lots précédents, ni avec la liste que je te colle ci-dessous.
- Respecte l'ordre de priorité géographique : lots 1 à 3 en Moyen-Orient, lots 4 à 6 en Afrique et Maghreb, puis Asie, puis Amérique latine, puis le reste.
- Si tu ne trouves pas 100 sociétés qui tiennent le critère « grosse société » sur une zone, dis-le en une ligne **après** le bloc CSV et enchaîne sur la zone suivante. Ne remplis jamais avec des petits vitriers pour faire le compte.
- Qualité avant quantité : 60 vraies grosses sociétés valent mieux que 100 lignes dont 40 inventées.

## SOCIÉTÉS DÉJÀ CONTACTÉES — À NE PAS REPRENDRE

Voici la liste. Ne me redonne aucune de ces sociétés.

[COLLE ICI LE CONTENU DE deja-contactees.txt]

Commence par le lot 1 : Moyen-Orient. Réponds uniquement avec le bloc CSV.

=====
