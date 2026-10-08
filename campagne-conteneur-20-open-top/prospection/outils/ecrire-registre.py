#!/usr/bin/env python3
"""Garde-fou d ecriture du registre.

A importer dans tout script qui modifie liste-prospects.csv, au lieu d ecrire le
fichier a la main. Il refuse d ecrire si une ligne n a pas exactement 10 champs
ou si un champ contient un point-virgule.

Pourquoi : le 08/10 j ai passe la matinee a reparer trois lignes cassees par un
point-virgule glisse dans une note, puis j ai commis exactement la meme faute
l apres-midi dans un script sans garde-fou, sur la fiche Manna Glass. Le
paragraphe 12 interdit le point-virgule dans une note ; il faut que le code le
refuse, pas seulement que la consigne le dise.
"""
import io

CHAMPS = 10

def ecrire(chemin, entete, lignes):
    """Ecrit le registre apres verification. Leve AssertionError si invalide."""
    propres = []
    for n, l in enumerate(lignes, start=2):
        if not l.strip():
            continue
        c = l.rstrip('\r').split(';')
        assert len(c) == CHAMPS, (
            'ligne %d : %d champs au lieu de %d. Un point-virgule a ete glisse '
            'dans un champ. Societe : %s' % (n, len(c), CHAMPS, c[3] if len(c) > 3 else '?'))
        propres.append(';'.join(c))
    io.open(chemin, 'w', encoding='utf-8').write(entete + '\n' + '\n'.join(sorted(propres)) + '\n')
    return len(propres)

def nettoyer(valeur):
    """Retire les points-virgules d une valeur avant de l ecrire dans un champ."""
    return str(valeur).replace(';', ',')
