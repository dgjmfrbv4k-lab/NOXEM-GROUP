// Enregistre index.html image par image (seek(t)) et l'encode en MP4 avec la musique.
//   node motion/piwa-showcase/render.mjs sortie.mp4 [musique.wav]
//   node motion/piwa-showcase/render.mjs --preview dossier 1.5,5,9
import { spawn } from "node:child_process";
import { mkdirSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { createRequire } from "node:module";
import { execSync } from "node:child_process";

// playwright est installé globalement sur la machine de rendu
const require = createRequire(import.meta.url);
let chromium;
try { ({ chromium } = require("playwright")); }
catch { ({ chromium } = require(join(execSync("npm root -g").toString().trim(), "playwright"))); }

const HERE = dirname(fileURLToPath(import.meta.url));
const FPS = 30;
const args = process.argv.slice(2);

const browser = await chromium.launch({ args: ["--disable-web-security"] });
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
await page.goto(pathToFileURL(join(HERE, "index.html")).href);
await page.evaluate(() => document.fonts.ready);
await page.waitForFunction(() => [...document.images].every((i) => i.complete));
const duration = await page.evaluate(() => window.TIMELINE.DURATION);

async function frame(t) {
  await page.evaluate((tt) => window.seek(tt), t);
  return page.screenshot({ type: "jpeg", quality: 94 });
}

if (args[0] === "--preview") {
  mkdirSync(args[1], { recursive: true });
  for (const t of args[2].split(",").map(Number)) {
    await page.evaluate((tt) => window.seek(tt), t);
    await page.screenshot({ path: join(args[1], `frame_${t.toFixed(1).padStart(5, "0")}.jpg`), type: "jpeg", quality: 90 });
  }
} else {
  const out = resolve(args[0]);
  const music = args[1] ? ["-i", resolve(args[1])] : [];
  const ff = spawn("ffmpeg", ["-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", String(FPS), "-i", "-", ...music,
    "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p",
    ...(music.length ? ["-c:a", "aac", "-b:a", "192k", "-shortest"] : []), "-movflags", "+faststart", out],
    { stdio: ["pipe", "inherit", "inherit"] });
  const total = Math.round(duration * FPS);
  for (let i = 0; i < total; i++) {
    const buf = await frame(i / FPS);
    if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once("drain", r));
    if (i % 150 === 0) console.log(`${i}/${total}`);
  }
  ff.stdin.end();
  await new Promise((r) => ff.on("close", r));
}
await browser.close();
