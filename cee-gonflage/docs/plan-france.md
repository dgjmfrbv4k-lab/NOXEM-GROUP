# Toutes les mairies de France — la séquence

La France compte environ **34 900 communes**. C'est un fond de roulement, pas une
campagne : à 150 envois par jour ouvré, il faut de l'ordre de **trois ans** pour en
faire le tour une fois. La bonne question n'est donc pas « combien par jour » mais
**dans quel ordre**.

Deux principes commandent l'ordre ci-dessous :

1. **Un rendez-vous doit rester faisable.** Un accord obtenu à 400 km sans possibilité
   d'aller qualifier le site sur place ne vaut pas un accord à 30 km. On avance en
   cercles autour de Dardilly.
2. **Le palier impose le rythme, pas l'envie.** `outils/envoyer.mjs` lit
   `envois/campagne.json` et calcule le volume autorisé du jour à partir de la date de
   démarrage : 10 par boîte la première semaine, 20 la deuxième, 30 la troisième, 40
   ensuite. Redemander 150 le troisième jour ne les débloque pas.

## Les vagues

Chaque vague donne un fichier autonome, importable dans l'onglet Prospection. Le nombre
de communes est indicatif : la commande affiche le compte réel, et surtout le nombre de
communes ayant **une adresse e-mail publiée** — c'est toujours moins.

| # | Zone | Départements | Pourquoi là |
|---|---|---|---|
| 1 | Rhône | `69` | Le terrain. Déplacement dans la journée, retour le soir. |
| 2 | Limitrophes directs | `01` `42` `38` | Moins d'une heure de route. |
| 3 | Couronne | `71` `26` `07` `73` `74` | Déplacement à la journée encore possible. |
| 4 | Reste Auvergne-Rhône-Alpes | `63` `03` `43` `15` | On termine la région avant d'en sortir. |
| 5 | Bourgogne-Franche-Comté | `21` `39` `25` `58` `89` `70` `90` | Région limitrophe au nord. |
| 6 | Vallée du Rhône et PACA | `30` `84` `13` `04` `05` `83` `06` | L'axe naturel vers le sud. |
| 7 | Occitanie nord et Massif central | `12` `48` `46` `19` `23` `87` | Continuité géographique. |
| 8 | Reste de la France | les autres départements | Une fois les sept premières purgées. |

```bash
cd cee-gonflage

# Vague 1
node outils/collecte-mairies.mjs --departement 69 --sortie mairies-01-rhone

# Vague 2
node outils/collecte-mairies.mjs --departement 01,42,38 --sortie mairies-02-limitrophes

# Vague 3
node outils/collecte-mairies.mjs --departement 71,26,07,73,74 --sortie mairies-03-couronne

# Vague 4
node outils/collecte-mairies.mjs --departement 63,03,43,15 --sortie mairies-04-aura

# Vague 5
node outils/collecte-mairies.mjs --departement 21,39,25,58,89,70,90 --sortie mairies-05-bfc

# Vague 6
node outils/collecte-mairies.mjs --departement 30,84,13,04,05,83,06 --sortie mairies-06-sud

# Vague 7
node outils/collecte-mairies.mjs --departement 12,48,46,19,23,87 --sortie mairies-07-massif
```

## La boucle quotidienne

Une fois une vague collectée, c'est **la même commande tous les jours** :

```bash
node outils/envoyer.mjs --sites mairies-01-rhone.json --modele mairie --quota 150 --envoyer
```

`--quota 150` est une demande, pas un ordre : le palier du jour la ramène à ce qui est
sûr. Le premier jour, la sortie ressemble à ceci :

```
Jour 1 de la campagne — palier : 10 par boîte.
Vous avez demandé 150 : le palier prime, ce sera 40.
```

Et trois semaines plus tard, sans rien changer à la commande :

```
Jour 25 de la campagne — palier : 40 par boîte.
150 message(s) au programme (150 demandé(s)).
```

Le journal empêche tout doublon d'un jour sur l'autre : quand une vague est épuisée,
l'outil le dit, et on passe à la suivante.

## La relance, dix jours après

Le premier message ne fait que la moitié du travail. Dix jours après avoir attaqué une
vague, la relance part sur la même liste, sans rien resélectionner à la main :

```bash
node outils/envoyer.mjs --sites mairies-01-rhone.json --modele relance --quota 150 --envoyer
```

Elle se rattache au fil du premier message, ne part qu'une fois par destinataire, et
saute ceux qui ont demandé à ne plus être contactés. En rythme de croisière, les deux
commandes alternent : premiers envois sur la vague en cours, relances sur la précédente.

## Prioriser à l'intérieur d'une vague

Une commune de 300 habitants n'a le plus souvent pas de parking ouvert au public qui
justifie une station. À l'intérieur d'un fichier, **traiter d'abord les communes de plus
de 2 000 habitants** : le CSV produit s'ouvre dans Excel et se trie.

Cela ne veut pas dire abandonner les petites communes — elles restent dans le fichier et
repassent en fin de vague. Cela veut dire que les premiers jours, qui sont ceux où le
volume est le plus faible à cause du palier, sont dépensés là où le taux de réponse est
le meilleur.

## Ce que cette séquence ne dit pas

Elle ne dit rien du **téléphone**. Une mairie répond mal à un e-mail froid et bien à un
appel au standard, surtout les petites où le DGS décroche lui-même. L'e-mail sert à
exister avant l'appel, pas à le remplacer. Les numéros collectés par
`collecte-mairies.mjs` sont dans le champ `notes` de chaque fiche.
