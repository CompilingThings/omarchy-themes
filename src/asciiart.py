#!/usr/bin/env python3
"""A photo as braille text art, for a theme's screensaver.txt.

Usage: asciiart.py <photo> <out.txt> [--cols 100] [--rows 28] [--box x0,y0,x1,y1] [--gamma 1.0] [--level 0.5]
                   [--edges 0.0] [--invert] [--title "SPORE GARDEN"]                 (needs numpy and Pillow)

Each terminal cell holds one braille character, a 2 x 4 grid of dots, so 100 x 28 cells draw 200 x 112 dots.
The photo (or the part in --box, fractions of the photo) is fitted into that grid, keeping its shape (a cell is
about twice as tall as wide), turned to brightness, and dithered (Floyd-Steinberg) so the dot density follows the
light: a bright subject on black comes out as a halftone of it. --level moves the cut (lower = more dots), --gamma
bends the brightness first (above 1 = fewer mid-tone dots), --edges mixes in the outline (0-1) so thin parts
survive. The text has no colour: the screensaver player colours it with the theme's palette.
Lone dots (no lit neighbour) are dropped so the dither leaves no dust, and empty rows and columns round the art are
trimmed. --title adds the theme's name, letter-spaced, centred one row under the art.
"""
import argparse

import numpy as np
from PIL import Image, ImageFilter

# Braille dot bits by (row, column) inside the 2 x 4 cell (Unicode U+2800 block).
BITS = [[0x01, 0x08], [0x02, 0x10], [0x04, 0x20], [0x40, 0x80]]
CELL_ASPECT = 2.05      # cell height / cell width in JetBrains Mono (Omarchy's screensaver font)


def load(path, box):
    im = Image.open(path).convert("RGB")
    if box:
        w, h = im.size
        x0, y0, x1, y1 = box
        im = im.crop((round(x0 * w), round(y0 * h), round(x1 * w), round(y1 * h)))
    return im


def dots(im, cols, rows):
    """Size of the dot grid that fits the photo's shape into cols x rows cells."""
    w, h = im.size
    # One dot is 1/2 cell wide and 1/4 cell high, so a dot is CELL_ASPECT/2 times as tall as wide.
    dot_aspect = CELL_ASPECT / 2
    gw, gh = cols * 2, rows * 4
    scale = min(gw / w, gh * dot_aspect / h)
    return max(2, round(w * scale) // 2 * 2), max(4, round(h * scale / dot_aspect) // 4 * 4)


def dither(a, level):
    a = a.copy()
    out = np.zeros(a.shape, bool)
    h, w = a.shape
    for y in range(h):
        for x in range(w):
            old = a[y, x]
            new = old >= level
            out[y, x] = new
            err = old - (1.0 if new else 0.0)
            if x + 1 < w:
                a[y, x + 1] += err * 7 / 16
            if y + 1 < h:
                if x > 0:
                    a[y + 1, x - 1] += err * 3 / 16
                a[y + 1, x] += err * 5 / 16
                if x + 1 < w:
                    a[y + 1, x + 1] += err * 1 / 16
    return out


def clean(on):
    """Drop dots with no lit neighbour among their eight."""
    p = np.pad(on, 1)
    n = sum(np.roll(np.roll(p, dy, 0), dx, 1) for dy in (-1, 0, 1) for dx in (-1, 0, 1) if dy or dx)[1:-1, 1:-1]
    return on & (n > 0)


def braille(on):
    h, w = on.shape
    lines = []
    for cy in range(0, h, 4):
        row = []
        for cx in range(0, w, 2):
            v = 0
            for r in range(4):
                for c in range(2):
                    if on[cy + r, cx + c]:
                        v |= BITS[r][c]
            row.append(chr(0x2800 + v) if v else " ")
        lines.append("".join(row).rstrip())
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    pad = min((len(l) - len(l.lstrip()) for l in lines if l.strip()), default=0)
    return [l[pad:] for l in lines]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("photo"); p.add_argument("out")
    p.add_argument("--cols", type=int, default=100); p.add_argument("--rows", type=int, default=28)
    p.add_argument("--box", type=lambda s: [float(v) for v in s.split(",")])
    p.add_argument("--gamma", type=float, default=1.0); p.add_argument("--level", type=float, default=0.5)
    p.add_argument("--edges", type=float, default=0.0); p.add_argument("--invert", action="store_true")
    p.add_argument("--title")
    a = p.parse_args()
    im = load(a.photo, a.box)
    gw, gh = dots(im, a.cols, a.rows)
    g = im.convert("L").resize((gw, gh), Image.LANCZOS)
    v = np.asarray(g, float) / 255
    if a.invert:
        v = 1 - v
    v = v ** a.gamma
    if a.edges:
        e = np.asarray(g.filter(ImageFilter.FIND_EDGES), float) / 255
        v = np.clip((1 - a.edges) * v + a.edges * e / max(e.max(), 1e-6), 0, 1)
    lines = braille(clean(dither(v, a.level)))
    if a.title:
        w = max(map(len, lines))
        name = " ".join(a.title.upper()).replace("   ", "     ")
        lines = [l.ljust(w) for l in lines] + ["", name.center(max(w, len(name)))]
        lines = [l.rstrip() for l in lines]
    with open(a.out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"{a.out}: {max(map(len, lines))} x {len(lines)} cells")


if __name__ == "__main__":
    main()
