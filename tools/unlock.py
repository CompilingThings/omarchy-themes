#!/usr/bin/env python3
"""Boot-screen files for each theme: unlock.png (the logo on the disk-unlock and login screens) and preview-unlock.png
(what that screen looks like, shown by Omarchy's boot-screen picker).

Usage: tools/unlock.py [<theme> ...]            (needs Pillow and Omarchy; all themes when none is named)

Made the way Omarchy makes its own (Omarchy 4.5):
- unlock.png is Omarchy's logo ($OMARCHY_PATH/default/plymouth/logo.png, MIT) in the theme's accent colour, the
  alpha kept, as the stock themes do (Catppuccin's unlock.png is that logo in its accent #89b4fa).
- omarchy-plymouth-set fills the screen with the theme's background, keeps the logo as it is, and paints the lock,
  the password field and its dots in the theme's foreground (magick +level-colors on their RGB). The layout copies
  default/plymouth/omarchy.script: logo centred, field 40 px under it, lock 15 px left of the field at 0.8 of its
  height, dots 7 px wide every 12 px from 20 px in. The preview shows four dots, like the stock previews.
"""
import os
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import themelib  # noqa: E402

PLYMOUTH = Path(os.environ.get("OMARCHY_PATH", "/usr/share/omarchy")) / "default" / "plymouth"
W, H = 1920, 1080


def tint(path, hexcolor):
    """The picture with every pixel's colour set to hexcolor and its alpha kept."""
    im = Image.open(path).convert("RGBA")
    out = Image.new("RGBA", im.size, (*themelib.rgb(hexcolor), 255))
    out.putalpha(im.getchannel("A"))
    return out


def make(slug):
    c = themelib.colors(slug)
    dest = themelib.THEMES / slug
    logo = tint(PLYMOUTH / "logo.png", c["accent"])
    logo.save(dest / "unlock.png", optimize=True)

    fg = c["foreground"]
    screen = Image.new("RGBA", (W, H), (*themelib.rgb(c["background"]), 255))
    lx, ly = W // 2 - logo.width // 2, H // 2 - logo.height // 2
    screen.alpha_composite(logo, (lx, ly))
    entry = tint(PLYMOUTH / "entry.png", fg)
    ex, ey = W // 2 - entry.width // 2, ly + logo.height + 40
    screen.alpha_composite(entry, (ex, ey))
    lh = entry.height * 0.8
    lw = 84 * lh / 96
    lock = tint(PLYMOUTH / "lock.png", fg).resize((round(lw), round(lh)), Image.LANCZOS)
    screen.alpha_composite(lock, (round(ex - lw - 15), round(ey + entry.height / 2 - lh / 2)))
    bullet = tint(PLYMOUTH / "bullet.png", fg).resize((7, 7), Image.LANCZOS)
    for i in range(4):
        screen.alpha_composite(bullet, (ex + 20 + i * 12, round(ey + entry.height / 2 - 3.5)))
    screen.convert("RGB").save(dest / "preview-unlock.png", optimize=True)
    print("unlock", slug, file=sys.stderr)


if __name__ == "__main__":
    for slug in sys.argv[1:] or themelib.themes():
        make(slug)
