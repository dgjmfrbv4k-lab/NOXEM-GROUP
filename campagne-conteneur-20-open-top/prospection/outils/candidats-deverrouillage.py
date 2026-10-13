# -*- coding: utf-8 -*-
"""Liste les fiches qui valent VRAIMENT un appel de recherche de deverrouillage.

POURQUOI CET OUTIL EXISTE, parce que la raison est la seule chose qui empeche de
le contourner. Le 13/10 j ai depense CINQ appels de recherche sur cinq fiches
dont le registre portait DEJA la reponse : Davis Glass, Univers du Verre, Crone
Wholesale Glass, Tempera Primos et Vitral Vidros Planos. Leurs notes disaient
toutes, en toutes lettres, AUCUNE ADRESSE PUBLIEE, formulaire uniquement, fiche
telephonique ou domaine introuvable.

LA CAUSE N EST PAS L ETOURDERIE, C EST LE FILTRE. Je selectionnais sur le STATUT
et sur un MARQUEUR en majuscules du type TESTEE ou DEVERROUILLEE. Or le registre
consigne son verdict EN PROSE. Un filtre sur marqueurs ne peut donc pas voir une
decision ecrite en mots - c est exactement la lecon Staklo Bakar du paragraphe 12,
un comptage automatique ne voit pas une decision ecrite en prose, prise par
l autre bout.

Le budget de recherche est de 200 appels par tour et la methode en coute deux par
fiche, soit 70 a 90 fiches au maximum. Cinq appels perdus sont donc trois fiches
reelles en moins.
"""
import io, re, sys, signal
# Sortie tronquee par un head ou un grep : on sort proprement au lieu d un
# BrokenPipeError, qui masquerait une vraie erreur dans le bruit.
signal.signal(signal.SIGPIPE, signal.SIG_DFL)

SRC = sys.argv[1] if len(sys.argv) > 1 else 'liste-prospects.csv'

# Verdicts deja rendus, en prose comme en marqueur. Toute fiche qui en porte un
# a DEJA ete travaillee : la rechercher de nouveau ne rend que le meme resultat.
VERDICTS = [
    r'aucune adresse',
    r'formulaire uniquement',
    r'ne propose qu un formulaire',
    r'fiche telephonique',
    r'dossier telephonique',
    r'domaine introuvable',
    r'irrecuperable',
    r'obfusqu',                      # adresses masquees sur la page
    r'\bTESTEE\b',
    r'\bRETESTEE\b',
    r'\bDEVERROUILLEE\b',
]
# Statuts qu on ne travaille pas : fiche fermee, compte protege, arbitrage en cours.
STATUTS_EXCLUS = ('ECARTE', 'NE PAS DEMARCHER', 'A VALIDER AARON')

lignes = [l for l in io.open(SRC, encoding='utf-8').read().rstrip('\n').split('\n')[1:]]
retenues, ecartees = [], []
for l in lignes:
    c = l.rstrip('\r').split(';')
    if len(c) != 10:
        continue
    pays, soc, site, mail, tel, note, statut = c[0], c[3], c[5], c[6], c[7], c[8], c[9]
    if mail.strip():                                  # deja joignable par mail
        continue
    if statut.startswith(STATUTS_EXCLUS):
        continue
    deja = [v for v in VERDICTS if re.search(v, note, re.I)]
    (ecartees if deja else retenues).append((pays, soc, site, tel, statut, deja))

retenues.sort(key=lambda r: (r[2] == '', r[0], r[1]))   # celles qui ont un site d abord
print('=== %d FICHE(S) A TRAVAILLER, site connu en tete ===' % len(retenues))
for pays, soc, site, tel, statut, _ in retenues:
    print('  %-22s %-42s %-28s %s' % (pays[:22], soc[:42], (site or '(pas de site)')[:28], statut))
print()
print('=== %d fiche(s) ECARTEES : le registre porte deja leur verdict ===' % len(ecartees))
for pays, soc, site, tel, statut, deja in ecartees[:12]:
    print('  %-22s %-38s motif : %s' % (pays[:22], soc[:38], ', '.join(d.strip('\\b') for d in deja[:2])))
if len(ecartees) > 12:
    print('  ... et %d autres.' % (len(ecartees) - 12))
