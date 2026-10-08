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

## Ajout du 08/10 a 15h45 — le lot du 10/10 sur les Ameriques

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
