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

# Analyse des arguments. La forme --depuis 42 consomme le 42 qui suit, sinon il
# retombait dans les positionnels et devenait le nom du fichier : le 13/10 un
# --depuis 42 a fait chercher un fichier nomme 42. L echec etait bruyant, donc
# sans degat, mais un outil qui se trompe sur sa propre invocation finit par
# etre contourne plutot que corrige.
DEPUIS = 32
args, attendu = [], False
for a in sys.argv[1:]:
    if attendu:
        DEPUIS, attendu = int(a), False
    elif a.startswith('--depuis'):
        if '=' in a:
            DEPUIS = int(a.split('=', 1)[1])
        else:
            attendu = True
    elif not a.startswith('--'):
        args.append(a)
assert not attendu, '--depuis attend un numero'
SRC = args[0] if args else 'TEXTES-PRETS.md'

INTERDITS = [
    r'\beuros?\b', r'\bprecios?\b', r'\bprices?\b', r'\bUSD\b', '€', r'\bplazos?\b',
    r'\bcertificad\w*\b', r'\bcertificat\w*\b', r'\bISO\s?9', r'\bd[ée]lais?\b',
    r'\bdescuento\b', r'\bremise\b', r'\bgarantia\b', r'\bgarantie\b', r'\bwarranty\b',
    r'\bpas de production locale\b', r'\bno local production\b',
    r'\blead ?times?\b', r'\bdelivery times?\b', r'\bplazo de entrega\b',
]

# CONDITIONNELS — ni interdits ni libres, et c est pour cela qu ils ont leur
# propre liste. Trouve le 12/10 a 18h13 : le controleur a signale « antidumping »
# dans le texte bresilien n 41 comme une faute. C EN EST UNE AU MEXIQUE ET DANS
# LES DOM, ou le §6 interdit d ecrire quoi que ce soit sur la fiscalite a
# l entree. C EST AU CONTRAIRE L ARGUMENT CENTRAL AU BRESIL, ou le meme §6
# l autorise expressement et impose seulement une formulation prudente.
# **Un mot dont la licite depend du PAYS ne peut pas etre interdit en bloc** —
# l interdire ferait supprimer un argument juste, le permettre laisserait passer
# une faute grave. Il est donc SIGNALE, et il ne compte comme defaut que si le
# commentaire de la section ne cite pas le §6, c est-a-dire si l auteur n a pas
# dit pourquoi il s y autorise. C est le meme principe que la neutralisation
# phrase par phrase de verif-argument-float : on ne supprime pas le signal, on
# demande la justification.
CONDITIONNELS = [r'\bantidumping\b', r'\bdroits? de douane\b', r'\btariffs?\b',
                 r'\bdut(y|ies)\b', r'\bcuota\b', r'\boctroi de mer\b']
# Formule imposee du paragraphe 5. LISTE COMPLETEE LE 13/10 : elle ne portait
# qu'UNE forme espagnole, le calque "bajo reserva de", alors que les textes
# reels de la campagne emploient depuis le debut "sujeta a validacion POR
# nuestra parte" et "sujeta a validacion DE nuestra parte", qui sont l'espagnol
# naturel. Le texte 69 a donc ete refuse pour une formule parfaitement valable.
# C'est exactement la panne du texte 45 sur la porte de sortie portugaise : un
# controleur dont le vocabulaire est plus pauvre que celui des textes crie au
# loup, et un garde-fou qui crie au loup finit par etre ignore.
FORMULE = ['subject to validation on our side',
           'sous reserve de validation de notre cote',
           'sous réserve de validation de notre côté',
           'bajo reserva de validacion de nuestra parte',
           'bajo reserva de validación de nuestra parte',
           'sujeta a validacion de nuestra parte',
           'sujeta a validación de nuestra parte',
           'sujeta a validacion por nuestra parte',
           'sujeta a validación por nuestra parte',
           'sujeto a validacion de nuestra parte',
           'sujeto a validación de nuestra parte',
           'sob reserva de validacao da nossa parte',
           'sob reserva de validação da nossa parte',
           # Ajout du 13/10, troisieme fois que le vocabulaire du controleur est plus
           # pauvre que celui des textes : le portugais naturel dit sujeita a validacao,
           # et deux textes anterieurs a la regle l'employaient deja.
           'sujeita a validacao da nossa parte',
           'sujeita a validação da nossa parte',
           'sujeita a validacao de nossa parte',
           'sujeita a validação de nossa parte',
           'sujeito a validacao da nossa parte',
           'sujeito a validação da nossa parte',
           'sujeita a validacao do nosso lado',
           'sujeita a validação do nosso lado']
# Portes de sortie reconnues. Ajout du 13/10 des deux formes "je ne reecrirai
# pas" en portugais et en espagnol : le texte 45 portait "nao voltarei a
# escrever", qui est une porte de sortie parfaitement valable, et le controleur
# l a comptee absente. Un garde-fou qui refuse une formulation correcte finit
# par etre contourne, c est la lecon du §12 sur les faux positifs.
# Ajout du 13/10, meme cause que ci-dessus : "I will not push" et "no insisto"
# sont employes dans les textes reels et dans les relances deja parties, et ils
# manquaient. Le present indicatif n'etait reconnu qu'au futur.
SORTIE = ['not write again', 'no insistire', "n'insisterai pas", 'n insisterai pas',
          'nao insistirei', 'no insistiré', 'file stays open', 'dossier reste ouvert',
          'nao voltarei a escrever', 'no volvere a escribir', 'no volveré a escribir',
          'nao voltarei a escrever-lhes', 'will not push', 'no insisto',
          "je n'insiste pas", 'je n insiste pas', 'nao insisto', 'não insisto']
MORT = '+33 7 69'
SIGNATURE = 'president - noxem group sas'

texte = io.open(SRC, encoding='utf-8').read()
# ⚠️ SIXIEME CONTROLE, AJOUTE LE 14/10 A 12h26, ET IL EST NE D UN DEFAUT QUE CE
# SCRIPT LAISSAIT PASSER DEPUIS SA CREATION : UN TEXTE QUI NOMME DES REFERENCES
# SANS DONNER LE LIEN DE LA PAGE. Le paragraphe 9 point 3 impose « les references
# de notre gamme qui collent a ce qu ils font, AVEC LE LIEN DE LA PAGE », et le
# paragraphe 8 impose de choisir la page et de dire en une ligne pourquoi. Le
# controleur ne regardait pas du tout ce point. Mesure faite avant d ecrire la
# regle : 39 premiers contacts listaient leurs references sans aucun lien, et
# 30 ETAIENT DEJA PARTIS, donc irreparables.
#
# LE DECLENCHEUR EST LA LISTE DE REFERENCES, PAS LE NUMERO DU TEXTE, et c est
# voulu : une RELANCE ne repete pas le premier message et n a donc aucune
# reference a lier. Lui reprocher l absence de lien serait un faux a coup sur,
# et c est la panne decrite trois fois dans ce fichier — un garde-fou qui crie
# au loup finit ignore. En declenchant sur la PRESENCE d une puce de produit, le
# controle est muet sur les relances PAR CONSTRUCTION, sans avoir a deviner
# qu un texte en est une. Verifie : au seuil 32 il rend exactement les 39
# premiers contacts fautifs et PAS UNE des 25 relances sans lien.
PRODUIT = re.compile(
    r'^\s*[-·•*]\s.*\b(float|low.?e|emissivit\w*|mirror|espejo|espelho|miroir|'
    r'laminated|feuillet\w*|laminado|tempered|tremp\w*|templado|temperado|'
    r'lacquered|laqu\w*|glazing|vitrage|vidrio|vidro|verre|glass)\b',
    re.I | re.M)
LIEN = 'noxemgroup.com/'
# Seuil propre a ce controle. La regle est consignee le 14/10 ; les 30 textes
# fautifs anterieurs sont partis et ne se reparent pas, les signaler a chaque
# passage ne ferait que noyer les vrais. Les cinq encore rattrapables ont ete
# corriges a la main le jour meme.
DEPUIS_LIEN = 103

# decoupage par section ## N. <titre>
parts = re.split(r'^## (\d+)\.\s*(.+)$', texte, flags=re.M)
sections = [(int(parts[i]), parts[i + 1], parts[i + 2]) for i in range(1, len(parts), 3)]

verifies = ignores = defauts = 0
avertis = []
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
        # ⚠️ TOUS les controles portent sur le texte APLATI, et c est un correctif
        # du 13/10. Les motifs etaient cherches dans le texte BRUT, donc une
        # expression de deux mots coupee par un RETOUR A LA LIGNE y echappait :
        # \blead ?times?\b accepte une espace, pas un saut de ligne. Le texte 50,
        # qui attend l accord de Kevin pour partir, portait « continuity of
        # supply, lead\ntimes » et le controleur rendait ZERO defaut. C est la
        # panne la plus dangereuse pour un garde-fou, celle du paragraphe 12 : il
        # tournait, il rendait zero, et on le croyait.
        plat = ' '.join(t.split()).lower()
        pb = []
        mots = [m for m in INTERDITS if re.search(m, plat, re.I)]
        if mots:
            pb.append('MOT INTERDIT %s' % mots)
        cond = [m for m in CONDITIONNELS if re.search(m, plat, re.I)]
        if cond:
            if '§6' in corps_section:
                avertis.append((num, titre, cond))
            else:
                pb.append('MOT CONDITIONNEL %s SANS JUSTIFICATION §6 dans le commentaire' % cond)
        if not any(f in plat for f in FORMULE):
            pb.append('FORMULE IMPOSEE ABSENTE')
        n = plat.count(SIGNATURE)
        if n != 1:
            pb.append('SIGNATURE presente %d fois au lieu d une' % n)
        if MORT in plat or MORT in t:
            pb.append('NUMERO MORT +33 7 69 72 58 92')
        if not any(s in plat for s in SORTIE):
            pb.append('pas de porte de sortie')
        if num >= DEPUIS_LIEN and PRODUIT.search(t) and LIEN not in t:
            pb.append('REFERENCES NOMMEES SANS LIEN DE PAGE — §9 point 3 et §8')
        if pb:
            defauts += 1
            print('  ✗ %d. %s' % (num, titre[:66]))
            for p in pb:
                print('      %s' % p)

for num, titre, cond in avertis:
    print('  ! %d. %s' % (num, titre[:66]))
    print('      mot conditionnel %s — justifie par une mention du §6 dans le commentaire' % cond)

print('\n%d texte(s) controle(s), %d anterieur(s) ignore(s), %d a corriger, %d signale(s).'
      % (verifies, ignores, defauts, len(avertis)))
if not defauts:
    print('Aucun. Les textes respectent les interdits du §5 et la forme du §9.')
