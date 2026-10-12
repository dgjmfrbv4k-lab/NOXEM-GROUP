#!/usr/bin/env python3
"""Consigne un lot d'envois dans liste-prospects.csv.

Usage : python3 outils/consigne-envoi.py <statut> <note> <pays|societe|idmsg> ...

  statut : ENVOYE 2026-10-12 | RELANCE 2026-10-12 | ADRESSE INVALIDE ...
  note   : texte ajoute a la note de chaque fiche, SANS point-virgule
           la chaine {ID} y est remplacee par l'identifiant de message

Garde-fous du paragraphe 12 : 10 champs par ligne, couverture des cles,
unicite des cles, aucune perte de fiche, aucun point-virgule dans la note.
"""
import io, sys, collections

def main(argv):
    if len(argv) < 3:
        sys.exit(__doc__)
    statut, note, cibles = argv[0], argv[1], argv[2:]
    assert ';' not in note, 'POINT-VIRGULE DANS LA NOTE, ecriture refusee'
    assert ';' not in statut, 'POINT-VIRGULE DANS LE STATUT, ecriture refusee'

    MAJ = {}
    for t in cibles:
        p = t.split('|')
        assert len(p) == 3, 'cible mal formee, attendu pays|societe|idmsg : %s' % t
        MAJ[(p[0], p[1])] = p[2]

    src = io.open('liste-prospects.csv', encoding='utf-8').read().rstrip('\n').split('\n')
    tete, corps = src[0], src[1:]
    out, vus = [], collections.Counter()
    for l in corps:
        c = l.rstrip('\r').split(';')
        k = (c[0], c[3]) if len(c) == 10 else None
        if k in MAJ:
            vus[k] += 1
            c[8] = c[8].rstrip() + ' ' + note.replace('{ID}', MAJ[k])
            c[9] = statut
        out.append(';'.join(c))

    manque = set(MAJ) - set(vus)
    assert not manque, 'CLES INTROUVABLES, ecriture refusee : %s' % manque
    mult = {k: n for k, n in vus.items() if n > 1}
    assert not mult, 'CLES EN DOUBLE, ecriture refusee : %s' % mult
    for i, l in enumerate(out):
        assert len(l.rstrip('\r').split(';')) == 10, 'MALFORME ligne %d' % (i + 2)
    assert len(out) >= len(corps), 'PERTE DE FICHES, ecriture refusee'

    io.open('liste-prospects.csv', 'w', encoding='utf-8').write(tete + '\n' + '\n'.join(out) + '\n')
    print('%d fiche(s) passee(s) en %s' % (len(MAJ), statut))

if __name__ == '__main__':
    main(sys.argv[1:])
