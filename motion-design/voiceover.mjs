// Génère la voix off avec ElevenLabs et la mixe dans la vidéo.
// usage : [ELEVENLABS_API_KEY=...] node voiceover.mjs noxem.mp4 noxem-voix.mp4 [musique.mp3]
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { execFileSync } from 'node:child_process';

const [video = 'noxem.mp4', out = 'noxem-voix.mp4', music] = process.argv.slice(2);
const key = process.env.ELEVENLABS_API_KEY;
// sans variable, la clé peut être ajoutée par le proxy de l'environnement (API credentials)
if (!key) console.warn('ELEVENLABS_API_KEY absente : on compte sur la clé ajoutée par le proxy');
const cfg = JSON.parse(readFileSync(new URL('./voiceover.json', import.meta.url)));
const voice = process.env.ELEVENLABS_VOICE_ID || cfg.voice_id;
mkdirSync('vo', { recursive: true });

const dur = f => +execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f]).toString();

const inputs = [], filters = [];
for (const [i, s] of cfg.segments.entries()) {
  const res = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${voice}?output_format=mp3_44100_128`, {
    method: 'POST',
    headers: { ...(key ? { 'xi-api-key': key } : {}), 'Content-Type': 'application/json' },
    body: JSON.stringify({ text: s.text, model_id: cfg.model_id,
      voice_settings: { stability: 0.5, similarity_boost: 0.8, style: 0.2, use_speaker_boost: true } }),
  });
  if (!res.ok) { console.error(`Segment ${i} : ${res.status} ${await res.text()}`); process.exit(1); }
  const f = `vo/seg${i}.mp3`;
  writeFileSync(f, Buffer.from(await res.arrayBuffer()));
  // accélère légèrement (max 15 %) si la phrase dépasse le créneau de sa scène
  const d = dur(f), slot = s.end - s.start, tempo = Math.min(1.15, Math.max(1, d / slot));
  console.log(`seg${i} ${d.toFixed(2)}s / créneau ${slot.toFixed(2)}s${tempo > 1 ? ` → x${tempo.toFixed(2)}` : ''}`);
  if (d / slot > 1.15) console.warn(`  ⚠ seg${i} trop long même accéléré : raccourcir le texte`);
  inputs.push('-i', f);
  filters.push(`[${i + 1}:a]aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo,atempo=${tempo.toFixed(3)},adelay=${Math.round(s.start * 1000)}:all=1[v${i}]`);
}
const n = cfg.segments.length, total = dur(video);
// piste silencieuse de la durée de la vidéo comme base du mixage
const bed = ['-f', 'lavfi', '-t', String(total), '-i', 'anullsrc=r=44100:cl=stereo'];
let mix = `${filters.join(';')};[${n + 1}:a]${cfg.segments.map((_, i) => `[v${i}]`).join('')}amix=inputs=${n + 1}:duration=first:normalize=0[vo]`;
const extra = [...bed];
if (music) {
  extra.push('-i', music);
  // musique baissée sous la voix (ducking) + fondu de fin
  mix += `;[vo]asplit=2[vo1][vo2];[${n + 2}:a]aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo,volume=0.35,afade=t=out:st=${total - 3}:d=3,apad[mu];[mu][vo1]sidechaincompress=threshold=0.03:ratio=8:release=400[duck];[vo2][duck]amix=inputs=2:duration=first:normalize=0[a]`;
} else mix += ';[vo]anull[a]';
execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-i', video, ...inputs, ...extra, '-filter_complex', mix,
  '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-t', String(total), '-movflags', '+faststart', out], { stdio: 'inherit' });
console.log('OK →', out);
