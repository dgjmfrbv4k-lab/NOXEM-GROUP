/**
 * ui.js — petits utilitaires d'interface (DOM + formatage francais).
 * Aucune dependance externe.
 */

/** Cree un element DOM. `attrs.html` injecte du HTML, `attrs.text` du texte. */
export function el(balise, attrs = {}, enfants = []) {
  const noeud = document.createElement(balise);
  for (const [cle, valeur] of Object.entries(attrs)) {
    if (valeur === null || valeur === undefined || valeur === false) continue;
    if (cle === 'class') noeud.className = valeur;
    else if (cle === 'text') noeud.textContent = valeur;
    else if (cle === 'html') noeud.innerHTML = valeur;
    else if (cle === 'dataset') Object.assign(noeud.dataset, valeur);
    else if (cle.startsWith('on') && typeof valeur === 'function') {
      noeud.addEventListener(cle.slice(2).toLowerCase(), valeur);
    } else noeud.setAttribute(cle, valeur);
  }
  for (const enfant of [].concat(enfants)) {
    if (enfant === null || enfant === undefined || enfant === false) continue;
    noeud.appendChild(typeof enfant === 'string' ? document.createTextNode(enfant) : enfant);
  }
  return noeud;
}

export const $ = (selecteur, racine = document) => racine.querySelector(selecteur);
export const $$ = (selecteur, racine = document) => [...racine.querySelectorAll(selecteur)];

/** Vide un element. */
export function vider(noeud) {
  while (noeud.firstChild) noeud.removeChild(noeud.firstChild);
}

const fmtEuro = new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR', maximumFractionDigits: 0 });
const fmtEuroPrecis = new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR', minimumFractionDigits: 2, maximumFractionDigits: 2 });
const fmtNombre = new Intl.NumberFormat('fr-FR');
const fmtDate = new Intl.DateTimeFormat('fr-FR', { dateStyle: 'long' });

export function euros(valeur, precis = false) {
  if (valeur === null || !Number.isFinite(valeur)) return '—';
  return (precis ? fmtEuroPrecis : fmtEuro).format(valeur);
}

export function nombreFr(valeur) {
  if (valeur === null || !Number.isFinite(valeur)) return '—';
  return fmtNombre.format(Math.round(valeur));
}

export function kwhCumac(valeur) {
  return `${nombreFr(valeur)} kWh cumac`;
}

export function dateFr(date) {
  if (!date) return '—';
  const d = date instanceof Date ? date : new Date(`${date}T00:00:00`);
  return Number.isNaN(d.getTime()) ? '—' : fmtDate.format(d);
}

/** Date du jour au format AAAA-MM-JJ (valeur d'un <input type="date">). */
export function aujourdhuiISO() {
  const d = new Date();
  const mois = String(d.getMonth() + 1).padStart(2, '0');
  const jour = String(d.getDate()).padStart(2, '0');
  return `${d.getFullYear()}-${mois}-${jour}`;
}

/** Affiche un message temporaire en bas de l'ecran. */
export function notifier(message, type = 'info') {
  let zone = $('#notifications');
  if (!zone) {
    zone = el('div', { id: 'notifications', class: 'notifications' });
    document.body.appendChild(zone);
  }
  const noeud = el('div', { class: `notification notification--${type}`, text: message });
  zone.appendChild(noeud);
  setTimeout(() => noeud.classList.add('notification--sortie'), 3200);
  setTimeout(() => noeud.remove(), 3600);
}

/** Copie un texte dans le presse-papiers (avec repli pour les contextes non securises). */
export async function copier(texte) {
  try {
    await navigator.clipboard.writeText(texte);
    notifier('Copié dans le presse-papiers.', 'succes');
  } catch (e) {
    const zone = el('textarea', { style: 'position:fixed;opacity:0' });
    zone.value = texte;
    document.body.appendChild(zone);
    zone.select();
    try {
      document.execCommand('copy');
      notifier('Copié dans le presse-papiers.', 'succes');
    } catch (err) {
      notifier('Copie impossible : sélectionnez le texte manuellement.', 'erreur');
    }
    zone.remove();
  }
}

/** Champ de formulaire etiquete. */
export function champ({ id, label, type = 'text', valeur = '', aide = '', options = null, attrs = {} }) {
  const conteneur = el('div', { class: 'champ' });
  conteneur.appendChild(el('label', { for: id, text: label }));
  let controle;
  if (options) {
    controle = el('select', { id, name: id, ...attrs });
    for (const opt of options) {
      const o = el('option', { value: opt.value, text: opt.label });
      if (String(opt.value) === String(valeur)) o.selected = true;
      controle.appendChild(o);
    }
  } else if (type === 'textarea') {
    controle = el('textarea', { id, name: id, rows: attrs.rows || 3, ...attrs });
    controle.value = valeur;
  } else {
    controle = el('input', { id, name: id, type, ...attrs });
    controle.value = valeur;
  }
  conteneur.appendChild(controle);
  if (aide) conteneur.appendChild(el('p', { class: 'champ__aide', text: aide }));
  return conteneur;
}
