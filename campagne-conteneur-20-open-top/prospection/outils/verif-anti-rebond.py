#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Controle AVANT-VOL de la REGLE ANTI-REBOND du paragraphe 5, sur la FILE D ENVOI.

POURQUOI CE SCRIPT EXISTE, et c est une faute du 20/10 qui l a fait naitre.
La fiche CRISTALERIA AMIGO (Porto Rico) etait en `A ENVOYER 2026-10-27` avec
`cr.amigo@hotmail.com` au champ. Second temps fait : LEUR PAGE DE CONTACT NE PUBLIE
QU UN FORMULAIRE. L adresse venait donc d un annuaire, son domaine n est pas celui du
site, et le paragraphe 5 exige dans ce cas que la societe la publie ELLE-MEME. Elle ne
la publiait pas. **Une fiche allait partir sur une adresse qui ne satisfait pas la
regle, et rien ne l aurait vu.**

CE QUE LE SCRIPT CONTROLE, ET IL NE CONTROLE QUE CELA :
toute fiche en `A ENVOYER` dont le domaine de l ADRESSE differe du domaine du SITE —
boite gratuite comprise — doit porter dans sa note la trace que la societe publie
elle-meme cette adresse. C est l EXCEPTION du paragraphe 5, et elle doit etre NOTEE
DANS LA FICHE, ce que le paragraphe 5 impose depuis le 08/10.

CE QU IL NE PEUT PAS CONTROLER, et il faut le dire plutot que de laisser croire :
il verifie que l exception est CONSIGNEE, pas qu elle est VRAIE. Une note qui dit
« publiee sur leur propre page » et qui se trompe passe le controle. Le script attrape
l oubli, pas le mensonge — comme `verif-texte.py` attrape le mot interdit et non
l argument faux.

MESURE A SA CREATION, le 20/10 : sur 104 fiches en file, 10 ont un domaine d adresse
different de celui du site, ET LES DIX PORTENT L EXCEPTION. Cristaleria Amigo etait la
onzieme et elle est sortie de la file le jour meme. Le controle rend donc ZERO, et c est
le bon resultat — un garde-fou qui rend zero n est rassurant que si l on a verifie qu il
regarde, lecon du 19/10 sur verif-argument-float.py.
"""
import io
import re
import sys

CSV = 'campagne-conteneur-20-open-top/prospection/liste-prospects.csv'

# Boites gratuites et messageries de fournisseur d acces : leur domaine n est JAMAIS
# celui du site, donc elles relevent toujours de l exception. Liste a completer EN
# LISANT ce qui sort, jamais en le supposant — meme consigne que MUTUALISES dans
# detecte-doublons.py et MOTS_GENERIQUES dans grep-nom.py.
MUTUALISES = (
    'gmail.', 'hotmail.', 'yahoo.', 'outlook.', 'live.', 'msn.', 'aol.', 'icloud.',
    'mail.ru', 'yandex.', 'qq.com', '163.com', 'terra.', 'uol.com', 'bol.com.br',
    'orange.fr', 'wanadoo', 'free.fr', 'protonmail', 'gmx.', 'web.de', 't-online',
    'comcast.net', 'bellsouth.net', 'sbcglobal.net', 'verizon.net', 'btinternet',
)

# Formules par lesquelles une note atteste que la SOCIETE publie l adresse elle-meme.
# ⚠️ Vocabulaire plus riche que la formule canonique, parce que la lecon des TROIS
# pannes de verif-texte.py est que le controleur ne doit jamais avoir un vocabulaire
# plus pauvre que les notes : un garde-fou qui crie au loup finit ignore.
EXCEPTION = re.compile(
    r'exception du (paragraphe|§) ?5'
    r'|exception du paragraphe cinq'
    r'|publie[e]? (elle-meme|par la societe)'
    r'|sur (sa|leur) (propre )?page de contact'
    r'|publiee sur leur propre'
    r'|leur propre (site|domaine|page)[^.]{0,40}publie'
    r'|la societe (la )?publie'
    r'|publiee par la societe elle-meme',
    re.I)


def charger(chemin):
    brut = io.open(chemin, encoding='utf-8').read().rstrip('\n').split('\n')
    return [l.rstrip('\r').split(';') for l in brut[1:] if len(l.rstrip('\r').split(';')) == 10]


def domaine(adresse):
    return adresse.split('@')[-1].strip().lower() if '@' in adresse else ''


def main():
    chemin = sys.argv[1] if len(sys.argv) > 1 else CSV
    R = charger(chemin)
    file = [c for c in R if c[9].startswith('A ENVOYER')]
    a_verifier, attestees = [], 0
    for c in file:
        mail = c[6].strip().lower()
        if '@' not in mail:
            continue
        dom = domaine(mail)
        site = re.sub(r'^www\.', '', c[5].strip().lower()).split('/')[0]
        mutualise = any(g in dom for g in MUTUALISES)
        if not mutualise and site and (dom in site or site in dom):
            continue                      # meme domaine : rien a attester
        motif = 'boite mutualisee' if mutualise else ('site absent du champ' if not site else 'domaine different du site')
        if EXCEPTION.search(c[8]):
            attestees += 1
        else:
            a_verifier.append((c[0], c[3], mail, c[5], c[9], motif))

    print('=== REGLE ANTI-REBOND DU §5 SUR LA FILE D ENVOI ===')
    print('%d fiche(s) en file. %d adresse(s) hors domaine du site, dont %d attestee(s) dans la note.'
          % (len(file), attestees + len(a_verifier), attestees))
    if not a_verifier:
        print('\n0 fiche(s) a corriger.')
        print("Aucune. Toute adresse hors domaine porte l exception du §5 dans sa fiche.")
        return
    print('\n⚠ %d FICHE(S) A CORRIGER — adresse hors domaine SANS exception consignee :' % len(a_verifier))
    for p, s, m, w, st, mo in a_verifier:
        print('  %-26s %-34s %-34s' % (p[:26], s[:34], m[:34]))
        print('      site %-28s %-22s motif : %s' % (w[:28], st, mo))
    print('\nCONDUITE : soit la societe publie bien cette adresse et la note doit le DIRE,')
    print('soit elle ne la publie pas et la fiche sort de la file — cas Cristaleria Amigo.')


if __name__ == '__main__':
    main()
