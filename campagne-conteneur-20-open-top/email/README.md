# Modèle d'e-mail — campagne conteneur

| Fichier | Rôle |
|---|---|
| `modele-fr.html` | Le message, version HTML. Tables et styles en ligne : tient dans Gmail, Outlook, Apple Mail. |
| `modele-fr.txt` | La version texte, à envoyer en alternative — elle évite le classement en spam. |
| `noxem-logo.png` | Le logo, 181 × 60 px, 2 Ko. À joindre en pièce inline sous le nom `noxem-logo.png` : le HTML le référence par `cid:noxem-logo.png`. |
| `banniere-image.png` | La même bannière sous forme d'image unique, 1200 × 420 px, si un outil d'emailing exige une image plutôt qu'un bandeau HTML. |

## Pourquoi la bannière est en HTML et non en image

Une bonne partie des messageries bloquent les images par défaut. Un bandeau
construit en tableaux et couleurs de fond s'affiche toujours : l'accroche
« Votre livraison à votre port, en conteneur complet » reste lisible même
images coupées. Seul le logo est une image, et son texte alternatif prend le
relais s'il ne charge pas.

## Champs à remplacer pour chaque destinataire

Le modèle est volontairement sans nom de société : il s'envoie tel quel. Pour
le personnaliser, remplacer `Bonjour,` par la formule d'appel du pays et
insérer l'accroche métier — la console `../prospection.html` produit ces deux
éléments dans la langue du destinataire.

## Avant l'envoi en nombre

- Authentifier le domaine d'envoi (SPF, DKIM, DMARC) sinon les messages
  partent en indésirables.
- Monter en volume progressivement depuis une adresse neuve.
- Tenir à jour la liste des sociétés qui ont répondu « STOP ».
