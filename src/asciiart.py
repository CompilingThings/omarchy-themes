#!/usr/bin/env python3
"""A photo as braille text art, for a theme's screensaver.txt.

Usage: asciiart.py --theme <theme>...         (a theme's own, from its wallpapers.json "screensaver")
       asciiart.py <photo> <out.txt> [--cols 100] [--rows 24] [--box x0,y0,x1,y1] [--gamma 1.0] [--level 0.5]
                   [--edges 0.0] [--invert] [--hide x0,y0,x1,y1]
                   [--mean 0.2] [--title "Spore Garden"]          (needs numpy and Pillow)

Each terminal cell holds one braille character, a 2 x 4 grid of dots, so 100 x 24 cells draw 200 x 96 dots.
The photo (or the part in --box, fractions of the photo) is fitted into that grid, keeping its shape (a cell is
about twice as tall as wide), turned to brightness, and dithered (Floyd-Steinberg) so the dot density follows the
light: a bright subject on black comes out as a halftone of it. --level moves the cut (lower = more dots), --gamma
bends the brightness first (above 1 = fewer mid-tone dots), --edges mixes in the outline (0-1) so thin parts
survive. --hide paints a box (fractions, before --box) over first with a mirror of the strip above it (black on a dark background), for a wallpaper's label; --mean picks the gamma
that makes that share of the dots lit (instead of --gamma); --zoom cuts to the bright subject first so it fills the
space; --color photo gives each character the photo's colour there, --color theme the nearest of the theme's
colours (--colors-toml, or the theme's own with --theme); --detail (0-4) sharpens structure a few dots across
(veins, rings, threads) before the dots are placed. Without --color the text has no colour and the
screensaver colours it with the theme's palette (extras/screensaver); with it, the picture keeps its own colours and
the screensaver's effect only animates them in.
Lone dots (no lit neighbour) are dropped so the dither leaves no dust, and empty rows and columns round the art are
trimmed. --title adds a name, letter-spaced, centred one row under the art (--theme: the theme's name).
"""
import argparse
import json
import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

# Braille dot bits by (row, column) inside the 2 x 4 cell (Unicode U+2800 block).
BITS = [[0x01, 0x08], [0x02, 0x10], [0x04, 0x20], [0x40, 0x80]]
CELL_ASPECT = 2.05      # cell height / cell width in JetBrains Mono (Omarchy's screensaver font)


def load(path, box, hide=None):
    im = Image.open(path).convert("RGB")
    if hide:
        w, h = im.size
        x0, y0, x1, y1 = hide
        bx0, by0, bx1, by1 = round(x0 * w), round(y0 * h), round(x1 * w), round(y1 * h)
        # Fill with a mirror of the strip just above the box, so the photo's texture carries on and a full-frame
        # photo gets no notch (on a black background the strip is black).
        strip = im.crop((bx0, max(0, 2 * by0 - by1), bx1, by0)).transpose(Image.FLIP_TOP_BOTTOM)
        if np.median(np.asarray(strip.convert("L"))) < 40:     # a dark background: plain black, no copied subject
            strip = Image.new("RGB", strip.size)
        im.paste(strip.resize((bx1 - bx0, by1 - by0)), (bx0, by0))
    if box:
        w, h = im.size
        x0, y0, x1, y1 = box
        im = im.crop((round(x0 * w), round(y0 * h), round(x1 * w), round(y1 * h)))
    return im


def zoom(im, margin=0.04):
    """Cut to the subject: the box round the pixels brighter than a fifth of the brightest (1 % trimmed each side)."""
    small = im.convert("L"); small.thumbnail((400, 400))
    v = np.asarray(small, float)
    ys, xs = np.nonzero(v > 0.2 * np.percentile(v, 99.9))
    if len(xs) < 20:
        return im
    x0, x1 = np.percentile(xs, [1, 99]); y0, y1 = np.percentile(ys, [1, 99])
    k = im.width / small.width; m = margin * max(x1 - x0, y1 - y0)
    return im.crop((max(0, round((x0 - m) * k)), max(0, round((y0 - m) * k)),
                    min(im.width, round((x1 + m) * k)), min(im.height, round((y1 + m) * k))))


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


def braille(on, colours=None):
    """Braille lines from the dot grid; with colours (one RGB per cell) each character gets its 24-bit colour."""
    h, w = on.shape
    cells = np.zeros((h // 4, w // 2), int)
    for r in range(4):
        for c in range(2):
            cells |= on[r::4, c::2][: h // 4, : w // 2].astype(int) * BITS[r][c]
    used = np.nonzero(cells.any(1))[0]; cols_used = np.nonzero(cells.any(0))[0]
    if not len(used):
        return []
    cells = cells[used[0]:used[-1] + 1, cols_used[0]:cols_used[-1] + 1]
    if colours is not None:
        colours = colours[used[0]:used[-1] + 1, cols_used[0]:cols_used[-1] + 1]
    lines = []
    for y, row in enumerate(cells):
        out, last = [], None
        end = max((x for x, v in enumerate(row) if v), default=-1)
        for x, v in enumerate(row[: end + 1]):
            if v and colours is not None:
                rgb = tuple(int(c) for c in colours[y, x])
                if rgb != last:
                    out.append("\033[38;2;%d;%d;%dm" % rgb); last = rgb
            out.append(chr(0x2800 + v) if v else " ")
        lines.append("".join(out) + ("\033[0m" if last else ""))
    return lines


def palette(colors_toml):
    """The theme's colours that dots may take: the accent, the terminal colours and their bright forms (no white or
    grey, so a pale photo still comes out in colour)."""
    keys = ["accent", "red", "orange", "yellow", "green", "cyan", "blue", "magenta", "bright_red", "bright_yellow",
            "bright_green", "bright_cyan", "bright_blue", "bright_magenta"]
    found = dict(re.findall(r'^(\w+) *= *"#([0-9A-Fa-f]{6})"', Path(colors_toml).read_text(), re.M))
    return np.array([[int(found[k][i:i + 2], 16) for i in (0, 2, 4)] for k in keys if k in found], float)


def cell_colours(im, shape, pal=None):
    """One colour per braille cell: the photo's colour there, made bright enough to read as thin dots, then snapped
    to the nearest theme colour by hue and lightness (both scaled to the brightest channel, so a dim red still
    finds the theme's red)."""
    rows, cols = shape
    c = np.asarray(im.convert("RGB").resize((cols, rows), Image.LANCZOS), float)
    peak = np.maximum(c.max(2, keepdims=True), 1)
    vivid = c / peak * np.clip(peak * 1.6, 110, 255)            # dim areas lifted, hue kept
    if pal is None:
        return vivid.round().clip(0, 255)
    grey = vivid.mean(2, keepdims=True)
    vivid = np.clip(grey + 3 * (vivid - grey), 0, 255)            # pale microscope colours pushed to their hue
    n = vivid / np.maximum(vivid.max(2, keepdims=True), 1)
    pn = pal / np.maximum(pal.max(1, keepdims=True), 1)
    d = ((n[:, :, None, :] - pn[None, None]) ** 2).sum(3) + 0.15 * ((vivid.mean(2)[:, :, None] - pal.mean(1)) / 255) ** 2
    return pal[d.argmin(2)]


def art(photo, cols=100, rows=24, box=None, hide=None, gamma=1.0, level=0.5, edges=0.0, invert=False, mean=None,
        title=None, zoom_in=False, detail=0.0, color=None, colors_toml=None):
    """The text art as a list of lines (with 24-bit colour codes when color is "photo" or "theme")."""
    im = load(photo, box, hide)
    if zoom_in:
        im = zoom(im)
    gw, gh = dots(im, cols, rows)
    grey = im.convert("L").resize((gw, gh), Image.LANCZOS)
    v = np.asarray(grey, float) / 255
    if detail:                      # boost structure smaller than ~6 dots over the smooth light behind it
        blur = np.asarray(grey.filter(ImageFilter.GaussianBlur(3)), float) / 255
        v = np.clip(v + detail * (v - blur), 0, 1)
    if invert:
        v = 1 - v
    if mean:                        # bisect the gamma that gives this mean brightness
        lo, hi = 0.05, 20.0
        for _ in range(40):
            gamma = (lo * hi) ** 0.5
            lo, hi = (gamma, hi) if (v ** gamma).mean() > mean else (lo, gamma)
    v = v ** gamma
    if edges:
        e = np.asarray(grey.filter(ImageFilter.FIND_EDGES), float) / 255
        v = np.clip((1 - edges) * v + edges * e / max(e.max(), 1e-6), 0, 1)
    on = clean(dither(v, level))
    rgb = None
    if color:
        pal = palette(colors_toml) if color == "theme" else None
        rgb = cell_colours(im.resize((gw, gh), Image.LANCZOS), (gh // 4, gw // 2), pal)
    lines = braille(on, rgb)
    if title:
        w = max(map(width, lines))
        name = " ".join(title.upper()).replace("   ", "     ")
        pad = " " * ((max(w, len(name)) - len(name)) // 2)
        if color:
            acc = palette(colors_toml)[0] if colors_toml else (255, 255, 255)
            name = "\033[38;2;%d;%d;%dm" % tuple(int(c) for c in acc) + name + "\033[0m"
        lines = lines + ["", pad + name]
    return lines


def width(line):
    """Columns a line takes on screen (colour codes take none)."""
    return len(re.sub(r"\033\[[0-9;]*m", "", line))


def parser():
    p = argparse.ArgumentParser()
    p.add_argument("--cols", type=int, default=100); p.add_argument("--rows", type=int, default=24)
    p.add_argument("--box", type=lambda s: [float(v) for v in s.split(",")])
    p.add_argument("--hide", type=lambda s: [float(v) for v in s.split(",")])
    p.add_argument("--gamma", type=float, default=1.0); p.add_argument("--level", type=float, default=0.5)
    p.add_argument("--edges", type=float, default=0.0); p.add_argument("--invert", action="store_true")
    p.add_argument("--mean", type=float); p.add_argument("--title")
    p.add_argument("--zoom", dest="zoom_in", action="store_true")
    p.add_argument("--detail", type=float, default=0.0)
    p.add_argument("--color", choices=["photo", "theme"])
    p.add_argument("--colors-toml", dest="colors_toml")
    return p


def main():
    if sys.argv[1:2] == ["--theme"]:
        # A theme's own: wallpapers.json "screensaver": {"from": <wallpaper>, "args": [<the options above>]}
        root = Path(__file__).resolve().parent.parent
        for slug in sys.argv[2:]:
            d = root / "themes" / slug
            spec = json.loads((d / "wallpapers.json").read_text())["screensaver"]
            name = (d / "README.md").read_text().splitlines()[0].lstrip("# ").strip()
            a = parser().parse_args(spec["args"])
            photo = next(p for p in (d / "backgrounds").iterdir() if p.stem == spec["from"])
            write(d / "screensaver.txt", art(photo, **{**vars(a), "title": a.title or name,
                                                       "colors_toml": d / "colors.toml"}))
        return
    p = parser(); p.add_argument("photo"); p.add_argument("out")
    a = vars(p.parse_args()); photo, out = a.pop("photo"), a.pop("out")
    write(out, art(photo, **a))


def write(out, lines):
    Path(out).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{out}: {max(map(width, lines))} x {len(lines)} cells")


if __name__ == "__main__":
    main()
