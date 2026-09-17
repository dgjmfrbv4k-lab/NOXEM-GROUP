/* =========================================================
   NOXEM GROUP FRANCE — générateur des pages par langue
   Usage :  node build.mjs
   Produit : /en/ /fr/ /ar/ /es/ /tr/ /pl/ /hr/ /nl/
             sitemap.xml et robots.txt
   Chaque page est entièrement traduite dans le HTML lui-même,
   pour que Google indexe chaque langue séparément.
   ========================================================= */

import { readFileSync, writeFileSync, mkdirSync } from "node:fs";

/* Adresse publique du site — à changer le jour d'un nom de domaine. */
const SITE = "https://dgjmfrbv4k-lab.github.io/NOXEM-GROUP";

globalThis.window = {};
new Function(readFileSync("i18n.js", "utf8"))();
const T = globalThis.window.NOXEM_I18N;
const LANGS = Object.keys(T);

const src = readFileSync("index.html", "utf8");

const esc = (t) => String(t).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
const escAttr = (t) => esc(t).replace(/"/g, "&quot;");

function translate(html, lang) {
  const d = T[lang];

  // contenu des éléments porteurs de data-i18n
  html = html.replace(
    /(<([a-zA-Z0-9]+)\b[^>]*\bdata-i18n="([^"]+)"[^>]*>)([\s\S]*?)(<\/\2>)/g,
    (m, open, tag, key, inner, close) =>
      typeof d[key] === "string" ? open + esc(d[key]) + close : m
  );

  // attributs de la page
  html = html.replace('<html lang="en" dir="ltr">', `<html lang="${lang}" dir="${d._dir}">`);
  html = html.replace(/<title>[\s\S]*?<\/title>/, `<title>${esc(d.meta_title)}</title>`);
  html = html.replace(/<meta name="description" content="[^"]*">/, `<meta name="description" content="${escAttr(d.meta_desc)}">`);
  html = html.replace(/<meta property="og:title" content="[^"]*">/, `<meta property="og:title" content="${escAttr(d.meta_title)}">`);
  html = html.replace(/<meta property="og:description" content="[^"]*">/, `<meta property="og:description" content="${escAttr(d.meta_desc)}">`);
  html = html.replace(/<meta property="og:locale" content="[^"]*">/, `<meta property="og:locale" content="${lang}">`);
  html = html.replace(/<meta name="twitter:title" content="[^"]*">/, `<meta name="twitter:title" content="${escAttr(d.meta_title)}">`);
  html = html.replace(/<meta name="twitter:description" content="[^"]*">/, `<meta name="twitter:description" content="${escAttr(d.meta_desc)}">`);
  html = html.replace(/<link rel="canonical" href="[^"]*">/, `<link rel="canonical" href="${SITE}/${lang}/">`);
  html = html.replace(/<meta property="og:url" content="[^"]*">/, `<meta property="og:url" content="${SITE}/${lang}/">`);

  // bandeau défilant : traduit en dur pour les robots
  html = html.replace(
    /(<div class="marquee__track" id="marquee-track">)[\s\S]*?(<\/div>)/,
    (m, open, close) => open + d.mq.map((t) => `<span>${esc(t)}</span><i>◆</i>`).join("") + close
  );

  // langue courante affichée sur le bouton
  html = html.replace(/(<span id="lang-current">)[^<]*(<\/span>)/, `$1${esc(d._name)}$2`);
  html = html.replace(/(<button type="button" role="option" data-lang="([a-z]{2})")/g,
    (m, start, code) => `${start} aria-selected="${code === lang ? "true" : "false"}"`);

  // pages légales : version française pour /fr/, version anglaise ailleurs
  const LEGAL = lang === "fr"
    ? { "legal-notice.html": "mentions-legales.html",
        "privacy-policy.html": "politique-de-confidentialite.html",
        "terms-of-sale.html": "conditions-generales-de-vente.html" }
    : {};
  html = html.replace(/href="legal\/([a-z-]+\.html)"/g,
    (m, file) => `href="../legal/${LEGAL[file] || file}"`);

  // chemins relatifs : la page vit dans un sous-dossier
  html = html.replace(/(href|src)="(styles\.css|app\.js|i18n\.js|assets\/)/g, '$1="../$2');
  html = html.replace(/href="([a-z]{2})\/"/g, 'href="../$1/"');

  // langue imposée à l'exécution
  html = html.replace('<script src="i18n.js">', `<script>window.NOXEM_LANG=${JSON.stringify(lang)};</script>\n<script src="i18n.js">`);
  html = html.replace('<script src="../i18n.js">', `<script>window.NOXEM_LANG=${JSON.stringify(lang)};</script>\n<script src="../i18n.js">`);

  return html;
}

for (const lang of LANGS) {
  mkdirSync(lang, { recursive: true });
  writeFileSync(`${lang}/index.html`, translate(src, lang));
  console.log(`  ${lang}/index.html`);
}

/* ---------- sitemap ---------- */
const today = new Date().toISOString().slice(0, 10);
const alts = (u) =>
  [`    <xhtml:link rel="alternate" hreflang="x-default" href="${SITE}/"/>`]
    .concat(LANGS.map((l) => `    <xhtml:link rel="alternate" hreflang="${l}" href="${SITE}/${l}/"/>`))
    .join("\n");

const LEGAL_PAGES = [
  "legal/mentions-legales.html", "legal/legal-notice.html",
  "legal/politique-de-confidentialite.html", "legal/privacy-policy.html",
  "legal/conditions-generales-de-vente.html", "legal/terms-of-sale.html",
];
const urls = [`${SITE}/`]
  .concat(LANGS.map((l) => `${SITE}/${l}/`))
  .concat(LEGAL_PAGES.map((f) => `${SITE}/${f}`));
writeFileSync(
  "sitemap.xml",
  `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">
${urls
  .map(
    (u) => `  <url>
    <loc>${u}</loc>
    <lastmod>${today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>${u === SITE + "/" ? "1.0" : "0.9"}</priority>
${u.includes("/legal/") ? "" : alts(u)}
  </url>`
  )
  .join("\n")}
</urlset>
`
);
console.log("  sitemap.xml");

/* ---------- robots ---------- */
writeFileSync(
  "robots.txt",
  `User-agent: *
Allow: /

Sitemap: ${SITE}/sitemap.xml
`
);
console.log("  robots.txt");
console.log(`\n${LANGS.length} langues générées pour ${SITE}`);
