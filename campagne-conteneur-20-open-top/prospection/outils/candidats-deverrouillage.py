# -*- coding: utf-8 -*-
"""Liste les fiches qui valent VRAIMENT un appel de recherche de deverrouillage.

POURQUOI CET OUTIL EXISTE, parce que la raison est la seule chose qui empeche de
le contourner. Le 13/10 j ai depense CINQ appels de recherche sur cinq fiches
dont le registre portait DEJA la reponse : Davis Glass, Univers du Verre, Crone
Wholesale Glass, Tempera Primos et Vitral Vidros Planos. Leurs notes disaient
toutes, en toutes lettres, AUCUNE ADRESSE PUBLIEE, formulaire uniquement, fiche
telephonique ou domaine introuvable.

LA CAUSE N EST PAS L ETOURDERIE, C EST LE FILTRE. Je selectionnais sur le STATUT
et sur un MARQUEUR en majuscules du type TESTEE ou DEVERROUILLEE. Or le registre
consigne son verdict EN PROSE. Un filtre sur marqueurs ne peut donc pas voir une
decision ecrite en mots - c est exactement la lecon Staklo Bakar du paragraphe 12,
un comptage automatique ne voit pas une decision ecrite en prose, prise par
l autre bout.

Le budget de recherche est de 200 appels par tour et la methode en coute deux par
fiche, soit 70 a 90 fiches au maximum. Cinq appels perdus sont donc trois fiches
reelles en moins.
"""
import io, re, sys, signal
# Sortie tronquee par un head ou un grep : on sort proprement au lieu d un
# BrokenPipeError, qui masquerait une vraie erreur dans le bruit.
signal.signal(signal.SIGPIPE, signal.SIG_DFL)

SRC = sys.argv[1] if len(sys.argv) > 1 else 'liste-prospects.csv'

# Verdicts deja rendus, en prose comme en marqueur. Toute fiche qui en porte un
# a DEJA ete travaillee : la rechercher de nouveau ne rend que le meme resultat.
VERDICTS = [
    r'aucune adresse',
    r'formulaire uniquement',
    r'ne propose qu un formulaire',
    r'fiche telephonique',
    r'dossier telephonique',
    r'domaine introuvable',
    r'irrecuperable',
    r'obfusqu',                      # adresses masquees sur la page
    # ⚠️ AJOUTE LE 15/10 : L ADRESSE EST CONNUE ET VOLONTAIREMENT NON PORTEE AU
    # CHAMP. Ces fiches-la n ont RIEN a deverrouiller - elles attendent une
    # DECISION de metier, pas une recherche. Mesure avant adoption : elles sont
    # SIX, et ce sont exactement les six que le script listait EN TETE, parmi les
    # douze a site connu. La moitie des candidats les plus attrayants etaient donc
    # des fiches ou chaque appel de recherche est perdu d avance. C est la faute du
    # 13/10 qui a fait naitre cet outil, reapparue par un autre bout : le registre
    # portait deja la reponse, sous une formulation que les verdicts ne couvraient pas.
    r'adresse disponible',
    r'adresses disponibles',
    r'deliberement non portee',
    r'deliberement non portees',
    r'non portee au champ',
    r'\bTESTEE\b',
    r'\bRETESTEE\b',
    r'\bDEVERROUILLEE\b',
]
# Statuts qu on ne travaille pas : fiche fermee, compte protege, arbitrage en cours.
STATUTS_EXCLUS = ('ECARTE', 'NE PAS DEMARCHER', 'A VALIDER AARON')

# ⚠️⚠️ LE CONTROLE SE FAIT PHRASE PAR PHRASE ET NON SUR LA NOTE ENTIERE, CORRECTIF
# DU 15/10 AU MATIN, ET C EST LA TROISIEME FOIS QU UN MARQUEUR DE CONVENTION SE
# DECLENCHE SUR MA PROPRE PROSE. Le paragraphe 12 l avait ECRIT NOIR SUR BLANC le
# 13/10 : « les deux autres marqueurs du registre, TESTEE et DEVERROUILLEE,
# pilotent candidats-deverrouillage.py de la meme facon et appellent la meme
# prudence ». L avertissement etait juste et il n a pas suffi.
# LE CAS REEL, ET IL COUTAIT UNE DES MEILLEURES CIBLES AMERICAINES : la note de
# COASTAL GLASS DISTRIBUTORS porte « AUCUNE ADRESSE, ET CE N EST PAS UN VERDICT DE
# TYPE TESTEE, c est la lecon Lahey du 13/10 appliquee ». La phrase dit EXACTEMENT
# L INVERSE de ce que le script y a lu, et la fiche etait ecartee du deverrouillage
# par le mot qui servait a dire qu elle ne l etait pas.
# C est la famille du mot DOUBLON ecrit en prose, qui avait rendu une fiche
# invisible aux cinq signaux du balayage, et celle du motif « sans float » de
# verif-argument-float.py, corrige le 09/10 par le MEME remede : on neutralise la
# PHRASE qui porte une negation, jamais la fiche, pour qu une note contenant a la
# fois une phrase benigne ET un vrai verdict ressorte quand meme.
# ⚠️⚠️ LE VERDICT TELEPHONIQUE SE DIT DE DOUZE FACONS ET LE SCRIPT N EN
# CONNAISSAIT QUE DEUX — correctif du 15/10, et c est la QUATRIEME fois que ce
# defaut se presente, apres les trois de verif-texte.py : le vocabulaire du
# CONTROLEUR est plus pauvre que celui des NOTES.
# Il cherchait « fiche telephonique » et « dossier telephonique », a la lettre.
# Le registre ecrit aussi « FICHE PASSEE AU TELEPHONE », « fiche au telephone »,
# « fiche a laisser au telephone, sans y redepenser de recherche », « la fiche
# reste telephonique », « fiche definitivement telephonique ou WhatsApp ».
# TREIZE fiches portaient ainsi un verdict que le script ne voyait pas, dont
# Grupo Araujo et Cyberglass, rebondies la veille et passees au telephone le
# jour meme. Elles repartaient donc au deverrouillage le lendemain.
# ⚠️ ET LE MOTIF LARGE A ETE MESURE PUIS REFUSE AVANT CELUI-CI, ce qui est le
# coeur de la lecon. « (fiche|dossier)[^.]{0,40}telephon » rend QUARANTE-CINQ
# fiches, dont une trentaine disent L INVERSE d un verdict : « fiche sans
# adresse email ET sans telephone », « fiche ne porte AUCUN telephone », « fiche
# n a ni adresse ni telephone ». Ces fiches-la n ont PAS ete travaillees, elles
# n ont simplement aucune coordonnee - les ecarter du deverrouillage les
# enterrerait. C est le refus du motif « aucune ligne float » du 12/10, qui
# criait huit fois pour zero loup.
# D ou la GARDE NEGATIVE ci-dessous. Mesure finale : 13 prises, 0 faux positif.
# Le seul faux positif de l avant-derniere version, GEOALPEN, etait une phrase
# META - « mon filtre du soir a manque cette fiche en exigeant email ET
# telephone vides » - donc un commentaire sur un filtre et non un verdict.
TEL_NIE = re.compile(
    r'sans t[ée]l[ée]phon|ni t[ée]l[ée]phon|aucun t[ée]l[ée]phon|'
    r'pas de t[ée]l[ée]phon|ne porte (pas|aucun)|n a ni|'
    r't[ée]l[ée]phones? vides?|en exigeant', re.I)
TEL_AFFIRME = re.compile(r'(fiche|dossier)[^.]{0,40}t[ée]l[ée]phon', re.I)

NEGATIONS = re.compile(
    r"n est pas|n'est pas|ce n est pas|pas un verdict|il ne s agit pas|"
    r"plutot qu un verdict|sans verdict|non pas un|ni un verdict|"
    r"pas de type|a ne pas confondre", re.I)

# Une note se coupe sur le point, le point d exclamation et les puces que le
# registre emploie. Le point-virgule est le separateur du CSV, il ne peut pas
# apparaitre ici.
COUPURE = re.compile(r'[.!?\u00b7]|\u26a0')


def verdicts_de(note):
    """Verdicts portes par la note, les phrases NIANT un verdict etant tues."""
    trouves = []
    for phrase in COUPURE.split(note):
        if NEGATIONS.search(phrase):
            continue
        for v in VERDICTS:
            if re.search(v, phrase, re.I) and v not in trouves:
                trouves.append(v)
        # Verdict telephonique sous ses formes libres, la garde negative
        # ecartant les phrases qui disent l ABSENCE de telephone.
        if TEL_AFFIRME.search(phrase) and not TEL_NIE.search(phrase):
            if 'fiche au telephone' not in trouves:
                trouves.append('fiche au telephone')
    return trouves

lignes = [l for l in io.open(SRC, encoding='utf-8').read().rstrip('\n').split('\n')[1:]]
retenues, ecartees = [], []
for l in lignes:
    c = l.rstrip('\r').split(';')
    if len(c) != 10:
        continue
    pays, soc, site, mail, tel, note, statut = c[0], c[3], c[5], c[6], c[7], c[8], c[9]
    if mail.strip():                                  # deja joignable par mail
        continue
    if statut.startswith(STATUTS_EXCLUS):
        continue
    deja = verdicts_de(note)
    (ecartees if deja else retenues).append((pays, soc, site, tel, statut, deja))

retenues.sort(key=lambda r: (r[2] == '', r[0], r[1]))   # celles qui ont un site d abord
print('=== %d FICHE(S) A TRAVAILLER, site connu en tete ===' % len(retenues))
for pays, soc, site, tel, statut, _ in retenues:
    print('  %-22s %-42s %-28s %s' % (pays[:22], soc[:42], (site or '(pas de site)')[:28], statut))
print()
print('=== %d fiche(s) ECARTEES : le registre porte deja leur verdict ===' % len(ecartees))
for pays, soc, site, tel, statut, deja in ecartees[:12]:
    print('  %-22s %-38s motif : %s' % (pays[:22], soc[:38], ', '.join(d.strip('\\b') for d in deja[:2])))
if len(ecartees) > 12:
    print('  ... et %d autres.' % (len(ecartees) - 12))
