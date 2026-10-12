#!/usr/bin/env python3
"""Controle avant-vol des textes de TEXTES-PRETS.md.

Verifie sur le CORPS DU MESSAGE seul :
  1. aucun mot interdit par le paragraphe 5 — prix, delai, certificat, garantie
  2. la formule imposee est presente, dans l une des langues de la campagne
  3. la signature du paragraphe 10 figure UNE SEULE FOIS
  4. le numero mort +33 7 69 72 58 92 n apparait nulle part
  5. une porte de sortie est offerte

TROIS CHOSES QU IL A FALLU CORRIGER AVANT DE LE GARDER, LE 12/10, ET ELLES SONT
LA RAISON D ETRE DE CE PAVE. Un garde-fou se juge sur son taux de faux positifs
autant que sur ses prises : la premiere version rendait **39 defauts sur 46
textes**, dont zero vrai, et un outil qui crie ainsi finit ignore — c est alors
un VRAI defaut qui passe. C est la lecon deja tiree sur verif-argument-float.

  a. IL CHERCHAIT DES SOUS-CHAINES. « euro » tombait dans « European origin » et
     « prix » dans « ceci n est pas une demande de prix », qui dit exactement le
     contraire d une offre de prix. Il cherche desormais des MOTS entiers.
  b. IL APPARIAIT MAL LES BLOCS ET LES TITRES. Un texte porte souvent DEUX blocs
     de code, l objet et le corps, donc le n-ieme bloc n est pas le n-ieme texte.
     Il decoupe desormais par SECTION `## N.` et ne retient, dans chacune, que
     les blocs d au moins cinq lignes — un objet tient sur une ligne.
  c. IL CONTROLAIT DES TEXTES ANTERIEURS A LA REGLE. La signature dans le corps
     date du 12/10 a 09h40 : reprocher son absence aux textes ecrits avant est
     un faux a coup sur. Il ne controle donc que les textes numerotes a partir
     de --depuis, 32 par defaut.

Lecture seule. Usage :
    python3 outils/verif-texte.py [fichier] [--depuis N]
"""
import io, re, sys

args = [a for a in sys.argv[1:] if not a.startswith('--')]
SRC = args[0] if args else 'TEXTES-PRETS.md'
DEPUIS = 32
for a in sys.argv[1:]:
    if a.startswith('--depuis'):
        DEPUIS = int(a.split('=')[1] if '=' in a else sys.argv[sys.argv.index(a) + 1])

INTERDITS = [
    r'\beuros?\b', r'\bprecios?\b', r'\bprices?\b', r'\bUSD\b', '€', r'\bplazos?\b',
    r'\bcertificad\w*\b', r'\bcertificat\w*\b', r'\bISO\s?9', r'\bd[ée]lais?\b',
    r'\bdescuento\b', r'\bremise\b', r'\bgarantia\b', r'\bgarantie\b', r'\bwarranty\b',
    r'\bpas de production locale\b', r'\bno local production\b',
    r'\bdroits? de douane\b', r'\btariffs?\b', r'\bdut(y|ies)\b', r'\bantidumping\b',
    r'\blead ?times?\b', r'\bdelivery times?\b', r'\bplazo de entrega\b',
]
FORMULE = ['subject to validation on our side',
           'sous reserve de validation de notre cote',
           'sous réserve de validation de notre côté',
           'bajo reserva de validacion de nuestra parte',
           'sob reserva de validacao da nossa parte']
SORTIE = ['not write again', 'no insistire', "n'insisterai pas", 'n insisterai pas',
          'nao insistirei', 'no insistiré', 'file stays open', 'dossier reste ouvert']
MORT = '+33 7 69'
SIGNATURE = 'president - noxem group sas'

texte = io.open(SRC, encoding='utf-8').read()
# decoupage par section ## N. <titre>
parts = re.split(r'^## (\d+)\.\s*(.+)$', texte, flags=re.M)
sections = [(int(parts[i]), parts[i + 1], parts[i + 2]) for i in range(1, len(parts), 3)]

verifies = ignores = defauts = 0
print('%s : %d section(s), controle a partir du n° %d\n' % (SRC, len(sections), DEPUIS))
for num, titre, corps_section in sections:
    if num < DEPUIS:
        ignores += 1
        continue
    blocs = [b for b in re.findall(r'```(.*?)```', corps_section, re.S)
             if len(b.strip().split('\n')) >= 5]
    if not blocs:
        print('  ? %d. %s — aucun corps de message trouve' % (num, titre[:60]))
        continue
    for t in blocs:
        verifies += 1
        plat = ' '.join(t.split()).lower()
        pb = []
        mots = [m for m in INTERDITS if re.search(m, t, re.I)]
        if mots:
            pb.append('MOT INTERDIT %s' % mots)
        if not any(f in plat for f in FORMULE):
            pb.append('FORMULE IMPOSEE ABSENTE')
        n = plat.count(SIGNATURE)
        if n != 1:
            pb.append('SIGNATURE presente %d fois au lieu d une' % n)
        if MORT in t:
            pb.append('NUMERO MORT +33 7 69 72 58 92')
        if not any(s in plat for s in SORTIE):
            pb.append('pas de porte de sortie')
        if pb:
            defauts += 1
            print('  ✗ %d. %s' % (num, titre[:66]))
            for p in pb:
                print('      %s' % p)

print('\n%d texte(s) controle(s), %d anterieur(s) ignore(s), %d a corriger.'
      % (verifies, ignores, defauts))
if not defauts:
    print('Aucun. Les textes respectent les interdits du §5 et la forme du §9.')
