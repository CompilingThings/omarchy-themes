#!/usr/bin/env python3
"""Check every theme against the contract in CONTRIBUTING.md. Standard library only; exits 1 on any error.

Usage: tools/check.py [<theme> ...]

Checks, per theme:
  files       the files Omarchy needs are there, nothing else is, and no file is over GitHub's 50 MB warning size
  colours     colors.toml has every key Omarchy's stock themes have, each a #rrggbb colour (borders: Hyprland rgba)
  contrast    WCAG 2.2: foreground 7:1 on the background (AAA), the accent and the twelve terminal colours 4.5:1
  terminal    foot.ini uses colors.toml's colours in the slots Omarchy's own foot template gives them
  borders     hyprland.lua's border colours are colors.toml's hyprland_*_border
  shell       shell.*.toml only uses colours from the palette
  pictures    wallpapers are 3840x2160 (16:9), previews 16:9, unlock.png is the 800x188 logo with alpha,
              preview-unlock.png is 1920x1080
  credits     wallpapers.json lists exactly the files in backgrounds/, each with an author, a licence that has a
              text in LICENSES/, and a source page or the script that made it
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import themelib as T  # noqa: E402

MAX_BYTES = 50 * 1000 * 1000
TERMINAL = ["red", "orange", "yellow", "green", "cyan", "blue", "magenta",
            "bright_red", "bright_yellow", "bright_green", "bright_cyan", "bright_blue", "bright_magenta"]
# foot.ini slot -> colors.toml key, as in $OMARCHY_PATH/default/themed/foot.ini.tpl (Omarchy 4.5; its "purple" is
# the magenta key)
FOOT = {"foreground": "foreground", "background": "background", "regular0": "background", "regular1": "red",
        "regular2": "green", "regular3": "yellow", "regular4": "blue", "regular5": "magenta", "regular6": "cyan",
        "regular7": "foreground", "bright0": "muted", "bright1": "bright_red", "bright2": "bright_green",
        "bright3": "bright_yellow", "bright4": "bright_blue", "bright5": "bright_magenta", "bright6": "bright_cyan",
        "bright7": "bright_foreground"}
RGBA = re.compile(r"rgba\(([0-9a-fA-F]{8})\)")
EXTRA = {"README.md", "wallpapers.json", "backgrounds"}


class Report:
    def __init__(self):
        self.errors = 0

    def error(self, slug, what):
        self.errors += 1
        print(f"  ERROR {slug}: {what}")


def check_files(r, slug, d):
    for name in T.REQUIRED:
        if not (d / name).is_file():
            r.error(slug, f"missing {name}")
    for p in d.iterdir():
        if p.name not in T.SHIPPED and p.name not in EXTRA:
            r.error(slug, f"unexpected file {p.name} (not one Omarchy reads; see CONTRIBUTING.md)")
    for p in d.rglob("*"):
        if p.is_file() and p.stat().st_size > MAX_BYTES:
            r.error(slug, f"{p.relative_to(d)} is {p.stat().st_size / 1e6:.0f} MB (limit 50 MB)")
    readme = d / "README.md"
    if readme.is_file() and not readme.read_text().startswith("# "):
        r.error(slug, "README.md must start with '# <Theme name>'")


def check_colours(r, slug, c):
    for k in T.COLOR_KEYS:
        if k not in c:
            r.error(slug, f"colors.toml: missing {k}")
        elif not T.HEX.match(str(c[k])):
            r.error(slug, f"colors.toml: {k} = {c[k]!r} is not #rrggbb")
    for k in T.BORDER_KEYS:
        if k not in c or not RGBA.search(str(c[k])):
            r.error(slug, f"colors.toml: {k} must be Hyprland rgba(rrggbbaa) colour(s)")
    if c.get("mode") not in ("dark", "light"):
        r.error(slug, "colors.toml: mode must be \"dark\" or \"light\"")
    if any(k not in c or not T.HEX.match(str(c[k])) for k in ["background", "foreground", "accent", *TERMINAL]):
        return
    bg = c["background"]
    if (x := T.contrast(c["foreground"], bg)) < 7:
        r.error(slug, f"foreground on background is {x:.1f}:1 (needs 7:1)")
    for k in ["accent", *TERMINAL]:
        if (x := T.contrast(c[k], bg)) < 4.5:
            r.error(slug, f"{k} on background is {x:.1f}:1 (needs 4.5:1)")


def check_terminal(r, slug, d, c):
    foot = {}
    section = None
    for line in (d / "foot.ini").read_text().splitlines():
        line = line.strip()
        if line.startswith("["):
            section = line
        elif "=" in line and not line.startswith("#") and section == "[colors-dark]":
            k, v = line.split("=", 1)
            foot[k.strip()] = v.strip()
    for slot, key in FOOT.items():
        want = str(c.get(key, "")).lstrip("#").upper()
        if foot.get(slot, "").upper() != want:
            r.error(slug, f"foot.ini: {slot}={foot.get(slot)} but colors.toml {key} is {want}")
    alpha = float(foot.get("alpha", 1))
    if alpha < 1 and foot.get("blur") != "yes":
        r.error(slug, "foot.ini: a see-through terminal (alpha < 1) needs blur=yes")


def check_borders(r, slug, d, c):
    lua = (d / "hyprland.lua").read_text().lower()
    m = re.search(r"local active_border_color = (.*)", lua)
    want = RGBA.findall(str(c.get("hyprland_active_border", "")).lower())
    if not m or RGBA.findall(m.group(1)) != want:
        r.error(slug, "hyprland.lua: active border is not colors.toml's hyprland_active_border")
    m = re.search(r"local inactive_border_color = (.*)", lua)
    want = RGBA.findall(str(c.get("hyprland_inactive_border", "")).lower())
    if not m or RGBA.findall(m.group(1)) != want:
        r.error(slug, "hyprland.lua: inactive border is not colors.toml's hyprland_inactive_border")


def check_shell(r, slug, d, c):
    palette = {str(v).upper() for k, v in c.items() if k in T.COLOR_KEYS}
    for p in sorted(d.glob("shell.*.toml")):
        for hexcolor in re.findall(r"#[0-9A-Fa-f]{6}\b", p.read_text()):
            if hexcolor.upper() not in palette:
                r.error(slug, f"{p.name}: {hexcolor} is not a colour of colors.toml")


def check_pictures(r, slug, d):
    def size(name):
        p = d / name
        return T.image_size(p) if p.is_file() else None

    if (s := size("preview.png")) and s[0] * 9 != s[1] * 16:
        r.error(slug, f"preview.png is {s[0]}x{s[1]}, not 16:9")
    if (s := size("unlock.png")) and (s != (800, 188) or T.png_mode(d / "unlock.png") != 6):
        r.error(slug, "unlock.png must be the 800x188 RGBA logo (tools/unlock.py)")
    if (s := size("preview-unlock.png")) and s != (1920, 1080):
        r.error(slug, f"preview-unlock.png is {s[0]}x{s[1]}, not 1920x1080")
    for p in sorted((d / "backgrounds").glob("*")):
        if p.suffix not in T.BACKGROUND_TYPES:
            r.error(slug, f"backgrounds/{p.name}: not a .jpg, .png or .mp4")
        elif p.suffix != ".mp4" and T.image_size(p) != (3840, 2160):
            r.error(slug, f"backgrounds/{p.name} is {T.image_size(p)}, not 3840x2160")


def check_credits(r, slug, d, licences):
    try:
        spec = T.wallpapers(slug)
    except (OSError, ValueError) as e:
        r.error(slug, f"wallpapers.json: {e}")
        return
    listed = set()
    for w in spec.get("wallpapers", []):
        name = f"{w.get('file')}.{w.get('format', 'jpg')}"
        listed.add(name)
        if not w.get("by"):
            r.error(slug, f"wallpapers.json {name}: no 'by' (who made it)")
        if w.get("licence") not in licences:
            r.error(slug, f"wallpapers.json {name}: licence {w.get('licence')!r} has no text in LICENSES/")
        page, made = w.get("page", ""), w.get("made_with")
        if not page.startswith("https://") and not (made and (T.ROOT / made).exists()):
            r.error(slug, f"wallpapers.json {name}: needs a source page (https) or made_with (a file in this repo)")
    found = {p.name for p in (d / "backgrounds").glob("*")}
    for name in sorted(found - listed):
        r.error(slug, f"backgrounds/{name} is not in wallpapers.json (no credit)")
    for name in sorted(listed - found):
        r.error(slug, f"wallpapers.json lists {name}, which is not in backgrounds/")
    if not found:
        r.error(slug, "no wallpapers in backgrounds/")


def main(slugs):
    licences = {p.stem for p in (T.ROOT / "LICENSES").glob("*.txt")}
    r = Report()
    for slug in slugs or T.themes():
        d = T.THEMES / slug
        if not d.is_dir():
            r.error(slug, "no such theme")
            continue
        before = r.errors
        check_files(r, slug, d)
        try:
            c = T.colors(slug)
        except (OSError, ValueError) as e:
            r.error(slug, f"colors.toml: {e}")
            c = {}
        check_colours(r, slug, c)
        if c:
            check_terminal(r, slug, d, c)
            check_borders(r, slug, d, c)
            check_shell(r, slug, d, c)
        check_pictures(r, slug, d)
        check_credits(r, slug, d, licences)
        if r.errors == before:
            print(f"  ok    {slug}")
    print(f"{r.errors} error(s)" if r.errors else "all themes pass")
    return 1 if r.errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
