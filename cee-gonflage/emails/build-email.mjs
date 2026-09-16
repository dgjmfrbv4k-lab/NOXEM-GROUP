/**
 * build-email.mjs — remplit le gabarit HTML avec les variables d'une fiche site.
 *
 *   node emails/build-email.mjs --nom "Carrefour Bron" --prenom Sophie > sortie.html
 *
 * Sans argument, produit la version de démonstration servant aux tests
 * d'affichage dans les différents clients de messagerie.
 */
import { readFileSync } from 'node:fs';

const args = process.argv.slice(2);
const lire = (cle, defaut) => {
  const i = args.indexOf(`--${cle}`);
  return i !== -1 && args[i + 1] ? args[i + 1] : defaut;
};

/** Signature Noxem Group (valeurs réelles, surchargeables en ligne de commande). */
export const SIGNATURE = {
  '[Votre nom]': lire('signataire', 'Aaron Harfi'),
  '[Votre fonction]': lire('fonction', 'Président'),
  '[Votre société]': lire('societe', 'NOXEM GROUP'),
  '[Votre téléphone]': lire('telephone', '02 59 50 84 59'),
  '[Votre email]': lire('email', 'aaron.harfi@noxemgroup.com'),
  '[Votre adresse]': lire('adresse', '5 chemin du Jubin – 69570 Dardilly'),
};

/**
 * Valeurs par défaut : version GÉNÉRIQUE, envoyable telle quelle à n'importe
 * quel établissement. Les options --prenom et --nom produisent la version
 * personnalisée, qui obtient de bien meilleurs taux de réponse quand le nom
 * du contact et celui du site sont connus (fiche CRM renseignée).
 */
export const VALEURS_GENERIQUES = {
  '[Prénom]': 'Madame, Monsieur',
  '[nom du site]': 'votre établissement',
  ...SIGNATURE,
};

/**
 * Lien du bouton « Réserver 15 minutes ».
 * Tant qu'aucun agenda en ligne n'est branché (Calendly, plages de rendez-vous
 * Google Agenda...), on retombe sur un message pré-rempli : le prospect envoie
 * ses disponibilités en un clic. Passer --rdv <url> pour brancher l'agenda.
 */
export function lienReservation(valeurs = SIGNATURE) {
  const url = lire('rdv', '');
  if (url) return url;
  const objet = encodeURIComponent('Réservation d\u2019un créneau de 15 minutes');
  const corps = encodeURIComponent(
    'Bonjour,\n\nJe souhaite réserver un créneau de 15 minutes au sujet de la station de gonflage.\n\n'
    + 'Mes disponibilités :\n- \n- \n\nÉtablissement :\nVille :\nTéléphone :\n',
  );
  return `mailto:${valeurs['[Votre email]']}?subject=${objet}&body=${corps}`;
}

export const VALEURS_DEMO = {
  '[Prénom]': lire('prenom', VALEURS_GENERIQUES['[Prénom]']),
  '[nom du site]': lire('nom', VALEURS_GENERIQUES['[nom du site]']),
  ...SIGNATURE,
};

export function construire(valeurs = VALEURS_DEMO) {
  let html = readFileSync(new URL('./email-gonflage.html', import.meta.url), 'utf8');
  // Le lien « tel: » ne doit pas contenir d'espaces.
  html = html.split('[Votre téléphone sans espaces]')
    .join((valeurs['[Votre téléphone]'] || '').replace(/[^0-9+]/g, ''));
  html = html.split('[lien de réservation]').join(lienReservation(valeurs));
  for (const [variable, valeur] of Object.entries(valeurs)) {
    html = html.split(variable).join(valeur);
  }
  return html;
}

/** Version texte brut, envoyée en alternative au HTML (clients sans images ni styles). */
export function versionTexte(valeurs = VALEURS_DEMO) {
  return `Bonjour ${valeurs['[Prénom]']},

1 véhicule sur 3 roule aujourd'hui avec des pneus mal gonflés. Vos clients peuvent y remédier sur votre parking, gratuitement - et l'État en finance l'essentiel.

Je me permets de vous contacter au sujet du parking de ${valeurs['[nom du site]']}.

Le dispositif des Certificats d'Économies d'Énergie, encadré par l'État, permet de financer en grande partie l'installation d'une station de gonflage en libre accès sur votre parking, ainsi que son entretien (fiche officielle TRA-SE-104).

- Un service visible et gratuit pour vos clients, sur votre parking
- Entretien assuré par un professionnel, pièces défectueuses remplacées sous 15 jours
- Aucune gestion de votre côté, aucun changement dans votre activité
- Aucun critère de surface, de chiffre d'affaires ni d'ancienneté

Une seule condition : que le gonflage reste gratuit pour les usagers. C'est la règle du dispositif, et c'est tout.

15 minutes suffisent pour que je vous présente le fonctionnement et le montant pris en charge pour ${valeurs['[nom du site]']}. Seriez-vous disponible cette semaine ou la suivante ?

Cordialement,

${valeurs['[Votre nom]']}
${valeurs['[Votre fonction]']} – ${valeurs['[Votre société]']}

Tél. : ${valeurs['[Votre téléphone]']}
E-mail : ${valeurs['[Votre email]']}
Adresse : ${valeurs['[Votre adresse]']}

--
Sources : ADEME (véhicules mal gonflés), Michelin (surconsommation liée au sous-gonflage).
Montants indicatifs, confirmés avec le délégataire CEE avant signature.
Pour ne plus être contacté, répondez « STOP » à ce message.`;
}

if (import.meta.url === `file://${process.argv[1]}`) {
  process.stdout.write(construire());
}
