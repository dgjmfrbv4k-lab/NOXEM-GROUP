"""PIWA Studio — « Lyon, 17 octobre » : reportage motion design vertical (1080x1920, 60 s).

Rendu image par image avec Pillow, encodé en MP4 par ffmpeg.
    python3 motion/lyon-17-octobre/render.py [sortie.mp4] [--preview t1,t2,...]
"""
import math
import random
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS, DURATION = 1080, 1920, 30, 60.0
ROOT = Path(__file__).resolve().parents[2]
FONT_DIR = Path("/usr/share/fonts/opentype/inter")

BG = (6, 7, 10)
FG = (244, 245, 250)
MUTE = (141, 147, 168)
GRAD = [(34, 211, 238), (139, 92, 246), (244, 114, 182)]  # charte PIWA


def font(weight, size):
    return ImageFont.truetype(str(FONT_DIR / f"InterDisplay-{weight}.otf"), size)


# ---------------------------------------------------------------- easing / temps
def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def prog(t, start, dur):
    return clamp((t - start) / dur)


def ease_out(x):
    return 1 - (1 - x) ** 3


def ease_in_out(x):
    return 4 * x ** 3 if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2


def window(t, start, end, fade_in=0.4, fade_out=0.4):
    """Opacité d'un élément visible entre start et end."""
    return min(ease_out(prog(t, start, fade_in)), 1 - prog(t, end - fade_out, fade_out))


# ---------------------------------------------------------------- calques fixes
def lerp_color(a, b, x):
    return tuple(int(a[i] + (b[i] - a[i]) * x) for i in range(3))


def make_gradient(w, h):
    g = Image.new("RGB", (w, h))
    px = g.load()
    for x in range(w):
        for y in range(0, h, 1):
            u = clamp((x / w * 0.75 + y / h * 0.25))
            c = lerp_color(GRAD[0], GRAD[1], u * 2) if u < 0.5 else lerp_color(GRAD[1], GRAD[2], (u - 0.5) * 2)
            px[x, y] = c
    return g


GRADIENT = make_gradient(W, 400)


def make_glow(color, radius):
    size = radius * 2
    g = Image.new("L", (size, size), 0)
    ImageDraw.Draw(g).ellipse((radius // 2, radius // 2, size - radius // 2, size - radius // 2), fill=255)
    g = g.filter(ImageFilter.GaussianBlur(radius // 3))
    layer = Image.new("RGBA", (size, size), color + (0,))
    layer.putalpha(g)
    return layer


GLOW_VIOLET = make_glow((139, 92, 246), 700)
GLOW_CYAN = make_glow((34, 211, 238), 600)
GLOW_RED = make_glow((239, 68, 68), 650)
GLOW_BLUE = make_glow((59, 130, 246), 650)


def make_vignette():
    v = Image.new("L", (W, H), 0)
    ImageDraw.Draw(v).ellipse((-300, -200, W + 300, H + 200), fill=255)
    v = v.filter(ImageFilter.GaussianBlur(220))
    dark = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dark.putalpha(v.point(lambda p: int((255 - p) * 0.75)))
    return dark


VIGNETTE = make_vignette()

logo = Image.open(ROOT / "piwa" / "logo-piwa-ai-sombre.png").convert("RGB")
LOGO = logo.resize((860, int(860 * logo.height / logo.width)), Image.LANCZOS).convert("RGBA")
# détourage : le fond sombre du logo devient transparent
LOGO.putalpha(LOGO.convert("L").point(lambda p: int(clamp((p - 12) * 6, 0, 255))))


# ---------------------------------------------------------------- texte
_mask_cache = {}


def text_mask(text, fnt, tracking=0):
    key = (text, fnt.path, fnt.size, tracking)
    if key not in _mask_cache:
        if tracking:
            widths = [fnt.getlength(ch) + tracking for ch in text]
            w = int(sum(widths))
        else:
            w = int(fnt.getlength(text))
        asc, desc = fnt.getmetrics()
        m = Image.new("L", (w + 4, asc + desc + 4), 0)
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


def draw_text(img, text, fnt, y, alpha=1.0, color=FG, x=None, dy=0, gradient=False, tracking=0, anchor="center"):
    if alpha <= 0.01:
        return
    m = text_mask(text, fnt, tracking)
    if alpha < 1:
        m = m.point(lambda p: int(p * alpha))
    if x is None:
        px = (W - m.width) // 2
    elif anchor == "left":
        px = int(x)
    else:
        px = int(x - m.width / 2)
    py = int(y + dy - m.height / 2)
    if gradient:
        src = GRADIENT.resize((W, max(m.height, 1))).crop((px, 0, px + m.width, m.height)) if px >= 0 else GRADIENT.resize((m.width, m.height))
        img.paste(src, (px, py), m)
    else:
        img.paste(color, (px, py, px + m.width, py + m.height), m)


def reveal_lines(img, lines, t, start, end, y0, step, stagger=0.25, rise=60):
    """Lignes (texte, police, options) qui montent l'une après l'autre."""
    for i, (txt, fnt, opts) in enumerate(lines):
        s = start + i * stagger
        a = window(t, s, end, 0.5, 0.45)
        dy = (1 - ease_out(prog(t, s, 0.6))) * rise
        draw_text(img, txt, fnt, y0 + i * step, a, dy=dy, **opts)


# ---------------------------------------------------------------- verre brisé
class Glass:
    """Impact au centre, fissures radiales puis éclatement en éclats qui tombent."""

    def __init__(self, cx, cy, seed=7, rays=16, rings=(0, 70, 170, 320, 520, 800, 1150, 1700)):
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
                speed = rnd.uniform(500, 1300)
                self.shards.append({
                    "poly": poly, "c": (gx, gy),
                    "v": (math.cos(ang) * speed, math.sin(ang) * speed - rnd.uniform(200, 700)),
                    "spin": rnd.uniform(-5, 5), "delay": rnd.uniform(0, 0.12),
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
            a = clamp(1 - tt / 1.3)
            if a <= 0:
                continue
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


GLASS = Glass(540, 880)


# ---------------------------------------------------------------- planches de bois
def draw_planks(img, t, start, y_top, y_bottom, alpha=1.0):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    rnd = random.Random(3)
    n = 5
    h = (y_bottom - y_top) / n
    for i in range(n):
        p = ease_out(prog(t, start + i * 0.18, 0.55))
        if p <= 0:
            continue
        from_left = i % 2 == 0
        x0 = -W * (1 - p) if from_left else W * (1 - p)
        y = y_top + i * h
        base = (rnd.randint(120, 150), rnd.randint(82, 100), rnd.randint(52, 64))
        box = (x0 + 90, y + 4, x0 + W - 90, y + h - 4)
        d.rounded_rectangle(box, radius=6, fill=base + (int(255 * alpha),))
        for k in range(6):
            yy = box[1] + (k + 1) * (h - 8) / 7 + rnd.uniform(-4, 4)
            d.line([(box[0] + 10, yy), (box[2] - 10, yy + rnd.uniform(-3, 3))], fill=(base[0] - 25, base[1] - 22, base[2] - 16, int(160 * alpha)), width=2)
        for sx in (box[0] + 30, box[2] - 30):
            cy = (box[1] + box[3]) / 2
            d.ellipse((sx - 7, cy - 7, sx + 7, cy + 7), fill=(70, 72, 80, int(255 * alpha)))
    img.alpha_composite(layer)


# ---------------------------------------------------------------- scènes
F_HUGE = font("Black", 300)
F_BIG = font("Black", 150)
F_XL = font("Black", 112)
F_L = font("ExtraBold", 84)
F_M = font("Bold", 64)
F_S = font("SemiBold", 44)
F_XS = font("Medium", 32)
F_TAG = font("SemiBold", 34)


def fmt_int(n):
    return f"{n:,}".replace(",", " ")


def background(img, t):
    # halos qui dérivent lentement
    x = int(-500 + 220 * math.sin(t * 0.25))
    y = int(-300 + 160 * math.cos(t * 0.2))
    img.alpha_composite(GLOW_VIOLET, (x, y))
    img.alpha_composite(GLOW_CYAN, (int(W - 700 + 180 * math.cos(t * 0.3)), int(H - 900 + 140 * math.sin(t * 0.22))))
    # gyrophares pendant les violences
    siren = window(t, 12, 37, 1.0, 1.0)
    if siren > 0:
        phase = (math.sin(t * 9) + 1) / 2
        red = GLOW_RED.copy()
        red.putalpha(red.getchannel("A").point(lambda p: int(p * siren * phase * 0.9)))
        blue = GLOW_BLUE.copy()
        blue.putalpha(blue.getchannel("A").point(lambda p: int(p * siren * (1 - phase) * 0.9)))
        img.alpha_composite(red, (-650, 250))
        img.alpha_composite(blue, (W - 650, 250))


def scene_intro(img, t):  # 0 – 6 s
    a = window(t, 0.4, 6.0, 0.8, 0.5)
    draw_text(img, "SAMEDI 17 OCTOBRE 2026", F_TAG, 600, window(t, 1.3, 6.0, 0.6, 0.5), color=MUTE, tracking=8)
    draw_text(img, "LYON", F_HUGE, 860, a, dy=(1 - ease_out(prog(t, 0.4, 1.0))) * 80, gradient=True, tracking=-6)
    draw_text(img, "Une journée qui a tout changé", F_S, 1100, window(t, 2.0, 6.0, 0.6, 0.5), color=FG)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    if t < 4.2:
        GLASS.draw_cracks(layer, ease_out(prog(t, 0.25, 1.6)), 1.0)
    else:
        GLASS.draw_shatter(layer, t - 4.2)
    img.alpha_composite(layer)
    if 4.2 <= t < 4.4:  # flash d'impact
        img.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(200 * (1 - prog(t, 4.2, 0.2))))))


def scene_crowd(img, t):  # 6 – 12 s
    draw_text(img, "Dans les rues de la ville,", F_M, 640, window(t, 6.2, 11.8), dy=(1 - ease_out(prog(t, 6.2, 0.6))) * 50)
    n = int(20000 * ease_in_out(prog(t, 6.8, 2.2)))
    draw_text(img, fmt_int(n), F_HUGE, 900, window(t, 6.7, 11.8), gradient=True, tracking=-8)
    reveal_lines(img, [
        ("personnes manifestent", F_L, {}),
        ("dans le calme.", F_L, {"color": MUTE}),
    ], t, 8.4, 11.8, 1140, 104)


def scene_1530(img, t):  # 12 – 19 s
    draw_text(img, "15H30", F_HUGE, 640, window(t, 12.2, 18.8, 0.3), dy=(1 - ease_out(prog(t, 12.2, 0.5))) * 90, gradient=True, tracking=-6)
    reveal_lines(img, [
        ("En marge du cortège,", F_M, {"color": MUTE}),
        ("des casseurs", F_XL, {}),
        ("s'attaquent", F_XL, {}),
        ("aux commerces.", F_XL, {"gradient": True}),
    ], t, 13.0, 18.8, 940, 132, stagger=0.35)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for i, (cx, cy) in enumerate([(170, 330), (900, 470), (130, 1560), (930, 1640), (560, 1700)]):
        s = 14.2 + i * 0.55
        if t >= s:
            mini_crack(layer, cx, cy, 160, ease_out(prog(t, s, 0.25)), window(t, s, 18.8, 0.05), seed=i + 11)
    img.alpha_composite(layer)


STREETS = ["Rue Victor-Hugo", "Rue Grenette", "Place Bellecour", "Rue de la Charité"]


def scene_streets(img, t):  # 19 – 29 s
    end = 28.8
    draw_text(img, "LA PRESQU'ÎLE TOUCHÉE", F_TAG, 470, window(t, 19.2, end), color=MUTE, tracking=8)
    x_line = 170
    y0, step = 680, 210
    d = ImageDraw.Draw(img)
    # tracé du parcours
    p = ease_in_out(prog(t, 19.6, 4.2))
    a = window(t, 19.6, end)
    y_end = y0 + p * step * (len(STREETS) - 1)
    if p > 0:
        line = GRADIENT.resize((8, max(1, int(y_end - y0)))).convert("RGBA")
        line.putalpha(int(255 * a))
        img.alpha_composite(line, (x_line - 4, y0))
    for i, name in enumerate(STREETS):
        s = 19.8 + i * 1.3
        ai = window(t, s, end, 0.5)
        if ai <= 0:
            continue
        dx = (1 - ease_out(prog(t, s, 0.6))) * -80
        r = 22 * ease_out(prog(t, s, 0.4))
        y = y0 + i * step
        d.ellipse((x_line - r, y - r, x_line + r, y + r), fill=(244, 114, 182) if i == len(STREETS) - 1 else (34, 211, 238))
        draw_text(img, name, F_L, y, ai, x=x_line + 70 + dx, anchor="left")
        draw_text(img, f"0{i + 1}", F_XS, y + 62, ai, x=x_line + 72 + dx, anchor="left", color=MUTE)
    draw_text(img, "Des dizaines de commerces", F_M, 1600, window(t, 25.4, end), dy=(1 - ease_out(prog(t, 25.4, 0.6))) * 40)
    draw_text(img, "vandalisés et pillés.", F_M, 1680, window(t, 25.7, end), color=MUTE, dy=(1 - ease_out(prog(t, 25.7, 0.6))) * 40)


BEATS = [
    (29.0, ["Vitrines", "brisées."]),
    (31.0, ["Magasins", "pillés."]),
    (33.0, ["L'office", "de tourisme", "incendié."]),
    (35.0, ["Le choc", "pour tout", "un quartier."]),
]


def scene_beats(img, t):  # 29 – 37 s
    for start, words in BEATS:
        if start <= t < start + 2.0:
            n = len(words)
            for i, w in enumerate(words):
                s = start + i * 0.12
                a = window(t, s, start + 2.0, 0.15, 0.2)
                dy = (1 - ease_out(prog(t, s, 0.3))) * 120
                draw_text(img, w, F_BIG, 960 + (i - (n - 1) / 2) * 165, a, dy=dy, gradient=(i == n - 1), tracking=-4)
            if t < start + 0.12:
                img.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(170 * (1 - prog(t, start, 0.12))))))


def scene_arrests(img, t):  # 37 – 43 s
    n = int(160 * ease_out(prog(t, 37.4, 1.6)))
    draw_text(img, str(n), F_HUGE, 820, window(t, 37.3, 42.8), gradient=True, tracking=-8)
    draw_text(img, "interpellations", F_L, 1050, window(t, 37.9, 42.8), dy=(1 - ease_out(prog(t, 37.9, 0.6))) * 40)
    draw_text(img, "selon la Tribune de Lyon", F_XS, 1140, window(t, 38.4, 42.8), color=MUTE)


def scene_wood(img, t):  # 43 – 51 s
    end = 50.8
    reveal_lines(img, [
        ("Le lendemain,", F_M, {"color": MUTE}),
        ("les vitrines", F_XL, {}),
        ("sont en bois.", F_XL, {}),
    ], t, 43.2, end, 380, 130)
    a = window(t, 44.2, end)
    draw_planks(img, t, 44.4, 780, 1300, a)
    reveal_lines(img, [
        ("Mais les commerçants", F_L, {}),
        ("sont toujours debout.", F_L, {"gradient": True}),
    ], t, 46.8, end, 1440, 110)


def scene_outro(img, t):  # 51 – 60 s
    a1 = window(t, 51.0, 55.0, 0.5, 0.5)
    reveal_lines(img, [
        ("Commerçants lyonnais,", F_L, {}),
        ("on est", F_BIG, {}),
        ("avec vous.", F_BIG, {"gradient": True}),
    ], t, 51.1, 55.0, 760, 170)
    a2 = ease_out(prog(t, 55.3, 0.8))
    if a2 > 0:
        lg = LOGO.copy()
        lg.putalpha(lg.getchannel("A").point(lambda p: int(p * a2)))
        img.alpha_composite(lg, ((W - lg.width) // 2, int(640 + (1 - a2) * 60)))
        draw_text(img, "soutient les commerces de Lyon", F_M, 1060, ease_out(prog(t, 55.9, 0.6)))
        draw_text(img, "Réparer, relancer, se faire voir à nouveau.", F_S, 1150, ease_out(prog(t, 56.4, 0.6)), color=MUTE)
        draw_text(img, "Une vidéo pour votre réouverture ? Écrivez-nous.", F_S, 1500, ease_out(prog(t, 57.0, 0.6)), gradient=True)
        draw_text(img, "#Lyon  #SoutienAuxCommerçants  #PiwaStudio", F_XS, 1600, ease_out(prog(t, 57.3, 0.6)), color=MUTE)
    del a1


SCENES = [scene_intro, scene_crowd, scene_1530, scene_streets, scene_beats, scene_arrests, scene_wood, scene_outro]


def render(t):
    img = Image.new("RGBA", (W, H), BG + (255,))
    background(img, t)
    for sc in SCENES:
        sc(img, t)
    img.alpha_composite(VIGNETTE)
    src = window(t, 6.2, 50.8, 0.6, 0.6)
    draw_text(img, "Sources : France 3, Europe 1, Tribune de Lyon, Lyon People", F_XS, H - 90, src * 0.8, color=MUTE)
    return img.convert("RGB")


def main():
    args = sys.argv[1:]
    if "--preview" in args:
        times = [float(x) for x in args[args.index("--preview") + 1].split(",")]
        out = Path(args[0]) if args[0] != "--preview" else Path(".")
        out.mkdir(parents=True, exist_ok=True)
        for tt in times:
            render(tt).save(out / f"frame_{tt:05.1f}.png")
        return
    out = args[0] if args else "lyon-17-octobre.mp4"
    ff = subprocess.Popen([
        "ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
        "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-pix_fmt", "yuv420p",
        "-movflags", "+faststart", out,
    ], stdin=subprocess.PIPE)
    total = int(DURATION * FPS)
    for i in range(total):
        ff.stdin.write(render(i / FPS).tobytes())
        if i % 150 == 0:
            print(f"{i}/{total}", flush=True)
    ff.stdin.close()
    ff.wait()


if __name__ == "__main__":
    main()
