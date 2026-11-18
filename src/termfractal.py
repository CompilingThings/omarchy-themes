#!/usr/bin/env python3
"""One of Seahorse Valley's fractals, drawn inside the terminal: the same formula, view and colours as its wallpaper
(fractal.c with the picture's own settings from themes/seahorse-valley/wallpapers.json), two square pixels per character cell (the upper
half block, 24-bit foreground and background colours).

Usage: termfractal.py <name> [cols rows]
  name       any part of a picture's file name: mandelbrot, rabbit, newton, buddhabrot, mandelbulb, ...
  cols rows  the drawing's size in cells (default: the terminal's width, its height less 4 rows: the prompt and its blank line, before and after)
Each drawing is kept in ~/.cache/omarchy-themes/seahorse-valley/term, so the second time it prints at once. fractal.c is compiled
there by fractalwall.py (or here, when it is missing). The Buddhabrot keeps the wallpaper's paths per pixel.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
CACHE = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")) / "omarchy-themes" / "seahorse-valley"


def main():
    name = sys.argv[1]
    if len(sys.argv) > 3:
        cols, rows = int(sys.argv[2]), int(sys.argv[3])
    else:
        size = os.get_terminal_size()
        cols, rows = size.columns, size.lines - 4
    photos = json.loads((HERE.parent / "themes" / "seahorse-valley" / "wallpapers.json").read_text())["wallpapers"]
    p = next((p for p in photos if name.lower() in p["file"]), None)
    if p is None:
        sys.exit("pictures: " + ", ".join(p["file"] for p in photos))
    kind, args = p["render"]["kind"], list(p["render"]["args"])
    w, h = cols, rows * 2
    if kind == "buddha":                       # the same number of paths per pixel as the 3840x2160 wallpaper
        args = [f"samples={max(int(float(a[8:]) * w * h / (3840 * 2160)), 2_000_000)}" if a.startswith("samples=")
                else a for a in args]
    exe = CACHE / "fractal"
    if not exe.exists() or exe.stat().st_mtime < (HERE / "fractal.c").stat().st_mtime:
        exe.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["gcc", "-O3", "-march=native", "-fopenmp", "-o", str(exe), str(HERE / "fractal.c"), "-lm"],
                       check=True)
    out = CACHE / "term" / f"{p['file']}-{cols}x{rows}.ppm"
    note = out.with_suffix(".args")
    want = " ".join([kind] + args)
    if not (out.exists() and note.exists() and note.read_text() == want):
        out.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run([str(exe), kind, str(w), str(h), str(out)] + args, check=True, stderr=subprocess.DEVNULL)
        note.write_text(want)
    px = np.asarray(Image.open(out).convert("RGB"))
    lines = []
    for r in range(rows):
        top, bot = px[2 * r], px[2 * r + 1]
        lines.append("".join(f"\x1b[38;2;{a[0]};{a[1]};{a[2]}m\x1b[48;2;{b[0]};{b[1]};{b[2]}m▀"
                             for a, b in zip(top, bot)) + "\x1b[0m")
    sys.stdout.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
