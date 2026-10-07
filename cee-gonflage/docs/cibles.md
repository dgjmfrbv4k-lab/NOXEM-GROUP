# Cartographie des clients potentiels — fiche TRA-SE-104

Ce document liste **qui peut accueillir une station de gonflage valorisable en CEE**,
et surtout **qui signe** dans chaque cas. Au sens de la fiche, le « bénéficiaire »
est l'exploitant du site : c'est lui qui signe le contrat d'entretien et l'état
récapitulatif. Viser le bon interlocuteur fait plus pour le taux de réponse que
le nombre d'e-mails envoyés.

---

## Type A — 534 200 kWh cumac par station

> Autoroutes et voies de type autoroutier disposant d'aires de repos.

C'est le mieux valorisé, et le plus difficile d'accès. Deux mondes très différents :

### A.1 Réseau concédé (payant)

Autour de Lyon, trois niveaux de décision se superposent :

| Axe | Concessionnaire | Groupe |
|---|---|---|
| A6, A40, A46, A42 | APRR | Eiffage |
| A43, A48, A432 | AREA (filiale d'APRR) | Eiffage |
| A7 (Lyon – Marseille) | ASF | Vinci Autoroutes |

**Le piège à éviter :** écrire au concessionnaire. Sur une aire de service, l'exploitant
au quotidien est le **sous-concessionnaire** (pétrolier ou groupe de restauration :
TotalEnergies, Eni/Agip, Avia, Autogrill, Groupe Le Duff…). C'est lui l'exploitant du
site au sens de la fiche. Le concessionnaire, lui, doit valider toute implantation sur
son domaine : son accord est une **condition technique**, pas la porte d'entrée
commerciale.

**Réalité du marché :** ces aires sont déjà largement équipées, et les appels d'offres
sont pilotés au niveau des groupes. À traiter comme une piste longue, pas comme un
démarrage.

### A.2 Réseau non concédé — la vraie piste

Les voies express et rocades gratuites relèvent de la puissance publique, et personne
ne les démarche :

- **M6 et M7** (anciennes A6/A7 déclassées dans la traversée de Lyon) : gérées par la
  **Métropole de Lyon**.
- **Voies rapides nationales** de la région : **DIR Centre-Est** (direction
  interdépartementale des routes).
- **Voies express départementales** : conseils départementaux du Rhône, de l'Ain,
  de l'Isère, de la Loire.

**Interlocuteur :** direction des routes / direction de la voirie, puis l'élu délégué
aux mobilités. Attention : sur le domaine public, il faut une **convention d'occupation**,
et une éventuelle dépense publique relève des règles de la commande publique. C'est
plus lent, mais le terrain est libre.

---

## Type B — 148 400 kWh cumac par station — **la cible prioritaire**

> Zones urbaines, ZI, zones d'activité, parkings ouverts au grand public,
> hors agglomération. Hors parkings privés d'entreprises ou de collectivités.

Le meilleur rapport gain / accessibilité. Par ordre de facilité réelle :

### B.1 Grande distribution — commencer par les indépendants

La distinction qui change tout :

| Enseignes | Structure | Qui décide |
|---|---|---|
| **E.Leclerc, Intermarché, Super U, Netto** | Indépendants adhérents | **Le directeur EST le propriétaire.** Décision possible en un rendez-vous. |
| Carrefour, Auchan, Casino, Monoprix, Lidl, Aldi | Intégrés | Direction régionale ou centrale ; le directeur de magasin remonte la demande. |

**Commence par les indépendants.** Même argumentaire, cycle de décision dix fois plus
court, et une première référence obtenue vaut plus que cinquante e-mails à des centrales.

**Interlocuteur :** le directeur du magasin. Le passage par l'accueil pour demander son
nom fonctionne mieux qu'un e-mail à `contact@`.

### B.2 Centres commerciaux

Le décideur est le **directeur du centre**, employé du gestionnaire (Klépierre, Unibail,
Nhood, Altarea, Frey, Apsys…), et non les enseignes locataires. Un centre = un parking
de plusieurs centaines de places = un site à fort passage.

### B.3 Parkings publics urbains

Deux cas :
- **exploités en délégation** (Indigo, Effia, Q-Park…) → direction régionale de
  l'exploitant ;
- **en régie municipale** → services techniques de la commune.

Vérifier lequel avant d'écrire : se tromper de destinataire coûte un cycle entier.

### B.4 Communes et collectivités

Le parking municipal ouvert au public relève du **type B** ; le parking des agents,
du type C. Beaucoup de communes ont les deux : c'est un **dossier groupé**, plus
intéressant qu'il n'y paraît.

**Interlocuteur, dans l'ordre :** le **DGS** (directeur général des services) dans les
petites communes, le **service technique / voirie** pour l'emplacement, l'**élu aux
mobilités ou à la transition écologique** pour l'arbitrage. Le maire ne traite pas ce
type de dossier.

### B.5 Stations-service indépendantes et zones d'activité

Stations hors réseau pétrolier, garages et centres auto avec parking ouvert,
concessions automobiles, zones d'activité avec parking mutualisé, parcs-relais TCL,
gares routières.

---

## Type C — 39 600 kWh cumac par station

> Parkings privés d'entreprises ou de collectivités (salariés, flotte).

Quatre fois moins valorisé que le type B : **rentable en complément, rarement seul**.
Deux cas où cela vaut le coup :

- l'entreprise a **plusieurs sites** : un contrat, plusieurs stations ;
- le site est **déjà client en type B** : on ajoute son parking salariés au même contrat.

**Interlocuteur :** responsable des services généraux, responsable de flotte, ou
directeur de site.

---

## Ordre d'attaque conseillé

1. **Supermarchés indépendants** de la métropole (Leclerc, Intermarché, Super U) —
   décision rapide, première référence.
2. **Centres commerciaux** — gros volumes, un interlocuteur clairement identifié.
3. **Communes** — dossiers groupés B + C, mais cycle long : à lancer tôt pour que
   ça aboutisse plus tard.
4. **Parkings publics délégués** — un accord au niveau régional peut couvrir
   plusieurs sites d'un coup.
5. **Type A non concédé** (Métropole, DIR, départements) — fort volume, terrain libre.
6. **Type A concédé** — seulement avec une référence solide à montrer.
7. **Type C** — en complément d'un contrat existant.

---

## Constituer la liste

Le script `outils/collecte-cibles.mjs` interroge OpenStreetMap et produit la liste
des sites d'une zone, déjà classés A / B / C :

```bash
cd cee-gonflage
node outils/collecte-cibles.mjs --zone "Métropole de Lyon" --sortie cibles-lyon
```

Il écrit `cibles-lyon.json`, à importer directement dans l'onglet **Prospection**
(bouton « Importer JSON »), et `cibles-lyon.csv` pour Excel.

**Ce que le script ne fait pas, et ne fera pas :** collecter des données personnelles.
OpenStreetMap décrit des établissements, pas des personnes. Le nom du directeur se
demande à l'accueil ou se lit sur le site institutionnel de l'enseigne — c'est plus
long, c'est légal, et le message qui en découle est bien mieux reçu.

## Constituer la liste des communes

Les mairies ne sont pas dans OpenStreetMap avec une adresse de contact fiable. La
source, c'est l'**Annuaire de l'administration** (service-public.fr), qui publie
l'adresse e-mail officielle de chaque mairie :

```bash
cd cee-gonflage
node outils/collecte-mairies.mjs --departement 69
node outils/collecte-mairies.mjs --departement 69,01,38,42 --sortie mairies-lyon
```

Puis :

```bash
node outils/preparer-envois.mjs --sites mairies-lyon.json --quota 50 --modele mairie
```

Ces adresses sont **institutionnelles**, publiées par l'État pour être utilisées :
ce sont des adresses d'établissement, pas des données personnelles. Aucun nom d'agent
ni d'élu n'est collecté.

> L'API de l'annuaire est publique mais bloquée depuis certains environnements
> d'exécution : lancer la commande depuis un poste avec un accès Internet ordinaire.

### Le message part sur un accueil, pas chez le décideur

L'adresse publiée est celle de l'accueil (`mairie@`, `contact@`, `accueil@`). Le
modèle `mairie` en tient compte : **la première ligne du corps demande la transmission
au service concerné** — DGS, services techniques, ou voirie / stationnement selon
l'organisation de la commune. C'est ce qui décide du sort du message : une mairie
transmet volontiers, elle ne répond pas elle-même.

L'angle du modèle est spécifique aux collectivités :

- **aucune dépense communale** — c'est la première objection, on la retire d'entrée ;
- **service aux administrés**, pas trafic client ;
- **convention d'occupation du domaine public** : le cadre juridique attendu, nommé
  dès le premier message, la commune reste propriétaire de son emplacement ;
- **parking public (B) + parking des agents (C)** dans le même dossier.

### Toute la France : l'ordre, pas le volume

34 900 communes à 50 envois par jour, cinq jours par semaine, cela fait **près de trois
ans**. Ce n'est pas une campagne, c'est un fond de roulement. Deux conséquences
pratiques :

1. **Prioriser par taille.** Une commune de 300 habitants a rarement un parking
   ouvert au public qui justifie une station. Commencer par les communes de plus de
   2 000 habitants, puis descendre. Le fichier CSV produit permet ce tri.
2. **Avancer par département, en cercles concentriques autour de Dardilly.**
   Un déplacement de qualification doit rester faisable : 69, puis 01 / 38 / 42 / 26 / 07 /
   71 / 73 / 74, puis le reste de la région, puis les régions limitrophes.

Chaque département donne un fichier autonome, importable dans l'onglet Prospection.
Les statuts et les relances se suivent là, pas dans un tableur.

## Rythme d'envoi

20 à 30 e-mails par jour depuis la boîte `@noxemgroup.com`, personnalisés depuis le
CRM. Au-delà, un domaine récent se fait classer en spam en quelques jours, et un
domaine grillé ne se répare pas. À ce rythme, la métropole est couverte en six
semaines, avec une délivrabilité intacte et des réponses réellement traitables.

**Monter à 50 par jour est possible, mais pas tout de suite.** Le volume n'est pas
le problème — la *marche* en est un : un domaine qui passe de 0 à 50 en une journée
est signalé. SPF, DKIM et DMARC doivent être en place, et le volume doit monter par
paliers sur trois à quatre semaines. La procédure est dans `docs/delivrabilite.md`.
Une fois le domaine chaud, 50 par jour tient sans difficulté.

---

## Annexe — commandes prêtes à lancer

Le script accepte `--categories` pour ne viser qu'une famille de sites. Les commandes
ci-dessous couvrent la totalité de ce que la fiche rend éligible sur ta zone.

```bash
cd cee-gonflage

# 1. Tout ce qui est éligible sur la Métropole de Lyon (A + B + C)
node outils/collecte-cibles.mjs --zone "Métropole de Lyon" --sortie 01-metropole

# 2. Les quatre départements limitrophes, un fichier chacun
node outils/collecte-cibles.mjs --zone "Rhône"  --sortie 02-rhone
node outils/collecte-cibles.mjs --zone "Ain"    --sortie 03-ain
node outils/collecte-cibles.mjs --zone "Isère"  --sortie 04-isere
node outils/collecte-cibles.mjs --zone "Loire"  --sortie 05-loire

# 3. Uniquement les aires d'autoroute (type A) sur ces zones
node outils/collecte-cibles.mjs --zone "Rhône" --categories A --sortie aires-rhone
node outils/collecte-cibles.mjs --zone "Isère" --categories A --sortie aires-isere

# 4. Le corridor A6 / A7 / A46 / A43 autour de Lyon, par emprise géographique
node outils/collecte-cibles.mjs --bbox 45.45,4.60,46.05,5.20 --categories A --sortie aires-corridor-lyon
```

Chaque commande écrit un `.json` (import direct dans l'onglet Prospection) et un `.csv`.
Pour les aires, les notes reprennent **l'axe** (`A7`, `A43`…), **l'exploitant** quand
OpenStreetMap le connaît, et les **coordonnées GPS** — de quoi préparer une tournée.

Deux repères utiles pour les aires, à recouper sur place :

- l'espacement entre aires est d'environ 15 km sur l'A7, un peu moins sur l'A6 ;
- l'**aire de Montélimar Ouest** (A7) est la plus grande d'Europe : c'est un site vitrine,
  mais aussi le plus disputé. À garder pour quand tu auras des références.

**Ne lance pas les cinq commandes d'affilée.** Overpass est un service public partagé :
une requête, on attend qu'elle finisse, on enchaîne. Sinon le serveur coupe.

## Ce que l'outil ne remplace pas

Il donne les **sites**. Il ne donne pas les **personnes** — et c'est volontaire :
OpenStreetMap décrit des équipements, pas des dirigeants. Le nom du directeur se
trouve en appelant l'accueil, en passant sur place, ou sur la page « qui sommes-nous »
de l'enseigne. C'est ce travail-là qui fait la différence entre un e-mail à `contact@`
et un e-mail qui obtient un rendez-vous.

---

# Annexe — cibles nommées (région lyonnaise)

Recherche menée le 16/09/2026. **À revérifier avant tout contact** : les périmètres,
les enseignes et les gestionnaires changent régulièrement.

## Les têtes de réseau — la meilleure piste

La simulation le montre sans ambiguïté : un accord au niveau d'un **groupement**
vaut mieux que cinquante rendez-vous magasin par magasin. Voici les structures qui
décident pour plusieurs dizaines de points de vente dans la région.

| Structure | Rôle | Pourquoi c'est la bonne porte |
|---|---|---|
| **SOCARA** — Société coopérative d'approvisionnement Rhône-Alpes | L'une des 16 centrales régionales du mouvement E.Leclerc. Siège et base logistique à Villette-d'Anthon / Saint-Quentin-Fallavier (38). | Les adhérents Leclerc de la région s'y retrouvent. Un référencement régional ouvre l'ensemble du parc. |
| **ITM Logistique International Sud-Est** (groupe Les Mousquetaires) | Base régionale desservant environ **96 points de vente** Intermarché. | 96 magasins, une seule structure de décision. Voir le chiffrage ci-dessous. |
| **Coopérative U** — centrale régionale | Les magasins U sont des indépendants regroupés en coopératives régionales. | Même logique : un référencement, puis les adhérents décident site par site, mais la porte est ouverte. |

**Attention à la nuance.** Chez ces enseignes, l'adhérent reste propriétaire de son
magasin : la centrale ne peut pas signer à sa place. Ce qu'un accord régional apporte,
c'est le **référencement** — vous cessez d'être un inconnu, vous devenez une offre
validée que les adhérents peuvent prendre. C'est ce qui fait passer le cycle de vente
de quatre rendez-vous à un.

### Ce que pèserait un parc entier

Hypothèses : 8,70 €/MWhc, 20 % de marge délégataire, 300 € d'entretien par station
et par an, 900 € d'installation.

| Périmètre | kWh cumac | CEE net / an | Marge / an | Investissement |
|---|---:|---:|---:|---:|
| 1 magasin | 148 400 | 1 033 € | 733 € | 900 € |
| Grappe de 10 magasins | 1 484 000 | 10 329 € | 7 329 € | 9 000 € |
| **Parc type d'une base régionale (96 points de vente)** | **14 246 400** | **99 155 €** | **70 355 €** | 86 400 € |

Le dernier chiffre est le plus important de tout ce document : **un seul accord de
référencement peut porter plus de 70 000 € de marge récurrente annuelle.** C'est le
scénario à viser, et il change la façon de préparer le rendez-vous : on ne vend pas
une station, on vend un dispositif clé en main pour un parc.

## Les centres commerciaux de la métropole

Le décideur est le **directeur du centre**, salarié de la foncière, jamais les
enseignes locataires.

| Centre | Commune | Foncière / gestionnaire |
|---|---|---|
| Westfield La Part-Dieu | Lyon 3e | Unibail-Rodamco-Westfield |
| Confluence | Lyon 2e | Unibail-Rodamco-Westfield |
| Carré de Soie | Vaulx-en-Velin | Altarea |
| Écully Grand Ouest | Écully | Klépierre (exploitation Ségécé) |
| Galeries adossées aux hypermarchés Carrefour | plusieurs communes | Carmila |

Quatre foncières couvrent l'essentiel du parc : **un accord-cadre avec l'une d'elles
vaut plusieurs sites**. La logique est la même que pour les groupements — viser la
direction régionale plutôt que chaque centre séparément.

## Méthode de contact pour ces structures

Ces organisations ne se démarchent pas par un e-mail à `contact@`. La séquence qui
fonctionne :

1. **Appeler le standard** et demander le service concerné : services généraux,
   direction technique, ou direction du développement selon la structure.
2. **Demander le nom et la fonction** de la personne qui traite les équipements de
   parking. C'est le seul moment où l'on collecte une donnée personnelle, et on la
   collecte auprès de l'entreprise elle-même.
3. **Envoyer l'e-mail nominatif** dans la foulée, en citant l'échange téléphonique
   dès la première ligne.

Ce que cela coûte : quelques appels. Ce que cela rapporte : un taux de réponse sans
commune mesure avec un envoi anonyme, et un interlocuteur qui attend votre message.
