/**
 * views/recharge.js — seconde offre : bornes de recharge (programme ADVENIR).
 *
 * Cette vue est volontairement prudente : elle rappelle en permanence que la
 * prise en charge est partielle et que les barèmes doivent être revalidés.
 */

import { PROGRAMME_RECHARGE, DEFAUTS_RECHARGE } from '../config.js';
import { estimerPrimeRecharge } from '../recharge.js';
import { chargerParametres, sauverParametres } from '../storage.js';
import { el, $, vider, euros, nombreFr } from '../ui.js';

const CHAMPS = [
  { cle: 'nbPoints', label: 'Nombre de points de charge', pas: 1, min: 0, aide: 'Un point de charge = une prise utilisable par un véhicule.' },
  { cle: 'coutHtParPoint', label: 'Coût HT par point de charge (€)', pas: 100, min: 0, aide: 'Matériel + installation + raccordement, chiffré par l’installateur IRVE.' },
  { cle: 'tauxPriseEnChargePct', label: 'Taux de prise en charge (%)', pas: 1, min: 0, max: 100, aide: 'Dépend de la cible et du barème en vigueur. À revalider sur advenir.mobi.' },
  { cle: 'plafondParPoint', label: 'Plafond de prime par point (€)', pas: 50, min: 0, aide: 'La prime réelle est le minimum entre le pourcentage et ce plafond.' },
  { cle: 'prixFactureClientParPoint', label: 'Prix facturé au client par point (€)', pas: 50, min: 0, aide: 'Votre rémunération éventuelle sur le dossier. Optionnel.' },
];

export function monter(racine) {
  const params = chargerParametres({ ...DEFAUTS_RECHARGE });

  racine.appendChild(el('div', { class: 'entete-vue' }, [
    el('h1', { text: 'Bornes de recharge — programme ADVENIR' }),
    el('p', { class: 'sous-titre', text: `${PROGRAMME_RECHARGE.nom}, piloté par l’${PROGRAMME_RECHARGE.pilote} et financé par les ${PROGRAMME_RECHARGE.financement}. ${PROGRAMME_RECHARGE.echeance}` }),
    el('p', { class: 'avertissement', text: 'Mécanisme différent du gonflage : il ne s’agit pas d’une fiche standardisée en kWh cumac, mais d’une prime à l’investissement, partielle et plafonnée. Ne jamais annoncer une borne « gratuite ». Les barèmes ci-dessous sont des valeurs par défaut à revalider avant toute proposition chiffrée.' }),
  ]));

  // --- Rappel des règles du programme --------------------------------------
  const regles = el('div', { class: 'carte carte--alerte' }, [
    el('h2', { text: 'À savoir avant de prospecter' }),
    el('ul', {}, PROGRAMME_RECHARGE.regles.map((r) => el('li', { text: r }))),
    el('p', { class: 'note' }, [
      el('span', { text: 'Sources à vérifier avant chaque campagne : ' }),
      ...PROGRAMME_RECHARGE.sources.map((url) => el('a', { href: url, target: '_blank', rel: 'noopener', text: url, style: 'margin-right:10px' })),
    ]),
  ]);

  // --- Formulaire ------------------------------------------------------------
  const formulaire = el('form', { class: 'carte formulaire' }, [el('h2', { text: 'Estimation de la prime' })]);
  for (const def of CHAMPS) {
    const attrs = { step: def.pas, min: def.min };
    if (def.max !== undefined) attrs.max = def.max;
    formulaire.appendChild(el('div', { class: 'champ' }, [
      el('label', { for: `rec-${def.cle}`, text: def.label }),
      el('input', { id: `rec-${def.cle}`, type: 'number', value: params[def.cle] ?? DEFAUTS_RECHARGE[def.cle], ...attrs }),
      el('p', { class: 'champ__aide', text: def.aide }),
    ]));
  }
  formulaire.appendChild(el('div', { class: 'actions' }, el('button', {
    type: 'button', class: 'btn btn--secondaire', text: 'Réinitialiser',
    onClick: () => { for (const d of CHAMPS) $(`#rec-${d.cle}`).value = DEFAUTS_RECHARGE[d.cle]; recalculer(); },
  })));

  const resultats = el('section', { id: 'resultats-recharge' });
  racine.appendChild(regles);
  racine.appendChild(el('div', { class: 'grille-2' }, [formulaire, resultats]));

  formulaire.addEventListener('input', recalculer);
  recalculer();

  function recalculer() {
    const valeurs = {};
    for (const def of CHAMPS) valeurs[def.cle] = $(`#rec-${def.cle}`).value;
    sauverParametres({ ...chargerParametres({}), ...valeurs });
    const r = estimerPrimeRecharge(valeurs);

    vider(resultats);
    resultats.appendChild(el('div', { class: 'kpis' }, [
      kpi('Prime par point', euros(r.primeParPoint, true), r.plafondAtteint ? 'Plafond atteint' : 'Pourcentage du coût HT'),
      kpi('Prime totale', euros(r.primeTotale, true), `${nombreFr(r.nbPoints)} point(s) de charge`),
      kpi('Reste à charge du site', euros(r.resteACharge, true), `soit ${euros(r.resteAChargeParPoint, true)} par point`),
      kpi('Taux réel de prise en charge', `${r.tauxReelPct.toFixed(1).replace('.', ',')} %`, 'Prime rapportée au coût total HT'),
    ]));

    if (r.plafondAtteint) {
      resultats.appendChild(el('p', {
        class: 'alerte alerte--vigilance',
        text: 'Le plafond par point de charge écrête la prime : le taux réel est inférieur au taux affiché. C’est ce taux réel qu’il faut présenter au client.',
      }));
    }

    resultats.appendChild(el('div', { class: 'carte' }, [
      el('h2', { text: 'Détail' }),
      el('table', { class: 'tableau tableau--compact' }, el('tbody', {}, [
        ligne('Coût total HT du projet', euros(r.coutTotal, true)),
        ligne('Prime ADVENIR estimée', euros(r.primeTotale, true)),
        ligne('Reste à charge du site', euros(r.resteACharge, true), 'fort'),
        ligne('Votre rémunération sur le dossier', euros(r.recettesContrats, true)),
      ])),
      el('p', { class: 'note', text: 'Estimation indicative. Le dossier ADVENIR doit être déposé et validé avant le début des travaux : une installation commencée trop tôt perd la prime.' }),
    ]));
  }
}

function kpi(titre, valeur, detail) {
  return el('div', { class: 'kpi' }, [
    el('span', { class: 'kpi__titre', text: titre }),
    el('strong', { class: 'kpi__valeur', text: valeur }),
    el('span', { class: 'kpi__detail', text: detail }),
  ]);
}

function ligne(libelle, valeur, variante = '') {
  return el('tr', { class: variante }, [el('th', { scope: 'row', text: libelle }), el('td', { class: 'num', text: valeur })]);
}
