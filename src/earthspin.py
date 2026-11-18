#!/usr/bin/env python3
"""A turning Earth as a looping video wallpaper, made from real satellite maps (not a photo: a globe wrapped in them).

Usage: earthspin.py <cache dir> <out.mp4> [--seconds 60] [--fps 30] [--crf 18] [--test]     (needs numpy, scipy, Pillow, ffmpeg)

Maps (downloaded once into <cache dir>/src):
  day     Blue Marble Next Generation, July 2004, topography and bathymetry (NASA Earth Observatory)
  night   Black Marble 2016, city lights (NASA Earth Observatory / NASA Goddard, Suomi NPP VIIRS)
  clouds  8K cloud map from Solar System Scope (CC BY 4.0), made from NASA's Blue Marble clouds (same clouds as NASA's
          2048 px cloud_combined, with four times the detail). The 8K map has a grey haze over some land that NASA's
          has not (US plains: 58 against 20 of 255), so the cloud cover comes from NASA's map and only the fine
          detail from the 8K one.
One full turn in --seconds; the last frame leads straight back to the first, so the loop has no jump. The Sun stays put,
so the night side with its city lights sweeps across the globe as it turns. The globe leans 23.4 degrees like the real
Earth and is seen from 20 degrees north, so Norway comes past. The label is drawn like the photo themes' (bottom right).
--test writes still frames next to out.mp4 instead of the video.

Sharpness without flicker: a screen pixel covers a patch of the map, and that patch moves every frame. Reading the map
at one point per pixel makes edges (ice, coasts) crawl and the rim sparkle, so each pixel averages 2 x M points spread
over its patch: M = 2 in the middle, up to 8 near the rim where the globe curves away and the patch gets long. The map
is 8192 px wide, about 1.2 map pixels per point. Rows near the poles are smoothed sideways first, since the map
stretches them (a row there is short on the globe). All of this is fixed per pixel, so it is worked out once.
"""
import argparse
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter1d

sys.path.insert(0, str(Path(__file__).resolve().parent))
import photowall  # noqa: E402  (fetch and the label; its size constants are set to the video's below)

Image.MAX_IMAGE_PIXELS = None
W, H = 2560, 1440
NASA = "https://assets.science.nasa.gov/content/dam/science/esd/eo"
MAPS = {
    "day": f"{NASA}/images/bmng/bmng-topography-bathymetry/july/world.topo.bathy.200407.3x21600x10800.jpg",
    "night": f"{NASA}/images/imagerecords/144000/144898/BlackMarble_2016_3km.jpg",
    "clouds": "https://www.solarsystemscope.com/textures/download/8k_earth_clouds.jpg",
    "clouds_nasa": f"{NASA}/content-feature/bluemarble/images/cloud_combined_2048.jpg",
}
LABEL = {
    "title": "EARTH, TURNING",
    "line1": "One turn of the Earth, wrapped in real satellite maps. City lights shine on the night side.",
    "line2": "NASA Blue Marble (day) and Black Marble 2016 (night lights)  ·  clouds: Solar System Scope, CC BY 4.0",
}
ACCENT = (79, 201, 196)
TILT, VIEW_LAT = np.radians(23.4), np.radians(20.0)
SUN = np.array([0.90, 0.20, 0.36])                   # from the right, a little above and in front: a fat crescent of night
SUN /= np.linalg.norm(SUN)
R = 540                                              # globe radius in pixels
CX, CY = W * 0.5, H * 0.5
MW, MH = 8192, 4096                                  # map size, level 0
LEVELS = 5                                           # 8192 .. 512 wide, the small ones only for the last pixels at the rim
MAX_M = 8                                            # most points along a pixel's long side; past that, a smaller map


def lin(a):                                          # sRGB 0..255 -> linear 0..1, and back
    return (np.asarray(a, np.float32) / 255.0) ** 2.2


def srgb(a):
    return np.clip(np.clip(a, 0, 1) ** (1 / 2.2) * 255 + 0.5, 0, 255).astype(np.uint8)


def load_maps(cache):
    """One 5-channel map (day R G B, night lights, clouds) in LEVELS sizes, each flattened to (pixels, 5)."""
    src = cache / "src"
    src.mkdir(parents=True, exist_ok=True)
    p = {k: photowall.fetch(u, src / Path(u).name) for k, u in MAPS.items()}
    day = Image.open(p["day"])
    day.draft("RGB", (day.width // 2, day.height // 2))
    day = np.asarray(day.convert("RGB").resize((MW, MH), Image.LANCZOS))
    night = lin(Image.open(p["night"]).convert("RGB").resize((MW, MH), Image.LANCZOS)).mean(axis=2)
    # Black Marble's colour map has a dark blue land-and-sea base under the lights: keep only the lights
    glow = srgb(np.clip(night - 0.012, 0, None))                   # stored like a colour (gamma), read back with lin()
    clouds = cloud_map(p["clouds"], p["clouds_nasa"])
    m = np.dstack([day, glow, clouds]).astype(np.float32)
    levels = []
    for lv in range(LEVELS):
        if lv:
            m = 0.25 * (m[0::2, 0::2] + m[1::2, 0::2] + m[0::2, 1::2] + m[1::2, 1::2])
        levels.append(polar_smooth(m).reshape(-1, 5))
    return levels


def cloud_map(hi_path, nasa_path):
    """The 8K clouds, scaled per area so that, seen at 2048 px, they match NASA's own cloud map."""
    from scipy.ndimage import gaussian_filter
    hi = Image.open(hi_path).convert("L").resize((MW, MH), Image.LANCZOS)
    nasa = Image.open(nasa_path).convert("L")
    small = np.asarray(hi.resize(nasa.size, Image.BOX), np.float32)
    gain = np.asarray(nasa, np.float32) / np.maximum(small, 8.0)
    gain = gaussian_filter(np.clip(gain, 0, 2), 1.0, mode=("nearest", "wrap"))
    gain = np.asarray(Image.fromarray(gain).resize((MW, MH), Image.BICUBIC))
    return np.clip(np.asarray(hi, np.float32) * gain + 0.5, 0, 255).astype(np.uint8)


def polar_smooth(m):
    """Smooth each row sideways by as much as the map stretches it: a row at latitude lat is 1/cos(lat) too long."""
    h, w = m.shape[:2]
    lat = (0.5 - (np.arange(h) + 0.5) / h) * np.pi
    sigma = 0.35 * np.abs(np.tan(lat))                             # extra width, in map pixels, past what a point covers
    out = np.empty(m.shape, np.uint8)
    q = np.round(sigma * 8) / 8                                    # rows with the same smoothing go in one call
    for s in np.unique(q):
        rows = np.nonzero(q == s)[0]
        band = m[rows]
        if s < 0.2:
            pass
        elif s > w / 16:
            band = np.broadcast_to(band.mean(axis=1, keepdims=True), band.shape)
        else:
            band = gaussian_filter1d(band, s, axis=1, mode="wrap")
        out[rows] = np.clip(band + 0.5, 0, 255)
    return out


def sphere(px, py):
    """Screen point -> the point on the globe it shows: (lat, lon at turn 0), and the view-space normal."""
    nx, ny = (px - CX) / R, -(py - CY) / R
    nz = np.sqrt(np.clip(1 - nx * nx - ny * ny, 0, 1))
    c, s = np.cos(TILT), np.sin(TILT)
    ex, ey, ez = c * nx - s * ny, s * nx + c * ny, nz             # undo the lean (about the view axis)
    c, s = np.cos(VIEW_LAT), np.sin(VIEW_LAT)
    ey, ez = c * ey + s * ez, -s * ey + c * ez                     # then the view from 20 degrees north (about x)
    return np.arcsin(np.clip(ey, -1, 1)), np.arctan2(ex, ez), nx, ny, nz


def geometry():
    """Per pixel of the globe's box: the light on it, and the map points it averages, grouped by how many."""
    x0, y0 = int(CX - R - 2), int(CY - R - 2)
    ys, xs = np.mgrid[y0:y0 + 2 * R + 4, x0:x0 + 2 * R + 4].astype(np.float64)
    px, py = xs + 0.5, ys + 0.5
    _, _, nx, ny, nz = sphere(px, py)
    r = np.hypot(nx, ny)
    inside = r < 1.0 + 1.5 / R
    mu = nx * SUN[0] + ny * SUN[1] + nz * SUN[2]                       # sunlight on the surface
    half = SUN + np.array([0, 0, 1.0])
    half /= np.linalg.norm(half)
    spec = np.clip(nx * half[0] + ny * half[1] + nz * half[2], 0, 1) ** 260
    edge = np.clip((1 - r) * R + 0.5, 0, 1)                            # anti-aliased rim
    g = dict(box=(x0, y0), inside=inside, mu=mu, nz=nz, spec=spec, edge=edge)

    # A pixel covers 1/R radians of the globe across (sideways) and 1/(R nz) along the line to the centre (radial).
    # In level-0 map pixels (MH/pi per radian): 2.41 across everywhere, 2.41/nz radial. Two points across and M along
    # keep every point at <= 1.4 map pixels; where M would pass MAX_M, read a smaller map.
    k = MH / np.pi / R
    px, py, nz, r, nx, ny = (a[inside] for a in (px, py, nz, r, nx, ny))
    need = k / 1.4 / np.maximum(nz, 1e-4)
    lv = np.clip(np.ceil(np.log2(np.maximum(need / MAX_M, 1))), 0, LEVELS - 1).astype(int)
    M = np.clip(np.ceil(need / 2.0 ** lv), 2, MAX_M).astype(int)
    rx = np.where(r > 1e-6, nx / np.maximum(r, 1e-6), 1.0)           # radial direction on screen (y down)
    ry = np.where(r > 1e-6, -ny / np.maximum(r, 1e-6), 0.0)
    groups = []
    for key in sorted(set(zip(lv.tolist(), M.tolist()))):
        lvl, m = key
        idx = np.nonzero((lv == lvl) & (M == m))[0]
        a = (np.arange(m) + 0.5) / m - 0.5                            # spread along the radial line, within the pixel
        b = np.array([-0.25, 0.25])                                   # and two across
        oa = np.repeat(a, 2)[:, None]
        ob = np.tile(b, m)[:, None]
        sx = px[idx][None] + oa * rx[idx][None] - ob * ry[idx][None]
        sy = py[idx][None] + oa * ry[idx][None] + ob * rx[idx][None]
        lat, lon = sphere(sx, sy)[:2]
        u = ((lon / (2 * np.pi) + 0.5) % 1.0) * MW                   # level-0 map pixels, turn 0
        v = (0.5 - lat / np.pi) * MH
        groups.append((lvl, idx, u, v.astype(np.float32)))
    g["groups"] = groups
    g["count"] = int(inside.sum())
    return g


def bilinear(flat, lvl, u, v):
    w, h = MW >> lvl, MH >> lvl
    x = u / (1 << lvl) - 0.5
    y = v / (1 << lvl) - 0.5
    xf, yf = np.floor(x), np.floor(y)
    fx, fy = (x - xf).astype(np.float32)[..., None], (y - yf).astype(np.float32)[..., None]
    x0 = xf.astype(np.int64) % w
    x1 = (x0 + 1) % w
    y0 = yf.astype(np.int64)
    y1 = np.clip(y0 + 1, 0, h - 1) * w
    y0 = np.clip(y0, 0, h - 1) * w
    t = lambda i: np.take(flat, i, axis=0).astype(np.float32)
    top = t(y0 + x0) * (1 - fx) + t(y0 + x1) * fx
    bot = t(y1 + x0) * (1 - fx) + t(y1 + x1) * fx
    return top * (1 - fy) + bot * fy


def background(g):
    """Black space with the thin blue air glowing just outside the lit edge, and the label."""
    img = np.zeros((H, W, 3), np.float32)
    ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
    nx, ny = (xs + 0.5 - CX) / R, -(ys + 0.5 - CY) / R
    r = np.hypot(nx, ny)
    toward_sun = np.clip((nx * SUN[0] + ny * SUN[1]) / np.maximum(r, 1e-6) * 0.5 + 0.6, 0, 1.2)
    halo = np.exp(-np.clip(r - 1, 0, None) * R / 9.0) * (r >= 1) * toward_sun ** 1.5 * 0.55
    img += halo[..., None] * np.array([0.30, 0.55, 1.0], np.float32)
    photowall.W, photowall.H, photowall.S = W, H, 1.0                 # draw the label at the video's size
    pic = photowall.label(Image.fromarray(srgb(img)), LABEL, ACCENT)
    return np.asarray(pic)


def frame(g, maps, base, turn):
    m = g["inside"]
    texel = np.empty((g["count"], 5), np.float32)
    shift = turn * MW                                                  # eastward: land moves left to right
    for lvl, idx, u, v in g["groups"]:
        uu = ((u - shift) % MW).astype(np.float32)
        texel[idx] = bilinear(maps[lvl], lvl, uu, v).mean(axis=0)
    d = lin(texel[:, :3])
    n = lin(texel[:, 3]) * 2.4
    n = n[:, None] * np.array([1.0, 0.72, 0.42], np.float32)          # sodium orange
    c = (texel[:, 4] / 255.0) ** 1.4
    mu, nz, spec = g["mu"][m], g["nz"][m], g["spec"][m]
    lit = np.clip(mu, 0, 1)
    dayside = np.clip((mu + 0.06) / 0.18, 0, 1)                        # soft line between day and night
    water = ((d[:, 2] > d[:, 0] * 1.4) & (c < 0.3)).astype(np.float32)
    surface = d * (1 - c[:, None]) + c[:, None] * 0.92
    col = surface * (0.008 + 0.992 * lit ** 0.95)[:, None]
    col += (water * spec * dayside * 0.35)[:, None]                    # the Sun's glint on the sea
    col += n * ((1 - dayside) * (1 - 0.7 * c) * 1.6)[:, None]          # city lights on the night side, dimmed by cloud
    rim = (1 - nz) ** 2.2
    col += (rim * (0.12 + 0.88 * np.clip(mu + 0.25, 0, 1)) * 0.45)[:, None] * np.array([0.30, 0.55, 1.0], np.float32)
    x0, y0 = g["box"]
    hh, ww = m.shape
    out = base.copy()
    patch = out[y0:y0 + hh, x0:x0 + ww].astype(np.float32) / 255.0
    globe = np.zeros_like(patch)
    globe[m] = srgb(col).astype(np.float32) / 255.0
    a = g["edge"][..., None]
    out[y0:y0 + hh, x0:x0 + ww] = np.clip((globe * a + patch * (1 - a)) * 255 + 0.5, 0, 255).astype(np.uint8)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cache", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("--seconds", type=float, default=60)
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--crf", type=int, default=18, help="x264 quality: 0 = lossless master, 18 = near-transparent")
    ap.add_argument("--test", action="store_true")
    a = ap.parse_args()
    maps = load_maps(a.cache)
    g = geometry()
    base = background(g)
    a.out.parent.mkdir(parents=True, exist_ok=True)
    n = round(a.seconds * a.fps)
    if a.test:
        for i in (0, 600, 601, 1200):
            Image.fromarray(frame(g, maps, base, i / n)).save(a.out.with_name(f"{a.out.stem}-test-{i}.png"))
        return
    enc = subprocess.Popen(["nice", "-n", "19", "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                            "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(a.fps), "-i", "-",
                            "-c:v", "libx264", "-preset", "slow", "-crf", str(a.crf),
                            "-pix_fmt", "yuv444p" if a.crf == 0 else "yuv420p", "-threads", "2",
                            "-movflags", "+faststart", str(a.out)], stdin=subprocess.PIPE)
    for i in range(n):
        enc.stdin.write(frame(g, maps, base, i / n).tobytes())
        if i % 150 == 0:
            print(f"frame {i}/{n}", file=sys.stderr, flush=True)
    enc.stdin.close()
    sys.exit(enc.wait())


if __name__ == "__main__":
    main()
