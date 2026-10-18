"""PIWA Studio — « France, 17 octobre » : motion design vertical (1080x1920, 46 s) avec bande-son.

Rendu image par image avec Pillow, son synthétisé avec numpy, encodé en MP4 par ffmpeg.
    python3 motion/france-17-octobre/render.py [sortie.mp4] [--clips dossier] [--preview dossier t1,t2,...]

Avec --clips, les vidéos trouvées dans le dossier passent en plein écran sous le motion design :
paris.mp4, marseille.mp4, lyon.mp4, bordeaux.mp4, rennes.mp4, poitiers.mp4, chambery.mp4
(une par ville) et casse1.mp4 … casse4.mp4 (une par phrase choc). Les fichiers absents sont
remplacés par l'animation seule. N'utiliser que des images dont on détient les droits.
"""
import math
import random
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageFont

W, H, FPS, DURATION = 1080, 1920, 30, 60.0
SPEED = 1.3  # la timeline est écrite sur 60 s puis jouée en accéléré
OUT_DURATION = DURATION / SPEED
ROOT = Path(__file__).resolve().parents[2]
FONT_DIR = Path("/usr/share/fonts/opentype/inter")

BG = (6, 7, 10)
FG = (244, 245, 250)
MUTE = (141, 147, 168)
CYAN, VIOLET, PINK = (34, 211, 238), (139, 92, 246), (244, 114, 182)
GRAD = [CYAN, VIOLET, PINK]  # charte PIWA


def font(weight, size):
    return ImageFont.truetype(str(FONT_DIR / f"InterDisplay-{weight}.otf"), size)


# ---------------------------------------------------------------- easing / temps
def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def prog(t, start, dur):
    return clamp((t - start) / dur)


def ease_out(x):
    return 1 - (1 - x) ** 3


def ease_back(x):
    c = 1.9
    return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2


def ease_in_out(x):
    return 4 * x ** 3 if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2


def window(t, start, end, fade_in=0.3, fade_out=0.3):
    """Opacité d'un élément visible entre start et end."""
    return min(ease_out(prog(t, start, fade_in)), 1 - prog(t, end - fade_out, fade_out))


# ---------------------------------------------------------------- calques fixes
def lerp_color(a, b, x):
    return tuple(int(a[i] + (b[i] - a[i]) * x) for i in range(3))


def grad_color(u):
    u = clamp(u)
    return lerp_color(GRAD[0], GRAD[1], u * 2) if u < 0.5 else lerp_color(GRAD[1], GRAD[2], (u - 0.5) * 2)


def make_gradient(w, h):
    g = Image.new("RGB", (w, h))
    px = g.load()
    for x in range(w):
        for y in range(h):
            px[x, y] = grad_color(x / w * 0.75 + y / h * 0.25)
    return g


GRADIENT = make_gradient(W, 400)
GRADIENT_FULL = GRADIENT.resize((W, H))


def make_glow(color, radius):
    size = radius * 2
    g = Image.new("L", (size, size), 0)
    ImageDraw.Draw(g).ellipse((radius // 2, radius // 2, size - radius // 2, size - radius // 2), fill=255)
    g = g.filter(ImageFilter.GaussianBlur(radius // 3))
    layer = Image.new("RGBA", (size, size), color + (0,))
    layer.putalpha(g)
    return layer


def faded(layer, a):
    out = layer.copy()
    out.putalpha(out.getchannel("A").point(lambda p: int(p * a)))
    return out


GLOW_VIOLET = make_glow(VIOLET, 700)
GLOW_CYAN = make_glow(CYAN, 600)
GLOW_RED = make_glow((239, 68, 68), 650)
GLOW_BLUE = make_glow((59, 130, 246), 650)
PIN_GLOW = make_glow(PINK, 90)


def make_vignette():
    v = Image.new("L", (W, H), 0)
    ImageDraw.Draw(v).ellipse((-300, -200, W + 300, H + 200), fill=255)
    v = v.filter(ImageFilter.GaussianBlur(220))
    dark = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dark.putalpha(v.point(lambda p: int((255 - p) * 0.75)))
    return dark


VIGNETTE = make_vignette()

logo = Image.open(ROOT / "piwa" / "logo-piwa-ai-sombre.png").convert("RGB")
LOGO = logo.resize((820, int(820 * logo.height / logo.width)), Image.LANCZOS).convert("RGBA")
# détourage : le fond sombre du logo devient transparent
LOGO.putalpha(LOGO.convert("L").point(lambda p: int(clamp((p - 12) * 6, 0, 255))))


# ---------------------------------------------------------------- texte
_mask_cache = {}


def text_mask(text, fnt, tracking=0):
    key = (text, fnt.path, fnt.size, tracking)
    if key not in _mask_cache:
        widths = [fnt.getlength(ch) + tracking for ch in text] if tracking else None
        w = int(sum(widths)) if tracking else int(fnt.getlength(text))
        asc, desc = fnt.getmetrics()
        m = Image.new("L", (max(w, 1) + 4, asc + desc + 4), 0)
        d = ImageDraw.Draw(m)
        if tracking:
            x = 0
            for ch, cw in zip(text, widths):
                d.text((x, 0), ch, font=fnt, fill=255)
                x += cw
        else:
            d.text((0, 0), text, font=fnt, fill=255)
        _mask_cache[key] = m
    return _mask_cache[key]


def draw_text(img, text, fnt, y, alpha=1.0, color=FG, x=None, dy=0, dx=0, gradient=False, tracking=0,
              anchor="center", scale=1.0):
    if alpha <= 0.01:
        return
    m = text_mask(text, fnt, tracking)
    if abs(scale - 1) > 0.01:
        m = m.resize((max(1, int(m.width * scale)), max(1, int(m.height * scale))), Image.BILINEAR)
    if alpha < 1:
        m = m.point(lambda p: int(p * alpha))
    if x is None:
        px = (W - m.width) // 2
    elif anchor == "left":
        px = int(x)
    else:
        px = int(x - m.width / 2)
    px += int(dx)
    py = int(y + dy - m.height / 2)
    if gradient:
        img.paste(GRADIENT_FULL.crop((px, py, px + m.width, py + m.height)), (px, py), m)
    else:
        img.paste(color, (px, py, px + m.width, py + m.height), m)


def slam(img, text, fnt, y, t, start, end, gradient=False, tracking=-4, color=FG):
    """Mot qui arrive en gros plan et se pose avec un rebond."""
    p = prog(t, start, 0.28)
    a = window(t, start, end, 0.08, 0.15)
    draw_text(img, text, fnt, y, a, scale=1.0 + (1 - ease_back(p)) * 0.9 if p < 1 else 1.0,
              gradient=gradient, tracking=tracking, color=color)


def reveal_lines(img, lines, t, start, end, y0, step, stagger=0.15, rise=70):
    """Lignes (texte, police, options) qui montent l'une après l'autre."""
    for i, (txt, fnt, opts) in enumerate(lines):
        s = start + i * stagger
        a = window(t, s, end, 0.25, 0.25)
        dy = (1 - ease_out(prog(t, s, 0.4))) * rise
        draw_text(img, txt, fnt, y0 + i * step, a, dy=dy, **opts)


# ---------------------------------------------------------------- verre brisé
class Glass:
    """Impact, fissures radiales puis éclatement en éclats qui tombent."""

    def __init__(self, cx, cy, seed=7, rays=18, rings=(0, 70, 170, 320, 520, 800, 1150, 1700)):
        rnd = random.Random(seed)
        self.cx, self.cy = cx, cy
        angles = sorted(i * 2 * math.pi / rays + rnd.uniform(-0.12, 0.12) for i in range(rays))
        pts = [[(cx, cy)] * rays]
        for r in rings[1:]:
            row = []
            for a in angles:
                rr = r * rnd.uniform(0.85, 1.15)
                aa = a + rnd.uniform(-0.05, 0.05)
                row.append((cx + rr * math.cos(aa), cy + rr * math.sin(aa)))
            pts.append(row)
        self.pts, self.rays, self.rings = pts, rays, rings
        self.shards = []
        for ri in range(len(pts) - 1):
            for ai in range(rays):
                bj = (ai + 1) % rays
                poly = [pts[ri][ai], pts[ri][bj], pts[ri + 1][bj], pts[ri + 1][ai]]
                gx = sum(p[0] for p in poly) / 4
                gy = sum(p[1] for p in poly) / 4
                ang = math.atan2(gy - cy, gx - cx)
                speed = rnd.uniform(700, 1600)
                self.shards.append({
                    "poly": poly, "c": (gx, gy),
                    "v": (math.cos(ang) * speed, math.sin(ang) * speed - rnd.uniform(200, 700)),
                    "spin": rnd.uniform(-6, 6), "delay": rnd.uniform(0, 0.08),
                    "shade": rnd.randint(18, 60),
                })

    def draw_cracks(self, layer, growth, alpha):
        d = ImageDraw.Draw(layer)
        col = (235, 240, 255, int(220 * alpha))
        max_r = self.rings[-1]
        for ai in range(self.rays):
            for ri in range(len(self.pts) - 1):
                if self.rings[ri] > growth * max_r:
                    break
                a, b = self.pts[ri][ai], self.pts[ri + 1][ai]
                f = clamp((growth * max_r - self.rings[ri]) / max(1, self.rings[ri + 1] - self.rings[ri]))
                d.line([a, (a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f)], fill=col, width=3 if ri < 2 else 2)
        for ri in range(1, len(self.pts) - 1):
            if self.rings[ri] < growth * max_r * 0.8:
                d.line(self.pts[ri] + [self.pts[ri][0]], fill=(235, 240, 255, int(140 * alpha)), width=2)
        d.ellipse((self.cx - 14, self.cy - 14, self.cx + 14, self.cy + 14), fill=(255, 255, 255, int(255 * alpha)))

    def draw_shatter(self, layer, dt):
        d = ImageDraw.Draw(layer)
        for s in self.shards:
            tt = max(0.0, dt - s["delay"])
            ox = s["v"][0] * tt
            oy = s["v"][1] * tt + 0.5 * 2600 * tt * tt
            rot = s["spin"] * tt
            cos, sin = math.cos(rot), math.sin(rot)
            gx, gy = s["c"]
            poly = []
            for px, py in s["poly"]:
                rx, ry = px - gx, py - gy
                poly.append((gx + ox + rx * cos - ry * sin, gy + oy + rx * sin + ry * cos))
            a = clamp(1 - tt / 1.1)
            if a > 0:
                d.polygon(poly, fill=(200, 215, 255, int(s["shade"] * a)), outline=(240, 245, 255, int(230 * a)))


def mini_crack(layer, cx, cy, size, growth, alpha, seed):
    rnd = random.Random(seed)
    d = ImageDraw.Draw(layer)
    for i in range(9):
        a = i * 2 * math.pi / 9 + rnd.uniform(-0.3, 0.3)
        r = size * rnd.uniform(0.5, 1.0) * growth
        mid = (cx + r * 0.5 * math.cos(a + rnd.uniform(-0.2, 0.2)), cy + r * 0.5 * math.sin(a + rnd.uniform(-0.2, 0.2)))
        d.line([(cx, cy), mid, (cx + r * math.cos(a), cy + r * math.sin(a))], fill=(240, 244, 255, int(200 * alpha)), width=2)
    d.ellipse((cx - 8, cy - 8, cx + 8, cy + 8), fill=(255, 255, 255, int(230 * alpha)))


GLASS = Glass(540, 900)


# ---------------------------------------------------------------- carte de France
# contour simplifié de la métropole (longitude, latitude)
FRANCE = [
    (2.55, 51.08), (1.85, 50.95), (1.6, 50.7), (1.55, 50.2), (0.1, 49.5), (-0.4, 49.3), (-1.25, 49.7),
    (-1.9, 49.7), (-1.6, 48.8), (-1.5, 48.65), (-2.0, 48.65), (-3.0, 48.8), (-4.0, 48.7), (-4.75, 48.35),
    (-4.4, 48.0), (-3.9, 47.85), (-3.4, 47.7), (-3.1, 47.5), (-2.2, 47.25), (-2.0, 46.9), (-1.8, 46.5),
    (-1.2, 46.15), (-1.05, 45.6), (-1.25, 44.65), (-1.4, 44.0), (-1.55, 43.48), (-1.78, 43.36), (-1.0, 43.0),
    (0.0, 42.8), (0.7, 42.85), (1.4, 42.6), (2.2, 42.43), (3.17, 42.45), (3.05, 42.8), (3.2, 43.2),
    (3.6, 43.4), (4.0, 43.55), (4.6, 43.4), (5.35, 43.3), (5.95, 43.1), (6.6, 43.2), (7.25, 43.7),
    (7.5, 43.78), (7.0, 44.2), (6.9, 44.5), (7.05, 45.0), (6.8, 45.15), (7.1, 45.5), (6.8, 45.85),
    (6.1, 46.15), (6.0, 46.4), (6.4, 46.7), (6.9, 47.4), (7.55, 47.6), (7.6, 48.1), (7.8, 48.6),
    (8.2, 48.97), (7.4, 49.15), (6.7, 49.15), (6.1, 49.47), (5.5, 49.5), (4.85, 49.8), (4.85, 50.1),
    (4.2, 49.95), (3.7, 50.3), (3.2, 50.75),
]
CITIES = [
    ("PARIS", (2.35, 48.86)),
    ("MARSEILLE", (5.37, 43.30)),
    ("LYON", (4.84, 45.76)),
    ("BORDEAUX", (-0.58, 44.84)),
    ("RENNES", (-1.68, 48.11)),
    ("POITIERS", (0.34, 46.58)),
    ("CHAMBÉRY", (5.92, 45.57)),
]
_K = math.cos(math.radians(46.5))
_xs = [p[0] * _K for p in FRANCE]
_ys = [-p[1] for p in FRANCE]
_MX, _MY = (min(_xs) + max(_xs)) / 2, (min(_ys) + max(_ys)) / 2
_SPAN = max(max(_xs) - min(_xs), max(_ys) - min(_ys))


def project(lon, lat, cx, cy, size):
    return cx + (lon * _K - _MX) / _SPAN * size, cy + (-lat - _MY) / _SPAN * size


def draw_map(img, cx, cy, size, draw_p=1.0, fill_a=0.0, line_a=1.0, glow=0.0):
    pts = [project(lon, lat, cx, cy, size) for lon, lat in FRANCE]
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    if fill_a > 0:
        m = Image.new("L", (W, H), 0)
        ImageDraw.Draw(m).polygon(pts, fill=int(255 * fill_a))
        layer.paste(GRADIENT_FULL.convert("RGBA"), (0, 0), m)
    d = ImageDraw.Draw(layer)
    if glow > 0:
        d.polygon(pts, fill=(139, 92, 246, int(40 * glow)))
    seg = list(zip(pts, pts[1:] + pts[:1]))
    lens = [math.dist(a, b) for a, b in seg]
    target = sum(lens) * draw_p
    acc = 0.0
    for (a, b), ln in zip(seg, lens):
        if acc >= target:
            break
        f = clamp((target - acc) / ln)
        end = (a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f)
        u = acc / sum(lens)
        d.line([a, end], fill=grad_color(u) + (int(255 * line_a),), width=6)
        acc += ln
    img.alpha_composite(layer)


def draw_pin(img, x, y, t, start, alpha=1.0):
    if t < start or alpha <= 0:
        return
    p = ease_back(prog(t, start, 0.35))
    d = ImageDraw.Draw(img)
    for k in range(2):  # ondes
        rt = ((t - start) * 0.9 + k * 0.5) % 1.0
        r = 20 + rt * 110
        d.ellipse((x - r, y - r, x + r, y + r), outline=PINK + (int(200 * (1 - rt) * alpha),), width=4)
    img.alpha_composite(faded(PIN_GLOW, alpha), (int(x - 90), int(y - 90)))
    r = 16 * p
    d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 255, 255, int(255 * alpha)))


# ---------------------------------------------------------------- planches de bois
def draw_planks(img, t, start, y_top, y_bottom, alpha=1.0):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    rnd = random.Random(3)
    n = 5
    h = (y_bottom - y_top) / n
    for i in range(n):
        p = ease_back(prog(t, start + i * 0.12, 0.4))
        base = (rnd.randint(120, 150), rnd.randint(82, 100), rnd.randint(52, 64))
        jit = [rnd.uniform(-4, 4) for _ in range(12)]
        if p <= 0:
            continue
        x0 = -W * (1 - p) if i % 2 == 0 else W * (1 - p)
        y = y_top + i * h
        box = (x0 + 90, y + 4, x0 + W - 90, y + h - 4)
        d.rounded_rectangle(box, radius=6, fill=base + (int(255 * alpha),))
        for k in range(6):
            yy = box[1] + (k + 1) * (h - 8) / 7 + jit[k]
            d.line([(box[0] + 10, yy), (box[2] - 10, yy + jit[k + 6] * 0.7)],
                   fill=(base[0] - 25, base[1] - 22, base[2] - 16, int(160 * alpha)), width=2)
        for sx in (box[0] + 30, box[2] - 30):
            cy = (box[1] + box[3]) / 2
            d.ellipse((sx - 7, cy - 7, sx + 7, cy + 7), fill=(70, 72, 80, int(255 * alpha)))
    img.alpha_composite(layer)


# ---------------------------------------------------------------- vidéos importées
class ClipBank:
    """Extrait chaque vidéo en images 1080x1920 (recadrage plein écran) et les sert à la demande."""

    def __init__(self):
        self.dir = None
        self.tmp = None
        self.frames = {}

    def get(self, name, t_in):
        if self.dir is None:
            return None
        if name not in self.frames:
            src = next((self.dir / f"{name}{ext}" for ext in (".mp4", ".mov", ".webm", ".mkv")
                        if (self.dir / f"{name}{ext}").exists()), None)
            files = []
            if src:
                out = Path(self.tmp) / name
                out.mkdir(parents=True, exist_ok=True)
                subprocess.run([
                    "ffmpeg", "-loglevel", "error", "-y", "-i", str(src), "-t", "4",
                    "-vf", f"fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}",
                    "-q:v", "3", str(out / "%04d.jpg"),
                ], check=True)
                files = sorted(out.glob("*.jpg"))
            self.frames[name] = files
        files = self.frames[name]
        if not files:
            return None
        return files[min(len(files) - 1, int(t_in / SPEED * FPS))]


CLIPS = ClipBank()


def draw_clip(img, name, t, start, end):
    """Vidéo plein écran, assombrie et teintée aux couleurs PIWA, avec léger zoom."""
    path = CLIPS.get(name, max(0.0, t - start))
    if path is None:
        return False
    fr = Image.open(path).convert("RGB")
    z = 1.0 + 0.10 * prog(t, start, end - start)
    fr = fr.resize((int(W * z), int(H * z)), Image.BILINEAR)
    fr = fr.crop(((fr.width - W) // 2, (fr.height - H) // 2, (fr.width - W) // 2 + W, (fr.height - H) // 2 + H))
    fr = ImageEnhance.Contrast(ImageEnhance.Color(fr).enhance(0.7)).enhance(1.25)
    fr = Image.blend(fr, GRADIENT_FULL, 0.18)
    fr = Image.blend(fr, Image.new("RGB", (W, H), BG), 0.45)
    a = window(t, start, end, 0.06, 0.06)
    img.alpha_composite(faded(fr.convert("RGBA"), a))
    # bandes sombres haut et bas pour garder le texte lisible
    shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(shade)
    for y in range(0, 620, 8):
        d.rectangle((0, y, W, y + 8), fill=BG + (int(200 * (1 - y / 620) * a),))
        d.rectangle((0, H - y - 8, W, H - y), fill=BG + (int(150 * (1 - y / 620) * a),))
    img.alpha_composite(shade)
    return True


def clip_name(city):
    return city.lower().replace("é", "e")


# ---------------------------------------------------------------- timeline
F_MEGA = font("Black", 360)
F_HUGE = font("Black", 260)
F_BIG = font("Black", 150)
F_XL = font("Black", 112)
F_L = font("ExtraBold", 84)
F_M = font("Bold", 64)
F_S = font("SemiBold", 44)
F_XS = font("Medium", 32)
F_TAG = font("SemiBold", 34)

SHATTER = 3.0
CITY_START, CITY_STEP = 19.0, 1.5
BEATS = [
    (36.5, ["Vitrines", "brisées."]),
    (38.0, ["Rideaux", "arrachés."]),
    (39.5, ["Boutiques", "incendiées."]),
    (41.0, ["Des commerçants", "à terre."]),
]
# instants d'impact : tremblement, glitch et coups dans la bande-son
HITS = ([SHATTER, 4.2, 8.2, 13.2, 16.3] + [CITY_START + i * CITY_STEP for i in range(len(CITIES))]
        + [30.0] + [b[0] for b in BEATS] + [43.6, 47.6, 51.0, 54.6])


def fmt_int(n):
    return f"{n:,}".replace(",", " ")


def background(img, t):
    x = int(-500 + 260 * math.sin(t * 0.35))
    y = int(-300 + 200 * math.cos(t * 0.3))
    img.alpha_composite(GLOW_VIOLET, (x, y))
    img.alpha_composite(GLOW_CYAN, (int(W - 700 + 220 * math.cos(t * 0.4)), int(H - 900 + 160 * math.sin(t * 0.33))))
    siren = window(t, 16.0, 43.5, 0.8, 0.8)
    if siren > 0:  # gyrophares
        phase = (math.sin(t * 11) + 1) / 2
        img.alpha_composite(faded(GLOW_RED, siren * phase * 0.9), (-650, 250))
        img.alpha_composite(faded(GLOW_BLUE, siren * (1 - phase) * 0.9), (W - 650, 250))


def scene_intro(img, t):  # 0 – 4.2 s
    if t >= 4.4:
        return
    draw_text(img, "SAMEDI", F_TAG, 560, window(t, 0.6, 4.2, 0.3, 0.2), color=MUTE, tracking=10)
    slam(img, "17.10", F_MEGA, 880, t, 0.3, 4.2, gradient=True, tracking=-10)
    draw_text(img, "Une journée. Tout un pays.", F_M, 1140, window(t, 1.2, 4.2, 0.3, 0.2))
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    if t < SHATTER:
        GLASS.draw_cracks(layer, ease_out(prog(t, 1.6, 0.9)), 1.0 if t >= 1.6 else 0.0)
    else:
        GLASS.draw_shatter(layer, t - SHATTER)
    img.alpha_composite(layer)


def scene_country(img, t):  # 4.2 – 16 s
    if not 4.0 <= t < 16.3:
        return
    a = window(t, 4.2, 16.0, 0.2, 0.3)
    draw_map(img, 540, 1080, 820, draw_p=ease_in_out(prog(t, 4.2, 2.0)), line_a=a * (0.35 if t > 8 else 1.0),
             fill_a=0.0, glow=a * 0.6)
    slam(img, "LA FRANCE", F_BIG, 300, t, 4.2, 8.0, gradient=True)
    draw_text(img, "descend dans la rue", F_L, 440, window(t, 4.6, 8.0), dy=(1 - ease_out(prog(t, 4.6, 0.4))) * 60)
    n = int(550000 * ease_out(prog(t, 8.2, 1.6)))
    slam(img, fmt_int(n), F_HUGE, 900, t, 8.2, 12.9, gradient=True, tracking=-10)
    draw_text(img, "manifestants", F_L, 1110, window(t, 8.6, 12.9), dy=(1 - ease_out(prog(t, 8.6, 0.4))) * 50)
    draw_text(img, "selon les autorités", F_XS, 1190, window(t, 9.0, 12.9), color=MUTE)
    slam(img, "CONTRE", F_BIG, 820, t, 13.2, 16.0)
    slam(img, "LA VIE CHÈRE.", F_XL, 980, t, 13.5, 16.0, gradient=True)


def scene_cut(img, t):  # 16.3 – 19 s
    if not 16.3 <= t < 19.0:
        return
    reveal_lines(img, [
        ("Mais en marge", F_XL, {}),
        ("des cortèges…", F_XL, {"gradient": True}),
    ], t, 16.3, 18.9, 860, 140)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for i, (cx, cy) in enumerate([(180, 420), (880, 560), (160, 1460), (900, 1380)]):
        s = 16.9 + i * 0.4
        if t >= s:
            mini_crack(layer, cx, cy, 170, ease_out(prog(t, s, 0.2)), window(t, s, 18.9, 0.05), seed=i + 11)
    img.alpha_composite(layer)


def scene_cities(img, t):  # 19 – 30 s
    end = CITY_START + CITY_STEP * len(CITIES) + 0.5
    if not CITY_START <= t < end + 0.1:
        return
    a = window(t, CITY_START, end, 0.2, 0.3)
    active = min(len(CITIES) - 1, int((t - CITY_START) / CITY_STEP))
    s = CITY_START + active * CITY_STEP
    if draw_clip(img, clip_name(CITIES[active][0]), t, s, s + CITY_STEP):
        # avec une vraie vidéo : mini-carte en bas à droite
        draw_map(img, 860, 1600, 300, line_a=a, fill_a=0.25 * a)
        lo, la = CITIES[active][1]
        x, y = project(lo, la, 860, 1600, 300)
        draw_pin(img, x, y, t, s, a)
        draw_text(img, f"{active + 1:02d} / {len(CITIES):02d}", F_TAG, 210, a, color=MUTE, tracking=6)
        slam(img, CITIES[active][0], F_BIG if len(CITIES[active][0]) < 8 else F_XL, 380, t, s, s + CITY_STEP,
             gradient=True)
        return
    # la carte glisse doucement vers la ville active
    lon, lat = CITIES[active][1]
    tx, ty = project(lon, lat, 540, 1200, 900)
    cx = 540 + (540 - tx) * 0.25
    cy = 1200 + (1200 - ty) * 0.15
    draw_map(img, cx, cy, 900, line_a=a, fill_a=0.10 * a, glow=a)
    for i, (name, (lo, la)) in enumerate(CITIES):
        x, y = project(lo, la, cx, cy, 900)
        draw_pin(img, x, y, t, CITY_START + i * CITY_STEP, a if i == active else a * 0.6)
    draw_text(img, f"{active + 1:02d} / {len(CITIES):02d}", F_TAG, 210, a, color=MUTE, tracking=6)
    slam(img, CITIES[active][0], F_BIG if len(CITIES[active][0]) < 8 else F_XL, 380, t, s, s + CITY_STEP,
         gradient=True)


def scene_count(img, t):  # 30 – 36.5 s
    if not 29.8 <= t < 36.5:
        return
    draw_text(img, "Au total", F_M, 640, window(t, 30.0, 36.3), color=MUTE)
    n = int(1500 * ease_out(prog(t, 30.0, 1.4)))
    slam(img, "+" + fmt_int(n), F_HUGE, 860, t, 30.0, 36.3, gradient=True, tracking=-10)
    reveal_lines(img, [
        ("magasins pillés", F_L, {}),
        ("ou vandalisés", F_L, {}),
    ], t, 30.5, 36.3, 1080, 100)
    draw_text(img, "selon FashionNetwork", F_XS, 1270, window(t, 31.0, 36.3), color=MUTE)


def scene_beats(img, t):  # 36.5 – 42.5 s
    for k, (start, words) in enumerate(BEATS):
        if start <= t < start + 1.5:
            draw_clip(img, f"casse{k + 1}", t, start, start + 1.5)
            n = len(words)
            for i, w in enumerate(words):
                f = F_BIG if len(w) <= 10 else F_XL
                slam(img, w, f, 960 + (i - (n - 1) / 2) * 170, t, start + i * 0.1, start + 1.5, gradient=(i == n - 1))


def scene_wood(img, t):  # 42.5 – 50.8 s
    if not 42.5 <= t < 51.0:
        return
    end = 50.8
    reveal_lines(img, [
        ("Le lendemain,", F_M, {"color": MUTE}),
        ("la France se réveille", F_L, {}),
        ("derrière des planches.", F_L, {}),
    ], t, 42.6, end, 360, 110)
    draw_planks(img, t, 43.6, 760, 1280, window(t, 43.6, end))
    reveal_lines(img, [
        ("Mais les commerçants", F_L, {}),
        ("se relèvent.", F_BIG, {"gradient": True}),
    ], t, 47.6, end, 1420, 150)


def scene_outro(img, t):  # 51 – 60 s
    if t < 50.9:
        return
    a1 = window(t, 51.0, 54.6, 0.3, 0.3)
    draw_map(img, 540, 1320, 900, fill_a=0.18 * a1, line_a=0.5 * a1, glow=a1)
    for i, (_, (lo, la)) in enumerate(CITIES):
        x, y = project(lo, la, 540, 1320, 900)
        draw_pin(img, x, y, t, 51.2 + i * 0.07, a1 * 0.8)
    slam(img, "Commerçants de France,", F_L, 360, t, 51.0, 54.6)
    slam(img, "ON EST", F_BIG, 530, t, 51.4, 54.6)
    slam(img, "AVEC VOUS.", F_BIG, 690, t, 51.7, 54.6, gradient=True)
    a2 = ease_out(prog(t, 54.6, 0.5))
    if a2 > 0:
        draw_map(img, 540, 1250, 520, fill_a=0.22 * a2, line_a=0.6 * a2)
        lg = faded(LOGO, a2)
        img.alpha_composite(lg, ((W - lg.width) // 2, int(470 + (1 - a2) * 60)))
        draw_text(img, "soutient tous les commerces de France", F_S, 850, ease_out(prog(t, 55.0, 0.4)))
        draw_text(img, "Une vidéo pour votre réouverture ?", F_M, 1620, ease_out(prog(t, 55.6, 0.4)), gradient=True)
        draw_text(img, "Écrivez-nous.", F_M, 1700, ease_out(prog(t, 55.8, 0.4)), gradient=True)
        draw_text(img, "#SoutienAuxCommerçants  #PiwaStudio", F_XS, 1790, ease_out(prog(t, 56.2, 0.4)), color=MUTE)


SCENES = [scene_intro, scene_country, scene_cut, scene_cities, scene_count, scene_beats, scene_wood, scene_outro]


def hit_energy(t):
    e = 0.0
    for h in HITS:
        if t >= h:
            e = max(e, math.exp(-(t - h) * 9))
    return e


def beat_pulse(t):
    """Petit coup de zoom sur chaque temps de la musique."""
    if not 4.2 <= t < 50.8 or 16.3 <= t < 19.0:
        return 0.0
    beat = 60 / 128 * SPEED
    return math.exp(-((t - 4.2) % beat) / SPEED * 14)


def post(img, t):
    """Effets caméra : flash, glitch RVB, zoom punch et tremblement sur les impacts."""
    e = hit_energy(t)
    rgb = img.convert("RGB")
    if e > 0.3:  # glitch RVB
        r, g, b = rgb.split()
        s = int(24 * e)
        rgb = Image.merge("RGB", (ImageChops.offset(r, s, 0), g, ImageChops.offset(b, -s, 0)))
    z = 1 + 0.07 * e + 0.018 * beat_pulse(t)
    if z > 1.002:
        zw, zh = int(W * z), int(H * z)
        rnd = random.Random(int(t * FPS))
        sx = rnd.uniform(-1, 1) * 40 * e
        sy = rnd.uniform(-1, 1) * 40 * e
        big = rgb.resize((zw, zh), Image.BILINEAR)
        left = (zw - W) / 2 + sx
        top = (zh - H) / 2 + sy
        rgb = big.crop((int(left), int(top), int(left) + W, int(top) + H))
    if e > 0.6:  # flash blanc
        rgb = Image.blend(rgb, Image.new("RGB", (W, H), (255, 255, 255)), (e - 0.6) * 0.9)
    return rgb


def render(t):
    img = Image.new("RGBA", (W, H), BG + (255,))
    background(img, t)
    for sc in SCENES:
        sc(img, t)
    img.alpha_composite(VIGNETTE)
    src = window(t, 8.2, 50.8, 0.5, 0.5)
    draw_text(img, "Sources : France 3, Europe 1, Tribune de Lyon, FashionNetwork", F_XS, H - 90, src * 0.8, color=MUTE)
    return post(img, t)


# ---------------------------------------------------------------- bande-son
SR = 44100


def soundtrack():
    n = int(OUT_DURATION * SR)
    out = np.zeros(n)
    rng = np.random.default_rng(1)

    def add(sig, at, gain=1.0):  # `at` est en temps de timeline
        i = int(at / SPEED * SR)
        j = min(n, i + len(sig))
        if i < n:
            out[i:j] += sig[: j - i] * gain

    def kick(dur=0.45):
        tt = np.arange(int(dur * SR)) / SR
        freq = 45 + 110 * np.exp(-tt * 28)
        return np.sin(2 * np.pi * np.cumsum(freq) / SR) * np.exp(-tt * 7)

    def noise(dur, decay, hp=True):
        s = rng.standard_normal(int(dur * SR))
        if hp:
            s = np.diff(s, prepend=0)
        return s * np.exp(-np.arange(len(s)) / SR * decay)

    def boom(dur=1.6):
        tt = np.arange(int(dur * SR)) / SR
        return np.sin(2 * np.pi * (38 + 40 * np.exp(-tt * 6)) * tt) * np.exp(-tt * 2.5)

    # nappe grave continue
    tt = np.arange(n) / SR
    pad = (np.sin(2 * np.pi * 55 * tt) + 0.6 * np.sin(2 * np.pi * 82.41 * tt) + 0.4 * np.sin(2 * np.pi * 65.41 * tt))
    pad *= 0.5 + 0.5 * np.sin(2 * np.pi * 0.25 * tt) ** 2
    env = np.clip(tt / 2, 0, 1) * np.clip((OUT_DURATION - tt) / 3, 0, 1)
    out += pad * env * 0.10

    # battements 128 BPM de 4,2 s à 50,8 s, pause au moment du « Mais en marge »
    beat = 60 / 128 * SPEED  # 128 BPM réels une fois accéléré
    b = 4.2
    while b < 50.8:
        if not 16.3 <= b < 19.0:
            add(kick(), b, 0.9)
            add(noise(0.05, 80), b + beat / 2, 0.08)  # charleston
        b += beat
    # coups sur chaque impact
    for h in HITS:
        add(boom(), h, 0.7)
        add(noise(0.4, 9), h, 0.25)
    # vitre qui éclate
    add(noise(1.4, 3.5), SHATTER, 0.6)
    for _ in range(40):
        f = rng.uniform(3000, 9000)
        d = np.arange(int(0.25 * SR)) / SR
        add(np.sin(2 * np.pi * f * d) * np.exp(-d * 18), SHATTER + rng.uniform(0, 1.0), 0.05)
    # montée avant la carte
    d = np.arange(int(2.7 / SPEED * SR)) / SR
    add(rng.standard_normal(len(d)) * (d / d[-1]) ** 2, 16.3, 0.18)
    # accord final
    d = np.arange(int(6 * SR)) / SR
    chord = sum(np.sin(2 * np.pi * f * d) for f in (220, 277.18, 329.63, 440)) * np.exp(-d * 0.6)
    add(chord, 54.6, 0.06)

    out = np.tanh(out * 1.2)
    out = out / np.max(np.abs(out)) * 0.9
    return (out * 32767).astype(np.int16)


def write_wav(path):
    data = soundtrack()
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(data.tobytes())


def main():
    args = sys.argv[1:]
    if "--clips" in args:
        i = args.index("--clips")
        CLIPS.dir = Path(args[i + 1])
        CLIPS.tmp = tempfile.mkdtemp(prefix="piwa-clips-")
        del args[i:i + 2]
    if "--preview" in args:
        i = args.index("--preview")
        out = Path(args[i + 1])
        out.mkdir(parents=True, exist_ok=True)
        for tt in [float(x) for x in args[i + 2].split(",")]:
            render(tt).save(out / f"frame_{tt:05.1f}.png")
        return
    out = args[0] if args else "piwa-france-17-octobre.mp4"
    with tempfile.TemporaryDirectory() as tmp:
        wav = Path(tmp) / "son.wav"
        write_wav(wav)
        ff = subprocess.Popen([
            "ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
            "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", str(wav),
            "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out,
        ], stdin=subprocess.PIPE)
        total = int(OUT_DURATION * FPS)
        for i in range(total):
            ff.stdin.write(render(i / FPS * SPEED).tobytes())
            if i % 300 == 0:
                print(f"{i}/{total}", flush=True)
        ff.stdin.close()
        ff.wait()


if __name__ == "__main__":
    main()
