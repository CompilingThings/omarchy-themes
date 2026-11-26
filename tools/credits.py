#!/usr/bin/env python3
"""Write CREDITS.md and REUSE.toml from each theme's wallpapers.json. Standard library only.

Usage: tools/credits.py            write both files
       tools/credits.py --check    exit 1 if either file is not what this script would write

REUSE.toml follows the REUSE specification 3.3 (https://reuse.software/spec-3.3/): it names the copyright holder and
SPDX licence of every file that cannot carry a comment header, so `reuse lint` can check the whole repository.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import themelib as T  # noqa: E402

OWNER = "2026 CompilingThings"
OMARCHY = "David Heinemeier Hansson (Omarchy)"
LICENCE_NAMES = {
    "CC0-1.0": ("CC0 1.0 (public domain)", "https://creativecommons.org/publicdomain/zero/1.0/"),
    "CC-BY-2.0": ("CC BY 2.0", "https://creativecommons.org/licenses/by/2.0/"),
    "CC-BY-4.0": ("CC BY 4.0", "https://creativecommons.org/licenses/by/4.0/"),
    "CC-BY-SA-2.0": ("CC BY-SA 2.0", "https://creativecommons.org/licenses/by-sa/2.0/"),
    "CC-BY-SA-3.0": ("CC BY-SA 3.0", "https://creativecommons.org/licenses/by-sa/3.0/"),
    "CC-BY-SA-4.0": ("CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0/"),
    "CC-BY-SA-3.0-IGO": ("CC BY-SA 3.0 IGO", "https://creativecommons.org/licenses/by-sa/3.0/igo/"),
    "LicenseRef-CC-BY-SA-3.0-NO": ("CC BY-SA 3.0 NO", "https://creativecommons.org/licenses/by-sa/3.0/no/"),
    "CC-BY-NC-SA-2.0": ("CC BY-NC-SA 2.0 (non-commercial)", "https://creativecommons.org/licenses/by-nc-sa/2.0/"),
    "CC-BY-NC-SA-3.0": ("CC BY-NC-SA 3.0 (non-commercial)", "https://creativecommons.org/licenses/by-nc-sa/3.0/"),
    "LicenseRef-NASA-Media": ("NASA media guidelines", "https://www.nasa.gov/nasa-brand-center/images-and-media/"),
    "LicenseRef-USGS-Public-Domain": ("USGS, U.S. public domain",
                                      "https://www.usgs.gov/information-policies-and-instructions/copyrights-and-credits"),
}
# Files a theme took unchanged from Omarchy's own themes (MIT); see the theme's README.
FROM_OMARCHY = {"seahorse-valley": ["neovim.lua", "vscode.json", "icons.theme"]}


def entries(slug):
    spec = T.wallpapers(slug)
    for w in spec["wallpapers"]:
        yield f"{w['file']}.{w.get('format', 'jpg')}", w


def preview_source(slug):
    """preview.png is the theme's first photo-label wallpaper made small, or its first wallpaper."""
    ws = T.wallpapers(slug)["wallpapers"]
    return next((w for w in ws if w.get("format", "jpg") == "jpg"), ws[0])


def screensaver_source(slug):
    """The wallpaper a theme's screensaver.txt (text art) was made from: wallpapers.json "screensaver"."""
    if not (T.ROOT / "themes" / slug / "screensaver.txt").exists():
        return None
    spec = T.wallpapers(slug)
    return next(w for w in spec["wallpapers"] if w["file"] == spec["screensaver"])


def source(w):
    if w.get("page"):
        url = w["page"].split()[0]
        return f"[source]({url})"
    return f"made with `{w['made_with']}`"


def toml_str(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def holder(w):
    return OWNER if w["by"] == "CompilingThings" else w["by"]


def reuse():
    out = ["# Copyright and licence of every file that cannot carry a header (REUSE specification 3.3).",
           "# Written by tools/credits.py from themes/*/wallpapers.json; do not edit by hand.", "version = 1", ""]

    def value(v):
        v = v if isinstance(v, list) else [v]
        return toml_str(v[0]) if len(v) == 1 else "[" + ", ".join(toml_str(x) for x in v) + "]"

    def ann(paths, who, lic, precedence="override"):
        out.extend(["[[annotations]]", f"path = {value(paths)}", f"precedence = {toml_str(precedence)}",
                    f"SPDX-FileCopyrightText = {value(who)}", f"SPDX-License-Identifier = {toml_str(lic)}", ""])

    ann("**", OWNER, "MIT", "closest")      # code, theme files, docs; the pictures below override it
    ann(["themes/*/unlock.png", "themes/*/preview-unlock.png"], [OWNER, OMARCHY], "MIT")
    for slug in T.themes():
        for name in FROM_OMARCHY.get(slug, []):
            ann(f"themes/{slug}/{name}", OMARCHY, "MIT")
        for name, w in entries(slug):
            ann(f"themes/{slug}/backgrounds/{name}", holder(w), w["licence"])
        w = screensaver_source(slug)
        if w:
            ann(f"themes/{slug}/screensaver.txt", holder(w), w["licence"])
        w = preview_source(slug)
        ann(f"themes/{slug}/preview.png", holder(w), w["licence"])
        ann(f"docs/images/{slug}.jpg", holder(w), w["licence"])
    firsts = [preview_source(s) for s in T.themes()]
    ann("docs/images/gallery.jpg", sorted({holder(w) for w in firsts}),
        " AND ".join(sorted({w["licence"] for w in firsts})))
    return "\n".join(out).rstrip() + "\n"


def credits():
    out = ["# Credits", "",
           "Written by `tools/credits.py` from each theme's `wallpapers.json`; do not edit by hand.", "",
           "Every wallpaper prints its credit on its label (photos and fractals) or title block (boards). This file "
           "lists each one with its author, licence and source. The code, the theme files and the pictures made "
           "for this repository are by CompilingThings; see [README.md](README.md#licence).", "",
           "**Changes made to every photo:** cut to 16:9, scaled to 3840 x 2160, and a label added in the bottom "
           "right corner (the preview is the first one, made small). A wallpaper made from a share-alike (SA) "
           "photo is shared under that photo's licence; one made from a non-commercial (NC) photo may not be "
           "used commercially.", "",
           "## Licences used", ""]
    used = sorted({w["licence"] for s in T.themes() for _, w in entries(s)} | {"MIT"})
    for lic in used:
        name, url = LICENCE_NAMES.get(lic, (lic, None))
        link = f"[{name}]({url})" if url else name
        out.append(f"- `{lic}`: {link}, full text in [LICENSES/{lic}.txt](LICENSES/{lic}.txt)")
    out.append("")
    for slug in T.themes():
        out += [f"## {T.title(slug)}", "", "| Wallpaper | By | Licence | Source |", "|---|---|---|---|"]
        for name, w in entries(slug):
            lic = LICENCE_NAMES.get(w["licence"], (w["licence"],))[0]
            by = w["by"].replace("|", "\\|")
            out.append(f"| `{name}` | {by} | {lic} | {source(w)} |")
        w = screensaver_source(slug)
        if w:
            out += ["", f"`screensaver.txt`: text art of `{w['file']}` (`src/asciiart.py`), so by {w['by']}, "
                        f"{LICENCE_NAMES.get(w['licence'], (w['licence'],))[0]}, like that wallpaper."]
        if slug in FROM_OMARCHY:
            files = ", ".join(f"`{n}`" for n in FROM_OMARCHY[slug])
            out += ["", f"{files}: from Omarchy's Tokyo Night theme, unchanged, MIT, copyright {OMARCHY}."]
        out.append("")
    out += ["## Boot screen", "",
            "Each theme's `unlock.png` is Omarchy's logo (`default/plymouth/logo.png`, MIT, copyright "
            f"{OMARCHY}) in the theme's accent colour, as Omarchy's own themes do; `preview-unlock.png` shows it "
            "on the boot screen drawn from Omarchy's Plymouth pictures (`tools/unlock.py`).", ""]
    return "\n".join(out)


def main(check):
    want = {T.ROOT / "REUSE.toml": reuse(), T.ROOT / "CREDITS.md": credits()}
    stale = [p.name for p, text in want.items() if not p.is_file() or p.read_text() != text]
    if check:
        for name in stale:
            print(f"  ERROR {name} is out of date: run tools/credits.py")
        return 1 if stale else 0
    for p, text in want.items():
        p.write_text(text)
    print("wrote", ", ".join(p.name for p in want))
    return 0


if __name__ == "__main__":
    sys.exit(main("--check" in sys.argv[1:]))
