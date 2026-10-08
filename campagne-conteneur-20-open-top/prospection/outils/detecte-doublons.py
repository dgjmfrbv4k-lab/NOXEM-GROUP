#!/usr/bin/env python3
"""Balayage systematique des doublons du registre.

Quatre signaux croises, parce qu aucun ne suffit seul :
  1. meme pays + nom normalise (suffixes societaires et ponctuation retires)
  2. meme domaine de site
  3. meme adresse e-mail
  4. meme telephone (chiffres seuls)

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
total += groupe(lambda c: (lambda t: t if len(t) >= 8 else None)(re.sub(r'[^0-9]', '', c[7])), 'MEME TELEPHONE')

print('\n%d fiches actives examinees, %d groupe(s) a verifier.' % (len(rows), total))
print("Attention : un meme domaine ou un meme standard peut couvrir des entites")
print("distinctes d un meme groupe (Mirodec SARL au Liban et Mirodec Gulf a Dubai,")
print("les quatre antennes PG sur pgglassafrica.com). Verifier avant de fusionner.")
