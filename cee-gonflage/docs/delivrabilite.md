# Délivrabilité — diagnostic et mise en conformité

Constat établi le 16/09/2026 à partir de la boîte connectée à l'outil.

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

## La mise en conformité, dans l'ordre

### 1. Envoyer depuis le bon domaine

Configurer `aaron.harfi@noxemgroup.com` comme véritable compte d'envoi, et non comme
simple signature. Avec Google Workspace, l'adresse professionnelle devient l'expéditeur
réel et le décalage disparaît.

### 2. Publier les trois enregistrements d'authentification

À créer dans la zone DNS de `noxemgroup.com`. Les valeurs dépendent de l'hébergeur de
messagerie ; celles-ci valent pour Google Workspace.

| Type | Nom | Valeur |
|---|---|---|
| TXT | `@` | `v=spf1 include:_spf.google.com ~all` |
| TXT | `google._domainkey` | la clé publique générée dans la console Workspace (Applications → Gmail → Authentifier les e-mails) |
| TXT | `_dmarc` | `v=DMARC1; p=none; rua=mailto:dmarc@noxemgroup.com; pct=100` |

Commencer DMARC en `p=none` : cette politique observe sans rien bloquer. Après deux à
quatre semaines de rapports propres, passer à `p=quarantine`, puis `p=reject`.

Sans ces trois enregistrements, les grands fournisseurs classent d'office un domaine
récent qui envoie du volume.

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
