#!/usr/bin/env python3
"""Boardroom wallpapers: the deck's own boards, rendered in 3D by KiCad, on a dark purple drawing sheet.

Usage: wallpaper.py <cache dir> <backgrounds dir> <preview.png>     (needs Pillow, numpy)
The cache holds <board>-top.png and <board>-iso.png (kicad-cli pcb render, transparent) and facts.json (facts.py).
Writes 1-all-boards.png (every board straight down, true size to each other) and one angled close-up per board,
each with a KiCad-style title block: name, job, size, layers, parts, vias.
"""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 3840, 2160
S = W / 2560                    # sizes below are set for a 2560-wide screen
# Omarchy crops a wallpaper to fill the screen. The drawing sheet (frame, zones, title block, boards) stays inside
# what a 3:2 screen shows, so it is whole on every common laptop; only the dot grid and glow run to the edges.
SAFE_X = round(W * (1 - (3 / 2) / (16 / 9)) / 2)
BG = np.array((12, 6, 18), np.float32)
GLOW = np.array((66, 22, 108), np.float32)
SILK = (240, 234, 248)
GOLD = (236, 198, 92)
DIM = (156, 138, 180)
FONT = "/usr/share/fonts/TTF/JetBrainsMonoNerdFont-{}.ttf"
TOP = round(64 * S)             # the Omarchy bar covers about 45 px at the top (28 px at scale 1.6) on a 2560 screen
SIDE, BOTTOM = SAFE_X + round(40 * S), round(40 * S)
M = round(22 * S)               # the zone-mark band
TB_W, TB_H = round(860 * S), round(196 * S)     # title block

BOARDS = {  # board: (name, job in plain words)
    "main-v1": ("MAIN", "Carrier for the LattePanda Mu Ultra: power, SSD, fans"),
    "io-v1": ("IO", "The ports: USB-C, USB-A, HDMI, microSD, headset, charging"),
    "keyboard-v1": ("KEYBOARD", "60 Kailh Choc hot-swap keys, white backlight"),
    "keyboard-plate-v1": ("KEYBOARD PLATE", "Holds the key switches in line"),
    "antenna-v1": ("ANTENNA", "The antenna bar along the top edge"),
    "screen-v1": ("SCREEN", "Screen adapter: the Mu's eDP and touch to the 7-inch panel"),
}
ORDER = ["main-v1", "io-v1", "keyboard-v1", "keyboard-plate-v1", "antenna-v1", "screen-v1"]
ROWS = [["keyboard-v1", "keyboard-plate-v1"], ["main-v1", "io-v1", "screen-v1"], ["antenna-v1"]]


def font(size, bold=False):
    return ImageFont.truetype(FONT.format("Bold" if bold else "Regular"), round(size * S))


def background(cx, cy):
    """Dark purple, a soft glow behind the board, and KiCad's dot grid."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    g = (np.clip(1 - np.hypot((xx - cx) / 1.3, yy - cy) / (1150 * S), 0, 1) ** 2 * 0.7)[..., None]
    img = BG * (1 - g) + GLOW * g
    pitch, dot = round(40 * S), round(2 * S)
    for dy in range(dot):
        for dx in range(dot):
            img[TOP + pitch // 2 + dy::pitch, pitch // 2 + dx::pitch] += 9
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).convert("RGBA")


def sheet(img, sheet_no, sheets, name, job, stats):
    """Drawing-sheet frame with zone marks and a title block, like a KiCad schematic page."""
    ov = Image.new("RGBA", img.size)
    d = ImageDraw.Draw(ov)
    line, faint = (*SILK, 70), (*SILK, 36)
    x0, y0, x1, y1 = SIDE, TOP, W - SIDE, H - BOTTOM
    lw = round(2 * S)
    d.rectangle((x0, y0, x1, y1), outline=faint, width=lw)
    m = M
    d.rectangle((x0 + m, y0 + m, x1 - m, y1 - m), outline=line, width=lw)
    small = font(15)
    for i in range(8):                                    # zones 1..8 across, A..E down
        xa = x0 + m + (x1 - x0 - 2 * m) * i / 8
        if i:
            for ya, yb in ((y0, y0 + m), (y1 - m, y1)):
                d.line((xa, ya, xa, yb), fill=faint, width=lw)
        xc = xa + (x1 - x0 - 2 * m) / 16
        for yc in (y0 + m / 2, y1 - m / 2):
            d.text((xc, yc), str(i + 1), font=small, fill=(*DIM, 150), anchor="mm")
    for i in range(5):
        ya = y0 + m + (y1 - y0 - 2 * m) * i / 5
        if i:
            for xa, xb in ((x0, x0 + m), (x1 - m, x1)):
                d.line((xa, ya, xb, ya), fill=faint, width=lw)
        yc = ya + (y1 - y0 - 2 * m) / 10
        for xc in (x0 + m / 2, x1 - m / 2):
            d.text((xc, yc), "ABCDE"[i], font=small, fill=(*DIM, 150), anchor="mm")
    bx1, by1 = x1 - m, y1 - m
    bx0, by0 = bx1 - TB_W, by1 - TB_H
    d.rectangle((bx0, by0, bx1, by1), fill=(10, 5, 16, 225), outline=line, width=lw)
    r1, r2, r3 = by0 + 70 * S, by0 + 116 * S, by0 + 162 * S
    thin = max(1, round(S))
    for y in (r1, r2, r3):
        d.line((bx0, y, bx1, y), fill=line, width=thin)
    d.line((bx1 - 210 * S, by0, bx1 - 210 * S, r1), fill=line, width=thin)
    tx = bx0 + 22 * S
    d.text((tx, by0 + 36 * S), name, font=font(44, True), fill=GOLD, anchor="lm")
    d.text((bx1 - 105 * S, by0 + 24 * S), "SHEET", font=font(15), fill=DIM, anchor="mm")
    d.text((bx1 - 105 * S, by0 + 48 * S), f"{sheet_no} / {sheets}", font=font(26, True), fill=SILK, anchor="mm")
    d.text((tx, (r1 + r2) / 2), job, font=font(23), fill=SILK, anchor="lm")
    d.text((tx, (r2 + r3) / 2), stats, font=font(23), fill=SILK, anchor="lm")
    d.text((tx, (r3 + by1) / 2), "BOARDROOM  ·  the cyberdeck's boards  ·  purple mask, white silk, ENIG",
           font=font(16), fill=DIM, anchor="lm")
    img.alpha_composite(ov)
    return (bx0, by0)


def load(path):
    """A render without KiCad's own drop shadow (pure black, part see-through): it reads as a grey box on a light
    page and a hard dark box here. The wallpaper draws a soft shadow of its own."""
    a = np.asarray(Image.open(path).convert("RGBA")).copy()
    a[(a[..., :3].max(axis=2) == 0) & (a[..., 3] < 255), 3] = 0
    return Image.fromarray(a)


def crop(path):
    im = load(path)
    return im.crop(im.getchannel("A").getbbox())


def board_box(im):
    """Bounding box of the solder mask (purple) in a straight-down render: the board's own outline, not the parts
    hanging over its edges."""
    a = np.asarray(im).astype(int)
    r, g, b, al = a[..., 0], a[..., 1], a[..., 2], a[..., 3]
    ys, xs = np.nonzero((al > 250) & (b > g + 30) & (r > g + 15))
    return xs.min(), ys.min(), xs.max() + 1, ys.max() + 1


def put(canvas, im, x, y):
    """alpha_composite that also takes a picture starting left of or above the canvas (cut off there)."""
    cx, cy = max(0, -x), max(0, -y)
    canvas.alpha_composite(im.crop((cx, cy, im.width, im.height)), (x + cx, y + cy))


def shadow(img, im, x, y, blur=36, drop=34, alpha=0.6):
    s = Image.new("RGBA", img.size)
    a = im.getchannel("A").point(lambda v: int(v * alpha))
    s.paste((0, 0, 0, 255), (x, y + round(drop * S)), a)
    img.alpha_composite(s.filter(ImageFilter.GaussianBlur(blur * S)))


def stats(f):
    parts = [f"{f['w']:g} x {f['h']:g} mm", f"{f['layers']} layers"]
    if f["parts"]:
        parts.append(f"{f['parts']} parts")
    if f["vias"]:
        parts.append(f"{f['vias']} vias")
    return "   ".join(parts)


def close_up(cache, b, f, sheet_no, sheets):
    im = crop(cache / f"{b}-iso.png")
    x0, y0 = SIDE + M + 60 * S, TOP + M + 50 * S
    x1, y1 = W - SIDE - M - 60 * S, H - BOTTOM - M - TB_H - 40 * S
    k = min((x1 - x0) / im.width, (y1 - y0) / im.height, 1.0)
    im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    x, y = round((x0 + x1 - im.width) / 2), round((y0 + y1 - im.height) / 2)
    img = background(x + im.width / 2, y + im.height / 2)
    shadow(img, im, x, y)
    img.alpha_composite(im, (x, y))
    name, job = BOARDS[b]
    sheet(img, sheet_no, sheets, f"{name}  {b.upper().split('-')[-1]}", job, stats(f))
    return img


def all_boards(cache, facts, sheets):
    gap, label = 12.0, 9.0                               # mm between boards; room under each for its name
    rows_w = [sum(facts[b]["w"] for b in row) + gap * (len(row) - 1) for row in ROWS]
    rows_h = [max(facts[b]["h"] for b in row) for row in ROWS]
    total_h = sum(rows_h) + label * len(ROWS) + gap * (len(ROWS) - 1)
    ax0, ay0 = SIDE + M + 70 * S, TOP + M + 60 * S
    ax1, ay1 = W - SIDE - M - 70 * S, H - BOTTOM - M - 50 * S
    k = min((ax1 - ax0) / max(rows_w), (ay1 - ay0) / total_h)   # px per mm, the same for every board
    img = background(W * 0.42, H * 0.5)
    over = Image.new("RGBA", img.size)
    labels = []
    y = ay0 + ((ay1 - ay0) - total_h * k) / 2
    left = ax0 + ((ax1 - ax0) - max(rows_w) * k) / 2      # the group centred, rows lined up on its left
    for row, rh in zip(ROWS, rows_h):
        x = left
        for b in row:
            im = load(cache / f"{b}-top.png")
            bx0, by0, bx1, by1 = board_box(im)
            s = k * facts[b]["w"] / (bx1 - bx0)          # render px -> wallpaper px, from the mask's width
            im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
            px, py = round(x - bx0 * s), round(y + (rh - facts[b]["h"]) * k / 2 - by0 * s)
            put(over, im, px, py)
            labels.append((x, y + (rh + facts[b]["h"]) * k / 2 + 14 * S, BOARDS[b][0],
                           f"{facts[b]['w']:g} x {facts[b]['h']:g} mm"))
            x += (facts[b]["w"] + gap) * k
        y += (rh + label + gap) * k
    shadow(img, over, 0, 0, blur=26, drop=24, alpha=0.65)
    img.alpha_composite(over)
    d = ImageDraw.Draw(img)
    for lx, ly, name, size in labels:
        d.text((lx, ly), name, font=font(24, True), fill=GOLD)
        d.text((lx + d.textlength(name, font=font(24, True)) + 16 * S, ly + 3 * S), size, font=font(20), fill=DIM)
    n = len(facts)
    tot = f"{n} boards   {sum(f['parts'] for f in facts.values())} parts   {sum(f['vias'] for f in facts.values())} vias"
    sheet(img, 1, sheets, "THE WHOLE DECK", "Every board, straight down, true size to each other", tot)
    return img


def main(cache, out, preview):
    facts = json.loads((cache / "facts.json").read_text())
    out.mkdir(parents=True, exist_ok=True)
    sheets = len(ORDER) + 1
    img = all_boards(cache, facts, sheets)
    img.convert("RGB").save(out / "1-all-boards.png")
    img.convert("RGB").resize((1280, 720), Image.LANCZOS).save(preview, optimize=True)
    for i, b in enumerate(ORDER, start=2):
        close_up(cache, b, facts[b], i, sheets).convert("RGB").save(out / f"{i}-{b}.png")
        print("wallpaper", i, b, file=sys.stderr)


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]))
