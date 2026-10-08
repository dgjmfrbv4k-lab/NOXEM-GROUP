# Plan d'envoi — du 09/10/2026, et pourquoi dans cet ordre

**Le problème à résoudre.** Au soir du 08/10 il y a **56 fiches déverrouillées qui attendent un
premier envoi** et **une trentaine de relances échues** des 1er au 5 octobre. Cela fait environ
85 messages à faire partir. Une boîte Google Workspace sur un domaine de deux jours, sans DMARC,
et qui a déjà reçu **deux verdicts de spam de serveurs sans rapport** dans la journée, ne fait pas
85 envois en deux jours sans se faire filtrer. **Il faut donc arbitrer, et l'arbitrage est ici.**

---

## 1. L'ordre, et la correction d'une erreur de ma part

**Les relances échues passent d'abord. Les nouvelles adresses ensuite.**

J'avais écrit l'inverse dans le fichier du lot 2 — « une relance sur une adresse déjà jointe vaut
moins qu'un premier contact sur une adresse neuve ». **C'était faux, et doublement.**

- **Je n'ai aucune donnée de conversion** qui établisse ça. Zéro réponse qualifiée sur les envois
  des deux derniers jours ne permet de comparer ni l'un ni l'autre. C'était une intuition
  présentée comme un fait.
- **Le §2 du mandat dit le contraire** : la routine quotidienne met « faire les relances échues »
  en deuxième position, avant « chercher de nouveaux acheteurs qualifiés ». Je n'avais pas à
  réinventer cet ordre parce que j'avais de nouvelles adresses sous la main.

Et le fichier de relances donne l'argument qui tranche, et il est technique, pas théorique :
**ces adresses ont déjà pris livraison d'un message.** C'est la meilleure preuve de délivrabilité
dont on dispose, et elle compte double tant que le contrôle MX est impossible — `verif-mx.py`
renvoie `RESOLVEUR INDISPONIBLE` parce que la session ne résout que les hôtes de sa liste blanche.
Une adresse neuve, même publiée par la société, peut encore rebondir : six l'ont fait aujourd'hui.

---

## 2. Le rythme, et l'argument qui n'est pas qu'une précaution

**Vagues de 5, espacées dans la journée. 15 à 20 messages par jour au maximum.**

**Et il faut dire que c'est une RÉDUCTION, pas une prudence abstraite.** Compté dans le registre :
**le 08/10 a produit 104 messages** — 30 premiers contacts, 73 relances et une relance de demande
de devis — auxquels s'ajoutent les deux comptes vivants dont le statut n'a pas bougé. **Et deux
serveurs sans rapport ont rendu un verdict de spam dans la journée.** Passer de 104 à 18 n'est donc
pas de la frilosité : c'est la conséquence de ce que la journée a mesuré.

La raison évidente est la réputation du domaine (§10, §13). Mais il y en a une seconde, qui change
la composition des vagues : **vingt messages longs de structure identique partis dans la même
heure, c'est le profil que les filtres anti-spam cherchent.** Un mélange de relances courtes et de
premiers contacts longs et différents ressemble à du trafic humain.

Donc **chaque vague mélange les deux** : 3 relances courtes + 2 premiers contacts, plutôt que
5 messages de même forme. Ce n'est pas seulement prudent, c'est mieux ciblé.

---

## 2 bis. L'ordre a changé en fin de journée, et c'est la recherche qui l'a changé

**Le plan ci-dessous a été écrit avant les vérifications douanières de l'après-midi. Elles le
réordonnent, et il faut dire pourquoi plutôt que de réécrire en silence.**

La carte établie entre 14 h et 14 h 35 dit ceci : **l'Afrique se ferme, les Amériques s'ouvrent.**
L'Afrique de l'Est est **déjà** desservie par un producteur local qui exporte vers six pays.
L'Afrique de l'Ouest se ferme, avec une échéance incertaine d'un an. Les États-Unis, le Brésil et
le Mexique ont une production locale **plus** des barrières contre l'Asie — donc un prix de marché
élevé, et c'est là que notre prix a la meilleure chance.

**Trois priorités en découlent, et elles ne sont pas celles d'hier :**

1. **L'Afrique de l'Ouest d'abord, parce qu'elle a une horloge.** ALUTRACO à Cotonou — notre porte
   vers le Burkina, le Mali et le Niger —, TechnoGlass à Lagos et Gr8 Vision à Freetown partent
   dans la première vague. Ce sont les seules fiches de la file dont la valeur **diminue avec le
   temps**.
2. **Puis l'Amérique du Nord et le Brésil, parce que le prix y a le plus de marge.** Les 43
   relances canadiennes et les 26 américaines, sur les deux arguments vérifiés aujourd'hui, plus
   Conlumi au Brésil et les trois fiches américaines de la file.
3. **Le reste ensuite**, dans l'ordre déjà prévu.

**Et une chose à ne pas faire : aucun envoi dans la zone est-africaine.** Aucune fiche de la file
n'y est, c'est vérifié — mais les relances du reliquat en contiennent, et elles doivent en être
retirées ou réécrites sur le low-E, le miroir sans cuivre et le vitrage technique uniquement.

## 3. Le plan, jour par jour

### Jeudi 09/10 — 18 messages

| Vague | Contenu |
|---|---|
| 1 (matin) | **3 relances échues** du reliquat (les mieux notées) + **AGPAR** et **Vitelsa** (textes 1 et 2, déjà écrits) |
| 2 (matin) | **3 relances** + **Green Glass** et **Saudi American Glass** (textes 3 et 4) |
| 3 (après-midi) | **3 relances** + **Hydra Glass** et **Pang Luon** (textes 5 et 6) |
| 4 (après-midi) | **2 relances** + **Med Glass**, **ALUTRACO** (textes 7 et 8) |

Soit **11 relances et 8 premiers contacts**. Les 5 fiches à renvoyer (boîtes pleines du 07/10 :
Zrcalo réparée, FITglass, Vidriería Universal, Glass Camp, Arte Vidro, Visemex, Vidrios y
Cristales Guadalajara) s'insèrent dans les vagues : ce sont des renvois sur des adresses dont on
sait que le domaine accepte le courrier.

### Vendredi 10/10 — 18 messages, et le contrôle qui compte

**D'abord, avant tout envoi : recontrôler les rebonds du 08 et du 09.** Deux rebonds anti-spam
sont arrivés 1 h 36 et 1 h 55 après l'envoi hier, et celui de Willem **1 h 48** après. Un contrôle
immédiat ne prouve rien. **Si un `5.7.1` est venu d'un serveur nouveau, la journée s'arrête à la
vague en cours** (§10).

Puis : **Almacenes Vidrí**, **Alico Egypt** (textes 9 et 10), les **cinq australiennes** (socle
commun, textes 11 à 15), **Albitar**, **Sahara Glass**, **SOVEP**, **TechnoGlass**, **Mirodec**
(textes 16 à 20), mélangées avec le reste des relances.

### Lundi 13/10 et au-delà — et le lot canadien devient la priorité

**Le Canada passe devant le reste de la file, et c'est un changement de priorité du 08/10 14 h 20.**
61 fiches, dont **43 avec une adresse et déjà contactées**, et un argument neuf vérifié le même
jour : ~90 % du verre des fabricants canadiens vient des États-Unis, et cette frontière est passée
sous droits de 50 % dans les deux sens en sept semaines. Ce n'est pas un argument de prix, c'est un
argument d'origine unique — et il ne demande pas d'être moins cher que les Américains, seulement
d'exister. Texte prêt dans `a-envoyer/2026-10-10-canada-angle-tarifaire.md`.

**Pourquoi devant le reste de la file :** 43 relances sur des adresses dont on sait qu'elles ont
pris livraison, avec un argument qui n'était pas dans le premier message, cela vaut mieux que
30 premiers contacts sur des marchés où nous n'avons aucun angle neuf. C'est le même raisonnement
que celui qui met les relances avant les nouvelles adresses, appliqué au bloc le plus gros.

### Et les États-Unis juste derrière — 26 relances, sur un argument encore plus fort

**Trouvé le 08/10 en toute fin de journée, et il corrige un jugement que j'avais porté le même
après-midi.** J'avais déclassé les fiches américaines au motif que les États-Unis produisent leur
float. **C'est l'inverse qui compte :** depuis les ordres du 06/04/2026, le float chinois porte
~181 % de droits antidumping et le malaisien jusqu'à 102 % de droits compensateurs. **L'Europe n'en
porte aucun.** Les deux origines qui cassaient les prix viennent d'être sorties du marché, et les
acheteurs qui s'y fournissaient cherchent une autre origine maintenant.

26 fiches américaines ont une adresse et ont déjà reçu un message. Texte prêt dans
`a-envoyer/2026-10-10-etats-unis-angle-antidumping.md`.

**Ordre retenu : Canada d'abord, États-Unis ensuite.** Non pas que l'argument américain soit plus
faible — il est plus fort — mais parce que le lot canadien est plus gros (43 contre 26) et que
l'argument américain demande une vérification préalable : les ordres datent d'avril, et révisions
ou recours peuvent avoir bougé. **Une vérification avant la première vague américaine**, et si les
taux ont changé le texte change avec eux.

### Le reste, ensuite

Le reste de la file, dans l'ordre du fichier du lot 2, **plus les cinq fiches volontairement
datées au 13/10** : GlasPro et Northwestern Glass Fab (États-Unis, float produit sur place),
Réunivitre (poseur et non importateur), Göteborgs Byggnadsglas (planchers de verre et vitrines,
petite série) et Vidral Guatemala. **Une adresse ne justifie pas un envoi : c'est le ciblage qui
le justifie**, et ces cinq-là ont une adresse valide avec un ciblage faible.

**Et le 13/10 est aussi la date de deux relances datées :** Imagic Glass, dont Adam rentre de
déplacement le 9, et les réponses attendues de United Glass et Rubex.

---

## 4. Ce qui ferait sauter ce plan, dans le bon sens

**Le DMARC.** C'est la première demande du dossier d'Aaron, elle prend cinq minutes et elle porte
directement sur le facteur limitant : un enregistrement `TXT` sur `_dmarc` avec
`v=DMARC1; p=none; rua=mailto:aaron.harfi@noxem-group.com`. Si la délivrabilité s'améliore, le
plafond de 18 messages par jour monte, et les 85 messages passent en trois jours au lieu de cinq.

**Une grille de prix.** Elle ne changerait pas le rythme d'envoi, mais elle changerait la nature du
travail : quatre demandes de prix fermes attendent, et aucun de ces 85 messages ne vaut une seule
commande signée.

---

## Ajout du 08/10 a 15h00 — le lot du 10/10 sur les Ameriques

Quatre fiches deverrouillees ou corrigees en fin d'apres-midi, **textes integraux ecrits** dans
`a-envoyer/2026-10-10-ameriques-quatre-textes.md` :

| Societe | Pays | Adresse | Particularite |
|---|---|---|---|
| Glass Camp | Bresil | `vendas@glasscamp.com.br` | boite pleine prouvee existante, peut partir groupee |
| Grupo Visemex | Mexique | `ventas1@visemex.com.mx` | idem ; `venta1@` sans S en second essai seulement |
| Javalfer | Mexique | `lindavista@javalfer.com` | **a envoyer SEULE**, sortie de rebond sur `info@` |
| Vidrios Dellorto | Chili | `contacto@dellorto.cl` | **a envoyer SEULE**, sortie de rebond sur `info@` |

**Pourquoi deux envois isoles.** Javalfer et Dellorto sortent d'un rebond sur une autre boite du
meme domaine. Les mettre dans un lot ferait courir au domaine le risque d'un second rebond groupe,
et c'est exactement ce que le §10 demande d'eviter sur une boite neuve sans DMARC.

**Condition prealable, non negociable :** verifier au matin du 10/10 qu'aucun nouveau
`5.7.1 High probability of spam` n'est tombe depuis les deux du 08/10. Un seul verdict d'un serveur
nouveau et ce lot attend.

**Deux fiches de la file restent sans texte, et c'est un choix assume :** Vidrios y Cristales
Guadalajara (Mexique) et Arte Vidro Mocambique. La premiere merite un texte, elle est dans un
marche prioritaire — a ecrire avant le 10/10. La seconde est dans la zone que la decouverte de
Sapphire a declassee le 08/10 : elle attend, et ce n'est pas un oubli.

---

## Ajout du 08/10 a 15h25 — le lot outre-mer des 12 et 13/10

Textes integraux dans `a-envoyer/2026-10-12-outre-mer-trois-textes.md`.

| Societe | Territoire | Adresse | Date | Particularite |
|---|---|---|---|---|
| **Savima** | Guadeloupe + Saint-Martin | `accueil@savima.fr` | 12/10 | **seule, et en premier du lot** — 10 M EUR de CA, aluminier agree Technal, deux sites. Secours : `contact@glassalusxm.fr` |
| Univers du Verre | Guadeloupe + 4 autres | `contact@universduverre.fr` | 12/10 | seule, apres Savima. Page vieille de 3 ans |
| SXM Aluminium | Saint-Martin, Sint Maarten, St Barths | `sxmaluinstallation@outlook.com` | 13/10 | seule. Message court, volume d'abord. Orthographe de l'adresse a recopier exactement |

**Aucun des trois ne se groupe** : deux ont des pages anciennes dont l'adresse peut avoir vieilli,
le troisieme est sur un domaine exterieur.

**ET LA RESERVE NEUVE QUI VAUT POUR TOUT L'OUTRE-MER, a ne pas oublier au moment d'envoyer :**
l'octroi de mer externe s'applique a notre verre europeen a l'entree des DOM, en vertu de la loi du
2 juillet 2004, et les taux du chapitre 70 pour 2026 ne sont pas etablis. **Aucun mot sur la
fiscalite a l'entree dans ces messages** — ni « livraison dans l'Union sans droits », ni « meme
marche interieur ». La question est partie chez Aaron.

## Rappel de la mise au point du 08/10 a 15h15, qui change la verification prealable

J'avais ecrit qu'il fallait verifier qu'aucun nouveau `5.7.1` n'etait tombe. **Precision : c'est un
serveur NOUVEAU qui compte.** Un `5.7.1` repete depuis un serveur deja connu n'arrete rien et
autorise a continuer a volume mesure. Le seul verdict du 08/10 venait de `info@yemenglass.com`,
qui nous avait deja rejetes la veille — donc rien de neuf. Ce qui limitait les envois le 08/10
etait le volume deja parti, 104 messages contre les 15 a 20 du plan, et non le filtrage.

---

# MESURE DU 08/10 A 15h50 — LE VRAI RESERVOIR N'EST PAS LES NOUVELLES ADRESSES, C'EST LES RELANCES

**Chiffre mesure dans le registre, pas estime : 136 fiches sont a `ENVOYE` des 05, 06 ou 07/10 et
n'ont JAMAIS ete relancees.** A cote, la file de premiers contacts compte 75 fiches. **Le
reservoir de relances est donc presque deux fois plus gros que celui des envois neufs** — et une
relance coute moins cher a ecrire, porte sur une adresse dont la delivrabilite est deja prouvee, et
touche quelqu'un qui a deja vu notre nom une fois.

C'est aussi l'ordre que le §2 impose : **relances echues avant nouvelle prospection.** Je l'ai
respecte dans l'ordre des vagues, mais je n'avais pas mesure l'ampleur du gisement.

## Et sa concentration geographique tombe exactement sur la carte du jour

| Pays | Fiches a relancer | Ce que la carte du 08/10 en dit |
|---|---|---|
| **Canada** | **33** | pas de production float, 90 % venu des Etats-Unis, frontiere sous droits reciproques depuis le 22/08/2026 |
| **Etats-Unis** | **12** | antidumping de 181 % sur le float chinois, plus CVD. Parapluie de prix le plus haut de la campagne |
| Australie | 6 | derniere ligne float d'Australasie fermee, tout est importe |
| Mexique | 5 | quotas contre la Chine et la Malaisie, mais droit general de 35 % — question en attente |
| Bresil | 4 | antidumping Malaisie, Pakistan, Turquie confirme |
| Costa Rica, Guatemala, Panama, Colombie | 16 | Amerique centrale et Caraibe |

**Quarante-cinq fiches canadiennes et americaines a relancer, dans les deux marches que la
verification douaniere a promus aujourd hui.** Et les textes existent deja :
`a-envoyer/2026-10-10-canada-angle-tarifaire.md` (43 relances) et
`a-envoyer/2026-10-10-etats-unis-angle-antidumping.md` (26 relances), ecrits ce matin.

## Les dix plus urgentes, et ce ne sont pas celles-la

**Dix fiches sont a `ENVOYE` depuis le 01/10 ou le 02/10 — six a sept jours sans relance.**
Elles passent AVANT les quarante-cinq nord-americaines, pour une raison de calendrier et
non de valeur : **six des dix sont en Afrique de l'Ouest**, le seul marche de la campagne qui ait
une date. L'usine ghaneenne de KEDA annonce sa premiere ligne pour aout 2026, avec une incertitude
d'environ un an ; chaque semaine compte, et une relance a huit jours est encore credible la ou une
relance a trois semaines ne l'est plus.

| Depuis | Pays | Societe | Adresse |
|---|---|---|---|
| 01/10 | Maurice | G&S Aluminium Mauritius | `gnscontracting2023@gmail.com` |
| 02/10 | Burkina Faso | Tropicalu | `tropicalu@yahoo.fr` |
| 02/10 | Gambie | KJ Glass & Aluminium Co. Ltd | `kjglass@hotmail.com` |
| 02/10 | Ghana | Prime Glass Ghana | `info@primeglassghana.com` |
| 02/10 | Liberia | International Aluminum Factory (IAF) | `sales@iafliberia.com` |
| 02/10 | Nigeria | GLASSAL Nigeria Ltd | `info@glassalng.com` |
| 02/10 | Nigeria | GlassFusion | `info@glassfusion.ng` |
| 02/10 | Guyana | Glaze Manufacturing | `glazemanufacturing@gmail.com` |
| 02/10 | Nepal | Nepal Glass Udhyog | `nepalglasstech@gmail.com` |
| 02/10 | Nepal | Sky Light Pvt. Ltd. | `info@skylight.com.np` |

**Reserve sur les deux fiches nepalaises :** le Nepal depend de l'Inde pour son transit, et l'Inde
a mis le float clair de 4 a 12 mm en regime restreint avec prix minimum depuis le 18/08/2026. A
verifier avant d'ecrire si cette restriction touche le transit vers un pays tiers — si oui, la
relance n'a pas de sens et les deux fiches se declassent.

**CORRECTION IMMEDIATE DE CE QUE JE VENAIS D ECRIRE.** J'avais mis **Staklo Bakar** (Croatie,
`ENVOYE 2026-09-22`) en tete de ce tableau comme la plus urgente des relances — seize jours. **A
tort :** sa fiche porte deja une decision contraire, prise et motivee, et je ne l'avais pas lue
avant de compter. Leur relance conteneur est **volontairement reportee au 13/10**, parce qu'ils ont
recu le 07/10 un message de l'autre campagne et que deux messages en deux jours depuis le meme
expediteur nuiraient a la credibilite. Elle est donc retiree du tableau, qui compte **dix fiches**
et non onze.

**Et cela met le doigt sur un manque du vocabulaire des statuts, deja signale a Aaron :** une
relance volontairement differee n'a pas de statut pour le dire. Elle reste a `ENVOYE` avec sa
vieille date, donc **elle ressort comme echue dans tout comptage automatique** — y compris le mien,
il y a cinq minutes. Tant qu'un statut `RELANCE DIFFEREE <date>` n'existe pas, **lire la note avant
de compter une fiche comme en retard.** Le texte de sa relance du 13/10 est ecrit dans
`a-envoyer/2026-10-13-qatar-maroc-deux-textes.md`.

## L'ordre des envois, revise a 15h50

1. **Les 11 relances les plus anciennes**, Afrique de l'Ouest d'abord. Deux vagues de 5 et une de 1.
2. **Les 57 premiers contacts du 09/10**, textes prets.
3. **Les 45 relances nord-americaines** du 10/10, textes prets, angle tarifaire verifie.
4. Les lots des 10, 12 et 13/10 deja decrits plus haut.

**Et le rappel de volume, qui prime sur tout le reste :** 15 a 20 envois par jour, par vagues de 5
espacees. 104 le 08/10 etait trop pour un domaine de huit jours sans DMARC, et c'est cela, et non
le filtrage, qui a arrete les envois de l'apres-midi.

---

# LA PREMIERE VAGUE DE DEMAIN, NOMMEE — pour n'avoir rien a decider au moment d'envoyer

Ecrit le 08/10 a 15h55. **L'ordre des vagues etait decrit, les destinataires ne l'etaient pas.**
Une decision prise la veille vaut mieux qu'une decision prise la main sur le clavier.

## Vague 1 du 09/10 — les cinq relances les plus en retard, Afrique de l'Ouest d'abord

| # | Societe | Pays | Adresse | Depuis | Texte |
|---|---|---|---|---|---|
| 1 | **Prime Glass Ghana** | Ghana | `info@primeglassghana.com` | 02/10 | `2026-10-09-reliquat-relances.md` |
| 2 | **GLASSAL Nigeria Ltd** | Nigeria | `info@glassalng.com` | 02/10 | idem |
| 3 | **GlassFusion** | Nigeria | `info@glassfusion.ng` | 02/10 | idem |
| 4 | **International Aluminum Factory** | Liberia | `sales@iafliberia.com` | 02/10 | idem |
| 5 | **KJ Glass & Aluminium** | Gambie | `kjglass@hotmail.com` | 02/10 | idem |

**Pourquoi ces cinq et dans cet ordre.** Ce sont les plus anciennes relances reellement echues du
registre — sept jours — et **toutes les cinq sont en Afrique de l'Ouest**, le seul marche de la
campagne qui ait une date : l'usine ghaneenne de KEDA annonce sa premiere ligne pour aout 2026 avec
une incertitude d'environ un an. Une relance a sept jours est encore credible ; a trois semaines,
elle ne l'est plus. Le Ghana passe premier parce que c'est le pays ou l'usine se construit.

## Vague 2 du 09/10 — le reste des relances echues

Tropicalu (Burkina Faso), Glaze Manufacturing (Guyana), G&S Aluminium (Maurice), Nepal Glass Udhyog
et Sky Light (Nepal). **Reserve sur les deux nepalaises** : verifier avant d'ecrire si la
restriction indienne a l'importation du float 4-12 mm, en vigueur depuis le 18/08/2026, touche le
transit vers un pays tiers. Si oui, les deux fiches se declassent au lieu d'etre relancees.

## Vagues 3 et suivantes — les premiers contacts du 09/10

Les 57 fiches de `2026-10-09-textes-prets.md`, dans l'ordre du fichier, qui met l'Afrique de l'Ouest
en tete pour la meme raison d'horloge. **Plafond du jour : 15 a 20 envois au total**, vagues 1 et 2
comprises. Donc en pratique : les 10 relances, puis 5 a 10 premiers contacts, et on s'arrete.

## Les trois controles a passer AVANT le premier envoi

1. **Un `5.7.1` venu d'un serveur NOUVEAU depuis hier ?** Si oui, le lot attend. Un verdict repete
   depuis un serveur deja connu n'arrete rien — mise au point du 08/10 a 15h15.
2. **Les rebonds de la veille**, et seulement maintenant : le rebond Alma Glass du 08/10 a mis
   **1h41** a revenir, donc un controle immediat apres un lot ne prouve rien.
3. **Le registre avant chaque envoi**, societe par societe, comme l'impose le §5 — et non apres.
