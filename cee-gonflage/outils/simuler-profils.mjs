/**
 * simuler-profils.mjs
 * ---------------------------------------------------------------------------
 * Chiffre chaque profil de client type avec le moteur de calcul de
 * l'application, et les classe par intérêt économique.
 *
 * L'objectif n'est pas de produire un chiffre exact — le prix du CEE bouge
 * chaque mois et les coûts ne sont pas encore contractualisés — mais de
 * répondre à une question de prospection : à effort commercial comparable,
 * quel type de client rapporte le plus ?
 *
 *   node outils/simuler-profils.mjs
 *   node outils/simuler-profils.mjs --prix 9 --marge 20 --entretien 300 --installation 900
 *   node outils/simuler-profils.mjs --md > docs/simulations.md
 * ---------------------------------------------------------------------------
 */

import { simuler } from '../js/calc.js';

/**
 * Profils de clients, tels qu'on les rencontre sur le terrain.
 * `effort` = nombre de rendez-vous typiques avant signature : c'est lui qui
 * transforme un gain brut en priorité commerciale.
 */
export const PROFILS = [
  { nom: 'Aire autoroutière (1 station)', nbA: 1, effort: 6, note: 'Sous-concessionnaire + accord du concessionnaire.' },
  { nom: 'Centre commercial (2 stations)', nbB: 2, effort: 3, note: 'Décision du directeur de centre.' },
  { nom: 'Hypermarché (2 stations)', nbB: 2, effort: 2, note: 'Grand parking, deux entrées.' },
  { nom: 'Supermarché indépendant (1 station)', nbB: 1, effort: 1, note: 'Le directeur est le propriétaire : décision rapide.' },
  { nom: 'Supermarché intégré (1 station)', nbB: 1, effort: 4, note: 'Remonte en direction régionale ou centrale.' },
  { nom: 'Parking municipal (1 station)', nbB: 1, effort: 3, note: 'Services techniques, puis convention d’occupation.' },
  { nom: 'Commune : parking public + parking agents', nbB: 1, nbC: 1, effort: 3, note: 'Dossier groupé B + C, un seul contrat.' },
  { nom: 'Station-service indépendante (1 station)', nbB: 1, effort: 1, note: 'Décision immédiate, petit parking.' },
  { nom: 'Entreprise, parking salariés (1 station)', nbC: 1, effort: 2, note: 'Faible volume : à vendre en complément.' },
  { nom: 'Groupement de 10 supermarchés', nbB: 10, effort: 8, note: 'Un accord, dix sites : le meilleur ratio.' },
];

/** Chiffre un profil avec les hypothèses de marché et de coûts fournies. */
export function chiffrer(profil, hypotheses) {
  const r = simuler({ nbA: profil.nbA || 0, nbB: profil.nbB || 0, nbC: profil.nbC || 0, ...hypotheses });
  return {
    nom: profil.nom,
    note: profil.note,
    effort: profil.effort,
    stations: r.stations.total,
    kwhCumac: r.volume.total,
    ceeNet: r.cee.net,
    margeAnnuelle: r.margeRecurrenteAnnuelle,
    investissement: r.investissementInitial,
    resultatAnnee1: r.resultatAnnee1,
    // Marge annuelle rapportée à l'effort commercial : l'indicateur de priorité.
    margeParRendezVous: profil.effort > 0 ? r.margeRecurrenteAnnuelle / profil.effort : null,
  };
}

/** Chiffre tous les profils et les classe par marge rapportée à l'effort. */
export function classer(hypotheses, profils = PROFILS) {
  return profils
    .map((p) => chiffrer(p, hypotheses))
    .sort((a, b) => (b.margeParRendezVous ?? 0) - (a.margeParRendezVous ?? 0));
}

/** Nombre de dossiers de ce type pour atteindre un objectif de marge annuelle. */
export function dossiersPourObjectif(ligne, objectif) {
  if (!(ligne.margeAnnuelle > 0)) return null;
  return Math.ceil(objectif / ligne.margeAnnuelle);
}

const euro = (v) => `${Math.round(v).toLocaleString('fr-FR')} €`;
const nb = (v) => Math.round(v).toLocaleString('fr-FR');

function principal() {
  const args = process.argv.slice(2);
  const lire = (cle, defaut) => {
    const i = args.indexOf(`--${cle}`);
    return i !== -1 && args[i + 1] ? Number(args[i + 1]) : defaut;
  };
  const markdown = args.includes('--md');

  const hypotheses = {
    prixBrutEurMWhc: lire('prix', 8.7),
    margeDelegatairePct: lire('marge', 20),
    coutEntretienAnnuelParStation: lire('entretien', 300),
    coutInstallationParStation: lire('installation', 900),
  };
  const objectif = lire('objectif', 50000);
  const lignes = classer(hypotheses);

  if (markdown) {
    console.log(`# Simulation par profil de client

Hypothèses : prix CEE brut **${hypotheses.prixBrutEurMWhc} €/MWhc**, marge délégataire
**${hypotheses.margeDelegatairePct} %**, entretien **${euro(hypotheses.coutEntretienAnnuelParStation)}/station/an**,
installation **${euro(hypotheses.coutInstallationParStation)}/station**.

> Chiffres indicatifs. Le prix du CEE varie chaque mois et les coûts ne sont pas encore
> contractualisés : ce tableau sert à **hiérarchiser la prospection**, pas à établir un devis.

| Profil de client | Stations | kWh cumac | CEE net / an | Marge / an | Marge par RDV | Dossiers pour ${euro(objectif)} |
|---|---:|---:|---:|---:|---:|---:|`);
    for (const l of lignes) {
      const d = dossiersPourObjectif(l, objectif);
      console.log(`| ${l.nom} | ${l.stations} | ${nb(l.kwhCumac)} | ${euro(l.ceeNet)} | ${euro(l.margeAnnuelle)} | ${euro(l.margeParRendezVous)} | ${d ?? 'jamais'} |`);
    }
    console.log(`
**Lecture.** « Marge par RDV » rapporte la marge annuelle au nombre de rendez-vous
typiques avant signature. C'est cet indicateur qui doit dicter l'ordre de prospection :
un profil très rémunérateur mais qui demande six rendez-vous vaut moins, à temps
commercial constant, qu'un profil moyen qui se signe en une visite.

**Ce que dit le tableau :**
${lignes.slice(0, 3).map((l, i) => `${i + 1}. **${l.nom}** — ${l.note}`).join('\n')}

Le type C seul ne couvre pas son entretien dans ces hypothèses : il ne se vend qu'en
complément d'un contrat existant. Le type A reste le mieux valorisé à la station, mais
le cycle de décision en efface une partie de l'avantage tant qu'il n'y a pas de référence
à montrer.`);
    return;
  }

  console.log(`Hypothèses : ${hypotheses.prixBrutEurMWhc} €/MWhc brut, ${hypotheses.margeDelegatairePct} % de marge délégataire, `
    + `${euro(hypotheses.coutEntretienAnnuelParStation)} d'entretien/an, ${euro(hypotheses.coutInstallationParStation)} d'installation.\n`);
  for (const l of lignes) {
    console.log(`${l.nom.padEnd(44)} ${nb(l.kwhCumac).padStart(11)} kWhc  ${euro(l.ceeNet).padStart(11)} net  `
      + `${euro(l.margeAnnuelle).padStart(11)} marge  ${euro(l.margeParRendezVous).padStart(9)} / RDV`);
  }
}

if (import.meta.url === `file://${process.argv[1]}`) principal();
