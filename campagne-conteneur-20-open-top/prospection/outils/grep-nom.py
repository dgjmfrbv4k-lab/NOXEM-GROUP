#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Greper un nom de societe contre le registre, en NORMALISANT les separateurs.

Ne : le 19/10 a 10h22 j ai cherche Glaz Tech Industries, grepe `glaz tech` puis
`glaztech`, obtenu ZERO aux deux, et depense un second temps complet. Le registre
porte `Glaz-Tech`, AVEC UN TRAIT D UNION, et aucun des deux tokens ne le voit.
La fiche etait deja relancee le 08/10 et portait deja, mot pour mot, le verdict
sur les epaisseurs que l appel venait de redecouvrir.

Le paragraphe 5 couvrait deja la paire espace / concatenation — Alpha Glass contre
Alphaglass, le 11/10 — et il ne disait rien du TRAIT D UNION, qui est le troisieme
separateur. Greper une forme ne peut structurellement pas trouver les deux autres.

Remede : on compare des chaines dont tout separateur a ete retire, des deux cotes.
`glaz tech`, `glaztech` et `glaz-tech` deviennent alors le meme token.

Et le second filet est celui de la regle Prodiesa du 19/10 : la recherche porte sur
le CHAMP RAISON SOCIALE, jamais sur la ligne entiere, pour qu un nom devenu nom de
regle dans les notes ne noie pas la reponse. Le comptage sur la ligne entiere est
imprime a part, a titre indicatif.

Usage : python3 outils/grep-nom.py "Glaz Tech Industries" "Walter Stern" ...
"""
import io
import os
import re
import sys
import unicodedata

CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'liste-prospects.csv')

# Tout ce qui separe deux mots dans une raison sociale, et qui varie d une source
# a l autre : espace, trait d union, point, apostrophe, underscore, esperluette.
# ⚠⚠ CORRECTIF DU 19/10 AU SOIR, 15e cas de la famille du caractere unique du §5. L ancien motif ne couvrait ni la PARENTHESE ni le TIRET
# CADRATIN, qui sont pourtant les deux signes de ponctuation que le registre emploie lui-meme par
# convention : la parenthese pour desambiguer un homonyme (Arista (verre, Colombie), Sunny Glass
# (Carthagene), Knight Industries (verre plat, Canada)) et le tiret cadratin pour accoler le nom
# legal au nom commercial (Linde Vidros — Vidracaria Linde Ltda).
# MESURE, ET ELLE EST A DIRE EXACTEMENT PARCE QUE J AI D ABORD ECRIT PLUS FORT QUE LE FAIT :
# 232 raisons sociales sur 1853 PORTENT un signe non couvert — 129 tirets cadratins, 102
# parentheses, 4 virgules, 3 plus. Mais toutes ne sont pas ATTEINTES : le defaut ne mord que quand
# le token cherche doit ENJAMBER la ponctuation. "Sunny Glass" trouve bien "Sunny Glass
# (Carthagene)", la parenthese venant APRES ; c est "Glasslam Mauritius" contre "Glasslam
# (Mauritius) Ltd" qui echoue, la parenthese etant AU MILIEU. Donc la famille atteinte est celle
# des noms dont la forme de registre INSERE un pays ou une ville entre parentheses.
# MESURE AVANT ET APRES, sur quinze noms dont treize sans piege : 13 trouves sur 15 avant,
# 15 sur 15 apres, et AUCUN faux positif neuf. Les treize sorties identiques, verifie par diff.
# CE QUE LE TROU A COUTE : le 19/10 au soir, "Glasslam Mauritius" est ressortie ABSENTE alors que
# le registre portait "Glasslam (Mauritius) Ltd" en RELANCE 2026-10-12. Seul l assert d unicite du
# script de creation l a arretee, et une fiche creee aurait fait un TROISIEME message a la
# meilleure cible mauricienne : la faute Shibaam. C est le cas Distrividrios LER une seconde fois.
# Les lettres non-ASCII restent des LETTRES et ne sont pas ajoutees a la classe, pour ne pas couper
# les noms portant un ss allemand, un o barre scandinave ou un l polonais.
SEPARATEURS = re.compile(r"[\s\-\._'’&/—–,\(\)\[\]\+\|:;!\?\"«»]+")


def sans_accent(s):
    """Depouille les accents. Ajoute le 19/10 a 16h31, TREIZIEME cas de la famille
    du paragraphe 5 et le premier qui ne soit pas un separateur.

    Ne : j ai grepe `Reunivitre`, sans accent, obtenu ABSENT, et j allais creer la
    fiche. Le registre porte `Reunivitre` AVEC UN E ACCENTU AIGU, avec son adresse
    contact arobase reunivitre point re, son telephone et un envoi en file. C etait
    un doublon de plus a une maison deja deverrouillee — la faute Shibaam.

    Les separateurs etaient couverts depuis le 19/10 au matin, les initiales depuis
    le meme jour, et l ACCENT ne l etait pas : `reunivitre` et `reunivitre` accentue
    n ont aucune sous-chaine commune pour une comparaison brute. C est la meme panne
    que le jeton `Nouvelle-Zelande` du paragraphe 13 — ou le registre ecrit SANS
    accent et ou j avais tape la forme accentuee, rendant zero sur douze fiches —
    sauf qu ici elle est dans le CODE, donc elle se repare une fois pour toutes
    plutot que de dependre de ma memoire a chaque appel.

    Le registre melange les deux formes : il porte `Reunivitre` et `Nigeria`
    accentues, et `Nouvelle-Zelande` et `Perou` non accentues. Aucune regle de
    saisie ne tiendra, donc la comparaison doit etre insensible aux accents.
    """
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')


def aplatir(s):
    """Retire les separateurs, les accents, et met en minuscules."""
    return SEPARATEURS.sub('', sans_accent(s.lower()))


def reduire(s):
    """Reduit toute lettre repetee a une seule. QUATORZIEME cas de la famille du
    caractere unique, ajoute le 19/10 a 16h40.

    Ne : l annuaire caraibe donne `Aluglass NV` a Oranjestad et LE REGISTRE PORTE
    `Aluglas Aruba`, avec UN SEUL S, relancee le 12/10 avec l adresse
    info arobase aluglassaruba point com — ou le domaine, lui, en a DEUX. Un grep sur
    le nom rendu par la source ne voyait donc PAS la fiche : `aluglass` n est pas une
    sous-chaine de `aluglasaruba`, dans aucun sens.

    Si la fiche avait ete creee, c etait un troisieme message a une maison deja
    relancee — la faute Shibaam.

    Les separateurs etaient couverts le matin, les initiales aussi, l accent a 16h31,
    et la LETTRE DOUBLEE ne l etait pas. Ce n est ni un separateur ni une
    normalisation : c est une faute de frappe ou une variante d orthographe, et le
    mot `glass` lui-meme en porte une.

    MESURE FAITE AVANT DE GARDER LE CORRECTIF, comme le mandat l impose depuis le
    motif `aucune ligne float` rejete le 12/10 pour huit faux positifs : la reduction
    rapproche ZERO paire du registre a tort, alors que MILLE raisons sociales sur
    1729 portent une lettre doublee. Le signal est donc sur et il protege mille
    fiches.

    Il est rendu A PART dans la sortie, pour qu une correspondance APPROCHEE ne se
    confonde jamais avec une correspondance exacte.
    """
    out = []
    for car in s:
        if not out or out[-1] != car:
            out.append(car)
    return ''.join(out)


def charger():
    lignes = io.open(CSV, encoding='utf-8').read().rstrip('\n').split('\n')
    return [l.rstrip('\r').split(';') for l in lignes[1:]]


# ⚠️⚠️ UN ACRONYME N EST PAS UNE VARIANTE D ECRITURE, C EST UNE AUTRE CHAINE —
# ajoute le 19/10 apres avoir CREE un doublon que ce script venait de declarer absent.
# J ai grepe `Infinity Glass Group` et obtenu ABSENT, a juste titre : le registre porte
# `IGG Glass`. Aucune normalisation de separateurs ne rapproche ces deux chaines, et la
# fiche existante etait en RELANCE 2026-10-12 — donc un troisieme message en une semaine,
# la faute Shibaam, arretee par detecte-doublons.py et non par ici.
# Le meme jour, AGNORA avait ete reconnue a temps comme l acronyme d Architectural Glass
# of NORth America, et RGT comme Rodriguez Glass and Tempering : trois cas en une matinee
# font une famille, pas un accident.
# Remede : on compare AUSSI les initiales, dans les deux sens. Les suffixes juridiques
# sont retires avant de les compter, sans quoi le L de Ltd et le I de Inc polluent tout.
SUFFIXES = {'inc', 'ltd', 'llc', 'sa', 'sas', 'sarl', 'srl', 'gmbh', 'bv', 'nv', 'ag',
            'corp', 'co', 'cie', 'lda', 'pty', 'plc', 'spa', 'aps', 'oy', 'ab', 'as',
            'limited', 'company', 'the', 'de', 'du', 'of', 'et', 'and', 'y', 'e'}


def initiales(s):
    """Initiales des mots significatifs : 'Infinity Glass Group Inc' -> 'igg'."""
    mots = [m for m in SEPARATEURS.split(sans_accent(s.lower())) if m and m not in SUFFIXES]
    return ''.join(m[0] for m in mots)


def premier_mot(s):
    """Premier mot significatif, aplati : 'IGG Glass' -> 'igg'."""
    mots = [m for m in SEPARATEURS.split(sans_accent(s.lower())) if m and m not in SUFFIXES]
    return mots[0] if mots else ''


def sans_pluriel(s):
    """Neutralise un S final sur chaque mot. QUINZIEME cas de la famille du caractere
    unique, ajoute le 19/10 au soir.

    Ne : la rubrique peruvienne du portail donnait `Vidrieria Noelia`. Grepe tel quel,
    le script a repondu ABSENT — et le registre porte `VidrieriaS Noelia`, au Venezuela,
    en A QUALIFIER. UN S. J allais creer la fiche sous le Perou, ce qui aurait fait un
    doublon ET sous un faux pays.

    Pourquoi ce cas devait arriver : ce secteur nomme ses maisons avec des mots qui
    s accordent — Vidrieria et VidrieriaS, Cristal et CristaleS, Vidro et VidroS,
    Espejo et EspejoS. Le pluriel est donc la variante la plus probable de toutes, et
    c etait la seule de la famille a ne pas etre couverte : les separateurs le sont
    depuis le matin, les initiales aussi, l accent depuis 16h31 et la lettre doublee
    depuis 16h40.

    MESURE FAITE AVANT DE RETENIR LE CORRECTIF, comme pour la lettre doublee et comme
    le correctif d initiales qui avait ete REJETE pour 29 faux positifs : la
    neutralisation du pluriel ne rapproche QU UNE SEULE paire nouvelle sur les 1875
    fiches du registre — `Glasslines` en Nouvelle-Zelande contre `Glassline` en Serbie,
    qui sont deux maisons reelles de deux pays, deja au registre et deja traitees. Donc
    un signalement de plus a lire, et zero faux positif de consequence.

    Le seuil de 4 lettres evite de mutiler un mot court dont le S est structurel.
    """
    return ''.join(m[:-1] if len(m) > 3 and m.endswith('s') else m
                   for m in SEPARATEURS.split(sans_accent(s.lower())) if m)


# Mots generiques du metier, dans les quatre langues du registre plus le hongrois.
# Un nom de societe COURT qui est un fragment de l un d eux n est pas distinctif : il
# rapprocherait des dizaines de fiches sans rapport. Liste a completer EN LISANT le
# groupe rendu, jamais en le supposant — meme consigne que MUTUALISES dans
# detecte-doublons.py.
MOTS_GENERIQUES = (
    'aluminium', 'aluminum', 'aluminio', 'alumini',
    'vidrio', 'vidros', 'vidraria', 'vidracaria', 'vidraceiro',
    'vitre', 'vitrerie', 'vitrage', 'vitraria',
    'glass', 'glas', 'verre', 'verrerie', 'sikuveg',
    'cristal', 'cristales', 'espejo', 'espelho', 'mirror', 'miroir', 'tempered',
)


def generique(plat):
    """Vrai si ce nom aplati est un fragment d un mot courant du metier."""
    return any(plat in m for m in MOTS_GENERIQUES)


def chercher(R, nom):
    """Rend les fiches dont la raison sociale correspond, separateurs ET acronymes."""
    cible = aplatir(nom)
    if not cible:
        return []
    ini = initiales(nom)
    hits = []
    for c in R:
        if len(c) != 10:
            continue
        plat = aplatir(c[3])
        # ⚠️ SYMETRIQUE, ajoute le 19/10 apres un SECOND doublon cree en dix minutes.
        # Je cherchais `Complete Line Glass Wholesalers Inc` et le registre porte
        # `Complete Line Glass` : la cible etait plus LONGUE que la fiche, donc
        # `cible in plat` ne pouvait pas correspondre. C est la regle Arabian Glass du
        # 09/10 — une societe se PUBLIE sous son nom court et se DEPOSE sous son nom
        # long — appliquee au code au lieu d etre seulement ecrite.
        # Le garde-fou de longueur evite qu un nom de deux lettres rende tout le registre.
        # ⚠⚠ SEUIL ABAISSE DE 6 A 4 LE 19/10 AU SOIR, APRES UN DOUBLON QUE CE SEUIL-LA A
        # LAISSE CREER. Je cherchais `Komo Glass` et le registre porte `KOMO` tout court :
        # quatre caracteres, donc le garde-fou `len(plat) >= 6` ecartait la fiche et le
        # script a repondu ABSENT. La comparaison etait deja symetrique depuis ce matin,
        # c est sa BORNE qui etait fausse.
        # CE QUE LE SEUIL DE 6 RENDAIT INVISIBLE : 20 raisons sociales du registre
        # s aplatissent sous 6 caracteres, et ce sont de vrais noms distinctifs — KOMO,
        # SAMIR, Gapex, Luvit, NASCO, Viseg, VIDSA, Iciza, SOJAG, ACMAK... ET SURTOUT
        # `Rubex`, QUI EST UN COMPTE PROTEGE DU PARAGRAPHE 7 avec une demande de prix
        # ouverte. Un `Rubex Glass Industries` rendu par une recherche aurait ete declare
        # absent, et la fiche creee en double sur un compte en negociation.
        # MESURE FAITE AVANT DE GARDER LE CORRECTIF, comme pour la lettre doublee et le
        # pluriel, et comme le correctif d initiales qui avait ete REJETE pour 29 faux
        # positifs : seuil 6 -> 99 rapprochements par inclusion inverse · seuil 4 NU ->
        # 281, donc INUTILISABLE · seuil 4 + REGLE DU GENERIQUE -> 103, soit QUATRE
        # signalements neufs dont UN vrai.
        # POURQUOI LE SEUIL 4 NU EST INUTILISABLE, et c est la panne `SA Vidros` qui a
        # rendu la premiere version de noyaux-voisins.py inexploitable : une seule fiche
        # nommee `ALUM` est sous-chaine de TOUT nom en aluminium ou aluminio, et elle
        # produisait a elle seule environ CENT CINQUANTE faux positifs. Meme chose pour
        # `Idra`, qui vit dans vidraria et vidracaria, et pour `UVEG`, qui vit dans
        # sikuveg. Le remede est celui que noyaux-voisins.py emploie deja : LE NOM COURT
        # NE COMPTE QUE S IL N EST PAS UN FRAGMENT DE MOT GENERIQUE DU METIER.
        court_utile = len(plat) >= 6 or (len(plat) >= 4 and not generique(plat))
        if cible in plat or (court_utile and plat in cible):
            hits.append(c)
        # ⚠️ EGALITE ET NON SOUS-CHAINE. Premiere version du 19/10 : je cherchais les
        # initiales N IMPORTE OU dans le nom aplati, et la mesure a rendu 29 signalements
        # sur 190 noms pour ZERO vrai — `atg` d Al Tbaynawi retrouve dans flo-ATG-lass, et
        # pire, `pgg` de Perfect Glass Ghana retrouve dans PG-G-lass Botswana, c est-a-dire
        # un rapprochement avec les comptes PROTEGES du paragraphe 7. Un garde-fou qui crie
        # au loup finit ignore : correctif rejete et refait, comme le motif
        # `aucune ligne float` l avait ete le 12/10 pour huit faux positifs.
        elif len(ini) >= 3 and ini == premier_mot(c[3]):
            hits.append(c)            # le registre porte l ACRONYME du nom cherche
        elif len(cible) >= 3 and cible == initiales(c[3]):
            hits.append(c)            # le registre porte le nom DEVELOPPE d un sigle
    return hits


def chercher_approche(R, nom, deja):
    """Correspondances APPROCHEES rendues a part : a LETTRE DOUBLEE pres, voir
    reduire(), ET a PLURIEL pres, voir sans_pluriel() — ajoute le 19/10 au soir
    apres le cas Vidrieria/VidrieriaS Noelia."""
    cible = reduire(aplatir(nom))
    cible_sp = reduire(sans_pluriel(nom))
    if len(cible) < 5:
        return []                      # garde-fou : un token court rendrait du bruit
    vus = {id(c) for c in deja}
    hits = []
    for c in R:
        if len(c) != 10 or id(c) in vus:
            continue
        plat = reduire(aplatir(c[3]))
        plat_sp = reduire(sans_pluriel(c[3]))
        if (cible in plat or (len(plat) >= 6 and plat in cible)
                or cible_sp in plat_sp or (len(plat_sp) >= 6 and plat_sp in cible_sp)):
            hits.append(c)
    return hits


def main(noms):
    R = charger()
    print('Registre : %d fiches.\n' % len(R))
    for nom in noms:
        hits = chercher(R, nom)
        approx = chercher_approche(R, nom, hits)
        brut = sum(1 for c in R if aplatir(nom) in aplatir(';'.join(c)))
        print('=== %s   (token aplati : %s)' % (nom, aplatir(nom)))
        if not hits:
            print('    ABSENT du champ raison sociale.')
            if brut:
                print('    ⚠ mais %d ligne(s) le portent AILLEURS — a lire avant de conclure.' % brut)
        else:
            print('    ⚠ %d FICHE(S) AU REGISTRE :' % len(hits))
            for c in hits:
                print('      %s | %s | %s | %s | %s'
                      % (c[0], c[2][:40], c[3], c[6] or '(pas d adresse)', c[9]))
        if approx:
            print('    ⚠⚠ %d FICHE(S) A UNE LETTRE DOUBLEE OU A UN PLURIEL PRES — cas Aluglas/Aluglass et Vidrieria/Vidrierias :'
                  % len(approx))
            for c in approx:
                print('      %s | %s | %s | %s | %s'
                      % (c[0], c[2][:40], c[3], c[6] or '(pas d adresse)', c[9]))
        print('')
    return 0


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1:]))
