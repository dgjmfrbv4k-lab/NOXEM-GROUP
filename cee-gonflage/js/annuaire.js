/**
 * annuaire.js — lecture de l'Annuaire de l'administration (service-public.fr).
 *
 * Ce module ne dépend NI de Node NI du navigateur : il ne contient que la
 * logique de lecture des enregistrements et la construction des URL. Il est
 * importé aussi bien par l'application (onglet Prospection) que par
 * outils/collecte-mairies.mjs. Une seule implémentation, testée une fois.
 *
 * Les coordonnées récupérées sont institutionnelles et publiées par l'État :
 * ce sont des adresses d'établissement, pas des données personnelles. Aucun
 * nom d'agent ni d'élu n'est collecté.
 */

export const API = 'https://api-lannuaire.service-public.fr/api/explore/v2.1'
  + '/catalog/datasets/api-lannuaire-administration/records';

/** Nombre d'enregistrements par appel (maximum accepté par l'API). */
export const PAR_PAGE = 100;

/**
 * URL d'une page de résultats pour un département.
 * `code_insee_commune` commence par le numéro de département, d'où le LIKE.
 */
export function urlRequete(departement, { limit = PAR_PAGE, offset = 0 } = {}) {
  const parametres = new URLSearchParams({
    where: `pivot LIKE "mairie" AND code_insee_commune LIKE "${departement}%"`,
    limit: String(limit),
    offset: String(offset),
  });
  return `${API}?${parametres}`;
}

/**
 * Les champs de l'annuaire sont parfois sérialisés en JSON dans une chaîne,
 * parfois déjà structurés. Cette fonction accepte les deux formes.
 */
export function lireChamp(valeur) {
  if (valeur === null || valeur === undefined || valeur === '') return null;
  if (typeof valeur === 'object') return valeur;
  if (typeof valeur !== 'string') return valeur;
  const texte = valeur.trim();
  if (!texte.startsWith('[') && !texte.startsWith('{')) return texte;
  try {
    return JSON.parse(texte);
  } catch (e) {
    return texte;
  }
}

/** Première adresse e-mail exploitable d'un enregistrement. */
export function extraireCourriel(enregistrement) {
  const brut = lireChamp(enregistrement.adresse_courriel);
  const candidats = []
    .concat(brut ?? [])
    .map((c) => (typeof c === 'string' ? c : c?.valeur ?? c?.value ?? ''))
    .filter((c) => typeof c === 'string' && c.includes('@'));
  return candidats[0] || '';
}

/** Téléphone principal, en texte lisible. */
export function extraireTelephone(enregistrement) {
  const brut = lireChamp(enregistrement.telephone);
  const candidats = []
    .concat(brut ?? [])
    .map((t) => (typeof t === 'string' ? t : t?.valeur ?? t?.value ?? ''))
    .filter(Boolean);
  return candidats[0] || '';
}

/** Adresse postale : on retient l'adresse physique si plusieurs sont fournies. */
export function extraireAdresse(enregistrement) {
  const brut = lireChamp(enregistrement.adresse);
  const liste = [].concat(brut ?? []).filter((a) => a && typeof a === 'object');
  const choisie = liste.find((a) => a.type_adresse === 'Adresse') || liste[0] || {};
  return {
    voie: [choisie.numero_voie, choisie.complement1, choisie.complement2].filter(Boolean).join(' ').trim(),
    codePostal: choisie.code_postal || '',
    ville: choisie.nom_commune || '',
  };
}

/**
 * Un enregistrement de l'annuaire -> une fiche site du CRM.
 *
 * Le type CEE reste vide : une commune a le plus souvent un parking ouvert au
 * public (type B) ET un parking d'agents (type C). C'est un dossier groupé,
 * à qualifier lors de l'échange.
 */
export function versSite(enregistrement) {
  const adresse = extraireAdresse(enregistrement);
  const courriel = extraireCourriel(enregistrement);
  const telephone = extraireTelephone(enregistrement);
  const nom = enregistrement.nom || `Mairie de ${adresse.ville}`;
  const maintenant = new Date().toISOString();

  return {
    id: `mairie_${enregistrement.id || adresse.codePostal + adresse.ville}`.replace(/[^a-zA-Z0-9_]/g, '_'),
    nom,
    societe: 'Commune',
    typeSite: 'Collectivité',
    adresse: adresse.voie,
    codePostal: adresse.codePostal,
    ville: adresse.ville,
    typeCee: '',
    nbStations: 1,
    contactPrenom: '',
    contactFonction: 'Direction générale des services',
    contactEmail: courriel,
    statut: 'a_contacter',
    dateRelance: '',
    dateSignature: '',
    notes: [
      telephone ? `Standard : ${telephone}.` : '',
      'Parking public = type B, parking des agents = type C : dossier groupé à qualifier.',
      'Demander le DGS ou le service technique. Source : Annuaire de l’administration (service-public.fr).',
    ].filter(Boolean).join(' '),
    eligibilite: {},
    pieces: {},
    creeLe: maintenant,
    majLe: maintenant,
  };
}

/** Écarte les fiches sans adresse e-mail et les doublons d'adresse. */
export function nettoyer(sites) {
  const vues = new Set();
  return sites.filter((s) => {
    if (!s.contactEmail) return false;
    const cle = s.contactEmail.toLowerCase();
    if (vues.has(cle)) return false;
    vues.add(cle);
    return true;
  });
}

/**
 * Collecte paginée pour un département.
 *
 * `fetch` est injectable : l'application passe celui du navigateur, l'outil en
 * ligne de commande celui de Node, et les tests un faux. `surAvancement` permet
 * d'afficher une progression pendant que ça tourne.
 */
export async function collecterDepartement(departement, {
  fetchFn = globalThis.fetch, parPage = PAR_PAGE, surAvancement = () => {}, maxOffset = 10000,
} = {}) {
  const resultats = [];
  let offset = 0;

  for (;;) {
    const reponse = await fetchFn(urlRequete(departement, { limit: parPage, offset }));
    if (!reponse.ok) {
      throw new Error(`L'annuaire a répondu ${reponse.status}. Réessayez dans quelques minutes.`);
    }
    const data = await reponse.json();
    const lot = data.results || [];
    resultats.push(...lot);
    surAvancement({ departement, recus: resultats.length, total: data.total_count ?? null });
    if (lot.length < parPage) break;
    offset += parPage;
    if (offset > maxOffset) break; // garde-fou
  }

  return resultats;
}
