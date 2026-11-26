#!/usr/bin/env python3
"""A moving (looping) or still trippy picture, drawn on the graphics chip: trippy.frag run by trippygl.c.

Usage: trippyvid.py --theme <theme dir> <cache dir>   (every wallpaper of wallpapers.json with a "draw", see below)
       trippyvid.py <kind> <out.mp4 | out.png> [--size 2560x1440] [--frames 360] [--fps 30] [--crf 20]
                    [--preview STEP] [--maxrate 12M] key=value ...
  kind   mandala  a Julia set z -> z^2 + c lit by orbit traps (a ring "tr" and a cross), as lace
         bloom    the same Julia set lit where its orbit crosses a ring of petals (pk petals, radius pr, wobble pa,
                  width petw; each later step fainter by pdec and shifted along the colours by tstep)
         liquid   warped value noise (fbm fed through itself, strength wk, scale ws), a bright ridge at its middle
         tunnel   the mandala or bloom (inner=bloom) tiled down a log-polar spiral: depth rings per e-fold, rep tiles
                  round, a glowing core (core, cores) and a dark mouth (fade)
         hyper    the {p,q} tiling of the hyperbolic plane, in the Poincare disk or (model=band) the band model
  keys   view: cx cy (centre), w (width), rot (degrees), ss (samples per pixel side), gain
         colour: grad (stops "pos:rrggbb,..." looping 0 to 1), bg (rrggbb), scale, offset
         symmetry: fold (wedges), mirror (0 or 1), twist (spiral twist of the wedges)
         Julia: ca cb (c), zs zx zy (zoom and shift of z), maxiter, esck escg (how bright escaping points glow),
         lace lacek cross tr (mandala)
         motion over one loop, each coming back to its start so the video loops without a seam: cyc (colour
         cycles), spin (wedges, or tile corners, turned), crad (radius of the circle c walks), zoom (tunnel rings
         fallen), flow (radius of the circle the liquid's noise walks)
  .png   one still frame (at phase "t", default 0) instead of a video
  --preview STEP   draw only every STEP-th frame (a quick look at the motion)
--theme: each wallpaper's "draw" is "<kind> key=value ..." (the arguments above); "frames" (default 360) and "size"
(default 2560x1440) are optional. A video is drawn again only when its draw, frames, size or trippy.frag change
(the cache keeps the last one); then it is copied to backgrounds/<file>.mp4, and preview.png is the first video's
first frame at 1280x720.
Needs gcc, EGL and OpenGL ES 3.1 (Mesa), ffmpeg. trippygl is compiled next to the output's cache on first use.
"""
import argparse
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
KINDS = {"mandala": 0, "bloom": 1, "liquid": 2, "tunnel": 3, "hyper": 4}
DEFAULTS = dict(cx=0, cy=0, w=4, rot=0, ss=3, scale=0.3, offset=0, gain=1, fold=0, mirror=1, twist=0,
                ca=-0.8, cb=0.156, zs=1, zx=0, zy=0, tr=0.5, lace=0.9, lacek=0.01, cross=0.6, esck=6, escg=1.4,
                pr=0.6, pa=0.35, pk=6, tstep=0.11, petw=0.012, pdec=0.86, maxiter=300,
                ws=1.5, wk=4, ridge=0.6, ridgek=0.006, lgam=1.6,
                depth=0.6, rep=8, spiral=1, ts=2.4, fade=0.35, core=0, cores=0.05,
                p=7, q=3, model=0, edge=1.2, edgek=0.006, cstep=0.07, tilek=1.5, tfill=0.55,
                cyc=0, spin=0, crad=0, zoom=0, flow=0, t=0)
INTS = {"ss", "maxiter"}
GRAD = "0:05020c,0.2:6a1bb0,0.4:ff3fa4,0.55:ffd24a,0.7:2fe0c8,0.85:2a4bd8"


def s2l(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def glf(x):
    """a float literal GLSL ES accepts (always with a point or an exponent)"""
    s = f"{float(x):.9g}"
    return s if any(ch in s for ch in ".e") else s + ".0"


def header(kind, kv):
    v = dict(DEFAULTS)
    for k, x in kv.items():
        if k in ("grad", "bg", "inner", "model"):
            continue
        if k not in v:
            sys.exit(f"unknown key {k}")
        v[k] = float(x)
    v["model"] = 1 if kv.get("model") == "band" else 0
    lines = ["#version 310 es", "precision highp float;", "precision highp int;",
             "uniform vec2 uRes;", "uniform float uT;", "out vec4 oColor;", f"#define KIND {KINDS[kind]}"]
    for k, x in v.items():
        if k == "t":
            continue
        name = {"w": "VW", "p": "HP", "q": "HQ", "maxiter": "MAXIT"}.get(k, k.upper())
        lines.append(f"#define {name} {int(x)}" if k in INTS else f"#define {name} {glf(x)}")
    lines.append(f"#define INNER_BLOOM {1.0 if kv.get('inner') == 'bloom' else 0.0}")
    bg = kv.get("bg", "030208")
    lines.append("#define BG vec3({:.6f}, {:.6f}, {:.6f})".format(*(s2l(int(bg[i:i + 2], 16) / 255) for i in (0, 2, 4))))
    stops = []
    for tok in kv.get("grad", GRAD).split(","):
        pos, col = tok.split(":")
        stops.append((float(pos), [s2l(int(col[i:i + 2], 16) / 255) for i in (0, 2, 4)]))
    stops.sort()
    lines.append(f"const int GN = {len(stops)};")
    lines.append("const float GP[GN] = float[](" + ", ".join(f"{p:.6f}" for p, _ in stops) + ");")
    lines.append("const vec3 GC[GN] = vec3[](" + ", ".join("vec3({:.6f}, {:.6f}, {:.6f})".format(*c) for _, c in stops) + ");")
    return "\n".join(lines) + "\n", v["t"]


def theme(tdir, cache):
    import hashlib
    import json
    import shlex
    import shutil
    tdir, cache = Path(tdir), Path(cache)
    cache.mkdir(parents=True, exist_ok=True)
    spec = json.loads((tdir / "wallpapers.json").read_text())
    shader = (HERE / "trippy.frag").read_bytes() + (HERE / "trippygl.c").read_bytes()
    made = []
    for w in spec["wallpapers"]:
        if "draw" not in w:
            continue
        args = shlex.split(w["draw"])
        size, frames = w.get("size", "2560x1440"), str(w.get("frames", 360))
        key = hashlib.sha256(shader + json.dumps([args, size, frames]).encode()).hexdigest()
        vid, stamp = cache / f"{w['file']}.mp4", cache / f"{w['file']}.key"
        if not (vid.exists() and stamp.exists() and stamp.read_text() == key):
            print(f"drawing {w['file']} ({frames} frames at {size})", file=sys.stderr, flush=True)
            subprocess.run([sys.executable, __file__, args[0], str(vid), "--size", size, "--frames", frames, *args[1:]],
                           check=True)
            stamp.write_text(key)
        dst = tdir / "backgrounds" / f"{w['file']}.mp4"
        dst.parent.mkdir(exist_ok=True)
        if not dst.exists() or dst.read_bytes() != vid.read_bytes():
            shutil.copyfile(vid, dst)
        made.append(dst)
    if made:
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(made[0]), "-frames:v", "1", "-vf", "scale=1280:720:flags=lanczos",
                        str(tdir / "preview.png")], check=True)


def main():
    if sys.argv[1:2] == ["--theme"]:
        return theme(sys.argv[2], sys.argv[3])
    ap = argparse.ArgumentParser()
    ap.add_argument("kind", choices=KINDS)
    ap.add_argument("out")
    ap.add_argument("--size", default="2560x1440")
    ap.add_argument("--frames", type=int, default=360)
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--crf", type=int, default=20)
    ap.add_argument("--preview", type=int, default=1)
    ap.add_argument("--maxrate", default="12M", help="bitrate cap, keeps a detailed loop small enough for git")
    ap.add_argument("keys", nargs="*")
    a = ap.parse_args()
    kv = dict(k.split("=", 1) for k in a.keys)
    head, t0 = header(a.kind, kv)
    w, h = map(int, a.size.split("x"))
    cache = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")) / "omarchy-themes" / "trippygl"
    cache.mkdir(parents=True, exist_ok=True)
    exe = cache / "trippygl"
    if not exe.exists() or exe.stat().st_mtime < (HERE / "trippygl.c").stat().st_mtime:
        subprocess.run(["gcc", "-O2", "-o", str(exe), str(HERE / "trippygl.c"), "-lEGL", "-lGLESv2"], check=True)
    with tempfile.NamedTemporaryFile("w", suffix=".frag", delete=False) as f:
        f.write(head + (HERE / "trippy.frag").read_text())
        frag = f.name
    out = Path(a.out)
    if out.suffix == ".png":
        # one frame at phase t: draw frame round(t * 1000) of a 1000-frame loop
        k = int(round(t0 * 1000)) % 1000
        gl = subprocess.Popen([str(exe), frag, str(w), str(h), "1000", str(k), "1000"], stdout=subprocess.PIPE)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}",
                        "-i", "-", "-frames:v", "1", str(out)], stdin=gl.stdout, check=True)
    else:
        gl = subprocess.Popen([str(exe), frag, str(w), str(h), str(a.frames), "0", str(a.preview)], stdout=subprocess.PIPE)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}",
                        "-r", str(a.fps // a.preview if a.preview > 1 else a.fps), "-i", "-",
                        "-c:v", "libx264", "-preset", "slow", "-crf", str(a.crf), "-maxrate", a.maxrate,
                        "-bufsize", str(2 * int(a.maxrate.rstrip("M"))) + "M", "-pix_fmt", "yuv420p",
                        "-movflags", "+faststart", str(out)], stdin=gl.stdout, check=True)
    gl.wait()
    os.unlink(frag)
    if gl.returncode:
        sys.exit(gl.returncode)


if __name__ == "__main__":
    main()
