#!/usr/bin/env python3
"""Pictures of each theme's screensaver for the READMEs: docs/images/screensavers/<theme>.png and, for the main
README, docs/images/screensavers.jpg (every one in a grid).

Usage: tools/screensavers.py        (needs Pillow; the font is Nimbus Sans from gsfonts, as in tools/gallery.py)

A screensaver.txt is braille text art (src/asciiart.py): each character a 2 x 4 grid of dots, coloured with 24-bit
colour codes. This draws it as it looks at the end of the screensaver's animation in Omarchy's full-screen terminal
(111 x 27 cells of JetBrains Mono at 18 pt on a 2560 x 1440 screen): each lit dot a round dot in its colour, on
black, centred, with the theme's name under it as on screen. Run it after a screensaver.txt changes.
"""
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
from themelib import ROOT, THEMES, themes, title  # noqa: E402

OUT = ROOT / "docs/images/screensavers"
FONT = "/usr/share/fonts/gsfonts/NimbusSans-Regular.otf"
COLS, ROWS = 111, 27                    # Omarchy's screensaver window in cells
CW, CH = 10, 20.5                       # one cell in pixels (JetBrains Mono's cell is about 2.05 times as tall as wide)
W, H = round(COLS * CW), round(ROWS * CH)
DOTS = [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (3, 0), (3, 1)]   # (row, column) of braille bits 0-7
CODE = re.compile(r"\033\[([0-9;]*)m|(.)", re.S)
GRID = 4                                # columns of the grid picture


def colour(params, default):
    p = params.split(";")
    return tuple(int(v) for v in p[2:5]) if p[:2] == ["38", "2"] else default


def draw(slug):
    lines = (THEMES / slug / "screensaver.txt").read_text(encoding="utf-8").splitlines()
    plain = [re.sub(r"\033\[[0-9;]*m", "", line) for line in lines]
    im = Image.new("RGB", (W, H), "black")
    d = ImageDraw.Draw(im)
    font = ImageFont.truetype(FONT, round(CH * 0.62))
    ox = (W - max(map(len, plain)) * CW) / 2
    oy = (H - len(lines) * CH) / 2
    r = CW * 0.17
    for row, line in enumerate(lines):
        rgb, col = (230, 230, 230), 0
        for m in CODE.finditer(line):
            if m.group(1) is not None:
                rgb = colour(m.group(1), (230, 230, 230))
                continue
            ch, x0, y0 = m.group(2), ox + col * CW, oy + row * CH
            bits = ord(ch) - 0x2800
            if 0 < bits < 256:
                for i, (dy, dx) in enumerate(DOTS):
                    if bits >> i & 1:
                        cx, cy = x0 + (dx + 0.5) * CW / 2, y0 + (dy + 0.5) * CH / 4
                        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=rgb)
            elif ch.strip():
                d.text((x0 + CW / 2, y0 + CH / 2), ch, font=font, fill=rgb, anchor="mm")
            col += 1
    return im


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    slugs = [s for s in themes() if (THEMES / s / "screensaver.txt").exists()]
    tiles = []
    for slug in slugs:
        im = draw(slug)
        im.save(OUT / f"{slug}.png", optimize=True)
        tiles.append(im.resize((W // 2, H // 2), Image.LANCZOS))
    tw, th = tiles[0].size
    rows = -(-len(tiles) // GRID)
    grid = Image.new("RGB", (tw * GRID, th * rows), "black")
    for i, t in enumerate(tiles):
        grid.paste(t, ((i % GRID) * tw, (i // GRID) * th))
    grid.save(ROOT / "docs/images/screensavers.jpg", quality=88, optimize=True)
    print(f"{len(slugs)} screensaver pictures and screensavers.jpg ({grid.width} x {grid.height}) in docs/images")


if __name__ == "__main__":
    main()
