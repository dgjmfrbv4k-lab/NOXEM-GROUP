# -*- coding: utf-8 -*-
"""Balayage des NOYAUX DE NOM : trouve les paires de fiches actives, dans un meme pays,
dont le noyau de raison sociale est inclus dans l autre.

POURQUOI CET OUTIL EXISTE, ecrit le 19/10 au soir.
detecte-doublons.py croise cinq signaux : pays plus nom normalise, domaine de site, adresse
e-mail, telephone, et domaines confondus. Il ne voit donc PAS une paire dont les deux noms
differaient ET dont l une des lignes n a aucune coordonnee — c est la fiche nee d un annuaire
sans site, sans adresse et sans telephone que le paragraphe 5 decrit comme invisible aux
signaux. Cas reel trouve par ce balayage : METAL SOUDAN MALI contre METALSOUDAN, meme quartier
du Fleuve a Bamako, meme metier, et la premiere sans aucune coordonnee. C est le cas Alpha Glass
contre Alphaglass du 11/10, qui avait coute un troisieme message.

CE QU IL FAIT, ET CE QU IL NE FAIT PAS.
Il travaille sur le NOYAU du nom : aplati, sans accents, sans separateurs — parentheses et
tirets cadratins compris depuis le correctif du 19/10 — et prive de ses suffixes de forme
juridique. Il SIGNALE, il ne conclut pas : le paragraphe 12 impose de trancher sur le siege et
l immatriculation, jamais sur le nom. Plusieurs de ses sorties sont de VRAIS homonymes a NE PAS
fusionner, et c est voulu — Insulite Glass au Kansas contre Insulite Inc. au New Jersey.

LE BRUIT ET COMMENT IL EST COUPE, parce que ma premiere version en etait inutilisable.
Elle rendait 112 paires dont 98 venaient d une seule fiche : SA Vidros, dont le noyau prive du
suffixe sa se reduit a vidros, mot generique present dans toute raison sociale bresilienne.
D ou deux garde-fous mesures : le noyau doit garder au moins un mot NON generique, et le plus
court des deux noyaux doit faire au moins huit caracteres. Mesure apres correctif, substituee et non tapee : 17 paires
sur 1685 fiches actives, toutes lisibles une par une. (J avais d abord ecrit 14, de memoire et
sans compter : c est la faute du paragraphe 13 et elle est corrigee ici meme.)
"""
import io, os, re, sys, unicodedata, collections

CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'liste-prospects.csv')

SEPARATEURS = re.compile(r"[\s\-\._'’&/—–,\(\)\[\]\+\|:;!\?\"«»]+")

# Formes juridiques : elles ne distinguent pas deux societes.
SUFFIXES = {'ltd', 'ltda', 'llc', 'inc', 'sa', 'sas', 'srl', 'gmbh', 'bv', 'nv', 'pty', 'corp',
            'co', 'cv', 'sac', 'eirl', 'spa', 'ag', 'as', 'kft', 'doo', 'ead', 'plc', 'limited',
            'company', 'sarl', 'eurl', 'snc', 'fze', 'wll', 'lda', 'cc', 'pvt', 'me', 'eirelli',
            'saicf', 'cia', 'aps', 'oy', 'ab', 'kk', 'pte', 'bhd', 'sdn'}

# Mots du metier : presents dans des centaines de raisons sociales, ils ne distinguent rien.
# C est ce garde-fou qui a rendu l outil utilisable, voir l en-tete.
GENERIQUES = {'glass', 'glasses', 'vidro', 'vidros', 'vidrio', 'vidrios', 'verre', 'verres',
              'cristal', 'cristales', 'glas', 'vitro', 'vitros', 'mirror', 'espejo', 'espejos',
              'aluminium', 'aluminum', 'alu', 'temper', 'tempering', 'temperados', 'vidraria',
              'vidracaria', 'glazing', 'industries', 'industria', 'group', 'grupo', 'comercial',
              'distribuidora', 'distributors', 'trading', 'international'}

MIN_NOYAU = 8


def sans_accent(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')


def mots(nom):
    return [m for m in SEPARATEURS.split(sans_accent(nom.lower())) if m]


def noyau(nom):
    """Nom aplati, sans suffixe de forme juridique. None si rien de distinctif ne reste."""
    utiles = [m for m in mots(nom) if m not in SUFFIXES]
    if not utiles:
        return None
    if not any(m not in GENERIQUES for m in utiles):
        return None                      # que des mots du metier : ne distingue rien
    return ''.join(utiles)


def neutralisee(c):
    """Meme definition que dans detecte-doublons.py : par le STATUT, jamais par un mot de la note."""
    return c[9].startswith(('NE PAS', 'ECARTE'))


def main():
    lignes = io.open(CSV, encoding='utf-8').read().rstrip('\n').split('\n')[1:]
    R = [(i + 2, l.split(';')) for i, l in enumerate(lignes)]
    R = [(n, c) for n, c in R if len(c) == 10 and not neutralisee(c)]

    par_pays = collections.defaultdict(list)
    for n, c in R:
        k = noyau(c[3])
        if k and len(k) >= MIN_NOYAU:
            par_pays[c[0]].append((n, c[3], k, c[9]))

    paires = []
    for pays in sorted(par_pays):
        lst = par_pays[pays]
        for i in range(len(lst)):
            for j in range(i + 1, len(lst)):
                a, b = lst[i], lst[j]
                court, long_ = sorted((a[2], b[2]), key=len)
                if court in long_:
                    paires.append((pays, a, b))

    print('=== NOYAUX DE NOM VOISINS : %d paire(s) ===' % len(paires))
    for pays, a, b in paires:
        print('  %s' % pays)
        print('      L%-6d %-46s %s' % (a[0], a[1][:46], a[3]))
        print('      L%-6d %-46s %s' % (b[0], b[1][:46], b[3]))
    print('\n%d fiches actives examinees.' % len(R))
    print('IL SIGNALE, IL NE CONCLUT PAS. Plusieurs de ces paires sont de VRAIS homonymes a ne')
    print('PAS fusionner : le paragraphe 12 tranche sur le siege et l immatriculation, jamais')
    print('sur le nom. Lire les deux fiches avant de toucher a l une des deux.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
