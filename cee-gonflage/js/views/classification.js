/**
 * views/classification.js — Module 2 : classification d'un site + eligibilite.
 */

import { CONDITIONS_ELIGIBILITE, TYPES_STATION, DEFAUTS_SIMULATEUR, AVERTISSEMENT } from '../config.js';
import { QUESTIONS, classifier, estimationPourType, evaluerEligibilite } from '../classify.js';
import { chargerParametres, ajouterSite } from '../storage.js';
import { el, $, vider, euros, nombreFr, notifier } from '../ui.js';

export function monter(racine) {
  const params = chargerParametres(DEFAUTS_SIMULATEUR);
  const reponses = {};
  const coches = {};

  racine.appendChild(el('div', { class: 'entete-vue' }, [
    el('h1', { text: 'Classification d’un site' }),
    el('p', { class: 'sous-titre', text: 'Trois questions pour déterminer le type A, B ou C au sens de la fiche TRA-SE-104, puis la checklist d’éligibilité.' }),
    el('p', { class: 'avertissement', text: AVERTISSEMENT }),
  ]));

  // --- Questionnaire --------------------------------------------------------
  const questionnaire = el('div', { class: 'carte' }, [el('h2', { text: 'Questionnaire' })]);
  for (const q of QUESTIONS) {
    const groupe = el('fieldset', { class: 'question' }, [
      el('legend', { text: q.question }),
      el('p', { class: 'champ__aide', text: q.aide }),
    ]);
    for (const [valeur, libelle] of [[true, 'Oui'], [false, 'Non']]) {
      const id = `q-${q.id}-${valeur}`;
      groupe.appendChild(el('label', { class: 'radio', for: id }, [
        el('input', {
          type: 'radio',
          name: q.id,
          id,
          value: String(valeur),
          onChange: () => { reponses[q.id] = valeur; rendre(); },
        }),
        el('span', { text: libelle }),
      ]));
    }
    questionnaire.appendChild(groupe);
  }

  // Parametres de l'estimation (reprennent ceux du simulateur, modifiables).
  questionnaire.appendChild(el('div', { class: 'grille-3' }, [
    champNombre('cls-nb', 'Nombre de stations envisagées', 1, 1, 0),
    champNombre('cls-prix', 'Prix CEE brut (€/MWhc)', params.prixBrutEurMWhc, 0.1, 0),
    champNombre('cls-marge', 'Marge délégataire (%)', params.margeDelegatairePct, 1, 0),
  ]));
  questionnaire.addEventListener('input', rendre);

  const resultat = el('div', { class: 'carte carte--resultat', id: 'resultat-classification' });

  // --- Checklist d'eligibilite ---------------------------------------------
  const checklist = el('div', { class: 'carte' }, [
    el('h2', { text: 'Checklist d’éligibilité' }),
    el('p', { class: 'note', text: 'Les conditions marquées « bloquant » sont exigées par la fiche : sans elles, l’opération n’est pas valorisable.' }),
  ]);
  for (const condition of CONDITIONS_ELIGIBILITE) {
    const id = `elig-${condition.id}`;
    checklist.appendChild(el('label', { class: 'case', for: id }, [
      el('input', {
        type: 'checkbox',
        id,
        onChange: (e) => { coches[condition.id] = e.target.checked; rendreEligibilite(); },
      }),
      el('span', {}, [
        el('strong', { text: condition.label }),
        condition.bloquant ? el('span', { class: 'etiquette etiquette--bloquant', text: 'bloquant' }) : null,
        el('span', { class: 'case__aide', text: condition.aide }),
      ]),
    ]));
  }
  const verdict = el('div', { class: 'verdict', id: 'verdict-eligibilite' });
  checklist.appendChild(verdict);

  racine.appendChild(el('div', { class: 'grille-2' }, [
    el('div', {}, [questionnaire, checklist]),
    resultat,
  ]));

  rendre();
  rendreEligibilite();

  /** Affiche le type retenu et l'estimation financiere. */
  function rendre() {
    const { type, motif, alerte } = classifier(reponses);
    const nb = Number($('#cls-nb').value) || 0;
    const prix = Number($('#cls-prix').value) || 0;
    const marge = Number($('#cls-marge').value) || 0;

    vider(resultat);
    resultat.appendChild(el('h2', { text: 'Résultat' }));

    if (!type) {
      resultat.appendChild(el('p', { class: 'vide', text: motif }));
      return;
    }

    const t = TYPES_STATION[type];
    const e = estimationPourType(type, nb, prix, marge);

    resultat.appendChild(el('div', { class: `badge-type badge-type--${type}`, text: `Type ${type}` }));
    resultat.appendChild(el('p', { class: 'resultat__titre', text: t.titre }));
    resultat.appendChild(el('p', { class: 'note', text: t.implantation }));
    resultat.appendChild(el('p', { text: motif }));
    if (alerte) resultat.appendChild(el('p', { class: 'alerte alerte--vigilance', text: alerte }));

    resultat.appendChild(el('table', { class: 'tableau tableau--compact' }, el('tbody', {}, [
      ligne('Volume par station', `${nombreFr(e.kwhCumacParStation)} kWh cumac`),
      ligne('Volume total', `${nombreFr(e.kwhCumacTotal)} kWh cumac`),
      ligne('Prix net retenu', `${e.prixNetEurMWhc.toFixed(2).replace('.', ',')} €/MWhc`),
      ligne('Montant net par station et par an', euros(e.montantNetParStation, true)),
      ligne('Montant net total par an', euros(e.montantNetTotal, true), 'fort'),
    ])));

    resultat.appendChild(el('button', {
      type: 'button',
      class: 'btn btn--primaire',
      text: 'Créer une fiche site dans le CRM',
      onClick: () => {
        const site = ajouterSite({ typeCee: type, nbStations: nb, eligibilite: { ...coches } });
        notifier('Fiche créée dans le CRM : complétez le nom et l’adresse.', 'succes');
        window.location.hash = `#/crm?site=${site.id}`;
      },
    }));
  }

  /** Affiche le verdict d'eligibilite. */
  function rendreEligibilite() {
    const r = evaluerEligibilite(coches);
    vider(verdict);
    verdict.className = `verdict ${r.eligible ? 'verdict--ok' : 'verdict--ko'}`;
    verdict.appendChild(el('strong', {
      text: r.eligible
        ? 'Conditions bloquantes réunies.'
        : `${r.bloquantsManquants.length} condition(s) bloquante(s) manquante(s).`,
    }));
    if (!r.eligible) {
      verdict.appendChild(el('ul', {}, r.bloquantsManquants.map((c) => el('li', { text: c.label }))));
    } else if (r.aCompleter.length) {
      verdict.appendChild(el('p', { text: 'Pièces à préparer pour le dossier :' }));
      verdict.appendChild(el('ul', {}, r.aCompleter.map((c) => el('li', { text: c.label }))));
    }
  }
}

function champNombre(id, label, valeur, pas, min) {
  return el('div', { class: 'champ' }, [
    el('label', { for: id, text: label }),
    el('input', { id, type: 'number', value: valeur, step: pas, min }),
  ]);
}

function ligne(libelle, valeur, variante = '') {
  return el('tr', { class: variante }, [
    el('th', { scope: 'row', text: libelle }),
    el('td', { class: 'num', text: valeur }),
  ]);
}
