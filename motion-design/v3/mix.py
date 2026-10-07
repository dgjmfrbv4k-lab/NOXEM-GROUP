"""Mixe la voix off ElevenLabs, les bruitages (générés ici) et une musique
optionnelle sur la vidéo.

usage : python3 mix.py noxem.mp4 noxem-final.mp4 [musique.mp3]

La voix off est un seul fichier (audio/voix.mp3) : on le découpe aux pauses
entre les phrases, puis chaque morceau est placé au début de sa scène.
"""
import subprocess, sys, wave
import numpy as np

SR = 44100
DUR = 60.0
VOICE = 'audio/voix.mp3'  # voix off de cette vidéo (à recevoir)

# (début dans le fichier voix, fin dans le fichier voix, position dans la vidéo)
# découpe aux pauses du fichier (ffmpeg silencedetect)
# (début dans le fichier voix, fin dans le fichier voix, position dans la vidéo)
VOICE_CUTS = [
    (0.00, 7.90, 0.50),    # NOXEM GROUP passe ... / Portes ... / On fabrique, on livre, on pose
    (7.90, 12.67, 8.50),   # Une porte moderne ? ... Voilà !
    (12.67, 18.85, 14.14), # fenêtres et baies ... volets, des dizaines de coloris
    (18.85, 21.76, 20.47), # Des dizaines de modèles ... sur mesure
    (21.76, 24.36, 23.46), # usines européennes
    (24.36, 25.15, 26.14), # Et la pose ?
    (26.74, 27.80, 28.52), # partout en France.  ("Ce sont nos propres artisans" retiré)
    (27.80, 31.55, 29.75), # Plus de lumière ... d'énergie
    (31.55, 36.55, 33.63), # Particuliers ou professionnels ...
    (36.55, 43.31, 38.88), # NOXEM GROUP. Très bientôt ... Appelez le ...
]

# instants des bruitages : exportés depuis index.html (node record.js sfx sfx.json)
import json, os
SFX = json.load(open('sfx.json')) if os.path.exists('sfx.json') else []


def decode(path, ch=1):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-f', 'f32le', '-ac', str(ch), '-ar', str(SR), '-'],
                         capture_output=True, check=True).stdout
    a = np.frombuffer(raw, dtype=np.float32).astype(np.float64)
    return a if ch == 1 else a.reshape(-1, ch)


def env(n, attack, decay):
    t = np.arange(n) / SR
    return np.minimum(1, t / max(attack, 1e-4)) * np.exp(-t / decay)


rng = np.random.default_rng(7)


def whoosh(d=0.9):
    n = int(d * SR)
    noise = rng.standard_normal(n)
    # passe-bas dont la fréquence monte puis redescend (souffle qui passe)
    t = np.linspace(0, 1, n)
    fc = 300 + 4200 * np.sin(np.pi * t) ** 2
    a = np.exp(-2 * np.pi * fc / SR)
    out = np.zeros(n); y = 0.0
    for i in range(n):
        y = (1 - a[i]) * noise[i] + a[i] * y
        out[i] = y
    return out / np.abs(out).max() * np.sin(np.pi * t) ** 1.5 * 0.5


def pop(d=0.09):
    n = int(d * SR); t = np.arange(n) / SR
    f = 260 + 700 * np.exp(-t / 0.012)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.002, 0.03) * 0.6


def tap(d=0.12):
    n = int(d * SR); t = np.arange(n) / SR
    body = np.sin(2 * np.pi * 180 * t) * env(n, 0.001, 0.035)
    return (body + 0.3 * rng.standard_normal(n) * env(n, 0.0005, 0.006)) * 0.5


def click(d=0.04):
    n = int(d * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * 2400 * t) * 0.6 + rng.standard_normal(n) * 0.4) * env(n, 0.0005, 0.006) * 0.35


def ding(d=0.7):
    n = int(d * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * 1320 * t) + 0.35 * np.sin(2 * np.pi * 1980 * t)) * env(n, 0.003, 0.18) * 0.18


def swish(d=0.35):
    return whoosh(d) * 0.6


def boom(d=0.6):
    n = int(d * SR); t = np.arange(n) / SR
    f = 45 + 70 * np.exp(-t / 0.05)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.002, 0.18)
    hit = rng.standard_normal(n) * env(n, 0.0005, 0.02) * 0.4
    return (body + hit) * 0.75


def shine(d=0.9):
    n = int(d * SR); t = np.arange(n) / SR
    out = sum(np.sin(2 * np.pi * f * t + p) for f, p in [(2093, 0), (2637, 1), (3136, 2), (4186, 3)])
    trem = 0.6 + 0.4 * np.sin(2 * np.pi * 14 * t)
    return out / 4 * trem * env(n, 0.05, 0.3) * 0.16


def draw(d=0.8):
    n = int(d * SR); t = np.arange(n) / SR
    return rng.standard_normal(n) * (0.5 + 0.5 * np.sin(2 * np.pi * 9 * t)) * env(n, 0.05, 0.5) * 0.06


def riser(d=2.0):
    n = int(d * SR); t = np.arange(n) / SR
    f = 200 + 900 * (t / d) ** 2
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.4 + rng.standard_normal(n) * 0.3
    return tone * (t / d) ** 2 * 0.25


def stamp(d=0.3):
    n = int(d * SR)
    return rng.standard_normal(n) * env(n, 0.001, 0.04) * 0.5


def drop(d=0.35):
    n = int(d * SR); t = np.arange(n) / SR
    f = 1400 * np.exp(-t / 0.08) + 200
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.002, 0.08) * 0.35


def truck(d=3.0):
    n = int(d * SR); t = np.arange(n) / SR
    eng = np.sin(2 * np.pi * 55 * t) + 0.5 * np.sin(2 * np.pi * 110 * t)
    road = rng.standard_normal(n) * 0.3
    pan = np.sin(np.pi * t / d)
    return (eng * 0.5 + road) * pan * 0.18


def type_(d=0.5):
    out = np.zeros(int(d * SR))
    for k in range(6):
        place(out, click() * 0.7, k * 0.075 + rng.random() * 0.02)
    return out


def place(track, clip, at):
    i = int(at * SR)
    j = min(len(track), i + len(clip))
    if j > i:
        track[i:j] += clip[:j - i]


def main():
    video, out = sys.argv[1], sys.argv[2]
    music = sys.argv[3] if len(sys.argv) > 3 else None
    dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', video], capture_output=True, text=True).stdout)
    n = int(dur * SR)

    voice = np.zeros(n)
    v = decode(VOICE) if VOICE_CUTS else np.zeros(1)
    for a, b, at in VOICE_CUTS:
        seg = v[int(a * SR):int(b * SR)].copy()
        fade = int(0.02 * SR)
        seg[:fade] *= np.linspace(0, 1, fade); seg[-fade:] *= np.linspace(1, 0, fade)
        place(voice, seg, at)
    voice /= max(1e-9, np.abs(voice).max())

    sfx = np.zeros(n)
    gen = {'whoosh': whoosh, 'swish': swish, 'pop': pop, 'tap': tap, 'click': click, 'ding': ding, 'boom': boom,
           'shine': shine, 'draw': draw, 'riser': riser, 'stamp': stamp, 'drop': drop, 'truck': truck, 'type': type_}
    for kind, at in SFX:
        place(sfx, gen[kind](), at)

    mix = np.repeat((voice * 0.9 + sfx * 0.45)[:, None], 2, axis=1)
    if music:
        m = decode(music, 2)[:n]
        m = np.pad(m, ((0, n - len(m)), (0, 0)))
        m /= max(1e-9, np.abs(m).max())
        # baisse la musique quand la voix parle (enveloppe lissée de la voix)
        k = int(0.25 * SR)
        e = np.convolve(np.abs(voice), np.ones(k) / k, mode='same')
        duck = 1 - 0.65 * np.clip(e / 0.05, 0, 1)
        fade_in = np.clip(np.arange(n) / (0.5 * SR), 0, 1)
        fade_out = np.clip((n - np.arange(n)) / (3 * SR), 0, 1)
        mix += m * (0.35 * duck * fade_in * fade_out)[:, None]
    mix /= max(1.0, np.abs(mix).max() / 0.95)

    pcm = (mix * 32767).astype('<i2')
    stereo = pcm
    with wave.open('audio/mix.wav', 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(stereo.tobytes())

    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', video, '-i', 'audio/mix.wav',
                    '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-ar', '48000',
                    '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
                    '-shortest', '-movflags', '+faststart', out], check=True)
    print('OK ->', out)


if __name__ == '__main__':
    main()
