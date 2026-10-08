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

SECOND GARDE-FOU, AJOUTE LE 08/10 A 15h40 APRES AVOIR DETRUIT LE REGISTRE.
Dans un script de mise a jour j ai oublie le out.append() de la boucle. Toutes
les lignes ont donc ete perdues et ecrire() a joyeusement ecrit un fichier de
deux lignes : l en-tete et une ligne vide. Le controle de champs n a rien vu,
puisqu il n y avait plus aucun champ a controler. Le fichier a ete restaure par
git checkout, sans perte, parce que le commit precedent datait de trois minutes.

La lecon n est pas de faire attention : c est qu un garde-fou qui ne verifie que
la FORME des lignes ne protege pas du tout contre leur DISPARITION. ecrire()
relit donc desormais le fichier existant, compte ses fiches, et REFUSE d ecrire
si le nouveau nombre est inferieur. Une fiche ne se supprime jamais dans ce
registre : elle change de statut. Une baisse du nombre de lignes est donc
toujours un bug, jamais une intention.
"""
import io
import os

CHAMPS = 10

def _compte_existant(chemin):
    """Nombre de fiches deja presentes dans le fichier, 0 s il n existe pas."""
    if not os.path.exists(chemin):
        return 0
    lignes = io.open(chemin, encoding='utf-8').read().split('\n')[1:]
    return len([l for l in lignes if l.strip()])

def ecrire(chemin, entete, lignes, permettre_baisse=False):
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

    avant = _compte_existant(chemin)
    if not permettre_baisse:
        assert len(propres) >= avant, (
            'REFUS D ECRIRE : %d fiches a ecrire contre %d deja dans le fichier. '
            'Une fiche ne se supprime jamais, elle change de statut. Verifier que '
            'la boucle du script fait bien son out.append() pour CHAQUE ligne, y '
            'compris celles qu elle ne modifie pas. Le fichier n a pas ete touche.'
            % (len(propres), avant))
    assert propres, 'REFUS D ECRIRE : aucune ligne a ecrire. Le fichier n a pas ete touche.'

    io.open(chemin, 'w', encoding='utf-8').write(entete + '\n' + '\n'.join(sorted(propres)) + '\n')
    return len(propres)

def nettoyer(valeur):
    """Retire les points-virgules d une valeur avant de l ecrire dans un champ."""
    return str(valeur).replace(';', ',')
