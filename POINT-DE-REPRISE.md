# Point de reprise — 07/10/2026, 17 h 50 Paris

## Blocage en cours : écriture GitHub impossible

Trois voies d'écriture testées, les trois fermées :

| Voie | Résultat |
|---|---|
| `git push` (10 tentatives, dont `--no-thin` et commit par commit) | `remote rejected ... (Internal Server Error)` |
| API Git Data via `gh api` (blobs) | `HTTP 403 — Write access to this GitHub API path is not permitted through this proxy` |
| Lecture : `gh api repos/...`, `git fetch` | **fonctionne normalement** |

Diagnostic : l'accès GitHub de la session est devenu **lecture seule en cours de journée**.
Les push ont fonctionné jusqu'à **14:58:50Z** (commit `c12ed8e`, le plan d'appels) puis se
sont arrêtés. Ce n'est donc pas une panne GitHub mais une permission d'écriture qui a sauté.

## Ce qui attend en local

**4 commits** sur `claude/campagne-conteneur-20-open-fl0382`, portant sur 4 fichiers :

| Fichier | Ce qui change |
|---|---|
| `CLAUDE.md` | journée de travail portée à 19 h (§15), contrôle MX obligatoire (§5), règle « aucune signature » (§10) |
| `campagne-conteneur-20-open-top/prospection/liste-prospects.csv` | 778 fiches, annotations des lots 11 et 12 |
| `campagne-conteneur-20-open-top/prospection/SUIVI-CAMPAGNE.md` | bilan du jour, mesure du blocage réseau |
| `POINT-DE-REPRISE.md` | ce fichier |

## Ce qui n'est PAS en risque

Les **145 messages de la journée sont partis** — 55 envois et 90 relances. C'est
irréversible et consultable dans les messages envoyés de `aaron.harfi@noxem-group.com`.
Seules les annotations du registre attendent, et elles se reconstruisent depuis les envois.

## Comment reprendre

1. `git push -u origin claude/campagne-conteneur-20-open-fl0382` — réessayer d'abord.
2. Si le 403 persiste : l'accès GitHub de la session doit être rétabli en écriture. C'est un
   réglage du côté d'Aaron (reconnexion GitHub dans les connecteurs claude.ai, ou
   réinstallation de l'app GitHub sur le dépôt).
3. Une fois poussé, vérifier l'intégrité du registre :
   `awk -F';' 'NR>1{gsub(/\r/,""); if(NF!=10) print "MALFORME "NR": "NF}' liste-prospects.csv`
   — 3 lignes à 11 champs sont légitimes.

## Second blocage, distinct et plus important commercialement

**Toute lecture web directe est coupée** par la politique réseau de la session. Testé sur
dix domaines : annuaires d'associations verrières (Brésil, Pérou, Mexique), listes
d'exposants des salons Big 5 Construct, portail Vidrioperfil, `noxemgroup.com` lui-même,
et jusqu'à `google.com`. Tous bloqués.

Conséquence : ma seule source est le résumé affiché par le moteur de recherche. Je ne peux
ouvrir aucune page contact, donc la règle anti-rebond écarte des adresses que je pourrais
sinon vérifier, et le gisement de prospects se tarit bien plus vite qu'il ne le devrait.

**C'est le levier le plus rentable de la campagne, et il se règle dans les paramètres réseau
de l'environnement.**
