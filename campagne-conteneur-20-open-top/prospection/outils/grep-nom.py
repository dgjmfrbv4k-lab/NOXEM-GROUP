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


def chercher(R, nom):
    """Rend les fiches dont la raison sociale contient le nom, separateurs ignores."""
    cible = aplatir(nom)
    if not cible:
        return []
    return [c for c in R if len(c) == 10 and cible in aplatir(c[3])]


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
