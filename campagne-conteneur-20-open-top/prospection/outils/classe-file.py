#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
classe-file.py — classe la file des fiches PRETES (statut `A ENVOYER *`) selon les
criteres mesures du paragraphe 6 du mandat, pour decider QUI part en premier quand
la file est plus profonde que la cadence quotidienne.

Ne par juge PAS si une fiche est bonne : il ordonne celles qui sont deja pretes.

⚠⚠ REGLE DE CONSTRUCTION, ET ELLE EST NEE D UNE FAUTE MESUREE LE 20/10 :
    LE CLASSEMENT SE FAIT SUR LE CHAMP ACTIVITE (c[4]), JAMAIS SUR LA NOTE (c[8]).
    La premiere version lisait les deux et rangeait 23 fiches sur 96 en « verrier + pose »
    — la classe a ZERO pour cent — parce que le mot « pose » est partout dans la prose
    francaise des notes : « verdict de deverrouillage POSE », « la question se POSE »,
    « le paragraphe 5 POSE ». Le cas le plus net etait Refricomp, dont la note dit
    « aucun rayon de pose », c est-a-dire exactement le contraire, et que l outil
    classait en poseur.
    C est le faux positif Klingshield du 09/10, reproduit une semaine plus tard dans un
    outil neuf. La NOTE ne sert qu a reperer les SIGNAUX D ENTREE, qui sont des
    expressions techniques et non des mots courants.

⚠ IL ORDONNE, IL NE DECIDE PAS. Les fenetres horaires, les jours feries et les
  interdits par pays restent a lire dans PLAN-ENVOIS.md et au paragraphe 6.
"""
import io, re, sys

CSV = 'liste-prospects.csv'

# Marches ou un argument VRAI existe (paragraphe 6), et marches ou il n en existe pas.
FORT = {'États-Unis':3,'Canada':3,'Brésil':3,'Australie':3,'Nouvelle-Zelande':3,
        'Colombie':2,'Mexique':2,'Chili':2,'Argentine':2,'Guatemala':2,
        'Finlande':2,'Suède':2,'Norvège':2,'Danemark':2,'Islande':2}
FAIBLE = {'Pérou':-2,'Nigéria':-2,'Égypte':-2,'Arabie saoudite':-2,
          'Émirats arabes unis':-2,'Singapour':-2,'Inde':-3,
          'Kenya':-2,'Ouganda':-2,'Tanzanie':-2}

# Signaux d entree, ponderes par leur FORCE MESUREE au paragraphe 6 :
# vocabulaire d import > mode de vente > fait douanier > epaisseur + format.
SIGNAUX = [
 (5, 'vocab IMPORT',      r'\bindent|mixed container|conteneur group|importacion directa|importa[cç][aã]o direta|mill direct'),
 (4, 'mode de vente',     r'by the case|full case|meia chapa|media lamina|half sheet|carga fechada|stock sheet|a la caisse|ter[cç]o'),
 (4, 'fait douanier',     r'recensement douanier|base des importateurs|fait douanier'),
 (2, 'epaisseur+format',  r'epaisseur|espessura|espesor|thickness|format de feuille'),
 (2, 'independant',       r'\bindepend'),
 (-2,'-echelle',          r'reserve d echelle|petite structure|sur mesure pour chaque|comptoir de negoce'),
]

def classe_metier(act):
    """Classe sur le CHAMP ACTIVITE SEUL. Voir l avertissement en tete de fichier."""
    a = act.lower()
    pose = re.search(r'\bpose\b|installat|vitrier', a)
    verr = re.search(r'tremp|temper|miroiter|vitrage isolant|insulating|feuillet|laminat|'
                     r'argentur|silvering|beneficiad|processador|faconn|fabricant de verre|transformateur', a)
    nego = re.search(r'grossiste|distribut|negoce|importat|stockist|wholesal|mayorista|atacad|merchant|negociant', a)
    indus= re.search(r'refrigeration|vitrine|serre|porte vitree|porte de verre|fenetre|insert|expositeur', a)
    if verr and not pose: return 4, 'verrier'
    if nego and not pose: return 3, 'negoce'
    if indus:             return 3, 'industrie consommatrice'
    if verr and pose:     return 0, 'verrier+pose'
    if re.search(r'aluminium|facade|mur-rideau|curtain wall|menuiserie|esquadria', a): return 1, 'facade'
    return 2, 'autre'

def note(c):
    s, why = classe_metier(c[4])
    why = [why]
    s += FORT.get(c[0], 0) + FAIBLE.get(c[0], 0)
    n = c[8].lower()
    for pts, nom, pat in SIGNAUX:
        if re.search(pat, n):
            s += pts; why.append(nom)
    return s, why

def main():
    lim = int(sys.argv[1]) if len(sys.argv) > 1 else 25
    R = [l.split(';') for l in io.open(CSV, encoding='utf-8').read().rstrip('\n').split('\n')[1:]
         if len(l.split(';')) == 10]
    F = [c for c in R if c[9].startswith('A ENVOYER')]
    F.sort(key=lambda c: -note(c)[0])
    print('FILE PRETE : %d fiches. Classement sur le CHAMP ACTIVITE, signaux lus dans la note.' % len(F))
    print('⚠ Il ORDONNE, il ne DECIDE pas : fenetres, feries et interdits par pays restent a lire.')
    print()
    print('%-4s %-4s %-16s %-42s %s' % ('rang', 'pts', 'pays', 'societe', 'motifs'))
    for i, c in enumerate(F[:lim], 1):
        s, w = note(c)
        print('%-4d %-4d %-16s %-42s %s' % (i, s, c[0][:16], c[3][:42], ' '.join(w)))

if __name__ == '__main__':
    main()
