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

La raison évidente est la réputation du domaine (§10, §13). Mais il y en a une seconde, qui change
la composition des vagues : **vingt messages longs de structure identique partis dans la même
heure, c'est le profil que les filtres anti-spam cherchent.** Un mélange de relances courtes et de
premiers contacts longs et différents ressemble à du trafic humain.

Donc **chaque vague mélange les deux** : 3 relances courtes + 2 premiers contacts, plutôt que
5 messages de même forme. Ce n'est pas seulement prudent, c'est mieux ciblé.

---

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

### Lundi 13/10 et au-delà

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
