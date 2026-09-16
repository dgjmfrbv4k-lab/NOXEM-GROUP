/**
 * build-banniere.mjs — exporte les visuels SVG en PNG pour les e-mails.
 *
 * Les clients de messagerie ne rendent pas le SVG : il faut un PNG.
 * Deux sorties :
 *   - illustration-borne.png : le visuel seul, utilisé dans l'en-tête HTML
 *     (le texte, lui, reste en HTML pour rester lisible si les images sont
 *     bloquées — cas fréquent en prospection à froid) ;
 *   - banniere-gonflage.png : le bandeau complet, pour les supports où le
 *     texte peut être dans l'image (plaquette, présentation, réseaux).
 *
 *   node emails/build-banniere.mjs
 */
import { readFileSync, writeFileSync } from 'node:fs';
import { chromium } from 'playwright-core';

const SORTIES = [
  { svg: 'illustration-borne.svg', png: 'illustration-borne.png', largeur: 200, hauteur: 150, echelle: 1.5 },
  { svg: 'banniere-gonflage.svg', png: 'banniere-gonflage.png', largeur: 620, hauteur: 200, echelle: 2 },
];

const navigateur = await chromium.launch({
  executablePath: process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
});

for (const sortie of SORTIES) {
  const svg = readFileSync(new URL(`./${sortie.svg}`, import.meta.url), 'utf8');
  const page = await navigateur.newPage({
    viewport: { width: sortie.largeur, height: sortie.hauteur },
    deviceScaleFactor: sortie.echelle,
  });
  // Fond transparent : l'illustration est posée sur le bleu nuit de l'e-mail.
  await page.setContent(`<body style="margin:0">${svg}</body>`);
  const png = await page.screenshot({
    clip: { x: 0, y: 0, width: sortie.largeur, height: sortie.hauteur },
    omitBackground: sortie.svg.startsWith('illustration'),
  });
  writeFileSync(new URL(`./${sortie.png}`, import.meta.url), png);
  console.log(`${sortie.png} : ${sortie.largeur * sortie.echelle}x${sortie.hauteur * sortie.echelle}, ${(png.length / 1024).toFixed(1)} Ko`);
  await page.close();
}

await navigateur.close();
