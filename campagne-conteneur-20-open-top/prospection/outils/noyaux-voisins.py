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

CORRECTIF ENVISAGE LE 19/10 AU SOIR PUIS REJETE SUR MESURE, ET IL FAUT DIRE POURQUOI POUR QU UNE
SESSION FUTURE NE LE REFASSE PAS EN CROYANT AMELIORER L OUTIL.
Les dix-huit paires ont ete lues une par une. UNE SEULE posait un vrai risque, et elle valait a
elle seule l outil : Wholesale Glass Distributors Inc, a Mauldin en Caroline du Sud, contre
Wholesale Glass Distributors Memphis, DEJA RELANCEE au 12/10. Tranchee, deux societes sans
rapport, indicatifs 864 contre 901 et deux domaines distincts, verdict ecrit dans les deux fiches.
En face, une dizaine de paires sont du BRUIT DE SOUS-CHAINE : un noyau se retrouve a une position
quelconque d un noyau plus long, EN TRAVERS DES MOTS. nationalglass est dans
interNATIONALGLASSproducts, glasscorp dans cullyGLASSCORPoration, glasstemp dans
starGLASSTEMPering, artvidros dans smARTVIDROS. C est exactement le defaut du correctif
d initiales rejete le 19/10 au matin, qui cherchait les initiales n importe ou dans le nom aplati.
LE CORRECTIF NATUREL ETAIT DONC D EXIGER QUE L INCLUSION TOMBE SUR UNE FRONTIERE DE MOT, en
comparant des SUITES DE MOTS au lieu de chaines aplaties. Teste a la main sur les dix-huit :
il supprime bien les neuf ou dix paires de bruit, il garde Wholesale Glass Distributors, il garde
Saudi Arabian Glass contre Arabian Glass, Texas Glass, Insulite et Innovative Glass.
MAIS IL PERD LA PAIRE DU GHANA, Glassworks Limited contre Kumasi Glass Works Ltd, parce que
glassworks en un mot n est pas une suite de mots de glass plus works — et c est une question
d identite REELLE et encore ouverte, portee au suivi depuis plusieurs jours.
Or la normalisation des separateurs est precisement ce qui fait vivre cet outil : c est elle qui
rend Alpha Glass contre Alphaglass et Glaz-Tech contre glaztech. Exiger la frontiere de mot, c est
la desactiver.
DECISION : ON NE TOUCHE PAS A L OUTIL. Payer une vraie prise pour reduire un bruit cosmetique est
le mauvais marche, et le mandat l accepte explicitement au paragraphe 12 — cinq lignes qu on
relit valent mieux qu un silence qui cache un sixieme. Dix-huit paires se lisent en une minute,
et cette lecture-la a rendu une vraie prise. Le jour ou le compte depassera la cinquantaine, le
remede a essayer d abord n est PAS la frontiere de mot mais l allongement de MIN_NOYAU et
l enrichissement de GENERIQUES, qui ne desactivent pas la normalisation.
A savoir aussi, parce que c est la source de bruit la plus concentree : la fiche americaine dont
la raison sociale est litteralement Architectural Glass — c est son vrai nom, son domaine est
architecturalglass.com — s apparie avec les TROIS fiches qui contiennent ces deux mots, Blue Star,
AMG et Nova. La donnee est juste, le bruit est structurel, et il se lit en trois lignes.
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
