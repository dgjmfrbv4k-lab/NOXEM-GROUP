# Délivrabilité — diagnostic et mise en conformité

Constat établi le 16/09/2026 à partir de la boîte connectée à l'outil, complété par un
relevé du DNS public de `noxemgroup.com` (voir « État réel du domaine » plus bas).

## Ce qui se passe aujourd'hui

| Constat | Détail |
|---|---|
| **Expéditeur réel** | `harfiaaron0@gmail.com` — une adresse Gmail personnelle. |
| **Signature des messages** | `aaron.harfi@noxemgroup.com` et `www.noxemgroup.com`. |
| **Volume** | environ **200 messages envoyés dans la journée**. |
| **Adresses visées** | adresses génériques (`info@`, `kontakt@`) collectées par domaine. |
| **Retours** | au moins un rejet dur constaté : `550 5.2.1 Account disabled`. |

Chacun de ces points, pris isolément, est une pratique courante. Réunis, ils forment
exactement le profil que les filtres anti-spam sont conçus pour arrêter.

## Pourquoi les messages n'arrivent pas

**1. L'expéditeur ne correspond pas à la signature.** Le message part d'une adresse
Gmail personnelle mais signe au nom d'un domaine professionnel. C'est le premier signal
que cherche un filtre : une usurpation d'identité a exactement cette forme. Un
destinataire attentif le voit aussi, et cela coûte la crédibilité au pire moment.

**2. Une boîte Gmail gratuite n'est pas faite pour ça.** Le plafond se situe autour de
500 destinataires par jour, et il ne s'agit pas d'une limite qu'on peut frôler
impunément : au-delà d'un certain rythme, l'envoi est suspendu, parfois le compte
entier. À 200 messages dans l'après-midi, le seuil est proche.

**3. Les rejets durs sont comptés.** `550 Account disabled` signifie que l'adresse
n'existe plus. Un taux de rejet élevé est le principal critère de dégradation de
réputation : plus il monte, plus les messages suivants partent en indésirables — y
compris ceux envoyés à des adresses parfaitement valides.

**4. Le risque se transmet au domaine.** Signer des envois massifs au nom de
`noxemgroup.com` associe ce domaine, encore récent, à un comportement d'envoi dégradé.
Un domaine grillé ne se répare pas : il se remplace.

## État réel du domaine `noxemgroup.com`

Relevé dans le DNS public. À revérifier après chaque modification :

```bash
node outils/verifier-domaine.mjs noxemgroup.com
```

| | Valeur relevée | Verdict |
|---|---|---|
| **Hébergeur mail** | `mx10/20/30.antispam.mailspamprotection.com` → SiteGround, via un revendeur (NS : `french-connexion.com`, `domaine.fr`) | — |
| **SPF** | `v=spf1 +a +mx include:noxemgroup.com.spf.auto.dnssmarthost.net ~all` | présent ✓ |
| **DKIM** | sélecteur `default`, clé **1024 bits** | présent, mais faible |
| **DMARC** | `v=DMARC1; p=none; rua=mailto:rua@dmarc.brevo.com` | présent, sans application |

**Bonne nouvelle : les trois piliers existent déjà.** Le domaine n'est pas nu. Ce n'est
pas ce qui explique les problèmes rencontrés jusqu'ici — l'envoi se faisait depuis une
adresse Gmail personnelle, pas depuis ce domaine.

### Le défaut grave : Brevo à moitié configuré

Le DNS porte un `brevo-code:…` de validation, et les rapports DMARC partent vers
`rua@dmarc.brevo.com`. Un compte **Brevo** a donc été branché sur le domaine. Mais le
SPF **ne contient pas** `include:spf.brevo.com`, et aucun sélecteur DKIM Brevo n'existe
(`mail._domainkey`, `brevo._domainkey` : absents).

Conséquence concrète : **tout envoi passant par Brevo échoue à l'authentification.**
La plateforme affiche le domaine comme validé, l'envoi part, et il arrive en spam ou
il est rejeté. Deux issues, au choix :

- **Brevo ne sert plus** → retirer le TXT `brevo-code:…` et reprendre la main sur les
  rapports DMARC (`rua=mailto:dmarc@noxemgroup.com`) ;
- **Brevo doit servir** → ajouter `include:spf.brevo.com` au SPF et publier la clé DKIM
  fournie par Brevo.

## La mise en conformité, dans l'ordre

### 1. Corriger les trois enregistrements existants

À modifier dans la zone DNS, chez le revendeur qui gère `french-connexion.com` /
`domaine.fr` :

| Type | Nom | Valeur à poser | Pourquoi |
|---|---|---|---|
| TXT | `@` | `v=spf1 +a +mx include:noxemgroup.com.spf.auto.dnssmarthost.net -all` | `~all` → `-all` : le softfail laisse passer les usurpations. À ne passer en `-all` qu'une fois certain qu'aucun autre service n'envoie en votre nom. |
| TXT | `default._domainkey` | clé **2048 bits** régénérée côté hébergeur | 1024 bits est en fin de vie ; certains fournisseurs commencent à l'ignorer. À demander au support. |
| TXT | `_dmarc` | `v=DMARC1; p=none; rua=mailto:dmarc@noxemgroup.com; pct=100` | Reprendre les rapports : aujourd'hui ils partent chez Brevo et vous ne les voyez pas. |

Puis, après deux à quatre semaines de rapports propres : `p=quarantine`, et enfin
`p=reject`.

### 2. Ne pas envoyer la prospection depuis la boîte principale

C'est le point structurel, et il découle de l'hébergeur relevé.

La messagerie est sur une **mutualisée SiteGround**. Deux limites qui comptent :

- le SMTP mutualisé plafonne bas (de l'ordre de quelques centaines de messages par
  heure), et le démarchage à froid en volume sort de ce que ces offres autorisent ;
- l'IP d'envoi est **partagée** avec d'autres clients : la réputation ne dépend pas
  seulement de vous.

`noxemgroup.com` est l'adresse qui reçoit les réponses, signe les devis et porte les
dossiers CEE. **C'est l'outil de travail des prochaines années — il ne doit jamais
servir de domaine de test.**

La pratique standard du démarchage à froid en volume : des **domaines secondaires**
dédiés à l'envoi, qui redirigent vers le site principal. Vérification faite, ils sont
libres :

| Domaine | État |
|---|---|
| `noxem-group.com` | libre |
| `noxemgroup.fr` | libre |
| `noxem-group.fr` | libre |
| `noxemgroup.net` | libre |

**Le montage pour 150 par jour :** 2 domaines secondaires × 2 boîtes chacun = 4 boîtes
à ~38 messages. Chaque domaine avec son SPF, son DKIM 2048 et son DMARC, chauffé trois
semaines. Si un domaine secondaire se fait classer, il est remplaçable — le principal
n'est jamais exposé.

Coût indicatif : une dizaine d'euros par domaine et par an, plus les boîtes.

### 3. Chauffer le domaine progressivement

Un domaine neuf qui envoie 200 messages le premier jour est traité comme une source de
spam. La montée en charge se fait sur trois à quatre semaines :

| Période | Volume quotidien |
|---|---|
| Jours 1 à 3 | 10 à 20 messages |
| Jours 4 à 7 | 30 à 40 |
| Semaine 2 | 50 à 80 |
| Semaine 3 | 100 à 150 |
| Ensuite | 200 et plus, si le taux de rejet reste bas |

Une réponse obtenue vaut mieux que dix envois : les interactions positives
(ouvertures, réponses) construisent la réputation aussi sûrement que les rejets la
détruisent.

### 4. Vérifier les adresses avant d'envoyer

Ne jamais deviner une adresse. Un `contact@` inventé qui rebondit coûte plus cher que
l'envoi ne rapporte. Deux règles simples :

- prendre l'adresse sur la page « contact » du site de l'entreprise, jamais par
  déduction sur le modèle `prenom.nom@` ;
- viser un **taux de rejet inférieur à 2 %**. Au-delà de 5 %, arrêter la campagne et
  nettoyer la liste avant de reprendre.

### 5. Garder la trace des désinscriptions

La mention « répondez STOP » n'a de valeur que si les réponses STOP sont effectivement
retirées de la liste. Le statut « Refusé » du CRM sert à cela : un site qui a répondu
STOP ne doit jamais ressortir dans une série d'envois.

## Ce que cela change pour la prospection CEE

Tant que ces cinq points ne sont pas réglés, augmenter le volume ne fait qu'accélérer
la dégradation. Une fois réglés, les mêmes messages atteignent réellement leur
destinataire — et 25 messages qui arrivent valent infiniment mieux que 200 qui
finissent en indésirables.
