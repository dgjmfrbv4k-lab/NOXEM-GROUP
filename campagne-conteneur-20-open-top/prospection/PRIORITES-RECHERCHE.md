# OU DEPENSER LES PROCHAINS APPELS DE RECHERCHE

**Regenere le 19/10 a 20h41. La liste de la section 1 est l INTERSECTION de deux choses : les fiches
a domaine connu et sans adresse du registre, ET ce que `candidats-deverrouillage.py` retient
reellement.** C est l intersection et non mon propre filtre, pour la raison dite au bas de la
section — j ai essaye les deux autres methodes et elles ont echoue toutes les deux.

Correction de fond du 19/10 : une priorite ne s inscrit ici qu apres un controle sur le REGISTRE.
Deux priorites ecrites de memoire ce matin ont ete dementies dans l heure — ABRAVIDRO donnee non
moissonnee quand 13 noms sur 16 y etaient, Santiago de los Caballeros donnee jamais testee quand 5
sur 6 y etaient. Je les avais baties sur le souvenir des REQUETES, pas sur le REGISTRE.

---

## 1. LE MEILLEUR GISEMENT DU MOMENT : 10 FICHES A **UN SEUL APPEL**

**Pourquoi elles valent mieux que tout le reste : leur DOMAINE EST DEJA CONNU.** La methode du §13
coute deux appels par fiche — un premier temps pour le domaine, un second restreint a ce domaine
pour l adresse. **Ici le premier temps est deja fait**, donc un appel au lieu de deux.

| Pays | Societe | Domaine connu | Statut |
|---|---|---|---|
| Brésil | Mais Vidros Salvador | `maisvidrossalvador.com.br` | A QUALIFIER |
| Brésil | Ponto do Vidro | `pontodovidro.com.br` | A QUALIFIER |
| Brésil | Soft Vidros | `softvidros.com` | A QUALIFIER |
| Brésil | Vidronorte | `vidronorterecife.com.br` | A QUALIFIER |
| Canada | Unicel Architectural Corp. — groupe Allegion | `unicelarchitectural.com` | A QUALIFIER |
| Maurice | Glazing Systems Ltd | `glazingsystemsmauritius.com` | A QUALIFIER |
| Maurice | Gre Ocean Concept Ltd | `greoceanconcept.com` | A QUALIFIER |
| République dominicaine | Alugav | `alugav.com` | A QUALIFIER |
| République dominicaine | Cristalados | `cristalados.com` | A QUALIFIER |
| Seychelles | VAB Aluminium | `vab-aluminium.central.sc` | A QUALIFIER |


**⚠️⚠️ TROIS TENTATIVES ONT ETE NECESSAIRES POUR ECRIRE CETTE LISTE, ET LES DEUX PREMIERES ETAIENT
FAUSSES. Je les consigne au titre du §16 parce que chacune illustre une regle du mandat que je
venais d ecrire dans ce fichier meme.**

**TENTATIVE 1 — MON PROPRE FILTRE. Elle a rendu 17 fiches, dont BROCANELLI et KOALA GLASS.** C est
-a-dire **les deux fiches memes** sur lesquelles le 15/10 a perdu deux appels, et dont les notes
disent en toutes lettres « adresse relevee et NON portee au champ » et « ADRESSE DISPONIBLE ET
DELIBEREMENT NON PORTEE AU CHAMP ». Mon vocabulaire improvise ne couvrait pas ces formulations ;
celui du script les couvre, `adresse disponible` et `non portee au champ` y ayant ete ajoutes
**precisement apres cette faute**. **J ai donc reproduit la faute Brocanelli dans le fichier ou
j ecrivais la regle contre elle.**

**TENTATIVE 2 — PARSER LA SORTIE FORMATEE DU SCRIPT. Elle en a perdu trois sur dix.** La sortie est
**ambigue par construction** : ses colonnes sont rembourrees a largeur fixe, donc **quand un nom
remplit sa colonne le double espace disparait** et la ligne ne se decoupe plus. `Republique
dominicaine` fait exactement la largeur du champ pays, et `Unicel Architectural Corp. — groupe
Allegion` celle du champ societe. **Une sortie d affichage n est pas une interface de donnees.**

**TENTATIVE 3, RETENUE — L INTERSECTION.** Les motifs de verdict sont **repris depuis la source du
script** et appliques au CSV, puis le resultat est **croise avec la presence du nom dans la sortie du
script**. Les deux ensembles doivent concorder, et c est le croisement qui le garantit.
**⚠️ ET IL FALLAIT LE FAIRE, parce que mon filtre n etait PAS plus severe que le script comme je
l avais d abord affirme : il laissait passer 2 fiches que le script ecarte — Vitromatic et Hourglass DFW. — groupe Allegion · Glazing Systems Ltd · Gre Ocean Concept Ltd · Vitromatic · Alugav · Cristalados · VAB Aluminium · Hourglass DFW.** Lecture
faite, le script a raison : sur Hourglass DFW le **second temps est DEJA FAIT** et son verdict est
que la seule adresse publiee est **nominative**, ce que le §5 interdit. Un appel y serait perdu.
**Ma phrase « il peut omettre un candidat, jamais en inclure un que le script ecarte » etait donc
fausse, et elle est corrigee ici plutot que laissee en place.**

**⚠️⚠️ ET LA PREMIERE MESURE SUR CETTE LISTE LA CORRIGE DES SA PREMIERE UTILISATION, LE 19/10 AU
SOIR : UNE FICHE A UN SEUL APPEL EST BON MARCHE, ELLE N EST PAS POUR AUTANT DE BONNE CLASSE.**
Les deux premieres converties — **Ponto do Vidro** (Fortaleza) et **Vidronorte** (Recife) — sont des
**vidracarias de detail**, c est-a-dire la classe *verrier plus pose*, **a zero pour cent sur onze
fiches**. Les deux ont bien rendu une adresse publiee sur leur propre page, donc la methode marche ;
mais elles ne valent rien a envoyer.
**ET LA CAUSE N EST PAS UN HASARD, ce qui la rend utilisable :** ces deux fiches sont nees de
**recherches par VILLE** dans le Nordeste, et la section 3 ci-dessous classe la recherche large par
ville comme **la plus pauvre des cinq methodes**. Une ville rend ce qu elle contient, et une ville
contient surtout des vitriers.
**CONDUITE : LE COUT EN APPELS CLASSE L ORDRE, LE METIER CLASSE LA VALEUR.** Une fiche a un appel de
la classe aluminium ne vaut pas une fiche a deux appels de la classe negoce. **Donc on lit la colonne
Societe avant de depenser**, et sur les dix ci-dessus les noms a privilegier sont ceux qui disent le
negoce ou la transformation, pas ceux qui disent la vitrerie.

**La regeneration canonique reste le script lui-meme, dont la premiere section sort deja triee site
connu en tete :**
```bash
python3 campagne-conteneur-20-open-top/prospection/outils/candidats-deverrouillage.py
```

---

## 2. CE QUI RESTE DERRIERE, ET POURQUOI C EST PLUS CHER

Le script retient **400 fiches a travailler**. Les autres n ont **aucune coordonnee** — ni site, ni
adresse — et exigent **les deux temps**, soit deux appels chacune. Le §13 rappelle qu une fiche nee
d un annuaire sans site est **invisible aux cinq signaux** de `detecte-doublons.py` : **le
`grep-nom.py` avant chaque second temps y est obligatoire**, et c est sur ce genre de fiche que les
cas Dialum et Infinity Glass ont cree des doublons.

**L ordre a tenir est celui du tri METIER du §6, pas celui du pays :** verrier pur et negoce
d abord, a 12,8 et 10 pour cent ; aluminium, facade et pose en dernier, a 3,6 ; verrier plus pose
jamais, a zero sur onze fiches. **Les blocs algerien et angolais qui ouvrent la liste du script sont
en majorite de la classe aluminium** — a lire avant de s y lancer.

---

## 3. LES METHODES DE DECOUVERTE, CLASSEES PAR CE QU ELLES ONT RENDU

1. **La requete de vocabulaire de stock** — `chapa inteira`, `lamina entera`, `full case`,
   `feuille entiere`, `meia chapa`. **La meilleure**, et validee par l aval : United Glass, seule
   maison a avoir demande un devis, annonce vendre a la feuille, a la caisse, a la demi-caisse ou au
   camion entier. Mesure du 19/10 : **31 noms rendus, 19 deja au registre**, et le quart restant a
   donne Indiana Glass et Dulles Glass.
2. **L axe des PROCEDES** — ligne d argenture, de feuilletage, de vitrage isolant. Trois argenteurs
   en un appel. Mieux cible que la geographie parce qu un argenteur **ne peut argenter que ce qu il
   achete**. ⚠️ Garde-fou : **a un argenteur, le miroir fini ne se propose jamais.**
3. **Le portail sectoriel du pays**, qui a refute la saturation americaine quatre fois le 14/10. Sa
   rubrique **fabricants** n a jamais ete lue et qualifie mieux que sa rubrique negoce.
4. **La piece de dossier antidumping publique** — elle a rendu ce soir les **quatre producteurs de
   miroir mexicains et leurs marques** depuis le texte du DOF.
5. **La recherche large par ville** — la plus pauvre, et **une ville par requete**.

---

## 4. CE QU IL NE FAUT PLUS CHERCHER, ET C EST UN GAIN

· **L OUTRE-MER PAR E-MAIL** : neuf deverrouillages, **zero** adresse. C est le creneau d appels qui
  debloque ce marche.
· **Les rubriques de NEGOCE de `vidrioperfil`** : un confirme pour quatre dementis.
· **⚠️⚠️ LA CARAIBE ANGLOPHONE PAR E-MAIL — MESURE DU 20/10, ET ELLE EST SANS APPEL : SEPT NOMS
  RENDUS, SEPT DEJA AU REGISTRE.** Une requete sur le vocabulaire du stock appliquee a la Jamaique,
  Trinite, la Barbade et les Bahamas a rendu Hepburn s Glass, Creative Glass and Aluminium, Jubilee
  Suppliers, Flintstones, Odoll s, Premier Importers et Storm Frame Windows — **les sept etaient
  deja la**, avec Caribbean Glass Co, Caribbean Glass Specialists et Kamri Glass.
  **ET SIX DES SEPT SONT EN `A APPELER` SANS LA MOINDRE ADRESSE.** Ce n est donc pas un probleme de
  DECOUVERTE, c est le meme mur que l outre-mer francais : **ces maisons publient un telephone et
  un annuaire, pas une boite.** La methode de deverrouillage du paragraphe 13 rend 38 pour cent dans
  le monde et **zero** sur le bloc DOM-COM, et la Caraibe anglophone se comporte pareil.
  **CONDUITE : ne plus depenser d appel de DECOUVERTE sur la Caraibe. Le marche est identifie, il
  est telephonique.** Et c est une raison de plus pour le creneau d appels demande a Kevin — ce sont
  des marches sans production locale, donc structurellement les mieux cibles de la campagne.

· **L EUROPE** : pas de nouvelle prospection tant que l arbitrage du partage entre les deux
  campagnes n est pas rendu. Cas concret consigne ce soir — A Biseladora do Norte, au Portugal,
  matiere gardee dans la note de VCP.

---

**Registre a 1869 fiches au moment de cette regeneration. AUCUN ENVOI N A ETE FAIT le 19/10 : la
file attend l accord expres de Kevin, message par message.**


---

# 🎯 OU DEPENSER LES APPELS DE DEMAIN — liste refaite a 14h06

**⚠️⚠️ ET LA FACON DONT CETTE LISTE EST CONSTRUITE EST LA MOITIE DE SA VALEUR, parce que je me suis
trompe une heure plus tot en la faisant autrement. ELLE TRIE LA SORTIE DE
`candidats-deverrouillage.py`, ELLE NE REFAIT PAS SON FILTRAGE.** Mon premier essai etait une regex
maison qui rendait **Brocanelli** — c est-a-dire exactement la fiche qui avait coute un appel le
15/10 — alors que le script, lui, l excluait deja. **Quand un script produit une liste, on trie SA
SORTIE.**

**LE CONTEXTE QUI REND CETTE LISTE NECESSAIRE AUJOURD HUI : le gisement a UN appel est epuise.**
Les huit fiches a site connu ont toutes ete traitees ce jour. **Les 412 restantes coutent DEUX
appels chacune** — la methode en deux temps du paragraphe 13 — **donc l ordre compte desormais.**

**LE TRI :** classe de metier d abord, marche ensuite, **plus 3 points si un site est deja connu et
1 si un telephone l est**, puisque ces deux-la reduisent le cout.
⚠️ **Honnetement : 395 des 412 fiches ont pu etre relues et classees automatiquement**, les 17 autres
ayant un nom ou un site trop long pour le format de sortie du script. **Elles ne sont pas perdues,
elles ne sont simplement pas classees ici.** ⚠️ Et j avais d abord ecrit **397**, chiffre tape de
memoire entre deux executions : **corrige par substitution avant le commit**, parce que le
paragraphe 13 interdit de taper un comptage a la main et que c est la faute du jour.

| # | Pays | Societe | Site | Motifs |
|---|---|---|---|---|
| 1 | Brésil | **Distribuidora Tec Vidros** | — | verrier · tel |
| 2 | Brésil | **Sergipe Vidros** | — | verrier · tel |
| 3 | Brésil | **Vidraçaria Marinho** | — | verrier · tel |
| 4 | Canada | **Lamiver** | — | verrier · tel |
| 5 | Australie | **Glass Market Vic Pty Ltd** | — | verrier |
| 6 | Australie | **Glass Surface Coatings WA** | — | verrier |
| 7 | Brésil | **Marvidros** | — | negoce · tel |
| 8 | Brésil | **Maxx Distribuidora de Vidros** | — | verrier |
| 9 | Brésil | **Raiol Vidros Ltda** | — | verrier |
| 10 | Brésil | **TVT Vidros Temperados** | — | verrier |
| 11 | Brésil | **Tempermat** | — | verrier |
| 12 | Brésil | **Vidrosistemas** | — | verrier |
| 13 | Canada | **Aqua Mirrors** | — | verrier |
| 14 | Canada | **Mirror Works** | — | verrier |
| 15 | États-Unis | **Bent Glass Design Inc.** | — | verrier |
| 16 | États-Unis | **Gardner Glass Products Denver** | — | verrier |
| 17 | États-Unis | **GlassTemp Inc.** | — | verrier |
| 18 | États-Unis | **Innovative Glass Corp** | — | verrier |
| 19 | États-Unis | **M and M Glass Company** | — | verrier |
| 20 | États-Unis | **NY Tempering** | — | verrier |

**⚠️ ET CE QUE CETTE LISTE NE DIT PAS, parce qu elle ne peut pas : elle ordonne, elle ne qualifie
pas.** Chaque nom garde son second temps, et le premier geste reste **le `grep-nom.py` sur le
RADICAL COURT** — la lecon Vitrum du jour, ou le nom d une source n etait pas celui de la societe.

**⚠️ RAPPEL DE BUDGET : la methode en deux temps coute DEUX appels par fiche, parfois trois.** Le
plafond de la session est de 200 appels par tour, soit **70 a 90 fiches** au maximum, et il se
partage avec la decouverte. **Vingt fiches de cette liste, c est une quarantaine d appels.**
