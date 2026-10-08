# -*- coding: utf-8 -*-
"""Regenere l'export de prospects Afrique / Moyen-Orient / Guadeloupe demande par Aaron.
A relancer apres chaque lot d'ajouts : python3 outils/genere-export-zone.py"""
import io, os, collections

ICI = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(ICI)
REG = os.path.join(BASE, 'liste-prospects.csv')
OUT = os.path.join(BASE, 'exports', 'PROSPECTS-AFRIQUE-MOYEN-ORIENT-GUADELOUPE.csv')

AFR = set("""Afrique du Sud|Algérie|Angola|Bénin|Botswana|Burkina Faso|Burundi|Cameroun|Cap-Vert|Comores|
Congo|Congo RDC|Côte d'Ivoire|Djibouti|Érythrée|Eswatini|Éthiopie|Gabon|Gambie|Ghana|Guinée|
Guinée équatoriale|Guinée-Bissau|Kenya|La Réunion|Lesotho|Liberia|Libye|Madagascar|Malawi|Mali|Maroc|
Maurice|Mauritanie|Mayotte|Mozambique|Namibie|Niger|Nigéria|Ouganda|Rwanda|Sénégal|Seychelles|
Sierra Leone|Somalie|Soudan|Soudan du Sud|Tanzanie|Tchad|Togo|Tunisie|Zambie|Zimbabwe""".replace('\n','').split('|'))
MO = set("""Arabie saoudite|Bahreïn|Émirats arabes unis|Irak|Iran|Jordanie|Koweït|Liban|Oman|Qatar|
Syrie|Yémen""".replace('\n','').split('|'))
AFR = set(x.strip() for x in AFR if x.strip()); MO = set(x.strip() for x in MO if x.strip())
AFR.add('Égypte')   # Egypte comptee en Afrique pour ne pas la compter deux fois

def zone(p):
    if p == 'Guadeloupe': return 'Guadeloupe'
    if p in AFR: return 'Afrique'
    if p in MO:  return 'Moyen-Orient'
    return None

def canal(mail, tel):
    if mail and tel: return 'e-mail + telephone'
    if mail:         return 'e-mail'
    if tel:          return 'telephone'
    return 'AUCUN CANAL'

def etat(st):
    s = st.strip()
    if s.startswith(('NE PAS', 'ECARTE', 'ADRESSE INVALIDE')):            return 'ecarte ou protege'
    if s.startswith(('DEMANDE DE PRIX','DEMANDE DE DEVIS','DEVIS ENVOYE',
                     'EN NEGOCIATION','REPONSE','A RELANCER','REFUS')):   return 'DOSSIER VIVANT'
    if s.startswith(('A ENVOYER', 'A RENVOYER', 'RELANCE DIFFEREE')):     return 'pret a partir'
    if s.startswith(('ENVOYE', 'RELANCE')):                              return 'deja contacte'
    return 'a ouvrir'

R = [l.rstrip('\r').split(';') for l in
     io.open(REG, encoding='utf-8').read().rstrip('\n').split('\n')[1:]]
R = [c for c in R if len(c) == 10]

lignes, stats = [], collections.defaultdict(collections.Counter)
for c in R:
    z = zone(c[0])
    if not z: continue
    e, k = etat(c[9]), canal(c[6].strip(), c[7].strip())
    stats[z][e] += 1; stats[z]['TOTAL'] += 1
    if c[6].strip(): stats[z]['avec e-mail'] += 1
    lignes.append([z] + c[:6] + [c[7], k, e, c[9]])

ORDRE = {'Afrique': 0, 'Moyen-Orient': 1, 'Guadeloupe': 2}
lignes.sort(key=lambda r: (ORDRE[r[0]], r[1], r[4]))

ENTETE = 'Zone;Pays;Ville;Societe;Activite;Site;Email;Telephone;Joignable par;Etat;Statut registre'
for r in lignes:
    assert len(r) == 11, 'ligne a %d champs' % len(r)
io.open(OUT, 'w', encoding='utf-8').write(
    ENTETE + '\n' + '\n'.join(';'.join(x.strip() for x in r) for r in lignes) + '\n')

tot = 0
for z in ('Afrique', 'Moyen-Orient', 'Guadeloupe'):
    s = stats[z]; tot += s['TOTAL']
    print('%-13s %4d prospects  (%d avec e-mail)  | %s' % (
        z, s['TOTAL'], s['avec e-mail'],
        '  '.join('%s %d' % (k, v) for k, v in sorted(s.items())
                  if k not in ('TOTAL', 'avec e-mail'))))
print('-' * 100)
print('TOTAL EXPORTE : %d prospects   |   objectif Aaron : 500   |   manquants : %d' % (tot, max(0, 500 - tot)))
print('Fichier : %s' % OUT)
