/**
 * views/dossiers.js — Module 5 : page de synthese « dossier CEE ».
 *
 * Pour chaque site signe : pieces justificatives a reunir, dates d'engagement
 * et d'achevement, alerte a l'approche de la date anniversaire.
 */

import { PIECES_DOSSIER, echeances, avancementPieces, messageEcheance } from '../dossier.js';
import { chargerSites, majSite, chargerParametres } from '../storage.js';
import { estimationPourType } from '../classify.js';
import { DEFAUTS_SIMULATEUR, TYPES_STATION, AVERTISSEMENT } from '../config.js';
import { el, vider, euros, dateFr, nombreFr, notifier } from '../ui.js';

export function monter(racine) {
  racine.appendChild(el('div', { class: 'entete-vue' }, [
    el('h1', { text: 'Dossiers CEE' }),
    el('p', { class: 'sous-titre', text: 'Pièces justificatives et échéances des sites signés. Un dossier incomplet expose à l’annulation des CEE en cas de contrôle du PNCEE.' }),
    el('p', { class: 'avertissement', text: AVERTISSEMENT }),
  ]));

  const conteneur = el('div', { id: 'liste-dossiers' });
  racine.appendChild(conteneur);
  rendre();

  function rendre() {
    const params = chargerParametres(DEFAUTS_SIMULATEUR);
    const sites = chargerSites().filter((s) => s.statut === 'signe');
    vider(conteneur);

    if (!sites.length) {
      conteneur.appendChild(el('p', { class: 'vide', text: 'Aucun site au statut « Signé ». Passez une fiche au statut « Signé » dans l’onglet Prospection pour ouvrir son dossier.' }));
      return;
    }

    // --- Bandeau des echeances proches -------------------------------------
    const urgents = sites
      .map((site) => ({ site, ech: echeances(site.dateSignature) }))
      .filter(({ ech }) => ech.niveau === 'urgent' || ech.niveau === 'vigilance')
      .sort((a, b) => (a.ech.joursRestants ?? 0) - (b.ech.joursRestants ?? 0));

    if (urgents.length) {
      conteneur.appendChild(el('div', { class: 'carte carte--alerte' }, [
        el('h2', { text: 'Renouvellements à préparer' }),
        el('ul', {}, urgents.map(({ site, ech }) => el('li', {}, [
          el('strong', { text: site.nom || '(sans nom)' }),
          el('span', { text: ` — ${messageEcheance(ech)} (${dateFr(ech.prochaineEcheance)})` }),
        ]))),
        el('p', { class: 'note', text: 'Le renouvellement doit être expressement formalisé : la reconduction tacite n’ouvre pas droit à une nouvelle valorisation.' }),
      ]));
    }

    // --- Un bloc par site ---------------------------------------------------
    for (const site of sites) {
      const ech = echeances(site.dateSignature);
      const avancement = avancementPieces(site.pieces);
      const estimation = site.typeCee
        ? estimationPourType(site.typeCee, site.nbStations || 1, params.prixBrutEurMWhc, params.margeDelegatairePct)
        : null;

      const carte = el('div', { class: 'carte dossier' });
      carte.appendChild(el('div', { class: 'dossier__entete' }, [
        el('div', {}, [
          el('h2', { text: site.nom || '(sans nom)' }),
          el('p', { class: 'note', text: [site.societe, [site.adresse, site.codePostal, site.ville].filter(Boolean).join(' ')].filter(Boolean).join(' — ') }),
        ]),
        site.typeCee ? el('span', { class: `badge-type badge-type--${site.typeCee}`, text: `Type ${site.typeCee}` }) : null,
      ]));

      carte.appendChild(el('table', { class: 'tableau tableau--compact' }, el('tbody', {}, [
        ligne('Date d’engagement (signature)', dateFr(ech.engagement)),
        ligne('Date d’achèvement (anniversaire)', dateFr(ech.achevement)),
        ligne('Prochaine échéance', `${dateFr(ech.prochaineEcheance)}${ech.anneeContrat ? ` (année ${ech.anneeContrat} du contrat)` : ''}`),
        ligne('Stations', site.nbStations ? `${nombreFr(site.nbStations)} × ${site.typeCee ? TYPES_STATION[site.typeCee].titre : 'type à qualifier'}` : '—'),
        ligne('Volume valorisé', estimation ? `${nombreFr(estimation.kwhCumacTotal)} kWh cumac` : '—'),
        ligne('Montant CEE net estimé / an', estimation ? euros(estimation.montantNetTotal, true) : '—'),
      ])));

      carte.appendChild(el('p', { class: `alerte alerte--${ech.niveau}`, text: messageEcheance(ech) }));

      // Checklist des pieces, cochable et persistee sur la fiche site.
      const liste = el('div', { class: 'pieces' });
      for (const piece of PIECES_DOSSIER) {
        const id = `piece-${site.id}-${piece.id}`;
        const case_ = el('input', {
          type: 'checkbox',
          id,
          onChange: (e) => {
            const pieces = { ...(site.pieces || {}), [piece.id]: e.target.checked };
            majSite(site.id, { pieces });
            notifier('Dossier mis à jour.', 'succes');
            rendre();
          },
        });
        if (site.pieces?.[piece.id]) case_.checked = true;
        liste.appendChild(el('label', { class: 'case', for: id }, [
          case_,
          el('span', {}, [
            el('strong', { text: piece.label }),
            piece.obligatoire ? el('span', { class: 'etiquette etiquette--bloquant', text: 'obligatoire' }) : el('span', { class: 'etiquette', text: 'si applicable' }),
            el('span', { class: 'case__aide', text: piece.aide }),
          ]),
        ]));
      }
      carte.appendChild(el('h3', { class: 'formulaire__groupe', text: `Pièces du dossier (${avancement.fournies}/${avancement.total})` }));
      carte.appendChild(barreProgression(avancement.progression));
      carte.appendChild(liste);
      carte.appendChild(el('p', {
        class: `verdict ${avancement.complet ? 'verdict--ok' : 'verdict--ko'}`,
        text: avancement.complet
          ? 'Toutes les pièces obligatoires sont réunies.'
          : `Pièces obligatoires manquantes : ${avancement.manquantes.map((p) => p.label).join(', ')}.`,
      }));

      conteneur.appendChild(carte);
    }
  }
}

function ligne(libelle, valeur) {
  return el('tr', {}, [el('th', { scope: 'row', text: libelle }), el('td', { class: 'num', text: valeur })]);
}

function barreProgression(ratio) {
  return el('div', { class: 'progression' }, el('div', {
    class: 'progression__barre',
    style: `width:${Math.round(ratio * 100)}%`,
  }));
}
