# Lancer la campagne

Il manque une seule chose pour envoyer : **les adresses**. Les fichiers de
campagne contiennent les pays, les ports, les langues et le message — pas les
sociétés. Elles se constituent marché par marché, et c'est là que la campagne
se gagne ou se perd.

## Les deux fichiers

| Fichier | À quoi il sert |
|---|---|
| `liste-a-remplir.csv` | Le format attendu. Une ligne par société : `societe ; pays ; interlocuteur ; email ; port`. Seules les deux premières colonnes sont obligatoires. |
| `pays-cibles.csv` | Les 171 pays à l'export, par région, avec la langue du message, les ports, le transit indicatif, les alertes et une note de marché. C'est la feuille de route pour chercher. |

Le pays s'écrit en toutes lettres ou en code ISO — `AE`, `CI`, `HR`. Laissez le
port vide et le premier port du pays sera pris.

## Où trouver les sociétés

- **Europages, Kompass** — recherche par activité et par pays : miroiterie,
  transformation du verre, menuiserie aluminium.
- **Listes d'exposants des salons** : glasstec (Düsseldorf), Zak Glass (Inde),
  Glass Expo Middle East, Big 5 (Dubaï), Batimatec (Alger). Publiques et à jour.
- **Chambres de commerce et fédérations nationales** du verre et de la menuiserie.
- **LinkedIn Sales Navigator** — pour trouver l'interlocuteur plutôt que
  l'adresse générique `info@`.
- **Statistiques douanières d'importation** — codes SH 7005 (float), 7007
  (feuilleté), 7009 (miroirs) : elles disent quels pays importent vraiment.

Commencez par un marché, pas par cent. Trente sociétés aux Émirats traitées
sérieusement valent mieux que mille adresses ramassées partout.

## Puis

1. Remplir `liste-a-remplir.csv`.
2. Ouvrir `../prospection.html`, onglet **Série de sociétés**, coller les lignes.
3. **Générer**, puis **Télécharger le CSV** : il contient l'objet, le HTML, le
   texte et le WhatsApp, chacun dans la langue du pays.
4. Importer ce CSV dans la plateforme d'envoi et lancer le publipostage.

## Avant le premier envoi en nombre

- **Authentifier le domaine** : SPF, DKIM et DMARC sur `noxemgroup.com`. Sans ça,
  tout part en indésirables, quel que soit le message.
- **Une plateforme d'envoi**, pas une boîte personnelle : Brevo, Mailchimp,
  Lemlist. Une messagerie ordinaire plafonne vers 500 messages par jour et se
  fait bloquer bien avant.
- **Monter en volume progressivement** : quelques dizaines par jour la première
  semaine, puis doubler. Une adresse neuve qui envoie mille messages le premier
  jour est grillée le lendemain.
- **Faire relire les 21 langues marquées** `"q":"check"` dans `../data/emails.js`.
- **Tenir la liste des « STOP »** et ne jamais y revenir.
