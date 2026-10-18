"""PIWA Studio — « Paris, le lendemain » : montage motion design sur images réelles (1080x1920).

Reprend la vidéo source plan par plan, ajoute une voix off (Piper, voix française siwis),
des sous-titres mot à mot, des étiquettes de lieu, des effets sur chaque coupe et une fin PIWA.
    python3 motion/paris-lendemain/montage.py SOURCE.mp4 VOIX.onnx SORTIE.mp4 [--preview dossier t1,t2,...]
"""
import math
import random
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "france-17-octobre"))
import render as fx  # noqa: E402  (palette, polices, texte, logo, effets)

W, H, FPS = fx.W, fx.H, fx.FPS
FOOTAGE_END = 58.2  # la fin de la source est l'écran de fin TikTok, on la coupe
END_CARD = 6.0
DURATION = FOOTAGE_END + END_CARD
CREDIT = "Images : @popcornpariss (TikTok)"

# coupes de la source (détection de plans)
CUTS = [5.733, 7.067, 8.433, 10.167, 11.467, 13.133, 14.667, 15.9, 17.833, 19.433, 20.867, 22.367,
        23.833, 25.3, 26.967, 28.567, 30.033, 31.3, 32.733, 34.3, 35.6, 37.033, 38.467, 39.933, 42.1,
        43.367, 44.8, 46.2, 47.367, 48.733, 50.133, 51.467, 52.833, 54.333, 55.5, 56.9]

# (début, texte dit par la voix off)
SCRIPT = [
    (0.6, "Samedi, dix-sept octobre. Le lendemain matin, Paris se réveille comme ça."),
    (6.0, "Des vitrines explosées. Des rayons vidés."),
    (10.4, "Place Vendôme, aux Galeries Lafayette, on pose du bois sur ce qui reste."),
    (16.1, "Même la République est couverte de tags."),
    (22.6, "Des voitures calcinées. Des kiosques brûlés."),
    (28.0, "Mais dès l'aube, ils sont là. Ceux qui nettoient. Ceux qui réparent."),
    (35.8, "Derrière chaque vitrine, il y a quelqu'un. Un commerçant. Une équipe. Une famille."),
    (46.4, "Ils ont tout cassé. Sauf notre envie de nous relever."),
    (52.4, "Commerçants de France, on est avec vous."),
    (59.0, "Piwa Studio, à vos côtés pour rouvrir."),
]
# sous-titres affichés (même découpage que SCRIPT, orthographe d'écran)
CAPTIONS = [
    "Samedi 17 octobre. Le lendemain matin, Paris se réveille comme ça.",
    "Des vitrines explosées. Des rayons vidés.",
    "Place Vendôme, aux Galeries Lafayette, on pose du bois sur ce qui reste.",
    "Même la République est couverte de tags.",
    "Des voitures calcinées. Des kiosques brûlés.",
    "Mais dès l'aube, ils sont là. Ceux qui nettoient. Ceux qui réparent.",
    "Derrière chaque vitrine, il y a quelqu'un. Un commerçant. Une équipe. Une famille.",
    "Ils ont tout cassé. Sauf notre envie de nous relever.",
    "Commerçants de France, on est avec vous.",
    None,  # l'écran de fin porte le texte
]
PLACES = [
    (10.167, 11.467, "PLACE VENDÔME"),
    (11.467, 13.133, "GALERIES LAFAYETTE"),
    (15.9, 17.833, "PLACE DE LA RÉPUBLIQUE"),
    (17.833, 19.433, "OPÉRA GARNIER"),
    (22.367, 23.833, "PLACE DE LA RÉPUBLIQUE"),
]

F_CAP = fx.font("Black", 76)
F_PLACE = fx.font("Bold", 38)
F_CREDIT = fx.font("Medium", 28)


# ---------------------------------------------------------------- voix off
def make_voice(model, tmp):
    """Synthétise chaque phrase, renvoie [(début, durée, échantillons)] et la fréquence."""
    lines = []
    sr = None
    for i, (start, text) in enumerate(SCRIPT):
        out = Path(tmp) / f"v{i}.wav"
        subprocess.run([sys.executable, "-m", "piper", "-m", str(model), "-f", str(out),
                        "--length-scale", "0.92", "--sentence-silence", "0.12"],
                       input=text.encode(), check=True, capture_output=True)
        with wave.open(str(out)) as w:
            sr = w.getframerate()
            data = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64) / 32768
        lines.append((start, len(data) / sr, data))
    return lines, sr


def word_timings(caption, start, dur):
    """Répartit la durée de la phrase sur les mots, au prorata de leur longueur."""
    words = caption.split()
    weights = [len(w) + 2 + (4 if w[-1] in ".,!?" else 0) for w in words]
    total = sum(weights)
    out, t = [], start
    for w, k in zip(words, weights):
        d = dur * k / total
        out.append((w, t, t + d))
        t += d
    return out


def chunk(words, max_chars=22):
    """Groupe les mots en lignes de sous-titre courtes (une idée à l'écran à la fois)."""
    groups, cur = [], []
    for item in words:
        if cur and (sum(len(w[0]) + 1 for w in cur) + len(item[0]) > max_chars or cur[-1][0][-1] in ".!?"):
            groups.append(cur)
            cur = []
        cur.append(item)
    if cur:
        groups.append(cur)
    return groups


TIMED = []  # [(groupe de mots, début, fin)]


def build_captions(voice):
    TIMED.clear()
    for (start, dur, _), cap in zip(voice, CAPTIONS):
        if cap is None:
            continue
        groups = chunk(word_timings(cap, start, dur))
        for gi, g in enumerate(groups):
            end = groups[gi + 1][0][1] if gi + 1 < len(groups) else g[-1][2] + 0.35
            TIMED.append((g, g[0][1], end))


def draw_captions(img, t):
    for words, start, end in TIMED:
        if not start <= t < end:
            continue
        p = fx.ease_back(fx.prog(t, start, 0.18))
        # mise en page de la ligne : mot courant en dégradé, mots à venir en transparence
        widths = [F_CAP.getlength(w[0]) for w in words]
        space = F_CAP.getlength(" ")
        total = sum(widths) + space * (len(words) - 1)
        x = (W - total) / 2
        y = 1380 + (1 - p) * 40
        for (w, ws, _), wd in zip(words, widths):
            said = t >= ws
            for ox, oy in ((5, 6), (-2, 3), (3, -2)):  # ombre pour rester lisible sur les fonds clairs
                fx.draw_text(img, w, F_CAP, y + oy, 0.55 if said else 0.2, x=x + ox, anchor="left", color=fx.BG)
            fx.draw_text(img, w, F_CAP, y, 1.0 if said else 0.35, x=x, anchor="left",
                         gradient=said and t < ws + 0.35, color=fx.FG)
            x += wd + space


# ---------------------------------------------------------------- image source
class Footage:
    """Lit la source image par image, redimensionnée en 1080x1920."""

    def __init__(self, path, start=0.0):
        self.path = path
        self.proc = subprocess.Popen([
            "ffmpeg", "-loglevel", "error", "-ss", str(start), "-i", str(path), "-t", str(FOOTAGE_END - start),
            "-vf", f"fps={FPS},scale={W}:{H}:flags=lanczos", "-f", "rawvideo", "-pix_fmt", "rgb24", "-",
        ], stdout=subprocess.PIPE)
        self.last = None

    def next(self):
        raw = self.proc.stdout.read(W * H * 3)
        if len(raw) == W * H * 3:
            self.last = Image.frombytes("RGB", (W, H), raw)
        return self.last


def shot_bounds(t):
    prev = 0.0
    for c in CUTS:
        if t < c:
            return prev, c
        prev = c
    return prev, FOOTAGE_END


def grade(frame, t):
    s0, s1 = shot_bounds(t)
    z = 1.0 + 0.07 * fx.prog(t, s0, s1 - s0)  # léger zoom sur chaque plan
    if z > 1.001:
        zw, zh = int(W * z), int(H * z)
        frame = frame.resize((zw, zh), Image.BILINEAR).crop(((zw - W) // 2, (zh - H) // 2, (zw - W) // 2 + W, (zh - H) // 2 + H))
    frame = ImageEnhance.Contrast(ImageEnhance.Color(frame).enhance(0.85)).enhance(1.12)
    frame = Image.blend(frame, fx.GRADIENT_FULL, 0.07)
    return frame.convert("RGBA")


def make_shade():
    shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(shade)
    for y in range(0, 760, 4):
        a = int(215 * (y / 760) ** 1.6)
        d.rectangle((0, H - 760 + y, W, H - 760 + y + 4), fill=fx.BG + (a,))
    for y in range(0, 300, 4):
        d.rectangle((0, y, W, y + 4), fill=fx.BG + (int(150 * (1 - y / 300)),))
    return shade


SHADE = make_shade()
LOGO_BUG = fx.LOGO.resize((230, int(230 * fx.LOGO.height / fx.LOGO.width)), Image.LANCZOS)


# ---------------------------------------------------------------- couches motion design
def draw_place(img, t):
    for s, e, name in PLACES:
        if s <= t < e:
            a = fx.window(t, s, e, 0.15, 0.15)
            dx = (1 - fx.ease_out(fx.prog(t, s, 0.35))) * -60
            tw = F_PLACE.getlength(name) + 8 * len(name)
            d = ImageDraw.Draw(img)
            d.rounded_rectangle((60 + dx, 196, 60 + dx + tw + 90, 264), radius=34, fill=fx.BG + (int(190 * a),))
            d.ellipse((84 + dx, 218, 108 + dx, 242), fill=fx.PINK + (int(255 * a),))
            fx.draw_text(img, name, F_PLACE, 230, a, x=128 + dx, anchor="left", tracking=8)


def draw_hud(img, t):
    # barre de progression
    p = min(1.0, t / FOOTAGE_END)
    bar = fx.GRADIENT_FULL.crop((0, 0, max(1, int(W * p)), 8)).convert("RGBA")
    img.alpha_composite(bar, (0, 0))
    img.alpha_composite(fx.faded(LOGO_BUG, 0.9), (W - LOGO_BUG.width - 50, 60))
    fx.draw_text(img, CREDIT, F_CREDIT, H - 70, 0.75, color=fx.FG)


def draw_titles(img, t):
    # ouverture
    if t < 5.6:
        a = fx.window(t, 0.0, 5.4, 0.1, 0.4)
        img.alpha_composite(Image.new("RGBA", (W, H), fx.BG + (int(120 * a),)))
        fx.draw_text(img, "PARIS · 18 OCTOBRE", fx.F_TAG, 640, fx.window(t, 0.2, 5.4, 0.2, 0.4), tracking=10)
        fx.slam(img, "LE", fx.F_BIG, 790, t, 0.1, 5.4, tracking=-4)
        fx.slam(img, "LENDEMAIN.", fx.F_BIG, 950, t, 0.3, 5.4, gradient=True, tracking=-4)
    # climax
    if 54.3 <= t < FOOTAGE_END:
        a = fx.window(t, 54.3, FOOTAGE_END, 0.15, 0.2)
        img.alpha_composite(Image.new("RGBA", (W, H), fx.BG + (int(140 * a),)))
        fx.slam(img, "ON EST", fx.F_BIG, 760, t, 54.3, FOOTAGE_END)
        fx.slam(img, "AVEC VOUS.", fx.F_BIG, 920, t, 54.6, FOOTAGE_END, gradient=True)


def end_card(t):
    img = Image.new("RGBA", (W, H), fx.BG + (255,))
    fx.background(img, t)
    lt = t - FOOTAGE_END
    a = fx.ease_out(fx.prog(lt, 0.0, 0.5))
    fx.draw_map(img, 540, 1250, 520, fill_a=0.22 * a, line_a=0.6 * a, glow=a)
    img.alpha_composite(fx.faded(fx.LOGO, a), ((W - fx.LOGO.width) // 2, int(470 + (1 - a) * 60)))
    fx.draw_text(img, "soutient les commerçants de France", fx.F_S, 850, fx.ease_out(fx.prog(lt, 0.4, 0.4)))
    fx.draw_text(img, "Une vidéo pour votre réouverture ?", fx.F_M, 1620, fx.ease_out(fx.prog(lt, 1.0, 0.4)), gradient=True)
    fx.draw_text(img, "Écrivez-nous.", fx.F_M, 1700, fx.ease_out(fx.prog(lt, 1.2, 0.4)), gradient=True)
    fx.draw_text(img, "#SoutienAuxCommerçants  #PiwaStudio", fx.F_XS, 1790, fx.ease_out(fx.prog(lt, 1.6, 0.4)), color=fx.MUTE)
    fx.draw_text(img, CREDIT, F_CREDIT, H - 40, 0.6, color=fx.MUTE)
    img.alpha_composite(fx.VIGNETTE)
    return img


def cut_energy(t):
    e = 0.0
    for c in CUTS + [FOOTAGE_END]:
        if t >= c:
            e = max(e, math.exp(-(t - c) * 14))
    return e


def post(img, t):
    """Sur chaque coupe : petit zoom punch, tremblement et glitch RVB."""
    e = cut_energy(t)
    rgb = img.convert("RGB")
    if e < 0.05:
        return rgb
    if e > 0.4:
        r, g, b = rgb.split()
        s = int(16 * e)
        rgb = Image.merge("RGB", (fx.ImageChops.offset(r, s, 0), g, fx.ImageChops.offset(b, -s, 0)))
    z = 1 + 0.045 * e
    zw, zh = int(W * z), int(H * z)
    rnd = random.Random(int(t * FPS))
    sx, sy = rnd.uniform(-1, 1) * 22 * e, rnd.uniform(-1, 1) * 22 * e
    big = rgb.resize((zw, zh), Image.BILINEAR)
    left, top = (zw - W) / 2 + sx, (zh - H) / 2 + sy
    rgb = big.crop((int(left), int(top), int(left) + W, int(top) + H))
    if e > 0.75:
        rgb = Image.blend(rgb, Image.new("RGB", (W, H), (255, 255, 255)), (e - 0.75) * 0.8)
    return rgb


def frame_at(t, footage):
    if t >= FOOTAGE_END:
        return post(end_card(t), t)
    img = grade(footage.next(), t)
    img.alpha_composite(fx.VIGNETTE)
    img.alpha_composite(SHADE)
    draw_place(img, t)
    draw_titles(img, t)
    draw_captions(img, t)
    draw_hud(img, t)
    return post(img, t)


# ---------------------------------------------------------------- son
def mix_audio(voice, vsr, path):
    sr = 44100
    n = int(DURATION * sr)
    out = np.zeros(n)
    rng = np.random.default_rng(2)

    def add(sig, at, gain):
        i = int(at * sr)
        j = min(n, i + len(sig))
        if i < n:
            out[i:j] += sig[: j - i] * gain

    tt = np.arange(n) / sr
    # nappe grave + battements 120 BPM
    pad = np.sin(2 * np.pi * 55 * tt) + 0.6 * np.sin(2 * np.pi * 82.41 * tt) + 0.4 * np.sin(2 * np.pi * 65.41 * tt)
    out += pad * np.clip(tt / 2, 0, 1) * np.clip((DURATION - tt) / 3, 0, 1) * 0.07
    d = np.arange(int(0.45 * sr)) / sr
    kick = np.sin(2 * np.pi * np.cumsum(45 + 110 * np.exp(-d * 28)) / sr) * np.exp(-d * 7)
    hat = np.diff(rng.standard_normal(int(0.05 * sr)), prepend=0) * np.exp(-np.arange(int(0.05 * sr)) / sr * 80)
    b = 0.0
    while b < FOOTAGE_END:
        add(kick, b, 0.55)
        add(hat, b + 0.25, 0.06)
        b += 0.5
    # « whoosh » sur chaque coupe
    for c in CUTS:
        s = np.diff(rng.standard_normal(int(0.25 * sr)), prepend=0)
        env = np.sin(np.linspace(0, np.pi, len(s))) ** 2
        add(s * env, c - 0.12, 0.10)
    # boom d'ouverture, de climax et de fin
    d = np.arange(int(1.6 * sr)) / sr
    boom = np.sin(2 * np.pi * (38 + 40 * np.exp(-d * 6)) * d) * np.exp(-d * 2.5)
    for h in (0.1, 54.3, FOOTAGE_END):
        add(boom, h, 0.8)
    d = np.arange(int(6 * sr)) / sr
    add(sum(np.sin(2 * np.pi * f * d) for f in (220, 277.18, 329.63, 440)) * np.exp(-d * 0.6), FOOTAGE_END, 0.05)

    # voix : rééchantillonnée en 44,1 kHz, la musique s'efface sous elle
    duck = np.ones(n)
    voice_track = np.zeros(n)
    for start, _, data in voice:
        x = np.interp(np.arange(int(len(data) * sr / vsr)) * vsr / sr, np.arange(len(data)), data)
        i = int(start * sr)
        j = min(n, i + len(x))
        voice_track[i:j] += x[: j - i]
        duck[max(0, i - 2000):j + 4000] = 0.45
    duck = np.convolve(duck, np.ones(2205) / 2205, mode="same")
    out = np.tanh(out * duck * 1.2) * 0.55 + voice_track * 1.6
    out = out / np.max(np.abs(out)) * 0.92
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes((out * 32767).astype(np.int16).tobytes())


def main():
    args = sys.argv[1:]
    src, model = Path(args[0]), Path(args[1])
    with tempfile.TemporaryDirectory() as tmp:
        voice, vsr = make_voice(model, tmp)
        for (start, dur, _), (_, text) in zip(voice, SCRIPT):
            print(f"{start:5.1f}s +{dur:4.1f}s  {text}")
        build_captions(voice)
        if "--preview" in args:
            i = args.index("--preview")
            out = Path(args[i + 1])
            out.mkdir(parents=True, exist_ok=True)
            for t in [float(x) for x in args[i + 2].split(",")]:
                fx_frame = frame_at(t, Footage(src, t) if t < FOOTAGE_END else None)
                fx_frame.save(out / f"frame_{t:05.1f}.png")
            return
        wav = Path(tmp) / "mix.wav"
        mix_audio(voice, vsr, wav)
        ff = subprocess.Popen([
            "ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
            "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", str(wav),
            "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", args[2],
        ], stdin=subprocess.PIPE)
        footage = Footage(src)
        total = int(DURATION * FPS)
        for k in range(total):
            ff.stdin.write(frame_at(k / FPS, footage).tobytes())
            if k % 300 == 0:
                print(f"{k}/{total}", flush=True)
        ff.stdin.close()
        ff.wait()


if __name__ == "__main__":
    main()
