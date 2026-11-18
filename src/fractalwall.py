#!/usr/bin/env python3
"""Fractal pictures for an Omarchy theme: draws each one with fractal.c, at 3840x2160, for photowall.py to label.

Usage: fractalwall.py <wallpapers.json> <cache dir>      (needs Pillow, numpy, and gcc with OpenMP)

wallpapers.json is photowall.py's list (title, line1, line2 for the label) where each picture has
  local   the file name it is drawn to in <cache dir>/src
  render  {"kind": "mandel" | "julia" | "ship" | "newton" | "lyap" | "buddha" | "bulb", "args": ["key=value", ...]}
Each picture's colours are its own "grad=pos:rrggbb,..." in args (a looping ramp of colour stops).
fractal.c is compiled once into <cache dir>/fractal (again when the source is newer). A picture is drawn again only
when its args change (they are kept beside it as <file>.args). THREADS sets the cores used (default: all but two).
"""
import json
import os
import subprocess
import sys
import time
from pathlib import Path

from PIL import Image

W, H = 3840, 2160
HERE = Path(__file__).resolve().parent


def main(spec, cache):
    cfg = json.loads(spec.read_text())
    src = cache / "src"
    src.mkdir(parents=True, exist_ok=True)
    exe = cache / "fractal"
    code = HERE / "fractal.c"
    if not exe.exists() or exe.stat().st_mtime < code.stat().st_mtime:
        subprocess.run(["gcc", "-O3", "-march=native", "-fopenmp", "-o", str(exe), str(code), "-lm"], check=True)
    threads = os.environ.get("THREADS", str(max(1, (os.cpu_count() or 4) - 2)))
    for p in cfg["wallpapers"]:
        r = p["render"]
        args = r["args"]
        png, note = src / p["local"], (src / p["local"]).with_suffix(".args")
        want = " ".join([r["kind"]] + args)
        if png.exists() and note.exists() and note.read_text() == want:
            continue
        ppm = png.with_suffix(".ppm")
        t = time.time()
        print("drawing", p["file"], file=sys.stderr, flush=True)
        subprocess.run([str(exe), r["kind"], str(W), str(H), str(ppm)] + args, check=True,
                       env={**os.environ, "OMP_NUM_THREADS": threads})
        Image.open(ppm).save(png, optimize=False)
        ppm.unlink()
        note.write_text(want)
        print(f"drew {p['file']} in {time.time() - t:.0f} s", file=sys.stderr, flush=True)


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
