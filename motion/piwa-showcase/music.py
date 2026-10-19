"""Musique originale de la vidéo showcase (26 s, 120 BPM), calée sur la timeline de index.html."""
import sys
import wave

import numpy as np

SR, DUR, BEAT = 44100, 26.0, 0.5
PRESS, WALL, SKILLS, FORMATS, PRICES, END = 3.0, 3.4, 7.6, 12.4, 16.4, 22.2
n = int(DUR * SR)
out = np.zeros(n)
rng = np.random.default_rng(7)
tt = np.arange(n) / SR


def add(sig, at, gain):
    i = int(at * SR)
    j = min(n, i + len(sig))
    if 0 <= i < n:
        out[i:j] += sig[: j - i] * gain


def env(dur, k):
    return np.exp(-np.arange(int(dur * SR)) / SR * k)


d = np.arange(int(0.45 * SR)) / SR
kick = np.sin(2 * np.pi * np.cumsum(45 + 120 * np.exp(-d * 30)) / SR) * np.exp(-d * 7)
hat = np.diff(rng.standard_normal(int(0.04 * SR)), prepend=0) * env(0.04, 100)
clap = np.diff(rng.standard_normal(int(0.2 * SR)), prepend=0) * env(0.2, 20)
d = np.arange(int(2.0 * SR)) / SR
boom = np.sin(2 * np.pi * (36 + 40 * np.exp(-d * 5)) * d) * np.exp(-d * 2)


def pluck(f, dur=0.4, k=7):
    d = np.arange(int(dur * SR)) / SR
    return sum(np.sin(2 * np.pi * f * h * d) / h ** 1.5 for h in range(1, 5)) * np.exp(-d * k)


# nappe douce + montée de l'intro
pad = sum(np.sin(2 * np.pi * f * tt + np.sin(tt * 0.3 + f)) for f in (110, 164.8, 220, 277.2))
out += pad * np.clip(tt / 2.5, 0, 1) * np.clip((DUR - tt) / 2, 0, 1) * 0.02
for k in range(12):  # touches du prompt
    add(np.diff(rng.standard_normal(int(0.03 * SR)), prepend=0) * env(0.03, 150), 0.7 + k * 0.14, 0.12)
add(rng.standard_normal(int(2.2 * SR)) * np.linspace(0, 1, int(2.2 * SR)) ** 3, PRESS - 2.2, 0.12)
add(boom, WALL, 0.9)

# beat 120 BPM et arpège à partir du mur de vidéos
arp = [220, 277.18, 329.63, 415.3, 440, 415.3, 329.63, 277.18]
b, k = WALL, 0
while b < END - 0.1:
    add(kick, b, 0.85)
    add(hat, b + BEAT / 2, 0.1)
    if k % 2:
        add(clap, b, 0.28)
    add(pluck(arp[k % 8]), b, 0.06)
    add(pluck(arp[(k + 2) % 8] * 2, 0.25, 10), b + BEAT / 2, 0.03)
    add(pluck(55 if (k // 8) % 2 == 0 else 61.74, BEAT, 4), b, 0.2)
    b += BEAT
    k += 1
for c in (SKILLS, FORMATS, PRICES):
    s = np.diff(rng.standard_normal(int(0.5 * SR)), prepend=0) * np.sin(np.linspace(0, np.pi, int(0.5 * SR))) ** 2
    add(s, c - 0.4, 0.12)
    add(boom, c, 0.5)
# « ding » sur chaque nouveau prix
for i in range(3):
    d = np.arange(int(0.4 * SR)) / SR
    add((np.sin(2 * np.pi * 1760 * d) + 0.6 * np.sin(2 * np.pi * 2637 * d)) * np.exp(-d * 9), PRICES + 1.0 + i * 0.35 + 1.25, 0.08)
# fin : boom + accord tenu
add(boom, END, 1.0)
d = np.arange(int(4 * SR)) / SR
add(sum(np.sin(2 * np.pi * f * d) for f in (220, 277.18, 329.63, 440, 554.4)) * np.exp(-d * 0.7), END, 0.05)

out = np.tanh(out * 1.3) * np.clip((DUR - tt) / 0.8, 0, 1)
out = out / np.max(np.abs(out)) * 0.9
with wave.open(sys.argv[1], "wb") as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((out * 32767).astype(np.int16).tobytes())
