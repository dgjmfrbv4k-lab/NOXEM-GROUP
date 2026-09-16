/**
 * views/emails-view.js — Module 4 : modeles d'e-mails de prospection.
 *
 * Les variables sont remplies depuis la fiche site du CRM ; la signature est
 * saisie une fois et conservee localement.
 */

import { MODELES, modele, remplir, variablesManquantes, lienMailto, VARIABLES } from '../emails.js';
import { chargerSites, chargerParametres, sauverParametres } from '../storage.js';
import { estimationPourType } from '../classify.js';
import { DEFAUTS_SIMULATEUR } from '../config.js';
import { el, $, vider, euros, copier, notifier } from '../ui.js';

const CHAMPS_SIGNATURE = [
  { cle: 'signatureNom', variable: '[Votre nom]', label: 'Votre nom' },
  { cle: 'signatureSociete', variable: '[Votre société]', label: 'Votre structure' },
  { cle: 'signatureTelephone', variable: '[Votre téléphone]', label: 'Votre téléphone' },
  { cle: 'signatureEmail', variable: '[Votre email]', label: 'Votre e-mail' },
];

export function monter(racine, requete = {}) {
  const params = chargerParametres(DEFAUTS_SIMULATEUR);
  const sites = chargerSites();
  let siteId = requete.site || sites[0]?.id || '';
  let modeleId = MODELES[0].id;

  racine.appendChild(el('div', { class: 'entete-vue' }, [
    el('h1', { text: 'Modèles d’e-mails' }),
    el('p', { class: 'sous-titre', text: 'Les variables sont remplies depuis la fiche site. Relisez toujours l’e-mail avant envoi : ne promettez jamais une prise en charge totale, parlez d’un financement « en grande partie » assuré par les CEE.' }),
  ]));

  // --- Selecteurs -----------------------------------------------------------
  const selectSite = el('select', { id: 'email-site', onChange: (e) => { siteId = e.target.value; rendre(); } });
  selectSite.appendChild(el('option', { value: '', text: sites.length ? '— Aucun site (variables non remplies) —' : 'Aucun site dans le CRM' }));
  for (const site of sites) {
    const option = el('option', { value: site.id, text: `${site.nom || '(sans nom)'}${site.ville ? ` — ${site.ville}` : ''}` });
    if (site.id === siteId) option.selected = true;
    selectSite.appendChild(option);
  }

  const selectModele = el('select', { id: 'email-modele', onChange: (e) => { modeleId = e.target.value; rendre(); } });
  for (const m of MODELES) selectModele.appendChild(el('option', { value: m.id, text: m.nom }));

  const barre = el('div', { class: 'carte' }, [
    el('div', { class: 'grille-2' }, [
      el('div', { class: 'champ' }, [el('label', { for: 'email-site', text: 'Site destinataire' }), selectSite]),
      el('div', { class: 'champ' }, [el('label', { for: 'email-modele', text: 'Modèle' }), selectModele]),
    ]),
    el('h3', { class: 'formulaire__groupe', text: 'Signature (enregistrée localement)' }),
    el('div', { class: 'grille-4' }, CHAMPS_SIGNATURE.map((c) => el('div', { class: 'champ' }, [
      el('label', { for: `sig-${c.cle}`, text: c.label }),
      el('input', {
        id: `sig-${c.cle}`, type: 'text', value: params[c.cle] || '',
        onInput: (e) => { params[c.cle] = e.target.value; sauverParametres(params); rendre(); },
      }),
    ]))),
  ]);
  racine.appendChild(barre);

  const apercu = el('div', { class: 'carte', id: 'apercu-email' });
  racine.appendChild(apercu);
  rendre();

  /** Construit les valeurs de variables a partir de la fiche site. */
  function valeursVariables() {
    const site = sites.find((s) => s.id === siteId);
    const valeurs = {};
    for (const c of CHAMPS_SIGNATURE) valeurs[c.variable] = params[c.cle];
    if (!site) return valeurs;

    const estimation = site.typeCee
      ? estimationPourType(site.typeCee, site.nbStations || 1, params.prixBrutEurMWhc, params.margeDelegatairePct)
      : null;
    return {
      ...valeurs,
      '[Prénom]': site.contactPrenom,
      '[nom du site]': site.nom,
      '[Société]': site.societe || site.nom,
      '[Ville]': site.ville,
      '[Type CEE]': site.typeCee,
      '[Montant estimé]': estimation ? euros(estimation.montantNetParStation) : '',
    };
  }

  function rendre() {
    const m = modele(modeleId);
    const valeurs = valeursVariables();
    const objet = remplir(m.objet, valeurs);
    const corps = remplir(m.corps, valeurs);
    const manquantes = [...new Set([...variablesManquantes(objet), ...variablesManquantes(corps)])];
    const site = sites.find((s) => s.id === siteId);

    vider(apercu);
    apercu.appendChild(el('h2', { text: m.nom }));
    apercu.appendChild(el('p', { class: 'note', text: m.description }));

    if (manquantes.length) {
      apercu.appendChild(el('p', { class: 'alerte alerte--vigilance' }, [
        el('strong', { text: 'Variables non remplies : ' }),
        el('span', { text: manquantes.join(', ') }),
        el('span', { text: ` — ${manquantes.some((v) => v.startsWith('[Votre')) ? 'complétez votre signature ci-dessus. ' : ''}Complétez la fiche site dans le CRM ou modifiez le texte avant envoi.` }),
      ]));
    }

    apercu.appendChild(el('div', { class: 'champ' }, [
      el('label', { for: 'email-objet', text: 'Objet' }),
      el('input', { id: 'email-objet', type: 'text', value: objet }),
    ]));

    const zoneCorps = el('textarea', { id: 'email-corps', rows: 26, class: 'email-corps' });
    zoneCorps.value = corps;
    apercu.appendChild(el('div', { class: 'champ' }, [
      el('label', { for: 'email-corps', text: 'Corps du message (modifiable avant copie)' }),
      zoneCorps,
    ]));

    apercu.appendChild(el('div', { class: 'actions' }, [
      el('button', { type: 'button', class: 'btn btn--primaire', text: 'Copier l’e-mail', onClick: () => copier(`${$('#email-objet').value}\n\n${$('#email-corps').value}`) }),
      el('button', { type: 'button', class: 'btn btn--secondaire', text: 'Copier le corps seul', onClick: () => copier($('#email-corps').value) }),
      el('a', {
        class: 'btn btn--secondaire',
        href: lienMailto(site?.contactEmail, objet, corps),
        text: 'Ouvrir dans ma messagerie',
        onClick: () => { if (!site?.contactEmail) notifier('Aucune adresse e-mail renseignée pour ce site.', 'info'); },
      }),
    ]));

    apercu.appendChild(el('details', { class: 'details' }, [
      el('summary', { text: 'Variables disponibles' }),
      el('ul', {}, Object.entries(VARIABLES).map(([v, description]) => el('li', {}, [
        el('code', { text: v }), el('span', { text: ` — ${description}` }),
      ]))),
    ]));
  }
}
