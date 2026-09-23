# Prompt à coller dans ChatGPT

Copie tout ce qui est entre les deux lignes `=====`.
Remplace le marqueur de fin par le contenu de `deja-contactees.txt`.

=====

Tu es analyste sourcing B2B. Je veux une base de 1 000 sociétés à prospecter, livrée par lots de 100, dans un format CSV strict que j'importe directement dans mon fichier. Lis toutes les règles avant de répondre.

## CE QUE JE FAIS

NOXEM GROUP, distributeur français de verre plat. Je vends **à l'export, en conteneur complet, rendu port de destination**.

## QUI JE CHERCHE

**Des clients qui achètent un conteneur entier directement au port et qui font eux-mêmes le dédouanement.** C'est le filtre central : si la société n'a pas la taille et la structure pour importer un conteneur, la dédouaner et la décharger, elle ne m'intéresse pas.

**Uniquement des grosses sociétés.** Au moins un de ces points doit être vrai, et tu le justifies en une phrase dans la colonne note :
- usine de transformation de verre en propre (trempe, feuilleté, vitrage isolant, argenture)
- plusieurs sites, agences ou showrooms
- importateur-distributeur national ou régional de verre plat
- façadier / curtain wall travaillant sur de gros chantiers
- groupe aluminium + verre d'envergure
- négociant multi-pays

**Ne me donne pas** : vitriers de dépannage, poseurs sans usine, pare-brise auto, boutiques de miroirs, emballage verre (bouteilles, flaconnage), verre optique, verrerie d'art, revendeurs Alibaba, sociétés d'une ou deux personnes, tout ce qui achète à la plaque ou à la palette.

## GÉOGRAPHIE

**Le monde entier**, toutes les grosses sociétés, partout.

Priorité de traitement :
1. Moyen-Orient et Golfe
2. Nigeria et toute l'Afrique
3. Maghreb
4. Asie du Sud et du Sud-Est
5. Amérique latine et Caraïbes
6. Asie centrale, Caucase, Océanie, Europe hors UE, Amérique du Nord

**DEUX EXCLUSIONS ABSOLUES :**
- **La Chine, Hong Kong et Macao.** C'est là que j'achète. Aucune société chinoise, jamais, sous aucun prétexte.
- **La France.**

Les pays enclavés sont acceptés : indique le port de transit dans la note (Ouganda → via Mombasa, Serbie → via Koper, Mali → via Dakar ou Abidjan).

## RÈGLE ABSOLUE SUR LES EMAILS

**N'invente jamais une adresse email. Jamais.**
- Une adresse uniquement si elle est **publiée par la société elle-même** (page contact de son site, son catalogue, sa fiche officielle).
- Interdit : deviner `info@ledomaine.com` parce que ça « doit » exister.
- Interdit : les adresses revendues par ZoomInfo, RocketReach, Lusha, Apollo, success.ai et consorts.
- Pas d'adresse publiée → **colonne email vide** + le **téléphone** dans sa colonne. Je les appellerai.
- Adresses génériques préférées, dans l'ordre : `info@`, `sales@`, `contact@`, `enquiries@`, `commercial@`, `export@`.

Une société sans email mais avec un vrai téléphone a de la valeur. Une adresse inventée me coûte ma réputation d'envoi. Dans le doute, laisse vide. Même règle pour le site et le téléphone : uniquement ce que tu as vu.

## FORMAT DE SORTIE — À LA LETTRE

CSV, séparateur **point-virgule**, **exactement 10 colonnes**, une société par ligne, **pas d'en-tête**, pas de numérotation, pas de puces, aucun texte avant ou après le bloc, pas de bloc de code markdown.

```
pays;code;ville;societe;activite;site;email;telephone;note;statut
```

1. **pays** — en français (Arabie saoudite, Émirats arabes unis, Nigéria, Côte d'Ivoire, Viêt Nam…)
2. **code** — ISO 2 lettres majuscules (SA, AE, NG, CI, VN…)
3. **ville** — ville, et quartier ou zone industrielle si tu l'as
4. **societe** — raison sociale exacte
5. **activite** — ce qu'elle fait, 3 à 12 mots
6. **site** — domaine sans `https://` ni `www.`, vide si inconnu
7. **email** — une seule adresse, publiée, sinon **vide**
8. **telephone** — format `+XXX ...`, sinon vide
9. **note** — 1 à 2 phrases : pourquoi c'est une grosse société capable d'importer un conteneur, plus ce qui m'aide à vendre (port de destination, contrainte locale type SASO/SABER, paiement, port de transit si pays enclavé)
10. **statut** — toujours vide

### Contraintes techniques impératives

- **Aucun point-virgule à l'intérieur d'un champ.** Virgule ou tiret à la place. C'est la règle qui casse mon import.
- **Aucun guillemet** `"`.
- **Aucun retour à la ligne** dans une ligne : une société = une ligne.
- **Exactement 9 points-virgules par ligne**, même quand des champs sont vides (tu écris `;;` de suite).
- UTF-8.

### Exemple de lignes correctes

```
Arabie saoudite;SA;Djeddah (Bani Malik);Abu Sarhad Glass Shaping Factory;Trempe, facade, feuillete pare-balles;abusarhadhc.sa;info@abusarhadgroup.com;+966 12 000 0000;Usine en propre et clients facade, importe au conteneur. Prevoir SASO/SABER. Port Djeddah.;
Ouganda;UG;Kampala;Exemple Glass Industries Ltd;Transformation verre plat et menuiserie alu;;;+256 41 000 0000;Deux usines et reseau national, dedouane lui-meme. Pays enclave : via Mombasa puis route.;
```

Deuxième ligne : pas de site, pas d'email, donc trois points-virgules de suite — c'est voulu.

## LIVRAISON

- **100 sociétés par réponse**, jamais plus, jamais moins.
- Je réponds `SUITE` pour le lot suivant, jusqu'à 1 000.
- **Zéro doublon** : dans le lot, avec les lots précédents, et avec la liste ci-dessous.
- Si une zone ne donne pas 100 vraies grosses sociétés, dis-le en une ligne **après** le bloc CSV et enchaîne sur la zone suivante. Ne remplis jamais avec des petits vitriers pour faire le compte.
- 60 vraies grosses sociétés valent mieux que 100 lignes dont 40 inventées.

## DÉJÀ CONTACTÉES — NE PAS REPRENDRE

[COLLE ICI LE CONTENU DE deja-contactees.txt]

Commence par le lot 1 : Moyen-Orient et Golfe. Réponds uniquement avec le bloc CSV.

=====
