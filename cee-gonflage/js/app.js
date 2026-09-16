/**
 * app.js — point d'entree de l'application.
 * Routage par ancre (#/vue?parametre=valeur), sans dependance ni build.
 */

import { monter as monterSimulateur } from './views/simulateur.js';
import { monter as monterClassification } from './views/classification.js';
import { monter as monterCrm } from './views/crm.js';
import { monter as monterEmails } from './views/emails-view.js';
import { monter as monterDossiers } from './views/dossiers.js';
import { chargerSites } from './storage.js';
import { echeances } from './dossier.js';
import { el, $, $$, vider } from './ui.js';

const VUES = {
  simulateur: { titre: 'Simulateur', monter: monterSimulateur },
  classification: { titre: 'Classification', monter: monterClassification },
  crm: { titre: 'Prospection', monter: monterCrm },
  emails: { titre: 'E-mails', monter: monterEmails },
  dossiers: { titre: 'Dossiers CEE', monter: monterDossiers },
};

const VUE_PAR_DEFAUT = 'simulateur';

/** Analyse l'ancre : "#/crm?site=abc" -> { vue:'crm', requete:{site:'abc'} }. */
function lireRoute() {
  const ancre = window.location.hash.replace(/^#\/?/, '');
  const [chemin, chaineRequete = ''] = ancre.split('?');
  const vue = VUES[chemin] ? chemin : VUE_PAR_DEFAUT;
  const requete = Object.fromEntries(new URLSearchParams(chaineRequete).entries());
  return { vue, requete };
}

function rendre() {
  const { vue, requete } = lireRoute();
  const racine = $('#vue');
  vider(racine);
  racine.scrollTop = 0;
  VUES[vue].monter(racine, requete);

  // Etat actif de la navigation.
  for (const lien of $$('.nav a')) {
    lien.classList.toggle('actif', lien.dataset.vue === vue);
  }
  document.title = `${VUES[vue].titre} — Stations de gonflage CEE`;
  window.scrollTo({ top: 0 });
}

/** Pastille du nombre de renouvellements a preparer, affichee dans la navigation. */
function majPastilleDossiers() {
  const nb = chargerSites()
    .filter((s) => s.statut === 'signe')
    .map((s) => echeances(s.dateSignature))
    .filter((e) => e.niveau === 'urgent' || e.niveau === 'vigilance')
    .length;
  const lien = $('.nav a[data-vue="dossiers"]');
  if (!lien) return;
  let pastille = lien.querySelector('.pastille');
  if (!nb) { pastille?.remove(); return; }
  if (!pastille) {
    pastille = el('span', { class: 'pastille' });
    lien.appendChild(pastille);
  }
  pastille.textContent = String(nb);
}

window.addEventListener('hashchange', () => { rendre(); majPastilleDossiers(); });
window.addEventListener('DOMContentLoaded', () => { rendre(); majPastilleDossiers(); });
