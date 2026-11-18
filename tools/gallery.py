#!/usr/bin/env python3
"""Make the README pictures from each theme's preview.png: docs/images/<theme>.jpg and docs/images/gallery.jpg.

Usage: tools/gallery.py        (needs Pillow; the font is Nimbus Sans from gsfonts, as in src/photowall.py)

Run it after a theme's preview.png changes. The gallery is a 4-column grid, one tile per theme with its name in the
theme's accent colour; when the last row has room, the first free cell holds the repository's title.
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
from themelib import ROOT, THEMES, colors, themes, title  # noqa: E402

OUT = ROOT / "docs" / "images"
FONT = "/usr/share/fonts/gsfonts/NimbusSans-{}.otf"
THUMB = (640, 360)                 # README table: shown at its own size, sharp on 2x screens at 320 x 180
COLS, TILE, GAP, NAME_H = 4, (480, 270), 12, 44
BG = "#0b0b0f"


def font(size, bold=False):
    return ImageFont.truetype(FONT.format("Bold" if bold else "Regular"), size)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    slugs = themes()
    previews = {s: Image.open(THEMES / s / "preview.png").convert("RGB") for s in slugs}

    for s, im in previews.items():
        im.resize(THUMB, Image.LANCZOS).save(OUT / f"{s}.jpg", quality=88, optimize=True, progressive=True)

    rows = -(-len(slugs) // COLS)
    w = COLS * TILE[0] + (COLS + 1) * GAP
    h = rows * (TILE[1] + NAME_H) + (rows + 1) * GAP
    sheet = Image.new("RGB", (w, h), BG)
    d = ImageDraw.Draw(sheet)
    for i, s in enumerate(slugs):
        x = GAP + (i % COLS) * (TILE[0] + GAP)
        y = GAP + (i // COLS) * (TILE[1] + NAME_H + GAP)
        sheet.paste(previews[s].resize(TILE, Image.LANCZOS), (x, y))
        d.text((x + 2, y + TILE[1] + NAME_H // 2), title(s).upper(), font=font(20, True),
               fill=colors(s)["accent"], anchor="lm")
    if len(slugs) % COLS:
        i = len(slugs)
        x = GAP + (i % COLS) * (TILE[0] + GAP)
        y = GAP + (i // COLS) * (TILE[1] + NAME_H + GAP)
        cx, cy = x + TILE[0] // 2, y + (TILE[1] + NAME_H) // 2
        d.text((cx, cy - 22), "OMARCHY THEMES", font=font(40, True), fill="#e8e8ee", anchor="mm")
        d.text((cx, cy + 26), f"{len(slugs)} themes  ·  4K wallpapers  ·  credited", font=font(22),
               fill="#9a9aa8", anchor="mm")
    sheet.save(OUT / "gallery.jpg", quality=88, optimize=True, progressive=True)
    print(f"{len(slugs)} thumbnails and gallery.jpg ({w} x {h}) in {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
