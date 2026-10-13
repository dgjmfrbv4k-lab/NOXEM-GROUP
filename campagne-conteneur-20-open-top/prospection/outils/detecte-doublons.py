#!/usr/bin/env python3
"""Balayage systematique des doublons du registre.

Cinq signaux croises, parce qu aucun ne suffit seul :
  1. meme pays + nom normalise (suffixes societaires et ponctuation retires)
  2. meme domaine de site
  3. meme adresse e-mail
  4. meme telephone, compare sur les 9 DERNIERS chiffres (voir national())
  5. meme domaine QUEL QUE SOIT LE CHAMP, site ou adresse (voir domaines())

Le cas Rozhano du 08/10 justifie les quatre premiers : les deux fiches ne differaient que
par Aluminum / Aluminium, donc le balayage par nom ne les voyait pas, et seul le
domaine les a reunies. Inversement Al-Manna et Almanco ne partagent qu un
telephone et NE SONT PAS fusionnees, les noms etant trop differents pour trancher.

Lecture seule : ce script signale, il ne modifie rien.
A relancer apres chaque lot d ajouts.
"""
import io, re, sys, unicodedata
from collections import defaultdict

CSV = sys.argv[1] if len(sys.argv) > 1 else 'liste-prospects.csv'
SUFFIXES = r'\b(ltd|llc|inc|sa|sas|sarl|srl|pty|pvt|bv|nv|gmbh|co|company|limited|group|groupe|the|and|et)\b'

def norm(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '', re.sub(SUFFIXES, ' ', s))

rows = []
for n, l in enumerate(io.open(CSV, encoding='utf-8').read().split('\n')[1:], start=2):
    if not l.strip():
        continue
    c = l.rstrip('\r').split(';')
    if len(c) < 10 or 'DOUBLON' in c[8].upper():
        continue
    rows.append((n, c))

def national(t):
    """Les 9 derniers chiffres du numero, indicatif et zero de depart retires.

    Corrige le 12/10 apres un ratage mesure : ALUBAT Guadeloupe porte
    `+590 590 26 64 40` et SOPROVER PLD `0590 26 64 40 a confirmer`. Les deux
    fiches sont a Jarry, Baie-Mahault, et c est le MEME standard — mais la
    comparaison sur TOUS les chiffres donnait 590590266440 contre 0590266440,
    donc aucun groupe. Le signal telephone etait neutralise par le FORMAT, ce
    qui est le pire cas pour un garde-fou : il tourne, il rend zero, et on le
    croit. ALUBAT est en NE PAS DEMARCHER et SOPROVER en file de qualification,
    donc le ratage menait droit a un envoi vers un compte deja ferme.

    Neuf chiffres et non huit : huit suffit a rapprocher des numeros sans
    rapport, neuf couvre le numero national de la quasi-totalite des pays du
    registre. Le choix est mesure, pas suppose — a huit le balayage rendait des
    groupes faux, a neuf il n en rend aucun.
    """
    d = re.sub(r'[^0-9]', '', t)
    return d[-9:] if len(d) >= 9 else None

# Domaines de messagerie mutualises : une adresse chez un fournisseur d acces ne
# dit RIEN d un lien de groupe. Mesure du 13/10 : sans cette liste le 5e signal
# rendait `moov.mg`, qui est l operateur malgache, et rapprochait C.I.C de
# Socavitre, deux societes sans rapport. A completer quand un cas se presente,
# et toujours apres avoir LU le groupe rendu plutot qu en le supposant.
MUTUALISES = set("""
gmail.com googlemail.com hotmail.com hotmail.fr hotmail.es hotmail.co.uk hotmail.it
yahoo.com yahoo.fr yahoo.co.in yahoo.es yahoo.com.br outlook.com outlook.fr outlook.es
live.com live.fr msn.com aol.com icloud.com me.com protonmail.com gmx.com gmx.de web.de
orange.fr wanadoo.fr free.fr sfr.fr laposte.net numericable.fr bbox.fr
qq.com 163.com 126.com sina.com rediffmail.com mail.ru yandex.ru
terra.com.br uol.com.br bol.com.br ig.com.br
moov.mg mail.pf canl.nc offratel.nc orange.mu intnet.mu
""".split())


def domaines(c):
    """Tous les domaines portes par une fiche, site ET adresse e-mail confondus.

    POURQUOI CE SIGNAL EXISTE, et c est un ratage mesure le 13/10 : les signaux 2
    et 3 comparent le domaine du SITE entre eux, et l ADRESSE entiere entre elles.
    Aucun des deux ne compare le domaine d une ADRESSE au domaine d un SITE. Or
    c est exactement sous cette forme qu un lien de groupe se montre : SOREMIR
    porte `soremir@riouglass.re` dans son champ adresse et `soremir.re` dans son
    champ site, tandis que SOFAVI porte `riouglass.re` dans son champ site. Meme
    groupe RIOU GLASS, meme compte au sens du paragraphe 7, et les quatre signaux
    etaient aveugles. Le paragraphe 6 avait pourtant tire la lecon en toutes
    lettres le 08/10 : le domaine de l adresse trahit l appartenance a un groupe
    la ou la raison sociale ne dit rien. Elle n etait pas dans le code.

    Mesure sur le registre reel au 13/10 : 3 groupes rendus, dont 2 deja connus
    et acceptes (les quatre antennes PG) et 1 vrai (riouglass.re). Un seul faux
    positif, de la classe MUTUALISES ci-dessus, corrige par la liste.
    """
    out = set()
    site = c[5].strip().lower()
    if site.startswith('www.'):
        site = site[4:]
    if site and '.' in site:
        out.add(site)
    mail = c[6].strip().lower()
    if '@' in mail:
        d = mail.rsplit('@', 1)[-1]
        if d and '.' in d:
            out.add(d)
    return {d for d in out if d not in MUTUALISES}


def sansw(site):
    """Domaine du site, prefixe www. retire PAR PREFIXE et non par caracteres.

    Corrige le 13/10. Le signal 2 employait `lstrip('www.')`, qui retire tout
    caractere de l ensemble {w, .} en tete de chaine et non le prefixe : sur
    `widrio.com` il rendait `idrio.com`, et sur `www.verre.fr` il aurait mange
    un v de moins mais un w de trop ailleurs. Meme classe de panne que le signal
    telephone neutralise par le format, et meme conduite : le garde-fou tournait,
    il rendait une cle fausse, et personne ne le voyait puisqu il ne se plaint
    jamais. Aucun groupe du registre n en dependait au moment du correctif, donc
    rien n a ete manque de ce fait - c est une reparation preventive.
    """
    d = site.strip().lower()
    return d[4:] if d.startswith('www.') else d


def groupe(cle, titre):
    d = defaultdict(list)
    for n, c in rows:
        k = cle(c)
        if not k:
            continue
        for kk in (k if isinstance(k, (set, list)) else [k]):
            d[kk].append((n, c[3]))
    sortie = [(k, v) for k, v in sorted(d.items(), key=lambda kv: str(kv[0])) if len(v) > 1]
    print('\n=== %s : %d groupe(s) ===' % (titre, len(sortie)))
    for k, v in sortie:
        print('  %s' % (' / '.join(k) if isinstance(k, tuple) else k,))
        for n, nom in v:
            print('      L%-5d %s' % (n, nom))
    return len(sortie)

total = 0
total += groupe(lambda c: (c[0], norm(c[3])) if norm(c[3]) else None, 'MEME PAYS ET MEME NOM')
total += groupe(lambda c: sansw(c[5]) or None, 'MEME DOMAINE DE SITE')
total += groupe(lambda c: c[6].strip().lower() if '@' in c[6] else None, 'MEME ADRESSE E-MAIL')
total += groupe(lambda c: national(c[7]), 'MEME TELEPHONE (9 derniers chiffres)')
total += groupe(domaines, 'MEME DOMAINE, SITE OU ADRESSE CONFONDUS')

print('\n%d fiches actives examinees, %d groupe(s) a verifier.' % (len(rows), total))
print("Attention : un meme domaine ou un meme standard peut couvrir des entites")
print("distinctes d un meme groupe (Mirodec SARL au Liban et Mirodec Gulf a Dubai,")
print("les quatre antennes PG sur pgglassafrica.com). Verifier avant de fusionner.")
