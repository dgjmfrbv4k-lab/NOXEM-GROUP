# Où dépenser les appels de recherche — refait le 11/10/2026 à 21h35

**Remplace entièrement la version du 08/10.** Sa prémisse était « les 26 fiches en rebond avec un
domaine propre, jamais retestées, c'est le meilleur gisement établi ». **Ce gisement est épuisé** et
le fichier devenait trompeur.

## LE FAIT QUI COMMANDE TOUT LE RESTE : LE DÉVERROUILLAGE EST TERMINÉ

Mesuré au registre ce soir, et c'est net :

```bash
# fiches avec un site, sans adresse, jamais testees
awk -F';' 'NR>1 && $6!="" && $7=="" && $9 !~ /TESTEE|DEVERROUILLEE/ && $10 !~ /^(ECARTE|NE PAS)/' liste-prospects.csv | wc -l
# fiches en rebond avec un site
awk -F';' 'NR>1 && $6!="" && ($10=="A RENVOYER" || $10=="ADRESSE INVALIDE")' liste-prospects.csv | wc -l
```

**95 fiches ont un site et pas d'adresse. 91 sont déjà marquées `TESTEE` ou `DEVERROUILLEE`.** Le §13
annonçait le 08/10 « de l'ordre de 70 adresses encore à prendre » : elles ont été prises.

**Les six fiches restantes, et chacune a un motif de ne pas y retourner :**

| Fiche | Motif |
|---|---|
| Commercial Glass & Aluminium (Bermudes) | ne remonte **aucune** page — le rebond disait vrai |
| Vitrolux (Côte d'Ivoire) | signature Vitrolux du §13 : site vivant, hébergement courrier abandonné. **Irrécupérable** |
| Vicar (Portugal) | Europe → pas de nouvelle prospection (§6) |
| Arte Vidro Moçambique | Mozambique est un marché d'export **documenté** de Sapphire → déclassé (§6) |
| Conciera (Maroc) | un rebond sur données structurées. **Un seul essai reste permis**, à faire seul |
| PG Centre Zimbabwe | `A VALIDER AARON` — relève du compte protégé PG Glass (§7). **Ne pas toucher** |

## DONC LE SEUL LEVIER QUI RESTE EST LA RECHERCHE DE CATÉGORIE — et c'est mesuré, pas supposé

**Sur le vivier marocain, chercher les fiches du registre une par une a rendu ZÉRO adresse utilisable
en quatre fiches travaillées. Deux recherches de catégorie ont rendu trois sociétés neuves avec site
indexé et adresse publiée.** Même résultat sur le Brésil le même soir : deux fiches neuves prêtes à
l'envoi plus une identité résolue, là où les noms du registre ne rendaient rien.

**La méthode, en deux appels :**
1. **Chercher le MÉTIER et le PAYS**, pas un nom — « importateur distributeur grossiste verre plat
   conteneur <pays> », dans la langue du pays. **Bloquer les annuaires ET les courtiers** dès le
   premier appel : sans cela ils occupent la moitié des résultats.
2. **Greper chaque nom rendu** — le plus court élément distinctif, jamais une concaténation — puis
   recherche restreinte au domaine de ceux qui sont absents.

**Et le corollaire, qui évite de gaspiller un tour :** la recherche de catégorie **retrouve surtout
des fiches du registre** dans les pays déjà denses. Sur les États-Unis et le Brésil ce soir, cinq des
huit sociétés rendues y étaient déjà, dont quatre déjà contactées — New Glass, NSA Vidros, Mundial
Vidros, American Pro Glass et GGI. C'est la leçon Ouganda du §5 : **le chiffre utile n'est pas le
nombre de sociétés trouvées, c'est le nombre de sociétés absentes du registre.**

## LES DEUX PISTES À OUVRIR EN PREMIER, et elles valent plus que des fiches

### 1. L'annuaire des membres d'ABRAVIDRO — la meilleure piste brésilienne

`abravidro.org.br/empresas-associadas/` publie la liste de ses membres, avec une page par société.

**ABRAVIDRO n'est PAS ABIVIDRO, et confondre les deux ferait prendre un client pour un adversaire.**
· **ABIVIDRO** = association des **industries** du verre, donc les **producteurs**. C'est elle qui
  demande les droits antidumping brésiliens cités au §6, et dont le recours a été rejeté par la
  Gecex 961.
· **ABRAVIDRO** = association des **distributeurs et transformateurs** de verre plat. **C'est notre
  clientèle, nommément listée.** Les deux noms ne diffèrent que de deux lettres.

**⚠️ CORRECTION MESURÉE LE 11/10 À 22h00, SUR SIX FICHES DE CE VIVIER — l'appartenance à ABRAVIDRO
OUVRE une fiche, elle ne la QUALIFIE pas.** J'avais écrit en créant ces fiches que le test du §5 était
satisfait *par construction*, le verre **plat** étant dans l'objet de l'association. **C'est vrai pour
la question plat contre creux, et c'est insuffisant : cela n'établit pas que le membre ACHÈTE du verre
plat.** Une association professionnelle admet aussi ses **fournisseurs**.
· **Abrasipa** est une **industrie d'abrasifs** : elle a bien une page « Soluções em Vidro », et elle y
  vend des abrasifs de **polissage du verre**. Fournisseur du secteur, pas acheteur. Fermée.
· **Alusupra** est un **extrudeur de profils d'aluminium** qui vend aux *vidraçarias* : elle vend
  l'aluminium à nos clients, c'est le vitrier qui apporte le verre. En attente d'un appel.
**Deux sur six sont tombées sur ce motif.** Donc le premier temps doit établir que la société
**transforme ou distribue** du verre, et non qu'elle vend quelque chose **à** ceux qui le font.

**Ce n'est pas un courtier de données** au sens du §5 : rien n'est vendu, c'est l'annuaire public
d'un syndicat professionnel. Mais ses pages sont des pages de tiers, donc l'adresse qu'elles donnent
ne satisfait pas la règle anti-rebond — **elles servent à obtenir le NOM et le DOMAINE**, et l'adresse
se prend ensuite sur le site de la société. C'est le premier temps de la méthode, déjà fait pour nous.
Repéré via la page membre de Penha Vidros.

### 2. La liste des importateurs américains de float, déposée au dossier C-570-189

`harris-sliwoski.com/wp-content/uploads/Float-Glass-importers.pdf` — **liste d'importateurs
américains de float déposée le 21/11/2024** au dossier **C-570-189**, l'affaire de droits
compensateurs sur le float chinois. Noms déjà lus dans les résultats : **Rapid Shower and Mirror Corp**
(Medley, FL), **MunnWorks** (Mount Vernon, NY), **Glasscorp** (West Palm Beach, FL), **WHTB Glass**,
**310 Tempering**, **All Kind Glass Shower Doors**. Les quatre premiers sont **absents du registre**
(grep fait : `rapid`, `munn`, `glasscorp`, `glass and metals`, `synergy`).

**Pourquoi c'est la meilleure liste de prospects de la campagne, et ce n'est pas une opinion :** ce
sont des sociétés dont il est **établi au dossier** qu'elles importent du float, et dont l'origine
d'approvisionnement vient d'être frappée le 06/04/2026 à **181,52 %** en antidumping plus **19,75 à
113,34 %** en compensateur. Leur chaîne d'achat est cassée, l'Europe n'est visée par aucun de ces
droits, et le §6 note que c'est l'importateur américain qui **paie** ces droits.

**Ce n'est pas un courtier de données :** c'est une pièce de procédure publique publiée par un cabinet
d'avocats, pas un relevé douanier vendu. Le §5 vise les services qui **vendent** des relevés
d'importation ou des contacts d'acheteurs ; celui-ci ne vend rien.

**LA LIMITE EST TECHNIQUE ET ELLE EST BLOQUANTE ICI : c'est un PDF, et aucun des trois chemins
(`curl`, `WebFetch`, DNS direct) n'atteint un fichier hors liste blanche** (§13). Je n'ai donc que
les noms que la recherche a bien voulu citer, **pas les colonnes adresse, téléphone et e-mail que le
document contient**. La liste complète demande l'accès réseau.

**→ C'est l'argument le plus concret à verser à la demande du réglage « Network access » (§13) :** un
document public, nominatif, qui liste précisément notre cible sur notre meilleur marché, et qui est à
deux clics d'un navigateur ordinaire. Réserve à dire : dépôt de novembre 2024, donc coordonnées à
revérifier une par une.

## CE QUI RESTE, PAR VALEUR DÉCROISSANTE

1. **Les deux pistes ci-dessus.**
2. **États-Unis (43 fiches), Brésil (14), Canada (61)** — les trois marchés où l'argument douanier
   est vérifié et favorable. Recherche de catégorie, pays par pays, en bloquant les annuaires.
3. **Les six fiches téléphoniques de valeur du Maroc** — Ouchtar, Sotraglace, Somaver, Alumgo,
   Med Glass, Metal Tanger. Coordonnées complètes dans les notes, **plus rien à chercher sur le web**.
4. **Ce qu'il ne faut PAS rechercher :** Kenya, Ouganda, Madagascar, Rwanda, Mozambique, Zambie,
   Malawi, Congo RDC (desservis par Sapphire, §6) · Inde (marché à 374 $/t, hors de portée) ·
   Nigéria (CNG Glass, capital chinois donc sans droit face à nous) · Égypte, Arabie saoudite,
   Émirats (float local abondant) · Europe (§6) · Chine, Hong Kong, Macao, France métropolitaine.
