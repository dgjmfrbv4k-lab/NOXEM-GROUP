/**
 * storage.js
 * ---------------------------------------------------------------------------
 * Persistance locale (localStorage). Aucun backend, aucune donnee ne quitte le
 * navigateur : c'est le choix retenu pour la V1.
 *
 * RGPD : ne stocker que les donnees necessaires a la relation commerciale
 * (contact professionnel). L'interface rappelle cette regle et ne collecte
 * aucune donnee personnelle au-dela du prenom et de la fonction du contact.
 * ---------------------------------------------------------------------------
 */

const CLE_SITES = 'cee.gonflage.sites.v1';
const CLE_PARAMS = 'cee.gonflage.parametres.v1';

/** Repli memoire si localStorage est indisponible (navigation privee, etc.). */
const memoire = new Map();

function lireBrut(cle) {
  try {
    return window.localStorage.getItem(cle);
  } catch (e) {
    return memoire.get(cle) ?? null;
  }
}

function ecrireBrut(cle, valeur) {
  try {
    window.localStorage.setItem(cle, valeur);
  } catch (e) {
    memoire.set(cle, valeur);
  }
}

function lireJSON(cle, parDefaut) {
  const brut = lireBrut(cle);
  if (!brut) return parDefaut;
  try {
    return JSON.parse(brut);
  } catch (e) {
    console.warn('Donnees illisibles pour', cle, e);
    return parDefaut;
  }
}

/** Identifiant simple et stable pour un site. */
export function nouvelId() {
  return `site_${Date.now().toString(36)}_${Math.random().toString(36).slice(2, 7)}`;
}

/** Fiche site vierge (sert de schema de reference). */
export function siteVide() {
  return {
    id: nouvelId(),
    nom: '',
    typeSite: '',
    adresse: '',
    codePostal: '',
    ville: '',
    typeCee: '',
    nbStations: 1,
    societe: '',
    contactPrenom: '',
    contactFonction: '',
    contactEmail: '',
    statut: 'a_contacter',
    dateRelance: '',
    dateSignature: '',
    notes: '',
    eligibilite: {},
    pieces: {},
    creeLe: new Date().toISOString(),
    majLe: new Date().toISOString(),
  };
}

/** @returns {Array<object>} tous les sites enregistres. */
export function chargerSites() {
  const sites = lireJSON(CLE_SITES, []);
  return Array.isArray(sites) ? sites.map((s) => ({ ...siteVide(), ...s })) : [];
}

export function sauverSites(sites) {
  ecrireBrut(CLE_SITES, JSON.stringify(sites));
}

export function ajouterSite(donnees = {}) {
  const sites = chargerSites();
  const site = { ...siteVide(), ...donnees, id: nouvelId() };
  sites.push(site);
  sauverSites(sites);
  return site;
}

export function majSite(id, patch = {}) {
  const sites = chargerSites();
  const index = sites.findIndex((s) => s.id === id);
  if (index === -1) return null;
  sites[index] = { ...sites[index], ...patch, id, majLe: new Date().toISOString() };
  sauverSites(sites);
  return sites[index];
}

export function supprimerSite(id) {
  sauverSites(chargerSites().filter((s) => s.id !== id));
}

export function trouverSite(id) {
  return chargerSites().find((s) => s.id === id) || null;
}

/** Parametres du simulateur (prix CEE, marge, couts...). */
export function chargerParametres(parDefaut = {}) {
  return { ...parDefaut, ...lireJSON(CLE_PARAMS, {}) };
}

export function sauverParametres(params) {
  ecrireBrut(CLE_PARAMS, JSON.stringify(params));
}

/** Sauvegarde complete (sites + parametres) au format JSON. */
export function exporterJSON() {
  return JSON.stringify(
    { version: 1, exporteLe: new Date().toISOString(), sites: chargerSites(), parametres: chargerParametres() },
    null,
    2,
  );
}

/**
 * Restaure une sauvegarde JSON.
 * @returns {{ok:boolean, message:string}}
 */
export function importerJSON(texte) {
  try {
    const data = JSON.parse(texte);
    if (!data || !Array.isArray(data.sites)) {
      return { ok: false, message: 'Fichier invalide : aucune liste de sites trouvée.' };
    }
    sauverSites(data.sites.map((s) => ({ ...siteVide(), ...s })));
    if (data.parametres) sauverParametres(data.parametres);
    return { ok: true, message: `${data.sites.length} site(s) importé(s).` };
  } catch (e) {
    return { ok: false, message: `Import impossible : ${e.message}` };
  }
}
