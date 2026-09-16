/**
 * build-email.mjs — remplit le gabarit HTML avec les variables d'une fiche site.
 *
 *   node emails/build-email.mjs --nom "Intermarché X" --prenom Claire > sortie.html
 *
 * Sans argument, produit la version de démonstration utilisée pour les tests
 * d'affichage dans les différents clients de messagerie.
 */
import { readFileSync } from 'node:fs';

const args = process.argv.slice(2);
const lire = (cle, defaut) => {
  const i = args.indexOf(`--${cle}`);
  return i !== -1 && args[i + 1] ? args[i + 1] : defaut;
};

export const VALEURS_DEMO = {
  '[Prénom]': lire('prenom', 'Claire'),
  '[nom du site]': lire('nom', 'Intermarché Vaulx-en-Velin'),
  '[Votre nom]': lire('signataire', 'Aaron Harfi'),
  '[Votre société]': lire('societe', 'Noxem Group'),
  '[Votre téléphone]': lire('telephone', '06 00 00 00 00'),
  '[Votre email]': lire('email', 'harfiaaron@icloud.com'),
};

export function construire(valeurs = VALEURS_DEMO, srcImage = 'illustration-borne.png') {
  let html = readFileSync(new URL('./email-gonflage.html', import.meta.url), 'utf8');
  html = html.replace('src="illustration-borne.png"', `src="${srcImage}"`);
  for (const [variable, valeur] of Object.entries(valeurs)) {
    html = html.split(variable).join(valeur);
  }
  return html;
}

/** Version texte brut, envoyée en alternative au HTML (clients sans images). */
export function versionTexte(valeurs = VALEURS_DEMO) {
  return `Bonjour ${valeurs['[Prénom]']},

Je me permets de vous contacter au sujet de votre parking ${valeurs['[nom du site]']}.

Le dispositif des Certificats d'Économies d'Énergie (CEE), encadré par l'État, permet de financer une station de gonflage des pneus en libre accès pour vos clients, ainsi que son entretien (fiche officielle TRA-SE-104).

Pour vous, c'est :
- un service gratuit et visible pour vos clients ;
- une station entretenue et réparée sous 15 jours en cas de panne ;
- un coût en grande partie couvert par la prime CEE.

Seule condition : que le gonflage reste gratuit pour les usagers.

Auriez-vous 15 minutes cette semaine pour que je vous présente le fonctionnement et une estimation pour votre site ?

Bien cordialement,

${valeurs['[Votre nom]']}
${valeurs['[Votre société]']}
${valeurs['[Votre téléphone]']} · ${valeurs['[Votre email]']}

--
Montants indicatifs, confirmés avec le délégataire CEE avant signature.
Pour ne plus être contacté, répondez « STOP » à ce message.`;
}

if (import.meta.url === `file://${process.argv[1]}`) {
  process.stdout.write(construire());
}
