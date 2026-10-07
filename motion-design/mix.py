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
VOICE = 'audio/voix.mp3'

# (début dans le fichier voix, fin dans le fichier voix, position dans la vidéo)
VOICE_CUTS = [
    (0.00, 2.25, 1.0),     # NOXEM GROUP déménage son entrepôt.
    (2.49, 10.58, 6.8),    # Et liquide tout son stock ... prêtes à charger.
    (10.83, 15.31, 15.0),  # Au total : plus de huit mille deux cents m² ...
    (15.53, 25.37, 23.9),  # Float Low-E ... Prix sur devis.
    (25.61, 32.16, 34.7),  # Tout est manipulé chez nous ...
    (32.34, 39.28, 45.5),  # Livraison en camion inloader ...
    (39.52, 43.73, 53.7),  # Une question, une offre ? ... NOXEM GROUP.
]

# instants des animations (voir SC / R dans index.html)
CUTS = [6.5, 14, 23.5, 34, 45, 53]
SFX = (
    [('whoosh', c - 0.45) for c in CUTS]
    + [('tap', 0.3 + i * 0.14 + 0.45) for i in range(4)]          # pièces du logo
    + [('click', 2.2), ('click', 2.55)]                             # barres du logo
    + [('pop', 6.5 + 2.6 + i * 0.22 + 0.1) for i in range(3)]       # étiquettes
    + [('ding', 14 + 0.7 + i * 0.55 + 1.6) for i in range(4)]       # compteurs
    + [('click', 23.5 + 1.2 + i * 0.32 + 0.1) for i in range(6)]    # lignes du stock
    + [('pop', 34 + 1.3 + i * 1.6 + 0.15) for i in range(4)]        # étapes
    + [('click', 45 + 1.8 + i * 0.55 + 0.3) for i in range(4)]      # coches
    + [('tap', 53 + 0.1 + i * 0.14 + 0.45) for i in range(4)]       # logo final
    + [('pop', 53 + 1.9 + 0.25)]                                    # bouton WhatsApp
)


def decode(path):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).astype(np.float64)


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


def place(track, clip, at):
    i = int(at * SR)
    j = min(len(track), i + len(clip))
    if j > i:
        track[i:j] += clip[:j - i]


def main():
    video, out = sys.argv[1], sys.argv[2]
    music = sys.argv[3] if len(sys.argv) > 3 else None
    n = int(DUR * SR)

    voice = np.zeros(n)
    v = decode(VOICE)
    for a, b, at in VOICE_CUTS:
        seg = v[int(a * SR):int(b * SR)].copy()
        fade = int(0.02 * SR)
        seg[:fade] *= np.linspace(0, 1, fade); seg[-fade:] *= np.linspace(1, 0, fade)
        place(voice, seg, at)
    voice /= max(1e-9, np.abs(voice).max())

    sfx = np.zeros(n)
    gen = {'whoosh': whoosh, 'pop': pop, 'tap': tap, 'click': click, 'ding': ding}
    for kind, at in SFX:
        place(sfx, gen[kind](), at)

    mix = voice * 0.9 + sfx * 0.45
    if music:
        m = decode(music)[:n]
        m = np.pad(m, (0, n - len(m)))
        m /= max(1e-9, np.abs(m).max())
        # baisse la musique quand la voix parle (enveloppe lissée de la voix)
        k = int(0.25 * SR)
        e = np.convolve(np.abs(voice), np.ones(k) / k, mode='same')
        duck = 1 - 0.65 * np.clip(e / 0.05, 0, 1)
        fade_in = np.clip(np.arange(n) / (0.5 * SR), 0, 1)
        fade_out = np.clip((n - np.arange(n)) / (3 * SR), 0, 1)
        mix += m * 0.35 * duck * fade_in * fade_out
    mix /= max(1.0, np.abs(mix).max() / 0.95)

    pcm = (mix * 32767).astype('<i2')
    stereo = np.repeat(pcm[:, None], 2, axis=1)
    with wave.open('audio/mix.wav', 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(stereo.tobytes())

    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', video, '-i', 'audio/mix.wav',
                    '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-ar', '48000',
                    '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
                    '-shortest', '-movflags', '+faststart', out], check=True)
    print('OK ->', out)


if __name__ == '__main__':
    main()
