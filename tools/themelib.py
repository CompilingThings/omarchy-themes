"""Shared reading of the themes in this repository, standard library only (so the checks run anywhere).

A theme is a folder themes/<slug>/ holding the files Omarchy reads (colors.toml and the rest), its wallpapers in
backgrounds/, and two files Omarchy ignores: README.md and wallpapers.json (credits and how each wallpaper is made).
"""
import json
import re
import struct
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
THEMES = ROOT / "themes"

# Every colour key of Omarchy's stock themes (tokyo-night/colors.toml, Omarchy 4.5), plus the two border keys.
COLOR_KEYS = [
    "accent", "selection", "muted",
    "background", "dark_background", "darker_background", "lighter_background",
    "foreground", "dark_foreground", "light_foreground", "bright_foreground",
    "red", "orange", "yellow", "green", "cyan", "blue", "magenta", "brown",
    "bright_red", "bright_yellow", "bright_green", "bright_cyan", "bright_blue", "bright_magenta",
]
BORDER_KEYS = ["hyprland_active_border", "hyprland_inactive_border"]

# Files a theme ships to ~/.config/omarchy/themes/<slug>/ (install copies only these, and backgrounds/).
REQUIRED = ["colors.toml", "icons.theme", "preview.png", "unlock.png", "preview-unlock.png",
            "hyprland.lua", "foot.ini",
            "shell.bar.toml", "shell.controls.toml", "shell.launcher.toml", "shell.menu.toml"]
OPTIONAL = ["neovim.lua", "vscode.json", "btop.theme", "chromium.theme", "keyboard.rgb"]
SHIPPED = REQUIRED + OPTIONAL
BACKGROUND_TYPES = {".jpg", ".png", ".mp4"}

HEX = re.compile(r"^#[0-9A-Fa-f]{6}$")


def themes():
    return sorted(p.name for p in THEMES.iterdir() if p.is_dir())


def colors(slug):
    return tomllib.loads((THEMES / slug / "colors.toml").read_text())


def wallpapers(slug):
    return json.loads((THEMES / slug / "wallpapers.json").read_text())


def title(slug):
    """The theme's name as its README's first heading gives it ("Seahorse Valley")."""
    for line in (THEMES / slug / "README.md").read_text().splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return slug.replace("-", " ").title()


def rgb(hexcolor):
    h = hexcolor.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def luminance(hexcolor):
    """WCAG 2.2 relative luminance."""
    def ch(c):
        c /= 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(c) for c in rgb(hexcolor))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def image_size(path):
    """(width, height) of a PNG or JPEG, read from its header; None for anything else."""
    with open(path, "rb") as f:
        head = f.read(26)
        if head[:8] == b"\x89PNG\r\n\x1a\n":
            return struct.unpack(">II", head[16:24])
        if head[:2] != b"\xff\xd8":
            return None
        f.seek(2)
        while True:
            marker = f.read(2)
            if len(marker) < 2 or marker[0] != 0xFF:
                return None
            if marker[1] in (0xD8, 0x01) or 0xD0 <= marker[1] <= 0xD7:
                continue
            (length,) = struct.unpack(">H", f.read(2))
            if marker[1] in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                h, w = struct.unpack(">xHH", f.read(5))
                return w, h
            f.seek(length - 2, 1)


def png_mode(path):
    """PNG colour type: 0 grey, 2 RGB, 3 palette, 4 grey + alpha, 6 RGBA."""
    with open(path, "rb") as f:
        return f.read(26)[25]


def dump_json(data):
    """JSON the way this repository writes it: two-space indent, short lists of numbers on one line."""
    text = json.dumps(data, indent=2, ensure_ascii=False)
    flat = re.compile(r"\[\s*((?:-?[\d.e+-]+,\s*)*-?[\d.e+-]+)\s*\]")
    return flat.sub(lambda m: "[" + ", ".join(x.strip() for x in m.group(1).split(",")) + "]", text) + "\n"
