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
· **L EUROPE** : pas de nouvelle prospection tant que l arbitrage du partage entre les deux
  campagnes n est pas rendu. Cas concret consigne ce soir — A Biseladora do Norte, au Portugal,
  matiere gardee dans la note de VCP.

---

**Registre a 1869 fiches au moment de cette regeneration. AUCUN ENVOI N A ETE FAIT le 19/10 : la
file attend l accord expres de Kevin, message par message.**
