/**
 * build-banniere.mjs — exporte les visuels SVG en PNG pour les e-mails.
 *
 *   npm i playwright-core   (une seule fois)
 *   node emails/build-banniere.mjs
 *
 * Deux jeux de sorties :
 *
 *  - les visuels « e-mail » (email-borne.png, email-scene.png) : rendus en
 *    DOUBLE résolution puis affichés à taille moitié, sur fond bleu nuit opaque,
 *    avec des traits épaissis et une seule teinte de cyan. C'est ce qui donne un
 *    rendu net sur écran haute densité tout en gardant un fichier léger : un
 *    trait fin rendu sur un demi-pixel paraît systématiquement flou, et les
 *    dégradés d'anti-crénelage sur fond transparent alourdissent le PNG ;
 *
 *  - la bannière complète (banniere-gonflage.png), pour la plaquette et les
 *    supports où le texte peut être dans l'image.
 */
import { readFileSync, writeFileSync } from 'node:fs';
import { chromium } from 'playwright-core';

const CHEMIN = (f) => new URL(`./${f}`, import.meta.url);

/**
 * Prépare la variante « e-mail » d'un visuel : fond opaque, teinte unique,
 * traits épaissis de 35 %.
 *
 * Le rectangle de fond est dimensionné dans le repère du dessin (viewBox) et
 * non dans la taille d'affichage : sinon il ne couvre qu'une partie du cadre.
 */
export function varianteEmail(svg, fond = '#0f2942') {
  const s = svg
    .replace(/#7fd9e1/gi, '#00a9b7')
    .replace(/#1d4a73/gi, '#24567f')
    .replace(/#1f5876/gi, '#24567f')
    .replace(/stroke-width="([\d.]+)"/g, (_, v) => `stroke-width="${Math.round(Number(v) * 1.35 * 10) / 10}"`);

  const viewBox = s.match(/viewBox="([\d.\s-]+)"/);
  if (!viewBox) throw new Error('viewBox absent du SVG : impossible de poser le fond.');
  const [, , largeurDessin, hauteurDessin] = viewBox[1].trim().split(/\s+/).map(Number);

  const i = s.indexOf('>', s.indexOf('<svg')) + 1;
  // Le fond déborde d'un point de chaque côté : sinon l'anti-crénelage laisse
  // un liseré clair d'un pixel sur le bord de l'image.
  return `${s.slice(0, i)}\n  <rect x="-1" y="-1" width="${largeurDessin + 2}" height="${hauteurDessin + 2}" fill="${fond}"/>${s.slice(i)}`;
}

const SORTIES = [
  { svg: 'illustration-borne.svg', png: 'email-borne.png', largeur: 150, hauteur: 113, echelle: 2, email: true },
  { svg: 'scene-parking.svg', png: 'email-scene.png', largeur: 240, hauteur: 69, echelle: 2, email: true },
  { svg: 'banniere-gonflage.svg', png: 'banniere-gonflage.png', largeur: 620, hauteur: 200, echelle: 2 },
];

const navigateur = await chromium.launch({
  executablePath: process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
});

for (const s of SORTIES) {
  const source = readFileSync(CHEMIN(s.svg), 'utf8');
  const svg = s.email ? varianteEmail(source) : source;
  const dimensionne = svg.replace(/width="\d+" height="\d+"/, `width="${s.largeur}" height="${s.hauteur}"`);

  const page = await navigateur.newPage({
    viewport: { width: s.largeur, height: s.hauteur },
    deviceScaleFactor: s.echelle,
  });
  await page.setContent(`<body style="margin:0"><div style="width:${s.largeur}px">${dimensionne}</div></body>`);
  const png = await page.screenshot({ clip: { x: 0, y: 0, width: s.largeur, height: s.hauteur } });
  writeFileSync(CHEMIN(s.png), png);
  console.log(`${s.png} : ${s.largeur * s.echelle}x${s.hauteur * s.echelle} px affichés en ${s.largeur} px — ${(png.length / 1024).toFixed(1)} Ko`);
  await page.close();
}

await navigateur.close();
