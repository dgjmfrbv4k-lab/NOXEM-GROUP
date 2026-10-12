# ⏱ 12/10/2026, 13h15 — LES 15 APPELS REFAITS, ET LE CLASSEMENT A CHANGE

**Bloc mis en tete apres la journee du 12/10.** `LISTE-APPELS.md` est regeneree : **146 societes**
portent un telephone et aucune adresse e-mail exploitable, et `A APPELER` compte **130 fiches, toutes
avec un numero**. L'e-mail ne peut pas atteindre ces maisons — seul le telephone les ouvre.

**⚠️ CE CHIFFRE A ETE FAUX PENDANT TROIS MINUTES, ET LA CAUSE MERITE D ETRE DITE PARCE QU ELLE EST
PLUS SUBTILE QUE CELLE DU §13.** J avais ecrit **147**, en le SUBSTITUANT depuis une commande comme le
mandat l exige — mais la commande comptait les lignes commencant par une barre verticale, et elle
attrapait donc aussi **la ligne de separation du tableau**. Le vrai chiffre, celui que
`genere-liste-appels.py` imprime lui-meme, est **146**.
**LA LECON COMPLETE LE §13 : substituer un chiffre ne suffit pas, il faut que la commande compte la
BONNE CHOSE.** Un comptage faux substitue est exactement aussi faux qu un comptage tape a la main, et
il est plus dangereux parce qu il a l air verifie. Quand un outil imprime deja le chiffre, c est SON
chiffre qu il faut reprendre, pas un second comptage improvise a cote. Meme famille que l erreur de
libelle sur la Guyane le meme jour : j ai cru mesurer, j ai en fait mesure autre chose.

## CE QUI A CHANGE AUJOURD'HUI DANS CE FICHIER

· **Six fiches camerounaises en sont SORTIES.** Elles promettaient un appel qui ne lèverait rien :
  leur ambiguïté — un message peut-être déjà parti de l'ancienne boîte `harfiaaron0` — ne se tranche
  ni par un appel ni par moi, seulement par Aaron. Passées en `A VALIDER AARON`.
· **Cinq fiches en sont sorties aussi** parce que leurs marchés sont déclassés par le §6 : deux
  indiennes, deux malgaches, une malawienne.
· **Quatre y sont entrées**, et c'est le gain net de la journée : **Glastec** (Casablanca) et
  **Accra Glass Company** (Ghana), déverrouillées au téléphone alors qu'elles n'avaient **aucune**
  coordonnée, plus **Alu Espace +** et **Solutions FAR** à Ducos.
· **Une date fausse corrigée dans l'outil lui-même.** `genere-liste-appels.py` écrivait
  « Regeneree le 08/10/2026 » **en dur**, si bien que chaque régénération affichait une date fausse en
  tête d'un fichier à jour. La date est désormais substituée depuis `date`, comme le §13 l'impose pour
  tout chiffre et toute heure.

## LES 15, DANS L'ORDRE, AVEC UN SEUL OBJECTIF CHACUN

| # | Qui | Téléphone | Fenêtre (Paris) | L'objectif de l'appel, et rien d'autre |
|---|---|---|---|---|
| 1 | **Amazon Temper** (Brésil) | `+55 85 3260-3076` | 14h-22h | **La plus grosse consommatrice de float du registre, et elle est injoignable par e-mail.** Huit parcs de trempe. Objectif : qui achète le float, et sur quelles épaisseurs. ⚠️ Signal à vérifier dans l'appel : un relevé associe son site d'Aquiraz à **Vivix**. Si l'approvisionnement est établi, l'angle devient la **seconde source**. |
| 2 | **North Africa for Importing Glass** (Libye) | `+218 91 209 1023` | 09h-17h · **dim-jeu** | **Importe déjà du float de Chine, de Belgique ET DE FRANCE** — donc rien à lui expliquer, il compare un prix rendu. ⚠️ Doute d'identité relevé le 08/10 : à lever au téléphone avant toute offre. Second numéro `+218 91 322 1953`. |
| 3 | **Nassau Glass Company** (Bahamas) | `+1 242 603 5521` | 15h-23h | Le plus gros du pays depuis 1959, avec sa sœur Bahamas Aluminum. Île sans production, tout importé. Objectif : référence et épaisseur dominantes, port Nassau. |
| 4 | **Alu Espace +** (Martinique) | `0596 54 14 36` | 15h-23h | **Nouvelle, et sur le marché de notre seul client export.** Fait tout à l'atelier et **monte du Schüco** : ils travaillent déjà à la spécification d'un fournisseur européen, donc rien à leur apprendre sur l'origine. Objectif : conteneur ou achat local à la feuille. |
| 5 | **Glastec** (Casablanca) | `+212 5 22 34 26 16` | 10h-18h | **Déverrouillée aujourd'hui, elle n'avait aucune coordonnée.** Trempé, feuilleté, double vitrage, façonnage : consommatrice de float par construction. Objectif : une adresse e-mail, puis les épaisseurs. |
| 6 | **MunnWorks** (États-Unis) | `+1 914 665 6100` | 15h-23h | **Le meilleur assortiment produit de la campagne** — miroirs lumineux pour l'hôtellerie — et **deux boîtes refusées en `5.4.1` par le même locataire**, donc le téléphone est le seul canal restant. L'argument se sert par le défaut évité : le piquage qui part du chant quand l'humidité atteint la couche de cuivre. |
| 7 | **Bars Facade** (Géorgie) | `+995 577 41 51 36` | 07h-15h | Importateur historique entre la Géorgie et la Turquie depuis 1998, deux sites. Transit Poti. |
| 8 | **Flat Glass Distributors** (États-Unis) | `+1 904 354 5413` | 15h-23h | Trois points de stock, Jacksonville, Houston, La Nouvelle-Orléans. ⚠️ **Et l'argument américain est le plus fort de la campagne depuis le 06/04/2026** : Chine 181,52 pour cent d'antidumping, Malaisie 17,3 à 102 pour cent de compensateur, **Europe non visée**. On ne dit pas que notre verre est bon marché, on dit que les deux origines les moins chères portent désormais des droits. |
| 9 | **Glass Enterprises** (États-Unis) | `+1 215 638 1007` | 15h-23h | Usine neuve de 180 000 pieds carrés, fabricant certifié float. Même argument douanier. |
| 10 | **Alma Glass** (Arabie saoudite) | `+966 11 498 3275` | 08h-16h · **dim-jeu** | Première usine de trempe de Dammam. ⚠️ **Ne JAMAIS employer l'argument du float absent** : le royaume compte au moins quatre producteurs — Obeikan, Zoujaj, Guardian, UFG. C'est le marché le mieux pourvu de la zone. |
| 11 | **Accra Glass Company** (Ghana) | `+233 302 713 836` | 11h-19h | **Déverrouillée aujourd'hui, aucune coordonnée avant.** ⚠️ **Premier objectif : établir si elle PRODUIT ou si elle transforme.** L'annuaire lui prête du float ; si c'est vrai, c'est un concurrent et non une cible. |
| 12 | **Technoglass** (Algérie) | `+213 555 62 47 74` | 10h-18h · **dim-jeu** | Importateur déclaré depuis 1987, import-distribution-transformation. ⚠️ Cevital produit en Algérie : pas d'argument d'absence d'offre locale. |
| 13 | **Punamactex** (Ghana) | `+233 21 689800` | 11h-19h | Négociant depuis 1995 annonçant float clair **et** teinté, donc importateur par construction. Port de Tema. |
| 14 | **Action Enterprises** (Haïti) | `+509 36 19 5572` | 15h-23h | Meilleure fiche haïtienne : fabricant-installateur avec entrepôt à Croix-des-Bouquets. Île sans float. |
| 15 | **Solutions FAR** (Martinique) | `0596 77 11 11` | 15h-23h | ⚠️ **La plus faible des quinze, et il faut le dire :** garde-corps aluminium **sans gamme vitrée confirmée**, et un garde-corps peut être à barreaux. L'appel est une **qualification** — posent-ils du verre ? — pas une approche. WhatsApp `0696 09 30 33`, qui est leur seul canal écrit. |

## ⚠️ ET LE POINT QUI VAUT PLUS QUE LA LISTE

**130 fiches attendent un appel et il n'en est parti aucun depuis le début de la campagne.** Les plus
grosses cibles identifiées — Amazon Temper et ses huit parcs de trempe, MunnWorks, Nassau Glass — sont
**précisément** celles qu'aucun e-mail n'atteint. C'est porté dans `DECISIONS-AARON.md` : il faut un
créneau et quelqu'un qui appelle. Le registre ne peut pas le faire à sa place.

---

# ⏱ LUNDI 12/10, 11h36 — CINQ CIBLES TELEPHONIQUES NEUVES, ET LA PREMIERE EST LA PLUS GROSSE DE LA CAMPAGNE

*Bloc mis en tete apres une matinee ou le gisement d adresses e-mail du registre est tombe a ZERO
deverrouillage disponible. Ce qui reste des plus grosses cibles ne s atteint plus que par telephone,
et c est le constat central de la journee. 137 fiches sont en `A APPELER`, toutes avec un numero.*

## 1. ⭐ AMAZON TEMPER (Bresil) — la plus grosse consommation de float identifiee a ce jour

**`+55 81 3341 7971` (Recife) · `+55 92 3611 2832` (Manaus) · creneau 14h00-22h00 heure de Paris**

**HUIT PARCS INDUSTRIELS, nommes par eux-memes :** Varzea Grande, Lucas do Rio Verde, Xanxere,
Aquiraz, Manaus, Cariri, Recife, Mossoro, plus deux unites a Fortaleza et Salvador en construction.
Gamme : trempe, feuillete, trempe-feuillete et **insulado**. Un groupe de huit sites de trempe n a
**qu une** matiere premiere, et il la consomme par conteneurs.

**Objet de l appel, et il n y en a qu un : qui achete le float pour les huit sites, et l achat
est-il centralise ?** Rien d autre. Le reste se decide quand on sait a qui on parle.

⚠️ **Deux choses a ne PAS dire.** Jamais qu il n y a pas de production locale au Bresil — Vivix
produit a Goiana et Cebrace a Jacarei, Cacapava et Barra Velha. Et **un releve de position associe
leur site d Aquiraz a VIVIX** : si l approvisionnement est etabli, l angle n est pas la nouveaute
d une origine europeenne mais **la seconde source**, exactement comme Induver avec AGC. A verifier
pendant l appel, pas apres.
⚠️ Pages du site vieilles d environ sept ans : confirmer les numeros.

## 2. ⭐ KAMRI GLASS INVESTMENTS (Trinite-et-Tobago) — une usine et une table de decoupe

**`+1 868 235 4527` · creneau 14h00-22h00**

Showroom et atelier a Marabella, **et une usine a la zone industrielle de POINT LISAS**. Ils
annoncent du trempe et une **machine de decoupe semi-automatique** presentee comme la seule de ce
type sur l ile. Une table de decoupe veut dire qu ils achetent de la **feuille**, pas du faconne.

**Et le marche est deja valide :** Caribbean Glass Specialists, a Trinite aussi, est un de nos
quatre dossiers de prix ouverts, et Central Glass y est en relance.

**Objet de l appel :** l adresse des achats, et les epaisseurs qui passent sur la table.

## 3. MUNNWORKS (Etats-Unis, Mount Vernon NY) — l e-mail est definitivement ferme

**`+1 914 665 6100` · creneau 15h00-23h00**

**Deux boites publiees par eux, deux refus `550 5.4.1` du meme locataire Microsoft** : c est un
blocage de maison, pas une boite morte, et une troisieme tentative est interdite. **L angle reste
excellent** : ils fabriquent des **miroirs lumineux d hotellerie**, donc le defaut de bord sous
humidite permanente est exactement ce que notre miroir sans cuivre ni plomb evite — et c est le
defaut evite qui porte l argument, jamais le produit.

## 4. HEPBURN'S GLASS SUPPLIES (Jamaique, Kingston 13)

**`+1 876 908 0962` · creneau 14h00-22h00**

Leur propre site annonce du **float clair et teinte et des miroirs a prix de gros** — c est notre
gamme de base mot pour mot. Adresse publiee mais **obfusquee** par une protection
anti-moissonnage. **Objet de l appel : l adresse des achats, rien d autre.**
⚠️ Une adresse gmail circule sur un reseau social : **ne pas l utiliser**, elle ne vient pas de leur
page de contact et son domaine differe du site.

## 5. WM GUADELOUPE (Baie-Mahault, ZI de Jarry)

**`+590 974 56 05 24` · creneau 13h00-16h00 heure de Paris**

Fournisseur des professionnels du BTP depuis 2002, **de la maconnerie a la menuiserie**, portes
fenetres et volets. RCS Baie-Mahault 44064727900023. **Leurs donnees structurees portent un domaine
casse** — `vm-` au lieu de `wm-`, partie locale tronquee — donc aucun envoi possible.

**A savoir avant de parler fiscalite : ne rien dire.** L octroi de mer sur le chapitre 70 n est pas
etabli et l exoneration des intrants de production pour un transformateur antillais est une question
ouverte du paragraphe 6. **Si la question vient, elle se note et se remonte.**

---

# Les 15 appels qui valent le temps d'Aaron — refait le 11/10/2026 à 22h27

**Remplace entièrement la version précédente.** Extrait de `LISTE-APPELS.md`, qui en compte plus de
cent vingt : personne ne passe cent vingt appels. Ici, **un objectif par appel, et un seul.**

**Fuseaux recalculés à la main**, Paris étant à UTC+2 jusqu'au 25/10. **Semaine ouvrée :** le Maroc, le
Brésil, Singapour, le Canada et les États-Unis travaillent du lundi au vendredi ; l'**Algérie, la Libye,
l'Oman et l'Égypte** vont du **dimanche au jeudi** — lundi y est donc un jour ouvré normal.

---

## Les cinq qui valent le plus

### 1. Amazon Temper (Brésil) — **la plus grosse consommatrice de float trouvée de la campagne**
**+55 85 3260-3076** (Aquiraz, Ceará) · créneau Paris **14 h – 18 h**
**Pourquoi :** groupe annonçant **huit usines de trempe** — Aquiraz, Manaus, Cariri, Lucas do Rio Verde,
Várzea Grande, Xanxerê, Recife, plus Salvador en construction. **Huit fours de trempe ne se nourrissent
pas à la feuille.** Et Manaus est en **zone franche**, ce qui change le calcul d'importation.
**Pourquoi un appel et pas un e-mail :** leur site n'expose qu'un **formulaire**. L'adresse vue sur leur
Facebook satisfait la lettre du §5 mais vient d'un tiers, et **sur une cible de cette taille un rebond
coûte plus qu'un appel.**
**OBJECTIF UNIQUE :** savoir **où se décide l'achat de float** et obtenir le nom du service. Secondaire
si la conversation le permet : **qui les approvisionne aujourd'hui** — un relevé de position associe
leur site d'Aquiraz à **Vivix**, et si c'est confirmé l'angle devient la seconde source.

### 2. Ouchtar Commerciale (Maroc) — **le meilleur profil marocain**
**+212 522 77 71 00** (Casablanca) · créneau Paris **10 h – 17 h**
**Pourquoi :** décrite en **importation et distribution** de verres de bâtiment, de sécurité et trempés,
plus des profilés aluminium. **Un importateur-distributeur raisonne au conteneur et à la rotation de
stock, pas au chantier.** Il achète déjà à l'étranger : il n'y a rien à lui démontrer sur la faisabilité.
**Pourquoi un appel :** quatre adresses trouvées, **toutes d'annuaire** (`menara.ma`, `iam.net.ma`), et
`ouchtar.com` n'est pas indexé. Le §5 n'est pas satisfait.
**OBJECTIF UNIQUE :** obtenir **une adresse e-mail que la société donne elle-même**.
⚠️ Fiche Kompass vieille de sept ans, numéros à confirmer. Piège : **Ouchtar 2** et **Ouchtar Logistique**
sont deux autres entités du groupe, sans rapport avec le verre.

### 3. Reliance Safety Glass (Singapour) — **le meilleur argument technique de la campagne**
**+65 6755 4555** (Woodlands) · créneau Paris **9 h – 11 h** *(leur 15 h – 17 h)*
**Pourquoi :** ils ont un four de **heat soak**. C'est le traitement qui élimine les **inclusions de
sulfure de nickel** après trempe, et on ne l'installe que pour du verre **structurel** où une casse
spontanée serait inacceptable. **Une maison qui investit là a un intérêt direct et chiffrable à la
propreté de sa matière d'entrée, puisque ce sont les inclusions du float qui provoquent le défaut
qu'elle traite.** Plus découpe de précision, polissage, façonnage de chants et feuilletage PVB.
**Pourquoi un appel :** leur adresse est **obfusquée** sur leur propre page.
**OBJECTIF UNIQUE :** une adresse, et le nom de qui spécifie la matière première.
⚠️ **Ne jamais argumenter sur le prix** : Woodlands est à une heure de camion du float malaisien.

### 4. WHTB Glass LLC (États-Unis) — **une question à trancher qui vaut mieux qu'un envoi**
**+1 631 924 4601** (Shirley, New York) · créneau Paris **15 h – 21 h**
**Pourquoi :** figure à l'exhibit I-7 des importateurs de float, et un annuaire industriel la décrit en
*flat glass processing*. **Mais des sources donnent WHTB pour Beijing Wuhua Tianbao Glass**, avec un WHTB
Glass Group en Chine. **Si c'est le bras américain d'un groupe verrier chinois, écrire serait écrire au
canal de vente d'un concurrent** — le motif pour lequel le §6 a classé SGC International.
**Et c'est exactement pour cela que l'appel vaut cher :** si au contraire elle transforme à Shirley et
que son substrat chinois porte depuis le 06/04/2026 **181,52 %** d'antidumping plus un compensateur,
elle a **l'intérêt le plus fort de toute la liste** à changer d'origine. **La meilleure cible du lot ou
son contraire exact.**
**OBJECTIF UNIQUE :** transforme-t-elle à Shirley, et la décision d'achat s'y prend-elle ?

### 5. Sotraglace Maroc — **la gamme la plus large du vivier marocain**
**05 22 34 93 65** (Casablanca, Sidi Bernoussi) · créneau Paris **10 h – 17 h**
**Pourquoi :** société anonyme de 1994, transformation de verre **architectural** — trempé, trempé
**émaillé**, feuilleté, **pare-balles** et double vitrage. Le pare-balles est du vitrage technique, et le
trempé émaillé suppose un four avec ligne d'émaillage, donc un investissement lourd et un atelier qui
tourne. **Des transformations à forte valeur exigent un float d'entrée de qualité constante.**
**Pourquoi un appel :** `info.sotraglace@gmail.com` ne figure que dans les **données structurées** de
Kompass, et la société n'a **aucun site officiel** — la réserve exacte qui a fait rebondir Conciera.
**OBJECTIF UNIQUE :** une adresse donnée par eux, et trancher l'adresse postale, qui diffère selon la
source (Sidi Bernoussi chez l'un, Aïn Sebaâ chez l'autre).

---

## Les dix suivants, dans l'ordre

| # | Société | Téléphone | Créneau Paris | Objectif unique |
|---|---|---|---|---|
| 6 | **Adriatic Glass** (Concord, Ontario) | +1 905 738 1587 | 15 h – 22 h | Leur page feuilleté annonce traiter les **commandes en volume**, prix au volume à demander aux ventes. Leur `sales@` **refuse le courrier externe** (`550 5.4.1`), donc la voie est **le téléphone ou leur formulaire** — obtenir la route d'achat |
| 7 | **Somaver** (Casablanca) | +212 5 22 35 05 66 | 10 h – 17 h | ⚠️ **réserve qui l'affaiblit** : le web la classe nettement en **pare-brise**, Kompass disait automobile *et* bâtiment. **Trancher la part bâtiment avant de dépenser un argumentaire** |
| 8 | **Disk Vidros** (Francisco Beltrão, PR) | +55 46 3524-1517 | 14 h – 18 h | Fabrication de trempé, feuilleté **et miroirs**. Page de contact sans adresse, les trois qui circulent viennent de tiers — obtenir l'adresse de la société |
| 9 | **North Africa for Importing Glass** (Libye) | +218 91 209 1023 | 9 h – 15 h | **« Importing Glass » est dans sa raison sociale** : le profil est déclaré. Dimanche-jeudi, donc lundi ouvré |
| 10 | **Agroleite** (Ibirá, SP) | 0800 351 9090 | 14 h – 18 h | Cabines de tracteur, mais **fours courbes ET plans** en propre, qui se nourrissent de float brut. ⚠️ **le volume est l'objet de l'appel** : un cabiniste achète en palettes et le §4 limite aux conteneurs complets |
| 11 | **Al Aliyat Glass Factory** (Oman) | +968 93021153 | 9 h – 13 h | Usine. Dimanche-jeudi |
| 12 | **Glasscorp LLC** (West Palm Beach) | +1 813 760 1136 | 15 h – 22 h | **Établir le domaine** : trois circulent, et `glasscorplnt` est probablement une lecture fautive de `glasscorpint` — mais le §5 interdit d'envoyer sur une hypothèse d'orthographe. ⚠️ 1 à 10 salariés, fondée 2023 |
| 13 | **Venster Egypt** (Le Caire) | +20 121 000 7500 | 8 h – 16 h | Aluminium et verre. Dimanche-jeudi |
| 14 | **Alusupra** (Palhoça, SC) | +55 48 3242-3473 | 14 h – 18 h | **Une seule question, et rien d'autre : portent-ils du verre au catalogue ?** C'est un **extrudeur d'aluminium** qui vend aux *vidraçarias*, donc il vend à nos clients. Huit succursales laissent un doute. **Pas d'argumentaire avant la réponse** |
| 15 | **Vitrosak** (Algérie) | +213 560 53 51 68 | 9 h – 16 h | Dimanche-jeudi. ⚠️ l'Algérie est un **marché téléphonique** : 3 sociétés sur 3 sans domaine propre indexé mais avec de bons numéros |

---

## Les trois appels d'IDENTITÉ — à passer avant tout envoi sur ces comptes

Ce ne sont pas des appels commerciaux. **Leur seul objet est de savoir si deux fiches sont une seule
société**, et tant qu'ils ne sont pas passés, **aucun envoi** : ce serait la faute Shibaam.

1. **First Glass / Technical Aluminum** (Amman) — **téléphone partagé**. Et la leçon est fraîche : j'ai
   écrit le 11/10 à *The First for Glass Industries* alors que le registre portait déjà *First Glass* à
   la même adresse.
2. **Cayman Glass / Arch Glass** — **boîte postale partagée**.
3. **GLASSIVOIRE / IVOIR GLASS / « Glass Ivoir »** (Abidjan) — **trois libellés** pour peut-être deux
   sociétés. C'est le motif des mêmes mots dans un ordre différent, celui de *Miroiterie des Antilles*
   contre *Antilles Miroiterie* : jamais un hasard.

---

## Ce qu'un appel ne doit JAMAIS faire (§5)

- **Aucun prix, aucun délai, aucun certificat, aucune condition non validée.** Formule imposée : « nous
  pouvons établir une offre pour la livraison à votre port de destination, **sous réserve de validation
  de notre côté** ».
- **Ne jamais nommer nos usines partenaires**, ni leur pays, ni leur nombre.
- **Ne jamais se présenter comme trader ou négociant** : **fournisseur de verre plat**.
- **Ne jamais affirmer qu'un pays n'a pas de production float sans avoir vérifié.** C'est l'argument qui
  se retourne le plus vite, et `verif-argument-float.py` existe pour cela.
