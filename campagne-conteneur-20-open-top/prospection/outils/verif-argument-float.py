#!/usr/bin/env python3
"""Controle des affirmations du type « ce pays n a pas de production float ».

C est l argument le plus employe de la campagne, et c est aussi celui qui se
retourne le plus vite : un acheteur sait mieux que nous ce qui se produit chez
lui. Deux erreurs de ce type ont ete commises le 08/10 — le Kenya, alors que
Sapphire produit a Mkuranga et livre la zone, et le Chili, alors que le
paragraphe 6 de notre propre mandat nomme Vidrios Lirquen. Dans le cas de
Forpec le message etait deja parti.

Le script croise les notes du registre avec la liste des pays qui abritent ou
sont desservis par un producteur float, et signale toute fiche qui affirme le
contraire. Lecture seule.

A relancer apres chaque lot, et SURTOUT avant d employer cet argument dans un
message neuf.
"""
import io, re, sys

# Pays dont le §6 nomme un producteur, ou qu un producteur voisin dessert directement.
PRODUCTEURS = {
    'Arabie saoudite': 'Obeikan, Zoujaj, Guardian et Arabian United Float Glass (UFG) : quatre\n                        producteurs, le marche le mieux pourvu de la zone',
    'Algérie': 'Mediterranean Float Glass / Cevital',
    'Pakistan': 'Tariq Glass ET Ghani Glass, tous deux nommes producteurs-exportateurs de float\n                 incolore par la Resolution Gecex 833/2025 du Bresil, droit de 59,97 USD/t.\n                 Ghani ajoute le 12/10 : l entree ne nommait que Tariq, donc elle sous-estimait\n                 le marche. Source de dossier, pas annuaire.',
    'Bangladesh': 'PHP Float Glass et Nasir Float Glass Industries (premier float du pays, en\n                   service depuis 2005, complexe de Tangail, ~55 pour cent du marche local)',
    'Azerbaïdjan': 'Azerfloat',
    'Mexique': 'Vitro via Vidrio Plano de Mexico, et Guardian Industries de Mexico (float et miroir)',
    'Indonésie': 'Asahimas',
    'Chili': 'Vidrios Lirquén',
    'Colombie': "VIDRIO ANDINO, a Soacha (Cundinamarca), km 6,5 route Soacha-Mondonedo.\n"
                 "                Ajoute le 14/10 et c'etait un TROU : le paragraphe 6 declare la Colombie\n"
                 "                bon marche sur le miroir et ne nommait aucun producteur colombien.\n"
                 "                Saint-Gobain majoritaire, Pilkington et Grupo Sura minoritaires, et\n"
                 "                Tecnoglass est entre au capital en minoritaire. La societe se dit la\n"
                 "                SEULE usine float de Colombie. ~200 000 t/an et 3 a 10 mm a\n"
                 "                l'ouverture, chiffres vieux d'environ treize ans donc NON CITABLES ;\n"
                 "                leur catalogue annonce aujourd'hui 2 a 19 mm. Une seconde usine pres\n"
                 "                de Barranquilla etait annoncee pour 2021, achevement NON CONFIRME.\n"
                 "                Trouvee le 14/10 par la page /vidrioandino/ de Vidrios de la Sabana,\n"
                 "                qui en est distributeur.",
    'Argentine': 'VASA / Vidrieria Argentina (coentreprise NSG-Pilkington et Saint-Gobain depuis 1938, usines Llavallol et Los Cardales, Cardales ~900 t/j)',
    'Inde': 'Pioneer Float Glass et autres',
    'Tanzanie': 'Sapphire (Mkuranga)',
    'Vietnam': 'Phu My, CFG Ha Long',
    'Égypte': 'Sphinx Glass, Guardian',
    'Brésil': 'QUATRE producteurs, nommes comme producteurs du produit similaire domestique par la\n               Circular MDIC 36 du 26/07/2024 qui ouvre l enquete antidumping float : AGC, CEBRACE,\n               GUARDIAN et VIVIX. Vivix a Goiana (PE), ~900 t/j, seul float a capital 100 pour cent\n               national. Cebrace est la coentreprise Saint-Gobain/NSG, usines Jacarei, Cacapava et\n               Barra Velha. AGC ajoute le 12/10 : l entree n en nommait que deux, donc elle\n               sous-estimait de moitie le marche le plus favorable de la campagne.',
    'Thaïlande': 'production float nationale',
    'Nigéria': 'CNG Glass (Igbesa, 500 t/j, en production depuis le 18/10/2019)',
    'Afrique du Sud': 'PFG Building Glass',
    'Kenya': 'Sapphire livre la zone depuis la Tanzanie',
    'Ouganda': 'Sapphire livre la zone',
    'Zambie': 'Sapphire livre la zone',
    'Malawi': 'Sapphire livre la zone',
    'Mozambique': 'PFG et Sapphire livrent la zone',
    'Namibie': 'PFG en Afrique du Sud',
    'Botswana': 'PFG en Afrique du Sud',
    'Bolivie': 'VASA y opere directement (groupe NSG-Pilkington / Saint-Gobain, present en Argentine, Bolivie, Paraguay et Uruguay)',
    'Paraguay': 'VASA y opere directement (groupe NSG-Pilkington / Saint-Gobain, 4 pays)',
    'Uruguay': 'VASA y opere directement (groupe NSG-Pilkington / Saint-Gobain, 4 pays)',
    # AJOUTS DU 12/10 — trois trous du dictionnaire, dont un que le paragraphe 6 interdisait
    # explicitement sans que le code puisse le faire respecter.
    'Émirats arabes unis': 'Emirates Float Glass (Abou Dabi, 600 t/j depuis 2009, Dubai Investments, '
                           'exporte vers plus de 65 pays) et Guardian. Le paragraphe 6 INTERDIT d y '
                           'employer l argument du float absent, et le garde-fou ne le couvrait pas',
    'Malaisie': 'Kibing Glass Malaysia, NSG Malaysian Sheet Glass et Jinjing Technology Malaysia, '
                'les trois nommes a la liste des producteurs du dossier float glass americain',
    'États-Unis': 'Vitro Flat Glass et Vitro Meadville, petitionnaires de la mesure de 2026, plus '
                  'Guardian, PPG et Fuyao Glass America. L argument americain est DOUANIER et non '
                  'celui de l absence d offre',
    # AJOUTS DU 14/10 — L EUROPE N AVAIT AUCUNE ENTREE, ET C ETAIT LE TROU LE PLUS BEANT
    # DU DICTIONNAIRE : 24 fiches allemandes, 15 belges, 9 neerlandaises, 1 suisse et 1
    # luxembourgeoise ont ete ouvertes ou travaillees ce jour-la, et le garde-fou ne
    # pouvait rien dire d aucune. Le paragraphe 6 ferme l Europe a la NOUVELLE prospection
    # mais autorise les relances, et ce lot-ci a ete ouvert sur consigne expresse de Kevin
    # au titre de la proximite de l entrepot : les fiches existent donc, et l argument peut
    # y etre employe par inadvertance.
    #
    # PRINCIPE RETENU, ET IL EST ASYMETRIQUE : une entree de TROP coute un argument qu on
    # s interdit a tort ; une entree MANQUANTE coute un message faux a un acheteur qui sait
    # mieux que nous ce qui se produit chez lui. On penche donc vers l inclusion — en disant,
    # pour chaque pays, ce qui est ETABLI et ce qui ne l est pas, afin que le garde-fou n ait
    # pas l air de crier au loup. C est la lecon du 09/10 sur Klingshield et celle du 12/10
    # sur les huit faux positifs.
    'Luxembourg': 'GUARDIAN y produit du float, sites de Bascharage, Dudelange et Grevenmacher. '
                  'Trouve le 14/10 en ouvrant le marche luxembourgeois, qui ne comptait qu une '
                  'fiche. Guardian est sur la liste des concurrents du paragraphe 6 depuis le '
                  'debut, mais le lien avec le Luxembourg n y etait pas fait : le plus petit pays '
                  'du releve abrite l un des plus gros producteurs float d Europe. '
                  'Reserve de source, releve sectoriel et non piece de dossier.',
    'Belgique': 'AGC Glass Europe, ET UNE LIGNE EUROGLAS PLANIFIEE A LOMMEL par Glas Troesch, 35 hectares, permis annonce fin 2023 et production visee 2025, ETAT NON VERIFIE donc a ne pas citer. Scheuten Glas a un site a DIEST et appartient a Glas Troesch depuis 2020.  Le paragraphe 6 note lui-meme que le site de Moustier a '
                'Jemeppe-sur-Sambre, RUE DE LA GLACERIE, est celui ou Glaverbel a monte en 1965 '
                'LA PREMIERE LIGNE FLOAT D EUROPE CONTINENTALE. Le fait etait dans le mandat '
                'depuis le matin du 14/10 sans que le code le porte. Trois fiches belges sont '
                'deja en NE PAS DEMARCHER pour appartenance a AGC ou a Saint-Gobain, ce qui le '
                'confirme par l autre bout.',
    # CORRIGE LE 14/10 A 16h36, quelques heures apres sa creation : la reserve honnete est LEVEE.
    'Allemagne': 'ETABLI. EUROGLAS, marque float du groupe suisse GLAS TROESCH, exploite les fours de '
                 'HALDENSLEBEN depuis 1997 et d OSTERWEDDINGEN depuis 2006. L entree avait ete tenue par '
                 'PRUDENCE le meme jour, avec la reserve honnete qu aucune ligne allemande n avait ete '
                 'verifiee. Elle l est desormais, et le principe asymetrique a paye : on avait inclus par '
                 'precaution un pays qui le meritait vraiment. S y ajoutent les operations allemandes de '
                 'Saint-Gobain, NSG-Pilkington, Guardian et AGC, et Interpane.',
    'Pays-Bas': 'NON ETABLI, et l entree sert justement a le dire. Aucune ligne float neerlandaise '
                'n a ete cherchee ni trouvee, et Pilkington Nederland y a des sites dont la nature, '
                'production ou transformation, n est pas connue. A VERIFIER avant d employer '
                'l argument, jamais a supposer. Neuf fiches concernees.',
    'Suisse': 'NON ETABLI, meme traitement que les Pays-Bas. Flachglas Schweiz y transforme et ne '
              'produit pas de float a notre connaissance, mais l absence de trace n est pas une '
              'preuve d absence, c est la reserve de methode du paragraphe 6 sur le Perou. '
              'A VERIFIER avant tout usage.',
    # ⚠️ NE PAS AJOUTER le Canada, l Australie ni la Nouvelle-Zelande : l absence de ligne float y
    # est VRAIE et c est precisement l argument de la campagne. Le Canada est le seul pays du G20
    # sans production nationale, et la derniere ligne d Australasie a ferme en 2025. Les inscrire
    # ici ferait crier le garde-fou sur des fiches qui disent juste — le defaut exact que le
    # correctif du 09/10 et celui du 12/10 ont tous deux eu a reparer.
}

MOTIFS = re.compile(
    r"sans (usine|ligne|production) float|aucune float|pas de (ligne|usine) float"
    r"|100 pour cent (du verre )?(est )?importe|n a pas de float|sans float"
    # Ajoute le 12/10 : le vocabulaire manquait le mot FOUR, et c est ce qui a laisse
    # passer ITA SEN ALU, dont la note porte « Aucun four float en Afrique de l Ouest ».
    # ⚠️ MESURE FAITE AVANT DE RETENIR CE MOTIF : la forme large « aucune ligne float »
    # produit HUIT faux positifs sur le registre et AUCUN vrai, parce que c est ainsi que
    # les fiches decrivent soit une SOCIETE qui ne produit pas, soit l INTERDICTION elle-meme.
    # Seul « four » est retenu, et le filtre de contexte ci-dessous fait le reste.
    r"|aucun four float"
    # Ajoute le 14/10 apres un jeu d essai : « il n y a aucune PRODUCTION float en
    # Argentine » passait entre les mailles. « aucune float » ne matche pas quand un mot
    # s intercale, et « sans (usine|ligne|production) float » exige « sans ». C est le
    # meme trou que le mot FOUR le 12/10, un mot insere que la forme ne prevoyait pas.
    # ⚠️ MESURE FAITE AVANT DE RETENIR CE MOTIF, comme pour « aucune ligne float » qui
    # avait ete REJETE pour huit faux positifs : celui-ci en produit ZERO sur le registre.
    r"|aucune production (locale )?(de )?float|aucune production float",
    re.I)

# AJOUT DU 12/10 — LES AFFIRMATIONS REGIONALES, QUE LA GRILLE DU PAYS NE POUVAIT PAS VOIR.
# Le filtre principal ecarte une fiche dont le PAYS n abrite pas de producteur. Une note
# qui affirme l absence de float dans une REGION ENTIERE echappait donc au controle des
# qu elle etait portee par une fiche d un pays sans producteur — cas reel : ITA SEN ALU,
# au Senegal, portant « aucun four float en Afrique de l Ouest » alors que CNG Glass
# produit 500 t/jour a Igbesa au Nigeria depuis 2019.
# Une region se verifie donc independamment du pays de la fiche.
REGIONS = {
    r"afrique de l[' ]ouest": 'CNG Glass produit 500 t/jour a Igbesa au Nigeria depuis 2019',
    r"afrique de l[' ]est|afrique orientale": 'Sapphire Float Glass produit a Mkuranga en Tanzanie',
    r"afrique australe": 'PFG Building Glass, 260 000 t/an en Afrique du Sud',
    r"afrique du nord|maghreb": 'Cevital en Algerie, Sphinx Glass et Misr Glass en Egypte',
    r"moyen-orient|golfe persique|pays du golfe": 'Obeikan, Zoujaj, Guardian et UFG en Arabie saoudite, EFG aux Emirats',
    r"asie du sud-est": 'Asahimas en Indonesie, Phu My et CFG Ha Long au Vietnam, Kibing et Xinyi en Malaisie',
    r"amerique du sud|amerique latine": 'Vidrios Lirquen au Chili, VASA en Argentine, Vivix et Cebrace au Bresil',
    r"amerique centrale": 'Vitro au Mexique dessert la zone',
}
REGIONS = {re.compile(k, re.I): v for k, v in REGIONS.items()}

# ELARGI LE 14/10, ET C EST LA MEME PANNE QUE LES TROIS DE verif-texte.py : LE VOCABULAIRE
# DU GARDE-FOU ETAIT PLUS PAUVRE QUE CELUI DES NOTES. La fiche Vidrieria Universal a ete
# corrigee le 14/10 avec les mots « CORRECTION DU 14/10 » et « ET ELLE EST FAUSSE », et
# l outil a continue de la signaler parce qu il n attendait que « CORRECTION FACTUELLE »
# et « C EST FAUX », a la lettre pres. Un garde-fou qui crie au loup finit par etre
# ignore, et c est alors un VRAI cas qui passe. Les formes retenues couvrent la facon
# dont ces corrections s ecrivent reellement dans le registre.
# Verifie DANS LES DEUX SENS avant d etre garde : zero signalement sur le registre reel,
# et une fausse affirmation injectee sans aucun de ces marqueurs ressort bien.
CORRIGEE = re.compile(
    r"CORRECTION FACTUELLE|CORRECTION DU \d|C EST FAUX|ELLE EST FAUSSE|IL EST FAUX|"
    r"CETTE PHRASE EST FAUSSE|AFFIRMATION FAUSSE|ARGUMENT FAUX|ANGLE A REFAIRE", re.I)

# « les marches sans float » designe les AUTRES marches, pas celui de la fiche :
# c est une phrase meta sur la conduite a tenir, et non une affirmation sur ce pays.
# Faux positif mesure le 09/10 sur Klingshield, dont la note cite au contraire TROIS
# FOIS les 260 000 t/an de PFG — la fiche disait donc exactement ce qu il faut, et
# l outil la signalait quand meme. Meme raison que l exception CORRIGEE ci-dessus :
# un garde-fou qui crie au loup finit ignore, et c est alors un VRAI cas qui passe.
# On NEUTRALISE la phrase benigne au lieu d ignorer la fiche, pour qu une fiche qui
# contiendrait a la fois cette phrase ET une vraie affirmation fausse sorte quand meme.
BENIGNE = re.compile(r"marche?s? sans (production )?float", re.I)

# AJOUT DU 12/10 — LE FILTRE DE CONTEXTE, ET C EST LUI QUI FAIT LE TRAVAIL.
# Mesure : sur le registre, une phrase contenant un motif d absence de float dit presque
# toujours l une de ces trois choses, et aucune n est une faute :
#   1. une SOCIETE ne produit pas de float (« il n a aucune ligne float, donc tout son
#      verre entrant est importe ») — c est une qualification juste et utile ;
#   2. l INTERDICTION est consignee (« NE JAMAIS EMPLOYER L ARGUMENT DE L ABSENCE DE
#      PRODUCTION LOCALE », « le paragraphe 6 interdit d ecrire que ») — c est la fiche
#      qui fait exactement ce qu il faut ;
#   3. une RECHERCHE est relatee (« la recherche n a fait remonter aucune ligne float »)
#      — c est un constat de methode, pas un argument servi au prospect.
# Une phrase portant un de ces marqueurs est donc neutralisee, comme la phrase meta du
# correctif du 09/10 : on NEUTRALISE LA PHRASE et non la fiche, pour qu une note contenant
# a la fois une phrase benigne ET une vraie faute ressorte quand meme.
PORTEE_SOCIETE = re.compile(
    r"\b(il|elle) n a aucune|n est pas un concurrent|annoncee sur leur site"
    r"|son verre entrant|leur verre entrant", re.I)
INTERDICTION = re.compile(
    r"ne jamais|ne plus|interdit|sans valeur|avertissement|ne doit pas|il est vrai a", re.I)
RECHERCHE = re.compile(
    r"la recherche n a (fait remonter|pas trouve)|aucune ligne float trouvee|non etablie", re.I)
# ET LE SIGNAL POSITIF, qui est le plus sur des quatre : la note DIT que l argument a ete
# employe dans le message. C est ce qui distingue ITA SEN ALU des huit faux positifs.
EMPLOI = re.compile(
    r"argument (pose|employe|servi|mis en premiere ligne)|pose en premiere ligne"
    r"|en premiere ligne|argument principal", re.I)

def phrases_fautives(note):
    """Rend les phrases qui affirment vraiment l absence de float sans la neutraliser."""
    gardees = []
    for ph in re.split(r"(?<=[.!?])\s+|\s—\s", note):
        if not MOTIFS.search(ph):
            continue
        if PORTEE_SOCIETE.search(ph) or INTERDICTION.search(ph) or RECHERCHE.search(ph):
            continue
        gardees.append(ph)
    return gardees

CSV = sys.argv[1] if len(sys.argv) > 1 else 'liste-prospects.csv'
suspects = []
corrigees = []
for n, l in enumerate(io.open(CSV, encoding='utf-8').read().split('\n')[1:], start=2):
    if not l.strip():
        continue
    c = l.rstrip('\r').split(';')
    if len(c) < 10 or 'DOUBLON' in c[8].upper():
        continue
    note = BENIGNE.sub(' ', c[8])
    fautives = phrases_fautives(note)
    if not fautives:
        continue
    note = ' '.join(fautives)
    # Deux chemins vers le signalement, et le second est l ajout du 12/10 :
    #   - le PAYS de la fiche abrite ou est desservi par un producteur ;
    #   - ou la note nomme une REGION qui en abrite un, quel que soit le pays.
    motif_pays = PRODUCTEURS.get(c[0])
    motif_region = None
    for rx, prod in REGIONS.items():
        if rx.search(note):
            motif_region = prod
            break
    if not motif_pays and not motif_region:
        continue
    cause = motif_pays or ('affirmation REGIONALE : ' + motif_region)
    # Une fiche deja corrigee CITE l affirmation fausse dans sa note de correction :
    # sans cette exception l outil la signalerait indefiniment et crierait au loup.
    if CORRIGEE.search(c[8]):
        corrigees.append((n, c[0], c[3]))
        continue
    suspects.append((n, c[0], c[3], c[9], cause))

print('=== Fiches affirmant l absence de float dans un pays qui en produit ===')
for n, pays, soc, st, prod in sorted(suspects):
    print('  L%-5d %-18s %-34s %-22s  <-- %s' % (n, pays, soc[:34], st, prod))
print('\n%d fiche(s) a corriger.' % len(suspects))
if not suspects:
    print("Aucune. L argument du float absent n est employe que la ou il est vrai.")
if corrigees:
    print('\n%d fiche(s) deja corrigee(s), ignoree(s) :' % len(corrigees))
    for n, pays, soc in sorted(corrigees):
        print('  L%-5d %-18s %s' % (n, pays, soc[:40]))
