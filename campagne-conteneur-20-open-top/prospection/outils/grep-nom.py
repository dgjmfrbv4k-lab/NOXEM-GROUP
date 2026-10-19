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

CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'liste-prospects.csv')

# Tout ce qui separe deux mots dans une raison sociale, et qui varie d une source
# a l autre : espace, trait d union, point, apostrophe, underscore, esperluette.
SEPARATEURS = re.compile(r"[\s\-\._'’&/]+")


def aplatir(s):
    """Retire les separateurs et met en minuscules."""
    return SEPARATEURS.sub('', s.lower())


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
    mots = [m for m in SEPARATEURS.split(s.lower()) if m and m not in SUFFIXES]
    return ''.join(m[0] for m in mots)


def premier_mot(s):
    """Premier mot significatif, aplati : 'IGG Glass' -> 'igg'."""
    mots = [m for m in SEPARATEURS.split(s.lower()) if m and m not in SUFFIXES]
    return mots[0] if mots else ''


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
        if cible in plat or (len(plat) >= 6 and plat in cible):
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


def main(noms):
    R = charger()
    print('Registre : %d fiches.\n' % len(R))
    for nom in noms:
        hits = chercher(R, nom)
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
        print('')
    return 0


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1:]))
