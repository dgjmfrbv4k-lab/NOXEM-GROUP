#!/usr/bin/env python3
"""Balayage systematique des doublons du registre.

Quatre signaux croises, parce qu aucun ne suffit seul :
  1. meme pays + nom normalise (suffixes societaires et ponctuation retires)
  2. meme domaine de site
  3. meme adresse e-mail
  4. meme telephone, compare sur les 9 DERNIERS chiffres (voir national())

Le cas Rozhano du 08/10 justifie les quatre : les deux fiches ne differaient que
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

def groupe(cle, titre):
    d = defaultdict(list)
    for n, c in rows:
        k = cle(c)
        if k:
            d[k].append((n, c[3]))
    sortie = [(k, v) for k, v in sorted(d.items(), key=lambda kv: str(kv[0])) if len(v) > 1]
    print('\n=== %s : %d groupe(s) ===' % (titre, len(sortie)))
    for k, v in sortie:
        print('  %s' % (' / '.join(k) if isinstance(k, tuple) else k,))
        for n, nom in v:
            print('      L%-5d %s' % (n, nom))
    return len(sortie)

total = 0
total += groupe(lambda c: (c[0], norm(c[3])) if norm(c[3]) else None, 'MEME PAYS ET MEME NOM')
total += groupe(lambda c: c[5].strip().lower().lstrip('www.') or None, 'MEME DOMAINE DE SITE')
total += groupe(lambda c: c[6].strip().lower() if '@' in c[6] else None, 'MEME ADRESSE E-MAIL')
total += groupe(lambda c: national(c[7]), 'MEME TELEPHONE (9 derniers chiffres)')

print('\n%d fiches actives examinees, %d groupe(s) a verifier.' % (len(rows), total))
print("Attention : un meme domaine ou un meme standard peut couvrir des entites")
print("distinctes d un meme groupe (Mirodec SARL au Liban et Mirodec Gulf a Dubai,")
print("les quatre antennes PG sur pgglassafrica.com). Verifier avant de fusionner.")
