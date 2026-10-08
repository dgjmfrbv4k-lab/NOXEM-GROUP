#!/usr/bin/env python3
"""Controle MX obligatoire avant tout envoi.

Usage : python3 verif-mx.py adresse1@domaine [adresse2@domaine ...]
        python3 verif-mx.py --registre   (verifie tous les domaines du registre)

Mis en place le 07/10/2026 apres deux rebonds "domaine introuvable" sur des
adresses pourtant publiees sur le site de la societe (vitrolux-ci.com,
arturaya.com). La regle anti-rebond du CLAUDE.md verifie que le domaine
apparait dans les URL de resultats : elle ne detecte pas un domaine sans MX.
Ce controle comble ce trou. Aucun envoi sans un OK ici.
"""
import sys
import dns.resolver

def mx(domaine):
    try:
        r = dns.resolver.resolve(domaine, 'MX', lifetime=8)
        return sorted((x.preference, str(x.exchange).rstrip('.')) for x in r)
    except dns.resolver.NXDOMAIN:
        return 'NXDOMAIN'
    except dns.resolver.NoAnswer:
        # pas de MX : repli sur un A, certains petits domaines recoivent ainsi
        try:
            dns.resolver.resolve(domaine, 'A', lifetime=8)
            return 'PAS DE MX mais A present — risque eleve'
        except Exception:
            return 'PAS DE MX ni A'
    except Exception as e:
        return 'ERREUR %s' % type(e).__name__

TEMOINS = ('gmail.com', 'google.com', 'outlook.com')


def resolveur_vivant():
    """Un domaine temoin doit repondre, sinon le resolveur est HS.

    Sans ce garde-fou, une panne DNS fait rendre NXDOMAIN a TOUS les domaines,
    y compris les bons. Le 08/10/2026 le resolveur est tombe et l outil a
    annonce gmail.com introuvable. Utilise tel quel, il aurait fait supprimer
    du registre des adresses parfaitement valides. Un faux NXDOMAIN coute
    beaucoup plus cher qu un rebond.
    """
    for t in TEMOINS:
        try:
            dns.resolver.resolve(t, 'MX', lifetime=8)
            return True
        except Exception:
            continue
    return False


def main(args):
    if not resolveur_vivant():
        print('RESOLVEUR INDISPONIBLE : aucun domaine temoin ne repond '
              '(%s).' % ', '.join(TEMOINS))
        print('La resolution DNS est hors service dans cette session.')
        print("AUCUN RESULTAT N EST EXPLOITABLE. Ne retirer aucune adresse du")
        print('registre sur la foi de cette execution, et ne pas conclure')
        print("qu un domaine est mort. Reessayer plus tard.")
        return 2

    if args and args[0] == '--registre':
        import csv, os
        base = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
        chemin = os.path.join(base, 'liste-prospects.csv')
        vus = {}
        with open(chemin, encoding='utf-8') as f:
            for ligne in list(csv.reader(f, delimiter=';'))[1:]:
                if len(ligne) < 7 or '@' not in ligne[6]:
                    continue
                for adr in ligne[6].replace(',', ' ').split():
                    if '@' in adr:
                        vus.setdefault(adr.split('@')[-1].strip().lower(), []).append(ligne[3])
        args = sorted(vus)
        cibles = [(d, vus[d]) for d in args]
    else:
        cibles = [((a.split('@')[-1] if '@' in a else a).strip().lower(), []) for a in args]
    for domaine, societes in cibles:
        res = mx(domaine)
        ok = isinstance(res, list)
        marque = 'OK   ' if ok else 'REBOND'
        detail = res[0][1] if ok else res
        print('%s %-34s %s%s' % (marque, domaine, detail,
                                 '  <- ' + ' / '.join(societes[:2]) if societes and not ok else ''))
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
