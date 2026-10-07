# Point de reprise — 07/10/2026

## 1. Blocage GitHub du 07/10 — RÉSOLU

Entre 15 h 05 et 17 h 50 (heure de Paris), toute écriture vers le dépôt a été refusée :

| Voie | Résultat pendant l'incident |
|---|---|
| `git push` (11 tentatives, dont `--no-thin` et commit par commit) | `remote rejected ... (Internal Server Error)` |
| API Git Data via `gh api` (création de blob) | `HTTP 403 — Write access to this GitHub API path is not permitted through this proxy` |
| Serveur MCP GitHub (`create_or_update_file`) | **fonctionnait** — seule voie d'écriture ouverte |
| Lecture (`git fetch`, `gh api` en GET) | fonctionnait |

**Comment c'est sorti :** un commit écrit par le serveur MCP a fait avancer la tête
distante ; après `git fetch` et rebase des commits locaux dessus, le `git push` est repassé
du premier coup.

**Si cela se reproduit :** écrire un fichier par le serveur MCP GitHub pour faire avancer la
référence distante, puis `git fetch` + `git rebase origin/<branche>` + `git push`. Ne pas
s'acharner sur `git push` seul, onze tentatives n'ont rien donné.

## 2. Blocage toujours actif, et c'est le plus coûteux commercialement

**Toute lecture web directe est coupée** par la politique réseau de la session. Testé le
07/10 sur dix domaines représentatifs — tous bloqués :

- annuaires des associations verrières : `abravidro.org.br` (Brésil), `apevic.org` (Pérou),
  `amevec.mx` (Mexique)
- listes d'exposants : `exhibitors.big5constructkenya.com`, `glasstec-online.com`
- portail du secteur : `vidrioperfil.com`
- sites d'entreprises : `wsglass.com`
- **notre propre site `noxemgroup.com`**
- et jusqu'à `google.com` et `duckduckgo.com`

**Conséquence directe :** la seule source est le résumé qu'affiche le moteur de recherche.
Impossible d'ouvrir une page contact, donc la règle anti-rebond du §5 écarte des adresses
qui seraient vérifiables autrement, et le gisement de prospects se tarit bien plus vite
qu'il ne le devrait. Mesure du 07/10 : sur les trois derniers tours de recherche, chaque
profil fort trouvé était **déjà au registre**.

**C'est le levier le plus rentable de la campagne. Il se règle dans les paramètres réseau de
l'environnement, et il ne dépend pas de moi.**

## 3. Où en est la campagne au soir du 07/10

- Registre : **778 fiches**, liste d'appels : **219**.
- Journée : **55 envois confirmés, 90 relances, 9 rebonds, 1 réponse** (Duravidrio).
- Reste à relancer : ~40 fiches de septembre, profils faibles.
- Plan d'appels prêt : `PLAN-APPELS-2026-10-08.md`, 25 cibles classées par valeur.

**Trois actions prioritaires, dans l'ordre :**
1. WhatsApp à Duravidrio, **+593 99 972 8592** — seule réponse obtenue, et ils font de
   l'acoustique, du blindé et du pare-balles, donc du float clair épais : notre gamme.
2. United Glass / John — grille de prix, conditions de paiement, faisabilité du
   2 438 × 3 302 mm. Seule demande de devis ouverte.
3. DMARC sur `noxem-group.com`, toujours absent. Sans lui, impossible de savoir si les
   145 messages du jour sont arrivés.
