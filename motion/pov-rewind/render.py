"""PIWA Studio — « POV : tout est gratuit… ◀◀ rewind » (1080x1920, 48 s).

On entre dans la tête d'un pilleur (vitrines, rayon 3D en motion design, compteur de butin),
puis tout se rembobine : les produits retournent en rayon, on voit qui paie, la vitrine se recolle.
Pas de voix : la voix off est enregistrée à part (ElevenLabs) sur le texte des sous-titres.

    python3 motion/pov-rewind/render.py SOURCE.mp4 SORTIE.mp4 [--music musique.wav] [--preview dossier t1,t2,...]
"""
import math
import random
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "france-17-octobre"))
import render as fx  # noqa: E402  (palette, polices, texte, logo, verre, effets)

W, H, FPS = fx.W, fx.H, fx.FPS
DURATION = 48.0
CREDIT = "Images : @popcornpariss (TikTok)"
GOLD = (236, 200, 120)
RED = (239, 68, 68)

# ---------------------------------------------------------------- découpage (temps de sortie)
POV_IN, NICO_IN, SEPHORA, AISLE, STOP, REWIND, REALITY, REPAIR, END = 0.0, 3.0, 6.0, 9.0, 21.0, 23.0, 29.0, 37.0, 42.0
NICO_SHELF = 4.4

# plans repris de la source : (début sortie, fin sortie, début source, vitesse)
SEGMENTS = [
    (NICO_IN, NICO_SHELF, 5.75, 1.0),      # Nicolas, devanture
    (NICO_SHELF, SEPHORA, 7.10, 0.8),      # Nicolas, rayons vides
    (SEPHORA, AISLE, 39.95, 0.7),          # Sephora, vitrine brisée
    (REALITY, 30.6, 11.50, 1.0),           # Galeries Lafayette, on pose du bois
    (30.6, 32.15, 17.85, 1.0),             # Opéra, on balaie
    (32.15, 33.7, 32.75, 1.0),             # agent qui nettoie les tags
    (33.7, 35.0, 34.30, 1.0),              # nettoyage haute pression
    (35.0, 36.15, 46.20, 1.0),             # Franprix barricadé
    (36.15, REPAIR, 30.05, 1.0),           # on sécurise une vitre
    (REPAIR, END, 0.10, 0.3),              # Dior, vitrine brisée (ralenti)
]
PUSH_INS = {NICO_SHELF: (560, 1000), AISLE: (540, 980)}  # on « rentre » dans le magasin

# sous-titres = texte à enregistrer pour la voix off : (début, fin, texte)
SUBTITLES = [
    (0.3, 2.9, "POV : 17 octobre. Dans ta tête, tout est gratuit."),
    (3.0, 5.9, "Une vitrine qui saute. Une bouteille. Puis deux."),
    (6.0, 8.9, "La porte est ouverte. Personne pour t'arrêter."),
    (9.2, 12.5, "Parfum. Rouge à lèvres. Palette. Tu te sers."),
    (12.6, 16.0, "Ça va vite. Le cœur tape. Le sac se remplit."),
    (16.2, 20.6, "Dans ta tête, c'est gratuit. Rien ne t'arrête."),
    (23.2, 28.6, "Maintenant… on rembobine."),
    (29.2, 33.0, "Ce que tu as pris, quelqu'un le paie."),
    (33.2, 36.8, "Le commerçant. Son équipe. Tout un quartier."),
    (37.2, 41.6, "Alors on répare. Ensemble."),
]

F_CAP = fx.font("Black", 74)
F_HUD = fx.font("Bold", 36)
F_HUD_S = fx.font("SemiBold", 28)
F_TAG = fx.font("Black", 52)
F_TOTAL = fx.font("Black", 96)
F_CREDIT = fx.font("Medium", 28)


# ---------------------------------------------------------------- outils
def ease_in(x):
    return x ** 3


def zoom_to(img, z, cx, cy):
    """Zoom centré sur (cx, cy)."""
    if z <= 1.001:
        return img
    cw, ch = W / z, H / z
    left = min(max(0, cx - cw / 2), W - cw)
    top = min(max(0, cy - ch / 2), H - ch)
    return img.crop((int(left), int(top), int(left + cw), int(top + ch))).resize((W, H), Image.BILINEAR)


def make_scanlines():
    s = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(s)
    for y in range(0, H, 6):
        d.rectangle((0, y, W, y + 2), fill=(0, 0, 0, 70))
    return s


SCANLINES = make_scanlines()


def make_shade():
    shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(shade)
    for y in range(0, 700, 4):
        d.rectangle((0, H - 700 + y, W, H - 700 + y + 4), fill=fx.BG + (int(215 * (y / 700) ** 1.6),))
    for y in range(0, 320, 4):
        d.rectangle((0, y, W, y + 4), fill=fx.BG + (int(160 * (1 - y / 320)),))
    return shade


SHADE = make_shade()


# ---------------------------------------------------------------- images source
class Clips:
    """Extrait chaque plan repris en JPEG 1080x1920 (une fois), puis sert l'image voulue."""

    def __init__(self, src, tmp):
        self.frames = []
        for k, (o0, o1, s0, speed) in enumerate(SEGMENTS):
            out = Path(tmp) / f"seg{k}"
            out.mkdir()
            length = (o1 - o0) * speed + 0.1
            subprocess.run([
                "ffmpeg", "-loglevel", "error", "-ss", str(s0), "-i", str(src), "-t", f"{length:.3f}",
                "-vf", f"fps={FPS},scale={W}:{H}:flags=lanczos", "-q:v", "2", str(out / "%04d.jpg"),
            ], check=True)
            self.frames.append(sorted(out.glob("*.jpg")))

    def at(self, t):
        for k, (o0, o1, _, speed) in enumerate(SEGMENTS):
            if o0 <= t < o1:
                files = self.frames[k]
                i = min(len(files) - 1, int((t - o0) * speed * FPS))
                return Image.open(files[i]).convert("RGB"), o0, o1
        return None, 0, 0


def graded(frame, t, o0, o1, cold=False):
    z = 1.0 + 0.06 * fx.prog(t, o0, o1 - o0)
    frame = zoom_to(frame, z, W / 2, H / 2)
    frame = ImageEnhance.Contrast(ImageEnhance.Color(frame).enhance(0.6 if cold else 0.9)).enhance(1.15)
    frame = Image.blend(frame, fx.GRADIENT_FULL, 0.08)
    # poussée vers l'intérieur du magasin sur la fin du plan
    if o1 in PUSH_INS:
        p = fx.prog(t, o1 - 0.45, 0.45)
        if p > 0:
            cx, cy = PUSH_INS[o1]
            frame = zoom_to(frame, 1 + 2.6 * ease_in(p), cx, cy)
            frame = frame.filter(ImageFilter.GaussianBlur(10 * p))
            frame = Image.blend(frame, Image.new("RGB", (W, H), (255, 255, 255)), 0.85 * p ** 4)
    return frame.convert("RGBA")


# ---------------------------------------------------------------- rayon 3D
F_LEN = 760.0
SPEED_3D = 3.2
AISLE_LEN = STOP - AISLE
SHELF_Y = [-0.55, -0.05, 0.45]
PRODUCT_KINDS = ["parfum", "rouge", "palette", "serum", "creme"]
COLORS = [fx.PINK, fx.VIOLET, fx.CYAN, GOLD, (250, 250, 255), (30, 30, 36), (220, 60, 90)]


def build_products():
    rnd = random.Random(5)
    items = []
    z = 2.0
    while z < SPEED_3D * AISLE_LEN + 14:
        for side in (-1, 1):
            for sy in SHELF_Y:
                if rnd.random() < 0.85:
                    items.append((z + rnd.uniform(-0.2, 0.2), side, sy, rnd.choice(PRODUCT_KINDS), rnd.choice(COLORS)))
        z += 0.9
    return items


PRODUCTS = build_products()
PICKS = []  # (instant local, côté, étagère, type, couleur, libellé, prix)
_LABELS = {"parfum": ("PARFUM", 129), "rouge": ("ROUGE À LÈVRES", 39), "palette": ("PALETTE", 65),
           "serum": ("SÉRUM", 89), "creme": ("CRÈME", 120)}
_rp = random.Random(9)
for k in range(17):
    tl = 0.5 + k * 0.66
    kind = PRODUCT_KINDS[k % len(PRODUCT_KINDS)]
    label, price = _LABELS[kind]
    PICKS.append((tl, -1 if k % 2 == 0 else 1, SHELF_Y[_rp.randrange(3)], kind, _rp.choice(COLORS[:5]), label,
                  price + _rp.choice([0, 0, 10, 20])))


def project(x, y, z, zc):
    dz = z - zc
    if dz <= 0.15:
        return None
    return W / 2 + F_LEN * x / dz, H / 2 + F_LEN * y / dz, F_LEN / dz


def draw_product(d, kind, color, cx, base_y, s, alpha=255):
    """Produit vu de face, posé sur base_y, échelle s (pixels par unité monde)."""
    w = 0.16 * s
    c = color + (alpha,)
    edge = (255, 255, 255, int(alpha * 0.55))
    if kind == "parfum":
        d.rounded_rectangle((cx - w, base_y - 1.9 * w, cx + w, base_y), radius=w * 0.25, fill=c, outline=edge, width=max(1, int(s * 0.006)))
        d.rectangle((cx - w * 0.35, base_y - 2.5 * w, cx + w * 0.35, base_y - 1.9 * w), fill=GOLD + (alpha,))
    elif kind == "rouge":
        d.rectangle((cx - w * 0.35, base_y - 1.4 * w, cx + w * 0.35, base_y), fill=(25, 25, 30, alpha))
        d.rounded_rectangle((cx - w * 0.28, base_y - 2.2 * w, cx + w * 0.28, base_y - 1.4 * w), radius=w * 0.25, fill=c)
    elif kind == "palette":
        d.rounded_rectangle((cx - w * 1.3, base_y - 0.6 * w, cx + w * 1.3, base_y), radius=w * 0.15, fill=(25, 25, 30, alpha))
        for i in range(4):
            px = cx - w * 0.95 + i * w * 0.63
            d.ellipse((px - w * 0.2, base_y - 0.48 * w, px + w * 0.2, base_y - 0.12 * w), fill=fx.grad_color(i / 3) + (alpha,))
    elif kind == "serum":
        d.rounded_rectangle((cx - w * 0.5, base_y - 1.5 * w, cx + w * 0.5, base_y), radius=w * 0.2, fill=c, outline=edge, width=1)
        d.ellipse((cx - w * 0.25, base_y - 2.2 * w, cx + w * 0.25, base_y - 1.5 * w), fill=(25, 25, 30, alpha))
    else:
        d.rounded_rectangle((cx - w * 0.9, base_y - 0.8 * w, cx + w * 0.9, base_y), radius=w * 0.3, fill=c, outline=edge, width=1)
        d.rectangle((cx - w * 0.95, base_y - 1.05 * w, cx + w * 0.95, base_y - 0.8 * w), fill=GOLD + (alpha,))


def aisle_frame(tl, rewind=False):
    """Rayon de cosmétiques vu à la première personne, au temps local tl (0 → AISLE_LEN)."""
    zc = SPEED_3D * tl
    sway = 18 * math.sin(tl * 4.2)  # pas de course
    img = Image.new("RGBA", (W, H), (10, 10, 16, 255))
    d = ImageDraw.Draw(img)
    # sol et plafond : lignes de fuite
    for k in range(-6, 7):
        d.line([(W / 2 + sway, H / 2), (W / 2 + k * 260 + sway, H)], fill=(60, 50, 90, 120), width=2)
    for k in range(40):
        z = math.floor(zc) + k + 1
        p = project(0, 1.0, z, zc)
        if p:
            a = int(160 * min(1, p[2] / 400))
            d.line([(0, p[1]), (W, p[1])], fill=(80, 60, 140, a), width=1)
            q = project(0, -1.0, z, zc)
            if k % 3 == 0:
                d.rectangle((W / 2 - 0.5 * q[2] + sway, q[1] - 2, W / 2 + 0.5 * q[2] + sway, q[1] + 2), fill=(240, 240, 255, a))
    # étagères (du fond vers l'avant)
    far = zc + 30
    img.alpha_composite(fx.faded(fx.GLOW_VIOLET, 0.8), (int(W / 2 - 700 + sway), int(H / 2 - 700)))
    for side in (-1, 1):
        for sy in SHELF_Y + [0.95]:
            quad = [project(1.25 * side, sy, zc + 0.4, zc), project(1.25 * side, sy, far, zc),
                    project(0.75 * side, sy, far, zc), project(0.75 * side, sy, zc + 0.4, zc)]
            col = fx.grad_color(0.2 if side < 0 else 0.8)
            d.polygon([(q[0] + sway, q[1]) for q in quad], fill=(28, 26, 40, 255), outline=col + (230,))
    for z, side, sy, kind, color in sorted(PRODUCTS, key=lambda it: -it[0]):
        if not zc + 0.5 < z < far:
            continue
        p = project(0.98 * side, sy, z, zc)
        if p:
            a = int(255 * min(1, (far - z) / 8))
            draw_product(d, kind, color, p[0] + sway, p[1], p[2], a)
    # produits attrapés : ils jaillissent de l'étagère vers le sac (bas de l'écran)
    taken = 0
    for tp, side, sy, kind, color, label, price in PICKS:
        if tl < tp:
            continue
        taken += price
        k = (tl - tp) / 0.5
        if k > 1:
            continue
        p = project(0.98 * side, sy, SPEED_3D * tp + 2.6, SPEED_3D * tp)
        sx, sy0 = p[0], p[1]
        ex, ey = W / 2 + 120 * side * -1, H + 200
        e = fx.ease_out(k) if not rewind else k
        x = sx + (ex - sx) * e
        y = sy0 + (ey - sy0) * e - 260 * math.sin(math.pi * e)
        draw_product(d, kind, color, x + sway * (1 - e), y, p[2] * (1 + 2.2 * e))
        fx.draw_text(img, f"+{price} €", F_TAG, sy0 - 150 - 120 * k, fx.clamp(1.4 - k), x=sx, color=GOLD)
        fx.draw_text(img, label, F_HUD_S, sy0 - 95 - 120 * k, fx.clamp(1.4 - k), x=sx, color=fx.FG, tracking=4)
    # traits de vitesse
    rnd = random.Random(int(tl * 20))
    for _ in range(26):
        ang = rnd.uniform(0, 2 * math.pi)
        r0 = rnd.uniform(380, 700)
        r1 = r0 + rnd.uniform(160, 420)
        d.line([(W / 2 + r0 * math.cos(ang), H / 2 + r0 * math.sin(ang)), (W / 2 + r1 * math.cos(ang), H / 2 + r1 * math.sin(ang))],
               fill=(255, 255, 255, 60), width=3)
    return img, taken


# ---------------------------------------------------------------- HUD « dans sa tête »
def draw_hud(img, t, total, rewind=False):
    d = ImageDraw.Draw(img)
    m, L = 60, 90
    col = (255, 255, 255, 200)
    for (x, y, dx, dy) in ((m, 300, 1, 1), (W - m, 300, -1, 1), (m, H - 330, 1, -1), (W - m, H - 330, -1, -1)):
        d.line([(x, y), (x + L * dx, y)], fill=col, width=5)
        d.line([(x, y), (x, y + L * dy)], fill=col, width=5)
    if rewind:
        if int(t * 3) % 2 == 0:
            for k in range(2):
                x0 = 90 + k * 38
                d.polygon([(x0 + 34, 200), (x0, 222), (x0 + 34, 244)], fill=(255, 255, 255, 255))
        fx.draw_text(img, "REWIND", F_HUD, 222, x=190, anchor="left", tracking=6)
    else:
        if int(t * 2) % 2 == 0:
            d.ellipse((92, 206, 124, 238), fill=RED + (255,))
        fx.draw_text(img, "REC", F_HUD, 222, x=140, anchor="left", tracking=6)
    bpm = 150 + int(18 * abs(math.sin(t * 2.3)))
    fx.draw_text(img, f"{bpm} BPM", F_HUD, 222, x=W - 90, anchor="center", color=RED)
    if total is not None:
        fx.draw_text(img, "DANS TON SAC", F_HUD_S, 360, color=fx.MUTE, tracking=8)
        fx.draw_text(img, f"{fx.fmt_int(total)} €", F_TOTAL, 450, gradient=True, tracking=-2)
        if not rewind and total > 0 and int(t * 2.5) % 2 == 0:
            fx.draw_text(img, "« GRATUIT »", F_HUD, 540, color=GOLD, tracking=4)


# ---------------------------------------------------------------- sous-titres mot à mot
def draw_subtitles(img, t):
    for s, e, text in SUBTITLES:
        if not s <= t < e:
            continue
        words = text.split()
        weights = [len(w) + 3 for w in words]
        tot = sum(weights)
        times, acc = [], s
        for k in weights:
            times.append(acc)
            acc += (e - s - 0.4) * k / tot
        # lignes courtes : une idée à la fois
        lines, cur = [], []
        for w, wt in zip(words, times):
            if cur and (sum(len(x[0]) + 1 for x in cur) + len(w) > 20 or cur[-1][0][-1] in ".?!:…"):
                lines.append(cur)
                cur = []
            cur.append((w, wt))
        lines.append(cur)
        current = [ln for ln in lines if ln[0][1] <= t]
        if not current:
            return
        line = current[-1]
        p = fx.ease_back(fx.prog(t, line[0][1], 0.16))
        widths = [F_CAP.getlength(w) for w, _ in line]
        space = F_CAP.getlength(" ")
        x = (W - sum(widths) - space * (len(line) - 1)) / 2
        y = 1400 + (1 - p) * 40
        for (w, wt), wd in zip(line, widths):
            said = t >= wt
            for ox, oy in ((5, 6), (-2, 3)):
                fx.draw_text(img, w, F_CAP, y + oy, 0.6 if said else 0.2, x=x + ox, anchor="left", color=fx.BG)
            fx.draw_text(img, w, F_CAP, y, 1.0 if said else 0.3, x=x, anchor="left", gradient=said and t < wt + 0.3)
            x += wd + space


# ---------------------------------------------------------------- scènes
def scene_pov(t):
    img = Image.new("RGBA", (W, H), (4, 4, 8, 255))
    a = fx.window(t, 0.1, POV_IN + 3.0, 0.1, 0.2)
    flick = 1.0 if random.Random(int(t * 30)).random() > 0.08 else 0.3
    fx.slam(img, "POV", fx.F_MEGA, 860, t, 0.1, 3.0, gradient=True, tracking=-8)
    fx.draw_text(img, "17 OCTOBRE · 15H30", fx.F_TAG, 1080, a * flick, tracking=10)
    return img


def scene_stop(t):
    # image figée du rayon, qui se vide de ses couleurs
    img, total = aisle_frame(AISLE_LEN)
    k = fx.prog(t, STOP, 0.6)
    rgb = ImageEnhance.Color(img.convert("RGB")).enhance(1 - 0.9 * k)
    img = rgb.convert("RGBA")
    img.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, int(150 * k))))
    fx.slam(img, "STOP.", fx.F_HUGE, 900, t, STOP + 0.1, REWIND, color=RED, tracking=-6)
    draw_hud(img, t, total)
    return img


def scene_rewind(t):
    k = fx.prog(t, REWIND, REALITY - REWIND)
    tl = AISLE_LEN * (1 - fx.ease_in_out(k))
    img, total = aisle_frame(tl, rewind=True)
    rgb = img.convert("RGB")
    r, g, b = rgb.split()
    rgb = Image.merge("RGB", (ImageChops.offset(r, 10, 0), g, ImageChops.offset(b, -10, 0)))
    rgb = ImageEnhance.Color(rgb).enhance(0.55)
    # bandes de déchirure VHS
    rnd = random.Random(int(t * FPS))
    for _ in range(3):
        y0 = rnd.randrange(0, H - 80)
        band = rgb.crop((0, y0, W, y0 + rnd.randint(20, 80)))
        rgb.paste(band, (rnd.randint(-60, 60), y0))
    img = rgb.convert("RGBA")
    img.alpha_composite(SCANLINES)
    draw_hud(img, t, total, rewind=True)
    return img


def scene_repair(t, frame, o0, o1):
    img = graded(frame, t, o0, o1)
    img.alpha_composite(fx.VIGNETTE)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    # éclats qui reviennent se coller (éclatement joué à l'envers)
    dt = 1.1 * (1 - fx.ease_out(fx.prog(t, REPAIR + 0.4, 1.6)))
    if dt > 0.001:
        fx.GLASS.draw_shatter(layer, dt)
    else:
        # vitre neuve : reflet qui balaie
        g = fx.prog(t, REPAIR + 2.1, 0.9)
        if 0 < g < 1:
            d = ImageDraw.Draw(layer)
            x = -400 + g * (W + 800)
            d.polygon([(x, 0), (x + 160, 0), (x - 500, H), (x - 660, H)], fill=(255, 255, 255, 70))
        d = ImageDraw.Draw(layer)
        d.rectangle((40, 280, W - 40, H - 330), outline=fx.CYAN + (int(160 * fx.window(t, REPAIR + 2.0, END, 0.3, 0.3)),), width=4)
    img.alpha_composite(layer)
    img.alpha_composite(SHADE)
    return img


def scene_end(t):
    img = Image.new("RGBA", (W, H), fx.BG + (255,))
    fx.background(img, t)
    lt = t - END
    a = fx.ease_out(fx.prog(lt, 0.0, 0.5))
    fx.draw_map(img, 540, 1250, 520, fill_a=0.22 * a, line_a=0.6 * a, glow=a)
    img.alpha_composite(fx.faded(fx.LOGO, a), ((W - fx.LOGO.width) // 2, int(470 + (1 - a) * 60)))
    fx.draw_text(img, "soutient les commerçants de France", fx.F_M, 860, fx.ease_out(fx.prog(lt, 0.4, 0.4)))
    fx.draw_text(img, "Une vidéo pour votre réouverture ?", fx.F_M, 1620, fx.ease_out(fx.prog(lt, 1.0, 0.4)), gradient=True)
    fx.draw_text(img, "Écrivez-nous.", fx.F_M, 1700, fx.ease_out(fx.prog(lt, 1.2, 0.4)), gradient=True)
    fx.draw_text(img, "#SoutienAuxCommerçants  #PiwaStudio", fx.F_XS, 1790, fx.ease_out(fx.prog(lt, 1.6, 0.4)), color=fx.MUTE)
    fx.draw_text(img, CREDIT, F_CREDIT, H - 40, 0.6, color=fx.MUTE)
    img.alpha_composite(fx.VIGNETTE)
    return img


CUTS = [NICO_IN, NICO_SHELF, SEPHORA, AISLE, STOP, REWIND, REALITY] + [s[0] for s in SEGMENTS[4:]] + [END]


def post(rgb, t):
    e = 0.0
    for c in CUTS:
        if t >= c:
            e = max(e, math.exp(-(t - c) * 12))
    beat = 60 / 128
    pulse = math.exp(-((t - AISLE) % beat) * 12) if AISLE <= t < STOP else 0.0
    if e < 0.05 and pulse < 0.05:
        return rgb
    if e > 0.4:
        r, g, b = rgb.split()
        s = int(20 * e)
        rgb = Image.merge("RGB", (ImageChops.offset(r, s, 0), g, ImageChops.offset(b, -s, 0)))
    rnd = random.Random(int(t * FPS))
    rgb = zoom_to(rgb, 1 + 0.05 * e + 0.025 * pulse, W / 2 + rnd.uniform(-1, 1) * 25 * e, H / 2 + rnd.uniform(-1, 1) * 25 * e)
    if e > 0.75:
        rgb = Image.blend(rgb, Image.new("RGB", (W, H), (255, 255, 255)), (e - 0.75) * 0.8)
    return rgb


def frame_at(t, clips):
    if t < NICO_IN:
        img = scene_pov(t)
    elif t < AISLE:
        frame, o0, o1 = clips.at(t)
        img = graded(frame, t, o0, o1)
        img.alpha_composite(fx.VIGNETTE)
        img.alpha_composite(SHADE)
        if NICO_SHELF <= t < SEPHORA:  # bouteilles attrapées chez le caviste
            d = ImageDraw.Draw(img)
            for k in range(3):
                tp = NICO_SHELF + 0.2 + k * 0.45
                if t >= tp:
                    q = fx.prog(t, tp, 0.5)
                    sx = 300 + k * 240
                    x = sx + (540 - sx) * fx.ease_out(q)
                    y = 900 + (2100 - 900) * fx.ease_out(q) - 300 * math.sin(math.pi * q)
                    w = 40 * (1 + 2 * q)
                    d.rounded_rectangle((x - w, y - 4 * w, x + w, y), radius=w * 0.5, fill=(60, 20, 40, 255), outline=(255, 255, 255, 140), width=3)
                    d.rectangle((x - w * 0.35, y - 5.2 * w, x + w * 0.35, y - 4 * w), fill=GOLD + (255,))
                    fx.draw_text(img, "+ 45 €", F_TAG, 800 - 120 * q, fx.clamp(1.4 - q), x=sx, color=GOLD)
        draw_hud(img, t, None)
    elif t < STOP:
        img, total = aisle_frame(t - AISLE)
        img.alpha_composite(fx.VIGNETTE)
        draw_hud(img, t, total)
    elif t < REWIND:
        img = scene_stop(t)
    elif t < REALITY:
        img = scene_rewind(t)
    elif t < REPAIR:
        frame, o0, o1 = clips.at(t)
        img = graded(frame, t, o0, o1, cold=True)
        img.alpha_composite(fx.VIGNETTE)
        img.alpha_composite(SHADE)
    elif t < END:
        frame, o0, o1 = clips.at(t)
        img = scene_repair(t, frame, o0, o1)
    else:
        img = scene_end(t)
    if NICO_IN <= t < END:
        fx.draw_text(img, CREDIT, F_CREDIT, H - 70, 0.7)
    draw_subtitles(img, t)
    return post(img.convert("RGB"), t)


# ---------------------------------------------------------------- musique
SR = 44100


def music():
    n = int(DURATION * SR)
    out = np.zeros(n)
    rng = np.random.default_rng(3)
    tt = np.arange(n) / SR

    def add(sig, at, gain=1.0):
        i = int(at * SR)
        j = min(n, i + len(sig))
        if 0 <= i < n:
            out[i:j] += sig[: j - i] * gain

    def env_exp(dur, k):
        return np.exp(-np.arange(int(dur * SR)) / SR * k)

    def kick():
        d = np.arange(int(0.45 * SR)) / SR
        return np.sin(2 * np.pi * np.cumsum(45 + 120 * np.exp(-d * 30)) / SR) * np.exp(-d * 7)

    def clap():
        s = np.diff(rng.standard_normal(int(0.18 * SR)), prepend=0)
        return s * env_exp(0.18, 22)

    def hat():
        return np.diff(rng.standard_normal(int(0.05 * SR)), prepend=0) * env_exp(0.05, 90)

    def bass(f, dur):
        d = np.arange(int(dur * SR)) / SR
        return (np.sin(2 * np.pi * f * d) + 0.3 * np.sin(4 * np.pi * f * d)) * np.exp(-d * 3)

    def chord(freqs, dur, k=0.8):
        d = np.arange(int(dur * SR)) / SR
        return sum(np.sin(2 * np.pi * f * d) * (1 + 0.3 * np.sin(2 * np.pi * 5 * d)) for f in freqs) * np.exp(-d * k)

    beat = 60 / 128
    # intro POV : battements de cœur + nappe sombre
    for b in np.arange(0.3, NICO_IN, 0.75):
        add(kick(), b, 0.5)
        add(kick(), b + 0.22, 0.3)
    drone = np.sin(2 * np.pi * 41.2 * tt) + 0.5 * np.sin(2 * np.pi * 61.7 * tt)
    out += drone * ((tt < STOP) * np.clip(tt / 1.5, 0, 1)) * 0.06
    # montée : vitrines puis rayon (128 BPM, basse qui bouge)
    notes = [41.2, 41.2, 49.0, 55.0]
    b, k = NICO_IN, 0
    while b < STOP:
        add(kick(), b, 0.9)
        add(hat(), b + beat / 2, 0.10)
        if b >= SEPHORA:
            add(hat(), b + beat / 4, 0.05)
            add(hat(), b + 3 * beat / 4, 0.05)
        if b >= AISLE and k % 2 == 1:
            add(clap(), b, 0.35)
        add(bass(notes[(k // 4) % 4], beat * 0.9), b, 0.35)
        b += beat
        k += 1
    # « ding » de caisse sur chaque produit attrapé
    for tp, *_ in PICKS:
        d = np.arange(int(0.3 * SR)) / SR
        add((np.sin(2 * np.pi * 1760 * d) + 0.5 * np.sin(2 * np.pi * 2640 * d)) * np.exp(-d * 14), AISLE + tp, 0.05)
    # montée de bruit avant le STOP
    d = np.arange(int(3 * SR)) / SR
    add(rng.standard_normal(len(d)) * (d / 3) ** 3, STOP - 3, 0.2)
    # STOP : arrêt de bande (la dernière seconde ralentit et descend)
    seg = out[int((STOP - 1.0) * SR):int(STOP * SR)].copy()
    speed = np.linspace(1.0, 0.0, len(seg)) ** 1.5
    pos = np.cumsum(speed)
    stop_sig = np.interp(pos, np.arange(len(seg)), seg)
    out[int(STOP * SR) - len(seg):int(STOP * SR)] = 0
    add(stop_sig, STOP - 1.0, 1.0)
    d = np.arange(int(1.6 * SR)) / SR
    boom = np.sin(2 * np.pi * (38 + 40 * np.exp(-d * 6)) * d) * np.exp(-d * 2.5)
    add(boom, STOP + 0.1, 0.9)
    # REWIND : la musique du rayon jouée à l'envers, accélérée
    src = out[int(AISLE * SR):int(STOP * SR)][::-1]
    rew = np.interp(np.arange(0, len(src), 2.0), np.arange(len(src)), src)
    rew = rew[: int((REALITY - REWIND) * SR)]
    add(np.convolve(rew, np.ones(6) / 6, mode="same"), REWIND, 0.8)
    # réalité : accords lents et doux
    for i, fs in enumerate([(220, 261.6, 329.6), (174.6, 220, 261.6), (196, 246.9, 293.7), (164.8, 207.7, 246.9)]):
        add(chord(fs, 3.0, 0.7), REALITY + i * 2.0, 0.06)
        add(bass(fs[0] / 4, 2.0), REALITY + i * 2.0, 0.25)
    # réparation : verre à l'envers puis reprise du rythme
    glass = np.diff(rng.standard_normal(int(1.4 * SR)), prepend=0) * env_exp(1.4, 3.5)
    add(glass[::-1], REPAIR + 0.4 - 0.2, 0.4)
    b = REPAIR + 2.0
    while b < DURATION - 0.5:
        add(kick(), b, 0.7)
        add(hat(), b + beat / 2, 0.08)
        b += beat
    add(chord((220, 277.18, 329.63, 440), 6.0, 0.5), END, 0.07)
    add(boom, END, 0.8)

    out = np.tanh(out * 1.3)
    fade = np.clip((DURATION - tt) / 1.5, 0, 1)
    out = out * fade / np.max(np.abs(out)) * 0.9
    return (out * 32767).astype(np.int16)


def write_music(path):
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(music().tobytes())


def main():
    args = sys.argv[1:]
    music_out = None
    if "--music" in args:
        i = args.index("--music")
        music_out = Path(args[i + 1])
        del args[i:i + 2]
    src = Path(args[0])
    with tempfile.TemporaryDirectory() as tmp:
        clips = Clips(src, tmp)
        if "--preview" in args:
            i = args.index("--preview")
            out = Path(args[i + 1])
            out.mkdir(parents=True, exist_ok=True)
            for t in [float(x) for x in args[i + 2].split(",")]:
                frame_at(t, clips).save(out / f"frame_{t:05.1f}.png")
            return
        wav = music_out or Path(tmp) / "musique.wav"
        write_music(wav)
        ff = subprocess.Popen([
            "ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
            "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", str(wav),
            "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", args[1],
        ], stdin=subprocess.PIPE)
        total = int(DURATION * FPS)
        for k in range(total):
            ff.stdin.write(frame_at(k / FPS, clips).tobytes())
            if k % 300 == 0:
                print(f"{k}/{total}", flush=True)
        ff.stdin.close()
        ff.wait()


if __name__ == "__main__":
    main()
