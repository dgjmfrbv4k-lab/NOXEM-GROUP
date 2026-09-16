/**
 * views/crm.js — Module 3 : mini-CRM de prospection.
 *
 * Donnees stockees dans le navigateur (localStorage), aucun backend.
 * RGPD : on ne collecte que le strict necessaire au suivi commercial B2B
 * (prénom + fonction + e-mail professionnel du contact).
 */

import { STATUTS, TYPES_SITE, ORDRE_TYPES, TYPES_STATION, DEFAUTS_SIMULATEUR } from '../config.js';
import {
  chargerSites, ajouterSite, majSite, supprimerSite, trouverSite,
  chargerParametres, exporterJSON, importerJSON,
} from '../storage.js';
import { estimationPourType } from '../classify.js';
import { sitesVersCSV, telecharger } from '../csv.js';
import { el, vider, euros, dateFr, aujourdhuiISO, notifier } from '../ui.js';

/** Etat local de la vue (filtres + site en cours d'edition). */
const etat = { statut: '', typeCee: '', recherche: '', editionId: null };

export function monter(racine, requete = {}) {
  etat.editionId = requete.site || null;

  racine.appendChild(el('div', { class: 'entete-vue' }, [
    el('h1', { text: 'Prospection' }),
    el('p', { class: 'sous-titre', text: 'Suivi des sites cibles. Données enregistrées uniquement dans ce navigateur : pensez à exporter une sauvegarde JSON régulièrement.' }),
  ]));

  const barre = el('div', { class: 'barre-outils' }, [
    el('button', { type: 'button', class: 'btn btn--primaire', text: '+ Nouveau site', onClick: creerSite }),
    selectFiltre('filtre-statut', 'Tous les statuts', STATUTS.map((s) => ({ value: s.id, label: s.label })), (v) => { etat.statut = v; rendreListe(); }),
    selectFiltre('filtre-type', 'Tous les types CEE', ORDRE_TYPES.map((t) => ({ value: t, label: `Type ${t}` })), (v) => { etat.typeCee = v; rendreListe(); }),
    el('input', {
      type: 'search', id: 'recherche', placeholder: 'Rechercher (nom, ville, société)…',
      onInput: (e) => { etat.recherche = e.target.value.toLowerCase(); rendreListe(); },
    }),
    el('button', { type: 'button', class: 'btn btn--secondaire', text: 'Export CSV', onClick: exporterCSV }),
    el('button', { type: 'button', class: 'btn btn--secondaire', text: 'Sauvegarde JSON', onClick: exporterSauvegarde }),
    el('label', { class: 'btn btn--secondaire', for: 'import-json', text: 'Importer JSON' }),
    el('input', { type: 'file', id: 'import-json', accept: 'application/json', class: 'cache', onChange: importerSauvegarde }),
  ]);
  racine.appendChild(barre);

  const zoneEdition = el('div', { id: 'zone-edition' });
  const zoneListe = el('div', { id: 'zone-liste' });
  racine.appendChild(zoneEdition);
  racine.appendChild(zoneListe);

  rendreEdition();
  rendreListe();

  // --- Actions --------------------------------------------------------------
  function creerSite() {
    const site = ajouterSite({});
    etat.editionId = site.id;
    rendreEdition();
    rendreListe();
  }

  function exporterCSV() {
    const sites = filtrer(chargerSites());
    if (!sites.length) return notifier('Aucun site à exporter.', 'erreur');
    telecharger(`prospection-cee-${aujourdhuiISO()}.csv`, sitesVersCSV(sites));
    notifier(`${sites.length} site(s) exporté(s) en CSV.`, 'succes');
  }

  function exporterSauvegarde() {
    telecharger(`sauvegarde-cee-${aujourdhuiISO()}.json`, exporterJSON(), 'application/json');
    notifier('Sauvegarde JSON téléchargée.', 'succes');
  }

  function importerSauvegarde(evenement) {
    const fichier = evenement.target.files?.[0];
    if (!fichier) return;
    const lecteur = new FileReader();
    lecteur.onload = () => {
      const r = importerJSON(String(lecteur.result));
      notifier(r.message, r.ok ? 'succes' : 'erreur');
      if (r.ok) { etat.editionId = null; rendreEdition(); rendreListe(); }
    };
    lecteur.readAsText(fichier);
    evenement.target.value = '';
  }

  // --- Rendu de la liste ----------------------------------------------------
  function rendreListe() {
    const sites = filtrer(chargerSites());
    vider(zoneListe);

    const compteurs = el('div', { class: 'compteurs' }, STATUTS.map((s) => {
      const nb = chargerSites().filter((site) => site.statut === s.id).length;
      return el('span', { class: `puce puce--${s.id}`, text: `${s.label} : ${nb}` });
    }));
    zoneListe.appendChild(compteurs);

    if (!sites.length) {
      zoneListe.appendChild(el('p', { class: 'vide', text: 'Aucun site ne correspond à ces critères.' }));
      return;
    }

    const params = chargerParametres(DEFAUTS_SIMULATEUR);
    const corps = el('tbody', {}, sites.map((site) => {
      const estimation = site.typeCee
        ? estimationPourType(site.typeCee, site.nbStations || 1, params.prixBrutEurMWhc, params.margeDelegatairePct)
        : null;
      return el('tr', { class: etat.editionId === site.id ? 'ligne--active' : '' }, [
        el('td', {}, [
          el('strong', { text: site.nom || '(sans nom)' }),
          el('span', { class: 'cellule__detail', text: [site.societe, site.typeSite].filter(Boolean).join(' — ') }),
        ]),
        el('td', { text: site.ville || '—' }),
        el('td', {}, site.typeCee
          ? el('span', { class: `badge-type badge-type--${site.typeCee}`, text: site.typeCee })
          : el('span', { class: 'note', text: '—' })),
        el('td', { class: 'num', text: estimation ? euros(estimation.montantNetTotal) : '—' }),
        el('td', {}, [
          el('span', { text: site.contactPrenom || '—' }),
          el('span', { class: 'cellule__detail', text: site.contactFonction || '' }),
        ]),
        el('td', {}, selectStatut(site)),
        el('td', { text: site.dateRelance ? dateFr(site.dateRelance) : '—' }),
        el('td', { class: 'actions-ligne' }, [
          el('button', { type: 'button', class: 'btn btn--mini', text: 'Éditer', onClick: () => { etat.editionId = site.id; rendreEdition(); rendreListe(); } }),
          el('button', { type: 'button', class: 'btn btn--mini', text: 'E-mail', onClick: () => { window.location.hash = `#/emails?site=${site.id}`; } }),
          el('button', { type: 'button', class: 'btn btn--mini btn--danger', text: 'Suppr.', onClick: () => supprimer(site) }),
        ]),
      ]);
    }));

    zoneListe.appendChild(el('div', { class: 'carte' }, el('table', { class: 'tableau' }, [
      el('thead', {}, el('tr', {}, ['Site', 'Ville', 'Type', 'CEE net / an', 'Contact', 'Statut', 'Relance', ''].map(
        (t) => el('th', { text: t }),
      ))),
      corps,
    ])));
  }

  function selectStatut(site) {
    const select = el('select', {
      class: `select-statut select-statut--${site.statut}`,
      onChange: (e) => { majSite(site.id, { statut: e.target.value }); rendreListe(); rendreEdition(); },
    });
    for (const s of STATUTS) {
      const option = el('option', { value: s.id, text: s.label });
      if (s.id === site.statut) option.selected = true;
      select.appendChild(option);
    }
    return select;
  }

  function supprimer(site) {
    if (!window.confirm(`Supprimer définitivement « ${site.nom || 'ce site'} » ?`)) return;
    supprimerSite(site.id);
    if (etat.editionId === site.id) etat.editionId = null;
    rendreEdition();
    rendreListe();
    notifier('Site supprimé.', 'info');
  }

  // --- Rendu du formulaire d'edition ---------------------------------------
  function rendreEdition() {
    vider(zoneEdition);
    if (!etat.editionId) return;
    const site = trouverSite(etat.editionId);
    if (!site) { etat.editionId = null; return; }

    const formulaire = el('form', { class: 'carte formulaire formulaire--large', id: 'form-site' });
    formulaire.appendChild(el('h2', { text: site.nom ? `Fiche : ${site.nom}` : 'Nouvelle fiche site' }));

    const champs = [
      { cle: 'nom', label: 'Nom du site', type: 'text' },
      { cle: 'societe', label: 'Société exploitante', type: 'text' },
      { cle: 'typeSite', label: 'Type de site', options: TYPES_SITE.map((t) => ({ value: t, label: t })) },
      { cle: 'typeCee', label: 'Type CEE', options: [{ value: '', label: 'À qualifier' }, ...ORDRE_TYPES.map((t) => ({ value: t, label: `${t} — ${TYPES_STATION[t].titre}` }))] },
      { cle: 'nbStations', label: 'Nombre de stations', type: 'number', attrs: { min: 0, step: 1 } },
      { cle: 'adresse', label: 'Adresse', type: 'text' },
      { cle: 'codePostal', label: 'Code postal', type: 'text' },
      { cle: 'ville', label: 'Ville', type: 'text' },
      { cle: 'contactPrenom', label: 'Prénom du contact', type: 'text', aide: 'Sert à personnaliser les e-mails. Aucune autre donnée personnelle n’est nécessaire.' },
      { cle: 'contactFonction', label: 'Fonction du contact', type: 'text', aide: 'Ex. : directeur de magasin, responsable technique.' },
      { cle: 'contactEmail', label: 'E-mail professionnel', type: 'email', aide: 'Adresse professionnelle uniquement.' },
      { cle: 'statut', label: 'Statut', options: STATUTS.map((s) => ({ value: s.id, label: s.label })) },
      { cle: 'dateRelance', label: 'Date de relance', type: 'date' },
      { cle: 'dateSignature', label: 'Date de signature du contrat', type: 'date', aide: 'Date d’engagement. Elle détermine la date anniversaire suivie dans l’onglet Dossiers CEE.' },
    ];

    const grille = el('div', { class: 'grille-3' });
    for (const def of champs) {
      const id = `site-${def.cle}`;
      let controle;
      if (def.options) {
        controle = el('select', { id, name: def.cle });
        for (const opt of def.options) {
          const o = el('option', { value: opt.value, text: opt.label });
          if (String(opt.value) === String(site[def.cle] ?? '')) o.selected = true;
          controle.appendChild(o);
        }
      } else {
        controle = el('input', { id, name: def.cle, type: def.type, ...(def.attrs || {}) });
        controle.value = site[def.cle] ?? '';
      }
      grille.appendChild(el('div', { class: 'champ' }, [
        el('label', { for: id, text: def.label }),
        controle,
        def.aide ? el('p', { class: 'champ__aide', text: def.aide }) : null,
      ]));
    }
    formulaire.appendChild(grille);

    const notes = el('textarea', { id: 'site-notes', name: 'notes', rows: 4, placeholder: 'Historique des échanges, contraintes techniques, emplacement envisagé…' });
    notes.value = site.notes || '';
    formulaire.appendChild(el('div', { class: 'champ' }, [el('label', { for: 'site-notes', text: 'Notes' }), notes]));

    formulaire.appendChild(el('div', { class: 'actions' }, [
      el('button', { type: 'submit', class: 'btn btn--primaire', text: 'Enregistrer' }),
      el('button', { type: 'button', class: 'btn btn--secondaire', text: 'Fermer', onClick: () => { etat.editionId = null; rendreEdition(); rendreListe(); } }),
    ]));

    formulaire.addEventListener('submit', (e) => {
      e.preventDefault();
      const donnees = Object.fromEntries(new FormData(formulaire).entries());
      donnees.nbStations = Math.max(0, Math.round(Number(donnees.nbStations) || 0));
      majSite(site.id, donnees);
      notifier('Fiche enregistrée.', 'succes');
      rendreListe();
    });

    zoneEdition.appendChild(formulaire);
  }
}

/** Applique les filtres courants a la liste des sites. */
function filtrer(sites) {
  return sites.filter((site) => {
    if (etat.statut && site.statut !== etat.statut) return false;
    if (etat.typeCee && site.typeCee !== etat.typeCee) return false;
    if (etat.recherche) {
      const cible = `${site.nom} ${site.ville} ${site.societe}`.toLowerCase();
      if (!cible.includes(etat.recherche)) return false;
    }
    return true;
  });
}

function selectFiltre(id, libelleVide, options, onChange) {
  const select = el('select', { id, onChange: (e) => onChange(e.target.value) });
  select.appendChild(el('option', { value: '', text: libelleVide }));
  for (const opt of options) select.appendChild(el('option', { value: opt.value, text: opt.label }));
  return select;
}
