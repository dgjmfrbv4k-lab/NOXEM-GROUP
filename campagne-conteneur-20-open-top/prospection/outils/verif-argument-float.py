#!/usr/bin/env python3
"""Controle des affirmations du type « ce pays n a pas de production float ».

C est l argument le plus employe de la campagne, et c est aussi celui qui se
retourne le plus vite : un acheteur sait mieux que nous ce qui se produit chez
lui. Deux erreurs de ce type ont ete commises le 08/10 — le Kenya, alors que
Sapphire produit a Mkuranga et livre la zone, et le Chili, alors que le
paragraphe 6 de notre propre mandat nomme Vidrios Lirquen. Dans le cas de
Forpec le message etait deja parti.

Le script croise les notes du registre avec la liste des pays qui abritent ou
sont desservis par un producteur float, et signale toute fiche qui affirme le
contraire. Lecture seule.

A relancer apres chaque lot, et SURTOUT avant d employer cet argument dans un
message neuf.
"""
import io, re, sys

# Pays dont le §6 nomme un producteur, ou qu un producteur voisin dessert directement.
PRODUCTEURS = {
    'Arabie saoudite': 'Obeikan, Zoujaj, Guardian',
    'Algérie': 'Mediterranean Float Glass / Cevital',
    'Pakistan': 'Tariq Glass',
    'Bangladesh': 'PHP Float Glass',
    'Azerbaïdjan': 'Azerfloat',
    'Mexique': 'Vitro',
    'Indonésie': 'Asahimas',
    'Chili': 'Vidrios Lirquén',
    'Argentine': 'VASA',
    'Inde': 'Pioneer Float Glass et autres',
    'Tanzanie': 'Sapphire (Mkuranga)',
    'Vietnam': 'Phu My, CFG Ha Long',
    'Égypte': 'Sphinx Glass, Guardian',
    'Brésil': 'production float nationale',
    'Thaïlande': 'production float nationale',
    'Nigéria': 'production float nationale',
    'Afrique du Sud': 'PFG Building Glass',
    'Kenya': 'Sapphire livre la zone depuis la Tanzanie',
    'Ouganda': 'Sapphire livre la zone',
    'Zambie': 'Sapphire livre la zone',
    'Malawi': 'Sapphire livre la zone',
    'Mozambique': 'PFG et Sapphire livrent la zone',
    'Namibie': 'PFG en Afrique du Sud',
    'Botswana': 'PFG en Afrique du Sud',
    'Bolivie': 'VASA dessert la zone',
    'Paraguay': 'VASA dessert la zone',
    'Uruguay': 'VASA dessert la zone',
}

MOTIFS = re.compile(
    r"sans (usine|ligne|production) float|aucune float|pas de (ligne|usine) float"
    r"|100 pour cent (du verre )?(est )?importe|n a pas de float|sans float",
    re.I)

CORRIGEE = re.compile(r"CORRECTION FACTUELLE|C EST FAUX|ANGLE A REFAIRE", re.I)

CSV = sys.argv[1] if len(sys.argv) > 1 else 'liste-prospects.csv'
suspects = []
corrigees = []
for n, l in enumerate(io.open(CSV, encoding='utf-8').read().split('\n')[1:], start=2):
    if not l.strip():
        continue
    c = l.rstrip('\r').split(';')
    if len(c) < 10 or 'DOUBLON' in c[8].upper():
        continue
    if not MOTIFS.search(c[8]) or c[0] not in PRODUCTEURS:
        continue
    # Une fiche deja corrigee CITE l affirmation fausse dans sa note de correction :
    # sans cette exception l outil la signalerait indefiniment et crierait au loup.
    if CORRIGEE.search(c[8]):
        corrigees.append((n, c[0], c[3]))
        continue
    suspects.append((n, c[0], c[3], c[9], PRODUCTEURS[c[0]]))

print('=== Fiches affirmant l absence de float dans un pays qui en produit ===')
for n, pays, soc, st, prod in sorted(suspects):
    print('  L%-5d %-18s %-34s %-22s  <-- %s' % (n, pays, soc[:34], st, prod))
print('\n%d fiche(s) a corriger.' % len(suspects))
if not suspects:
    print("Aucune. L argument du float absent n est employe que la ou il est vrai.")
if corrigees:
    print('\n%d fiche(s) deja corrigee(s), ignoree(s) :' % len(corrigees))
    for n, pays, soc in sorted(corrigees):
        print('  L%-5d %-18s %s' % (n, pays, soc[:40]))
