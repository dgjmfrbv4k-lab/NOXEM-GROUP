/**
 * verifier-mx.mjs
 * ---------------------------------------------------------------------------
 * Vérifie, sans envoyer un seul message, que les domaines d'une liste
 * acceptent bien du courrier.
 *
 * Un domaine sans enregistrement MX ne reçoit rien : chaque adresse qui s'y
 * trouve est un rebond dur garanti. C'est la seule vérification de masse
 * possible à froid, et elle coûte une requête DNS par domaine, pas un envoi.
 *
 * Elle ne dit pas qu'une boîte existe — seulement que le domaine peut en
 * héberger. C'est un plancher, pas une garantie.
 *
 *   node outils/verifier-mx.mjs adresses.txt --sortie adresses-vivantes.txt
 * ---------------------------------------------------------------------------
 */

import { promises as dns } from 'node:dns';
import { readFileSync, writeFileSync } from 'node:fs';

/** Un domaine accepte-t-il du courrier ? */
export async function aDuCourrier(domaine, resolveur = dns) {
  try {
    const mx = await resolveur.resolveMx(domaine);
    return mx.length > 0 && mx.some((m) => m.exchange && m.exchange !== '.');
  } catch (e) {
    // NXDOMAIN : le domaine n'existe plus. NODATA : pas de MX publié.
    // Certains domaines acceptent le courrier sur leur A à défaut de MX ;
    // c'est rare et déconseillé, mais on ne veut pas écarter à tort.
    if (e.code === 'ENOTFOUND' || e.code === 'ENODATA') {
      try {
        const a = await resolveur.resolve4(domaine);
        return a.length > 0;
      } catch (e2) {
        return false;
      }
    }
    return false; // SERVFAIL, timeout : on ne prend pas le risque
  }
}

/**
 * Vérifie un lot de domaines, avec une concurrence bornée pour ne pas
 * saturer le résolveur.
 */
export async function verifierDomaines(domaines, { concurrence = 40, surAvancement = () => {}, resolveur = dns } = {}) {
  const resultats = new Map();
  const file = [...domaines];
  let faits = 0;

  const ouvrier = async () => {
    for (;;) {
      const domaine = file.shift();
      if (!domaine) return;
      resultats.set(domaine, await aDuCourrier(domaine, resolveur));
      faits += 1;
      if (faits % 200 === 0) surAvancement({ faits, total: domaines.length });
    }
  };

  await Promise.all(Array.from({ length: Math.min(concurrence, domaines.length) }, ouvrier));
  return resultats;
}

/** Ne garde que les adresses dont le domaine accepte du courrier. */
export function filtrer(adresses, vivants) {
  return adresses.filter((e) => vivants.get(e.split('@')[1]) === true);
}

async function principal() {
  const args = process.argv.slice(2);
  const fichier = args[0];
  if (!fichier) {
    console.error('Usage : node outils/verifier-mx.mjs adresses.txt [--sortie vivantes.txt]');
    process.exit(1);
  }
  const i = args.indexOf('--sortie');
  const sortie = i !== -1 ? args[i + 1] : '';

  const adresses = readFileSync(fichier, 'utf8').split(/\r?\n/).map((l) => l.trim()).filter((l) => l.includes('@'));
  const domaines = [...new Set(adresses.map((e) => e.split('@')[1]))];
  console.log(`${adresses.length} adresse(s), ${domaines.length} domaine(s) à interroger…`);

  const vivants = await verifierDomaines(domaines, {
    surAvancement: ({ faits, total }) => console.log(`  ${faits}/${total} domaines vérifiés`),
  });

  const morts = [...vivants.entries()].filter(([, ok]) => !ok).map(([d]) => d);
  const gardees = filtrer(adresses, vivants);

  console.log(`\n${morts.length} domaine(s) ne reçoivent aucun courrier (${(100 * morts.length / domaines.length).toFixed(1)} %).`);
  console.log(`${adresses.length - gardees.length} adresse(s) écartée(s) : rebond dur garanti.`);
  console.log(`${gardees.length} adresse(s) conservée(s) (${(100 * gardees.length / adresses.length).toFixed(1)} %).`);
  if (morts.length) console.log(`\nExemples de domaines morts : ${morts.slice(0, 8).join(', ')}`);

  if (sortie) {
    writeFileSync(sortie, gardees.join('\n'));
    console.log(`\nÉcrit dans ${sortie}`);
  }
}

if (import.meta.url === `file://${process.argv[1]}`) {
  principal().catch((e) => { console.error(e.message); process.exit(1); });
}
