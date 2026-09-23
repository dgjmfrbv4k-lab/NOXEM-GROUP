/**
 * views/simulateur.js — Module 1 : simulateur de rentabilite.
 *
 * Tous les parametres sont modifiables et sauvegardes localement.
 * Aucun prix n'est fige dans le code en dehors des valeurs par defaut.
 */

import { DEFAUTS_SIMULATEUR, TYPES_STATION, ORDRE_TYPES, AVERTISSEMENT, FICHE } from '../config.js';
import { simuler } from '../calc.js';
import { chargerParametres, sauverParametres } from '../storage.js';
import { el, $, vider, euros, nombreFr, kwhCumac, notifier } from '../ui.js';

/** Definition des champs du formulaire (ordre d'affichage). */
const CHAMPS = [
  { groupe: 'Parc de stations', cle: 'nbA', label: 'Nombre de stations type A', pas: 1, min: 0, aide: 'Autoroutes et voies assimilées (534 200 kWh cumac / station).' },
  { groupe: 'Parc de stations', cle: 'nbB', label: 'Nombre de stations type B', pas: 1, min: 0, aide: 'Parkings ouverts au public, zones d’activité (148 400 kWh cumac / station).' },
  { groupe: 'Parc de stations', cle: 'nbC', label: 'Nombre de stations type C', pas: 1, min: 0, aide: 'Parkings privés d’entreprises ou de collectivités (39 600 kWh cumac / station).' },
  { groupe: 'Marché CEE', cle: 'prixBrutEurMWhc', label: 'Prix CEE brut (€ / MWh cumac)', pas: 0.1, min: 0, aide: 'Cours du marché (registre EMMY). À mettre à jour à chaque simulation.' },
  { groupe: 'Marché CEE', cle: 'margeDelegatairePct', label: 'Marge du délégataire (%)', pas: 1, min: 0, max: 100, aide: 'Part prélevée par le délégataire entre le prix brut et le net versé.' },
  { groupe: 'Marché CEE', cle: 'partCeeConserveePct', label: 'Part de la prime revenant à votre structure (%)', pas: 1, min: 0, max: 100, aide: '100 % = vous percevez toute la prime nette. En dessous, le reste est reversé à l’exploitant du site.' },
  { groupe: 'Coûts et recettes', cle: 'coutEntretienAnnuelParStation', label: 'Coût d’entretien annuel par station (€)', pas: 10, min: 0, aide: 'Maintenance, pièces, déplacements. À chiffrer avec le fabricant / mainteneur.' },
  { groupe: 'Coûts et recettes', cle: 'coutInstallationParStation', label: 'Coût d’installation par station (€)', pas: 10, min: 0, aide: 'Investissement initial, compté en année 1. Optionnel.' },
  { groupe: 'Coûts et recettes', cle: 'prixFactureClientParStation', label: 'Prix facturé au client par station et par an (€)', pas: 10, min: 0, aide: 'Recette complémentaire éventuelle du contrat d’entretien. Optionnel.' },
  { groupe: 'Coûts et recettes', cle: 'fraisFixesAnnuels', label: 'Frais fixes annuels de structure (€)', pas: 100, min: 0, aide: 'Charges indépendantes du nombre de sites. Sert au calcul du point mort.' },
  { groupe: 'Coûts et recettes', cle: 'variationAnnuellePrixPct', label: 'Variation annuelle du prix CEE (%)', pas: 1, aide: 'Hypothèse d’évolution du cours pour la projection à 3 ans (peut être négative).' },
];

export function monter(racine) {
  const params = chargerParametres(DEFAUTS_SIMULATEUR);

  const formulaire = el('form', { class: 'carte formulaire', id: 'form-simulateur' });
  formulaire.appendChild(el('h2', { text: 'Paramètres' }));

  // Regroupement des champs par section.
  let groupeCourant = null;
  for (const def of CHAMPS) {
    if (def.groupe !== groupeCourant) {
      groupeCourant = def.groupe;
      formulaire.appendChild(el('h3', { class: 'formulaire__groupe', text: groupeCourant }));
    }
    const attrs = { step: def.pas, min: def.min };
    if (def.max !== undefined) attrs.max = def.max;
    if (def.min === undefined) delete attrs.min;
    const conteneur = el('div', { class: 'champ' }, [
      el('label', { for: `sim-${def.cle}`, text: def.label }),
      el('input', { id: `sim-${def.cle}`, name: def.cle, type: 'number', value: params[def.cle], ...attrs }),
      el('p', { class: 'champ__aide', text: def.aide }),
    ]);
    formulaire.appendChild(conteneur);
  }

  const actions = el('div', { class: 'actions' }, [
    el('button', { type: 'button', class: 'btn btn--secondaire', text: 'Réinitialiser', onClick: reinitialiser }),
  ]);
  formulaire.appendChild(actions);

  const resultats = el('section', { class: 'resultats', id: 'resultats-simulateur' });

  racine.appendChild(el('div', { class: 'entete-vue' }, [
    el('h1', { text: 'Simulateur de rentabilité' }),
    el('p', { class: 'sous-titre', text: `Fiche ${FICHE.code} (version ${FICHE.version}) — ${FICHE.libelle}. ${FICHE.periode}.` }),
    el('p', { class: 'avertissement', text: AVERTISSEMENT }),
  ]));
  racine.appendChild(el('div', { class: 'grille-2' }, [formulaire, resultats]));

  formulaire.addEventListener('input', recalculer);
  recalculer();

  function lireFormulaire() {
    const valeurs = {};
    for (const def of CHAMPS) valeurs[def.cle] = $(`#sim-${def.cle}`).value;
    return valeurs;
  }

  function recalculer() {
    const valeurs = lireFormulaire();
    sauverParametres(valeurs);
    afficherResultats(resultats, simuler(valeurs));
  }

  function reinitialiser() {
    for (const def of CHAMPS) $(`#sim-${def.cle}`).value = DEFAUTS_SIMULATEUR[def.cle];
    recalculer();
    notifier('Paramètres réinitialisés.', 'info');
  }
}

/** Construit l'affichage des resultats. */
function afficherResultats(racine, r) {
  vider(racine);

  if (r.stations.total === 0) {
    racine.appendChild(el('div', { class: 'carte', html: '<p class="vide">Renseignez au moins une station pour lancer la simulation.</p>' }));
    return;
  }

  // --- Indicateurs cles ---------------------------------------------------
  const kpis = el('div', { class: 'kpis' }, [
    kpi('Volume total', kwhCumac(r.volume.total), `${r.stations.total} station(s)`),
    kpi('Montant CEE brut', euros(r.cee.brut, true), `${r.prix.brut.toLocaleString('fr-FR')} €/MWhc`),
    kpi('Montant CEE net', euros(r.cee.net, true), `${r.prix.net.toFixed(2).replace('.', ',')} €/MWhc après ${r.prix.margeDelegatairePct} % de marge`),
    kpi('Résultat annuel récurrent', euros(r.margeRecurrenteAnnuelle, true), 'Recettes − charges, hors installation', r.margeRecurrenteAnnuelle >= 0 ? 'positif' : 'negatif'),
  ]);
  racine.appendChild(kpis);

  if (r.coutsNonRenseignes) {
    racine.appendChild(el('p', {
      class: 'alerte alerte--vigilance',
      text: 'Coûts d’entretien et d’installation non renseignés : le résultat affiché est un plafond théorique, pas une marge réelle.',
    }));
  }

  // --- Detail par type ----------------------------------------------------
  const lignes = ORDRE_TYPES
    .filter((t) => r.stations[t] > 0)
    .map((t) => el('tr', {}, [
      el('td', { text: `Type ${t}` }),
      el('td', { class: 'num', text: nombreFr(r.stations[t]) }),
      el('td', { class: 'num', text: nombreFr(TYPES_STATION[t].kwhCumac) }),
      el('td', { class: 'num', text: nombreFr(r.volume[t]) }),
      el('td', { class: 'num', text: euros(r.margeParStation[t], true) }),
      el('td', { class: 'num', text: r.pointMort[t] === null ? 'jamais' : `${nombreFr(r.pointMort[t])} station(s)` }),
    ]));

  racine.appendChild(el('div', { class: 'carte' }, [
    el('h2', { text: 'Détail par type de station' }),
    el('table', { class: 'tableau' }, [
      el('thead', {}, el('tr', {}, [
        el('th', { text: 'Type' }),
        el('th', { class: 'num', text: 'Nb' }),
        el('th', { class: 'num', text: 'kWh cumac / station' }),
        el('th', { class: 'num', text: 'kWh cumac total' }),
        el('th', { class: 'num', text: 'Marge annuelle / station' }),
        el('th', { class: 'num', text: 'Point mort' }),
      ])),
      el('tbody', {}, lignes),
    ]),
    el('p', { class: 'note', text: 'Marge par station = prime CEE nette conservée + prix facturé au client − coût d’entretien (hors frais fixes et hors installation).' }),
    el('p', { class: 'note', text: 'Point mort = nombre de stations de ce type nécessaires pour couvrir les frais fixes annuels de structure. « jamais » = la marge unitaire est négative.' }),
  ]));

  // --- Synthese economique ------------------------------------------------
  const synthese = el('div', { class: 'carte' }, [
    el('h2', { text: 'Synthèse économique annuelle' }),
    el('table', { class: 'tableau tableau--compact' }, el('tbody', {}, [
      ligne('Recettes CEE nettes conservées', euros(r.recettes.cee, true)),
      ligne('Recettes contrats facturés aux sites', euros(r.recettes.contrats, true)),
      ligne('Total des recettes', euros(r.recettes.total, true), 'fort'),
      ligne('Charges d’entretien', euros(-r.charges.entretien, true)),
      ligne('Frais fixes de structure', euros(-r.charges.fraisFixes, true)),
      ligne('Résultat annuel récurrent', euros(r.margeRecurrenteAnnuelle, true), 'fort'),
      ligne('Investissement d’installation (année 1)', euros(-r.investissementInitial, true)),
      ligne('Résultat année 1', euros(r.resultatAnnee1, true), 'fort'),
      ligne('Marge moyenne par station', euros(r.margeParStation.moyenne, true)),
      ligne('Point mort (mix actuel)', r.pointMort.moyenne === null ? 'jamais atteint' : `${nombreFr(r.pointMort.moyenne)} station(s)`),
      ligne(
        'Retour sur investissement d’installation',
        r.retourInvestissementMois === null ? 'jamais atteint'
          : r.retourInvestissementMois === 0 ? 'immédiat (aucun investissement)'
            : `${r.retourInvestissementMois.toFixed(1).replace('.', ',')} mois`,
      ),
    ])),
  ]);
  racine.appendChild(synthese);

  // --- Projection 3 ans ---------------------------------------------------
  const lignesProjection = r.projection.map((a) => el('tr', {}, [
    el('td', { text: `Année ${a.annee}` }),
    el('td', { class: 'num', text: `${a.prixNetEurMWhc.toFixed(2).replace('.', ',')} €` }),
    el('td', { class: 'num', text: euros(a.recettesCee, true) }),
    el('td', { class: 'num', text: euros(a.recettesContrats, true) }),
    el('td', { class: 'num', text: euros(-a.charges, true) }),
    el('td', { class: 'num', text: euros(-a.investissement, true) }),
    el('td', { class: `num ${a.resultat >= 0 ? 'positif' : 'negatif'}`, text: euros(a.resultat, true) }),
    el('td', { class: `num ${a.cumule >= 0 ? 'positif' : 'negatif'}`, text: euros(a.cumule, true) }),
  ]));

  racine.appendChild(el('div', { class: 'carte' }, [
    el('h2', { text: 'Projection sur 3 ans' }),
    el('table', { class: 'tableau' }, [
      el('thead', {}, el('tr', {}, [
        el('th', { text: '' }),
        el('th', { class: 'num', text: 'Prix net' }),
        el('th', { class: 'num', text: 'CEE' }),
        el('th', { class: 'num', text: 'Contrats' }),
        el('th', { class: 'num', text: 'Charges' }),
        el('th', { class: 'num', text: 'Installation' }),
        el('th', { class: 'num', text: 'Résultat' }),
        el('th', { class: 'num', text: 'Cumulé' }),
      ])),
      el('tbody', {}, lignesProjection),
    ]),
    el('p', {
      class: 'note',
      text: 'La durée de vie conventionnelle de l’opération est d’un an : les années 2 et 3 supposent un contrat actif et expressement renouvelé (la reconduction tacite n’ouvre pas droit à une nouvelle valorisation).',
    }),
  ]));
}

function kpi(titre, valeur, detail, variante = '') {
  return el('div', { class: 'kpi' }, [
    el('span', { class: 'kpi__titre', text: titre }),
    el('strong', { class: `kpi__valeur ${variante}`, text: valeur }),
    el('span', { class: 'kpi__detail', text: detail }),
  ]);
}

function ligne(libelle, valeur, variante = '') {
  return el('tr', { class: variante }, [
    el('th', { scope: 'row', text: libelle }),
    el('td', { class: 'num', text: valeur }),
  ]);
}
