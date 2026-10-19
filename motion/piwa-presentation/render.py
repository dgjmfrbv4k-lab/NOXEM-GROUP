"""PIWA Studio — vidéo de présentation de l'agence avec tarifs « cassés » (1080x1920, 42 s).

Logo, accroche, showreel des réalisations (piwa/videos), savoir-faire, puis les tarifs :
l'ancien prix vole en éclats comme une vitrine et le nouveau prix tombe à sa place.
    python3 motion/piwa-presentation/render.py SORTIE.mp4 [--music musique.wav] [--preview dossier t1,t2,...]
"""
import importlib.util
import math
import random
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "france-17-octobre"))
import render as fx  # noqa: E402  (palette, polices, texte, logo, verre, carte)

_spec = importlib.util.spec_from_file_location("pov", HERE.parent / "pov-rewind" / "render.py")
pov = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(pov)  # rayon 3D du POV, réutilisé dans le showreel

W, H, FPS = fx.W, fx.H, fx.FPS
ROOT = HERE.parents[1]
DURATION = 42.0
BEAT = 60 / 128
GOLD = (236, 200, 120)
RED = (239, 68, 68)
WHATSAPP = "06 86 12 13 71"

# ---------------------------------------------------------------- découpage
INTRO, HOOK, REEL, SKILLS, PRICES, CTA = 0.0, 3.0, 6.0, 16.0, 24.0, 36.5
HOOK_WORDS = [(3.0, "VOTRE MARQUE."), (3.94, "VOTRE OFFRE."), (4.88, "VOS VENTES.")]
SLOT = 2 * BEAT
# (fichier ou générateur, début dans la source, libellé)
REEL_ITEMS = [
    ("noxem-menuiseries", 4.0, "NOXEM GROUP · MENUISERIES"),
    ("application", 3.0, "APPLICATION"),
    ("aisle", 0.0, "MOTION DESIGN 3D"),
    ("immobilier", 4.0, "IMMOBILIER"),
    ("restaurant", 4.0, "RESTAURANT"),
    ("map", 0.0, "DATA & CARTES ANIMÉES"),
    ("recrutement", 4.0, "RECRUTEMENT"),
    ("noxem-destockage", 6.0, "NOXEM GROUP · DÉSTOCKAGE"),
    ("sport", 4.0, "SALLE DE SPORT"),
    ("renovation", 4.0, "RÉNOVATION"),
]
SKILL_CARDS = [
    ("01", "Script sur mesure", "écrit pour capter dès la 1re seconde"),
    ("02", "Voix off", "plus de 25 langues"),
    ("03", "Musique & sound design", "calés sur chaque animation"),
    ("04", "Tous les formats", "TikTok · Reels · YouTube · LinkedIn"),
]
# (durée, ancien prix, nouveau prix, usage)
TIERS = [
    ("15 S", 390, 190, "Réseaux sociaux"),
    ("30 S", 690, 390, "Pub · offre · produit"),
    ("1 MIN", 990, 700, "Présentation complète"),
]
TIER_START, TIER_STEP = PRICES + 1.6, 2.8

F_MEGA, F_HUGE, F_BIG, F_XL, F_L, F_M, F_S, F_XS, F_TAG = (fx.F_MEGA, fx.F_HUGE, fx.F_BIG, fx.F_XL, fx.F_L,
                                                           fx.F_M, fx.F_S, fx.F_XS, fx.F_TAG)
F_PRICE = fx.font("Black", 230)
F_OLD = fx.font("Black", 120)
F_NUM = fx.font("Black", 64)
F_LABEL = fx.font("Bold", 36)


# ---------------------------------------------------------------- showreel
class Reel:
    def __init__(self, tmp):
        self.frames = {}
        for name, start, _ in REEL_ITEMS:
            if name in ("aisle", "map"):
                continue
            out = Path(tmp) / name
            out.mkdir()
            subprocess.run([
                "ffmpeg", "-loglevel", "error", "-ss", str(start), "-i", str(ROOT / "piwa" / "videos" / f"{name}.mp4"),
                "-t", f"{SLOT + 0.2:.2f}", "-vf", f"fps={FPS},scale=1000:-2:flags=lanczos", "-q:v", "2", str(out / "%03d.jpg"),
            ], check=True)
            self.frames[name] = sorted(out.glob("*.jpg"))

    def frame(self, name, lt):
        files = self.frames[name]
        return Image.open(files[min(len(files) - 1, int(lt * FPS))]).convert("RGB")


def map_card(lt):
    img = Image.new("RGBA", (W, H), fx.BG + (255,))
    fx.background(img, 20 + lt)
    fx.draw_map(img, 540, 1000, 900, draw_p=fx.ease_out(fx.clamp(lt / 0.6)), fill_a=0.15, glow=1.0)
    for i, (_, (lo, la)) in enumerate(fx.CITIES):
        x, y = fx.project(lo, la, 540, 1000, 900)
        fx.draw_pin(img, x, y, lt, 0.1 + i * 0.08)
    return img


def scene_reel(img, t):
    k = min(len(REEL_ITEMS) - 1, int((t - REEL) / SLOT))
    name, _, label = REEL_ITEMS[k]
    s = REEL + k * SLOT
    lt = t - s
    if name == "aisle":
        full, _ = pov.aisle_frame(6.0 + lt * 1.4)
        img.alpha_composite(full)
    elif name == "map":
        img.alpha_composite(map_card(lt))
    else:
        fr = self_reel.frame(name, lt)
        # fond : la même image agrandie et floutée
        bg = fr.resize((int(H * fr.width / fr.height), H), Image.BILINEAR)
        bg = bg.crop(((bg.width - W) // 2, 0, (bg.width - W) // 2 + W, H)).filter(ImageFilter.GaussianBlur(40))
        bg = Image.blend(bg, Image.new("RGB", (W, H), fx.BG), 0.55)
        img.paste(bg)
        # carte vidéo qui entre en glissant avec un léger angle
        p = fx.ease_back(fx.prog(lt, 0, 0.3))
        card = fr.convert("RGBA")
        mask = Image.new("L", card.size, 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, card.width, card.height), radius=36, fill=255)
        card.putalpha(mask)
        ang = (1 - p) * (8 if k % 2 else -8) + 2.5 * math.sin(lt * 2)
        scale = 0.92 + 0.08 * p + 0.04 * lt
        card = card.resize((int(card.width * scale), int(card.height * scale)), Image.BILINEAR).rotate(ang, expand=True, resample=Image.BICUBIC)
        dx = (1 - p) * (700 if k % 2 else -700)
        glow = fx.faded(fx.GLOW_VIOLET, 0.7)
        img.alpha_composite(glow, (W // 2 - 700, 960 - 700))
        img.alpha_composite(card, (int((W - card.width) / 2 + dx), int(960 - card.height / 2)))
    # libellé + compteur
    a = fx.window(t, s, s + SLOT, 0.1, 0.1)
    fx.draw_text(img, "NOS RÉALISATIONS", F_TAG, 300, 1.0, color=fx.MUTE, tracking=10)
    fx.draw_text(img, f"{k + 1:02d}", F_NUM, 390, 1.0, gradient=True)
    fx.draw_text(img, label, F_LABEL, 1420, a, dy=(1 - fx.ease_out(fx.prog(lt, 0, 0.25))) * 30, tracking=6)


# ---------------------------------------------------------------- savoir-faire
def scene_skills(img, t):
    fx.background(img, t)
    fx.draw_text(img, "UNE ÉQUIPE COMPLÈTE", F_TAG, 260, fx.window(t, SKILLS, 20.2), color=fx.MUTE, tracking=10)
    d = ImageDraw.Draw(img)
    for i, (num, title, sub) in enumerate(SKILL_CARDS):
        s = SKILLS + 0.15 + i * BEAT
        p = fx.ease_back(fx.prog(t, s, 0.35))
        a = fx.window(t, s, 20.2, 0.15, 0.25)
        if a <= 0:
            continue
        y = 420 + i * 300
        x0 = 70 + (1 - p) * (W if i % 2 == 0 else -W)
        d.rounded_rectangle((x0, y, x0 + W - 140, y + 250), radius=40, fill=(18, 20, 30, int(235 * a)),
                            outline=fx.grad_color(i / 3) + (int(255 * a),), width=4)
        fx.draw_text(img, num, F_NUM, y + 125, a, x=x0 + 70, anchor="left", gradient=True)
        fx.draw_text(img, title, F_M, y + 95, a, x=x0 + 210, anchor="left")
        fx.draw_text(img, sub, F_S, y + 165, a, x=x0 + 210, anchor="left", color=fx.MUTE)
    # 7 jours
    if t >= 20.3:
        fx.slam(img, "LIVRÉE EN", F_XL, 620, t, 20.3, PRICES)
        fx.slam(img, "7 JOURS", F_HUGE, 860, t, 20.6, PRICES, gradient=True, tracking=-10)
        fx.draw_text(img, "2 retouches incluses", F_L, 1110, fx.window(t, 21.3, PRICES), dy=(1 - fx.ease_out(fx.prog(t, 21.3, 0.4))) * 40)
        fx.draw_text(img, "Script · voix off · musique · animation", F_S, 1200, fx.window(t, 21.7, PRICES), color=fx.MUTE)


# ---------------------------------------------------------------- tarifs cassés
PRICE_Y = 1000
GLASSES = [fx.Glass(540, PRICE_Y, seed=20 + i, rays=14, rings=(0, 30, 75, 130, 200, 290, 400, 560)) for i in range(len(TIERS))]


def scene_prices(img, t):
    fx.background(img, t)
    if t < TIER_START + 0.1:
        fx.slam(img, "ON CASSE", F_BIG, 820, t, PRICES, TIER_START)
        fx.slam(img, "LES PRIX.", F_BIG, 990, t, PRICES + 0.47, TIER_START, gradient=True)
        return
    summary = TIER_START + TIER_STEP * len(TIERS)
    if t < summary:
        i = int((t - TIER_START) / TIER_STEP)
        dur, old, new, use = TIERS[i]
        s = TIER_START + i * TIER_STEP
        brk = s + 1.0
        a = fx.window(t, s, s + TIER_STEP, 0.15, 0.15)
        fx.draw_text(img, "VIDÉO", F_TAG, 470, a, color=fx.MUTE, tracking=10)
        fx.slam(img, dur, F_HUGE, 640, t, s, s + TIER_STEP, tracking=-6)
        fx.draw_text(img, use, F_L, 820, a)
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        if t < brk:
            # ancien prix, barré puis fissuré
            fx.draw_text(img, f"{old} €", F_OLD, PRICE_Y, a, color=fx.MUTE)
            d = ImageDraw.Draw(img)
            sp = fx.ease_out(fx.prog(t, s + 0.3, 0.3))
            if sp > 0:
                d.line([(300, PRICE_Y + 10), (300 + 480 * sp, PRICE_Y - 10)], fill=RED + (255,), width=12)
            GLASSES[i].draw_cracks(layer, fx.ease_out(fx.prog(t, s + 0.6, 0.4)), 1.0 if t >= s + 0.6 else 0.0)
        else:
            GLASSES[i].draw_shatter(layer, t - brk)
            fx.slam(img, f"{new} €", F_PRICE, PRICE_Y + 10, t, brk + 0.05, s + TIER_STEP, gradient=True, tracking=-8)
            fx.draw_text(img, f"au lieu de {old} €", F_S, PRICE_Y + 170, fx.window(t, brk + 0.3, s + TIER_STEP), color=fx.MUTE)
            fx.draw_text(img, f"−{old - new} €", F_TAG, PRICE_Y + 250, fx.window(t, brk + 0.2, s + TIER_STEP),
                         color=GOLD, tracking=4)
        img.alpha_composite(layer)
        return
    # récapitulatif des trois formules
    fx.draw_text(img, "TARIFS DE LANCEMENT", F_TAG, 380, fx.window(t, summary, CTA), color=fx.MUTE, tracking=10)
    d = ImageDraw.Draw(img)
    for i, (dur, old, new, use) in enumerate(TIERS):
        s = summary + i * 0.15
        p = fx.ease_back(fx.prog(t, s, 0.35))
        a = fx.window(t, s, CTA, 0.12, 0.25)
        y = 500 + i * 330
        x0 = 70 + (1 - p) * W
        hot = i == 1
        d.rounded_rectangle((x0, y, x0 + W - 140, y + 280), radius=40, fill=(18, 20, 30, int(240 * a)),
                            outline=(fx.PINK if hot else fx.grad_color(i / 2)) + (int(255 * a),), width=6 if hot else 3)
        fx.draw_text(img, dur, F_XL, y + 120, a, x=x0 + 60, anchor="left")
        fx.draw_text(img, use, F_XS, y + 210, a, x=x0 + 64, anchor="left", color=fx.MUTE)
        fx.draw_text(img, f"{new} €", F_XL, y + 120, a, x=x0 + W - 330, anchor="center", gradient=True)
        fx.draw_text(img, f"{old} €", F_S, y + 215, a * 0.8, x=x0 + W - 330, anchor="center", color=fx.MUTE)
        ow = F_S.getlength(f"{old} €")
        d.line([(x0 + W - 330 - ow / 2 - 6, y + 220), (x0 + W - 330 + ow / 2 + 6, y + 210)], fill=RED + (int(255 * a),), width=5)
        if hot:
            tw = F_XS.getlength("LA PLUS DEMANDÉE") + 60
            d.rounded_rectangle((x0 + 60, y - 26, x0 + 60 + tw, y + 26), radius=26, fill=fx.PINK + (int(255 * a),))
            fx.draw_text(img, "LA PLUS DEMANDÉE", F_XS, y, a, x=x0 + 90, anchor="left")
    fx.draw_text(img, "Prix HT · voix off, musique et 2 retouches inclus", F_XS, 1530, fx.window(t, summary + 0.6, CTA), color=fx.MUTE)


# ---------------------------------------------------------------- intro, accroche, fin
def scene_intro(img, t):
    fx.background(img, t)
    a = fx.ease_out(fx.prog(t, 0.25, 0.5))
    if a > 0:
        lg = fx.faded(fx.LOGO, a)
        z = 1 + (1 - fx.ease_back(fx.prog(t, 0.25, 0.5))) * 0.6
        lg = lg.resize((int(lg.width * z), int(lg.height * z)), Image.BILINEAR)
        img.alpha_composite(lg, ((W - lg.width) // 2, int(800 - lg.height / 2)))
    fx.draw_text(img, "STUDIO DE MOTION DESIGN", F_TAG, 1020, fx.window(t, 1.0, HOOK, 0.3, 0.2), tracking=12)
    fx.draw_text(img, "Des vidéos qui font vendre.", F_M, 1110, fx.window(t, 1.5, HOOK, 0.3, 0.2), gradient=True)


def scene_hook(img, t):
    fx.background(img, t)
    fx.draw_text(img, "ON MET EN MOUVEMENT", F_TAG, 700, fx.window(t, HOOK, REEL), color=fx.MUTE, tracking=10)
    for i, (s, w) in enumerate(HOOK_WORDS):
        fx.slam(img, w, F_BIG if len(w) < 12 else F_XL, 880 + i * 170, t, s, REEL, gradient=(i == 2), tracking=-4)


def scene_cta(img, t):
    fx.background(img, t)
    lt = t - CTA
    fx.slam(img, "LANCEZ", F_BIG, 360, t, CTA, DURATION)
    fx.slam(img, "VOTRE VIDÉO.", F_BIG, 520, t, CTA + 0.25, DURATION, gradient=True)
    a = fx.ease_out(fx.prog(lt, 0.6, 0.4))
    img.alpha_composite(fx.faded(fx.LOGO, a), ((W - fx.LOGO.width) // 2, int(720 + (1 - a) * 40)))
    d = ImageDraw.Draw(img)
    b = fx.ease_back(fx.prog(lt, 1.1, 0.4))
    if b > 0:
        bw = 820 * b
        d.rounded_rectangle((540 - bw / 2, 1180, 540 + bw / 2, 1330), radius=75, fill=(37, 211, 102, 255))
        fx.draw_text(img, f"WhatsApp  {WHATSAPP}", F_M, 1255, fx.clamp(b), color=(255, 255, 255))
    fx.draw_text(img, "Kevin · du lundi au samedi", F_S, 1400, fx.ease_out(fx.prog(lt, 1.5, 0.4)), color=fx.MUTE)
    fx.draw_text(img, "Tarifs de lancement · places limitées", F_S, 1520, fx.ease_out(fx.prog(lt, 1.9, 0.4)), color=GOLD)


# ---------------------------------------------------------------- effets & rendu
CUTS = [HOOK] + [s for s, _ in HOOK_WORDS[1:]] + [REEL + k * SLOT for k in range(len(REEL_ITEMS))] + [SKILLS, 20.3, PRICES, PRICES + 0.47] \
    + [TIER_START + i * TIER_STEP + 1.0 for i in range(len(TIERS))] + [TIER_START + TIER_STEP * len(TIERS), CTA]


def post(rgb, t):
    e = 0.0
    for c in CUTS:
        if t >= c:
            e = max(e, math.exp(-(t - c) * 11))
    pulse = math.exp(-(t % BEAT) * 14) if 3.0 <= t < 40.5 else 0.0
    if e < 0.05 and pulse < 0.05:
        return rgb
    if e > 0.4:
        r, g, b = rgb.split()
        s = int(20 * e)
        rgb = Image.merge("RGB", (ImageChops.offset(r, s, 0), g, ImageChops.offset(b, -s, 0)))
    rnd = random.Random(int(t * FPS))
    rgb = pov.zoom_to(rgb, 1 + 0.05 * e + 0.02 * pulse, W / 2 + rnd.uniform(-1, 1) * 24 * e, H / 2 + rnd.uniform(-1, 1) * 24 * e)
    if e > 0.75:
        rgb = Image.blend(rgb, Image.new("RGB", (W, H), (255, 255, 255)), (e - 0.75) * 0.8)
    return rgb


def frame_at(t):
    img = Image.new("RGBA", (W, H), fx.BG + (255,))
    if t < HOOK:
        scene_intro(img, t)
    elif t < REEL:
        scene_hook(img, t)
    elif t < SKILLS:
        scene_reel(img, t)
    elif t < PRICES:
        scene_skills(img, t)
    elif t < CTA:
        scene_prices(img, t)
    else:
        scene_cta(img, t)
    img.alpha_composite(fx.VIGNETTE)
    # barre de progression
    bar = fx.GRADIENT_FULL.crop((0, 0, max(1, int(W * t / DURATION)), 8)).convert("RGBA")
    img.alpha_composite(bar, (0, 0))
    return post(img.convert("RGB"), t)


# ---------------------------------------------------------------- musique
SR = 44100


def music():
    n = int(DURATION * SR)
    out = np.zeros(n)
    rng = np.random.default_rng(4)
    tt = np.arange(n) / SR

    def add(sig, at, gain=1.0):
        i = int(at * SR)
        j = min(n, i + len(sig))
        if 0 <= i < n:
            out[i:j] += sig[: j - i] * gain

    def ex(dur, k):
        return np.exp(-np.arange(int(dur * SR)) / SR * k)

    d = np.arange(int(0.45 * SR)) / SR
    kick = np.sin(2 * np.pi * np.cumsum(45 + 120 * np.exp(-d * 30)) / SR) * np.exp(-d * 7)
    hat = np.diff(rng.standard_normal(int(0.05 * SR)), prepend=0) * ex(0.05, 90)
    clap = np.diff(rng.standard_normal(int(0.18 * SR)), prepend=0) * ex(0.18, 22)
    d = np.arange(int(1.6 * SR)) / SR
    boom = np.sin(2 * np.pi * (38 + 40 * np.exp(-d * 6)) * d) * np.exp(-d * 2.5)

    def synth(f, dur, k=4.0):
        d = np.arange(int(dur * SR)) / SR
        saw = sum(np.sin(2 * np.pi * f * h * d) / h for h in range(1, 6))
        return saw * np.exp(-d * k)

    # nappe
    pad = sum(np.sin(2 * np.pi * f * tt) for f in (110, 138.6, 164.8)) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.2 * tt))
    out += pad * np.clip(tt / 2, 0, 1) * 0.025
    # intro : montée
    add(rng.standard_normal(int(2.8 * SR)) * np.linspace(0, 1, int(2.8 * SR)) ** 3, 0.2, 0.12)
    # beat 128 BPM avec arpège
    arp = [220, 277.18, 329.63, 440, 329.63, 277.18, 246.94, 329.63]
    b, k = HOOK, 0
    while b < DURATION - 1.0:
        quiet = PRICES <= b < TIER_START
        add(kick, b, 0.9 if not quiet else 0.0)
        add(hat, b + BEAT / 2, 0.10)
        if k % 2 == 1 and not quiet:
            add(clap, b, 0.3)
        if b >= REEL:
            add(synth(arp[k % 8], BEAT * 0.9, 6), b, 0.045)
            add(synth(arp[(k + 3) % 8], BEAT * 0.4, 9), b + BEAT / 2, 0.03)
        add(synth(55 if (k // 8) % 2 == 0 else 61.7, BEAT * 0.8, 5), b, 0.12)
        b += BEAT
        k += 1
    for c in CUTS:
        add(np.diff(rng.standard_normal(int(0.2 * SR)), prepend=0) * np.sin(np.linspace(0, np.pi, int(0.2 * SR))) ** 2, c - 0.1, 0.07)
    # « on casse les prix » : silence, boom, puis un fracas de verre à chaque prix
    add(boom, PRICES, 0.9)
    for i in range(len(TIERS)):
        brk = TIER_START + i * TIER_STEP + 1.0
        add(np.diff(rng.standard_normal(int(1.2 * SR)), prepend=0) * ex(1.2, 4), brk, 0.4)
        for _ in range(25):
            f = rng.uniform(3000, 9000)
            dd = np.arange(int(0.2 * SR)) / SR
            add(np.sin(2 * np.pi * f * dd) * np.exp(-dd * 20), brk + rng.uniform(0, 0.8), 0.04)
        add(boom, brk, 0.6)
    # caisse enregistreuse sur le nouveau prix
    for i in range(len(TIERS)):
        dd = np.arange(int(0.35 * SR)) / SR
        add((np.sin(2 * np.pi * 1760 * dd) + 0.6 * np.sin(2 * np.pi * 2637 * dd)) * np.exp(-dd * 10), TIER_START + i * TIER_STEP + 1.1, 0.08)
    dd = np.arange(int(5 * SR)) / SR
    add(sum(np.sin(2 * np.pi * f * dd) for f in (220, 277.18, 329.63, 440)) * np.exp(-dd * 0.6), CTA, 0.06)
    out = np.tanh(out * 1.3)
    out = out * np.clip((DURATION - tt) / 1.2, 0, 1)
    out = out / np.max(np.abs(out)) * 0.9
    return (out * 32767).astype(np.int16)


self_reel = None


def main():
    global self_reel
    args = sys.argv[1:]
    music_out = None
    if "--music" in args:
        i = args.index("--music")
        music_out = Path(args[i + 1])
        del args[i:i + 2]
    with tempfile.TemporaryDirectory() as tmp:
        self_reel = Reel(tmp)
        if "--preview" in args:
            i = args.index("--preview")
            out = Path(args[i + 1])
            out.mkdir(parents=True, exist_ok=True)
            for t in [float(x) for x in args[i + 2].split(",")]:
                frame_at(t).save(out / f"frame_{t:05.1f}.png")
            return
        wav = music_out or Path(tmp) / "musique.wav"
        with wave.open(str(wav), "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes(music().tobytes())
        ff = subprocess.Popen([
            "ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
            "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", str(wav),
            "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", args[0],
        ], stdin=subprocess.PIPE)
        total = int(DURATION * FPS)
        for k in range(total):
            ff.stdin.write(frame_at(k / FPS).tobytes())
            if k % 300 == 0:
                print(f"{k}/{total}", flush=True)
        ff.stdin.close()
        ff.wait()


if __name__ == "__main__":
    main()
