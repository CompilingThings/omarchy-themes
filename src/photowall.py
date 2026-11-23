#!/usr/bin/env python3
"""Photo wallpapers for an Omarchy theme: real photos, cropped to 16:9, with a small label in the corner.

Usage: photowall.py <wallpapers.json> <cache dir> <backgrounds dir> <preview.png>     (needs Pillow)

wallpapers.json: {"accent": "#rrggbb", "wallpapers": [{"file", "by", "licence", "url", "page", "title", "line1",
                                                      "line2", "crop"}, ...]}
  file   output name without extension ("1-cosmic-cliffs")
  by, licence   the credit and its SPDX licence (for CREDITS.md and REUSE.toml, see tools/credits.py; not drawn)
  format optional: a wallpaper made by another script ("mp4", "png"); photowall.py leaves it alone
  url    the full-size picture; downloaded once into <cache dir>/src (kept under the link's own file name, shortened
         with a hash when it is too long for a file name)
  local  instead of url: a picture already in <cache dir>/src (one drawn here, like the fractals of Seahorse Valley)
  page   where the picture and its facts come from (for the README, not drawn)
  title, line1, line2   the label (bottom right): name, one line in plain words, then who took it, when, credit
  crop   [cx, cy, zoom]: centre of the cut as a fraction of the picture, zoom 1 = the biggest 16:9 cut that fits
  marks  optional [[x, y, "name"], ...]: a small tick and name under a point (pixels of the full picture),
         for something too small to find, like Earth seen from Saturn
  panel  optional true: a neat dark panel behind the label instead of the soft patch, for a bright photo;
         or a number 0-1 for how dark (true = 0.67; Nordlys' town lights needed 0.85)
  accent optional "#rrggbb": this picture's own label bar colour instead of the list's
  plate  optional true: a museum scan of a round photomicrograph mounted on a card (Snow Crystal's Bentley prints):
         the dark round plate is cut out and set on a field of its own dark colour first (needs numpy and scipy)
  fit    optional true or {"h", "w", "x", "y", "box", "field", "hide"}: a tall or square photo of one subject on a plain
         background (a water flea on black): the whole photo, or the part in "box" ([x0, y0, x1, y1] as fractions),
         is set "h" of the screen high (default 0.94; above 1 cuts into it) and at most "w" of it wide (default 0.96;
         0.84 keeps it inside a 3:2 screen) with its centre at "x", "y" (default 0.42, 0.5, left of centre
         so the label stays clear), on a field of the photo's own edge colour ("field": "#rrggbb" to choose it);
         its edges fade into the field over "feather" of its shorter side (default 0.15). "hide": boxes (fractions of
         the whole photo) painted in the field colour first, for a scale bar on the plain background. "oval": true
         or [inner, outer] (default 0.98, 1.15, as fractions of the oval that just fits the photo): the fade follows
         an oval instead of the photo's box, for a round slice on a coloured background (Stem Glow's twigs), so no
         lit box shows round it. "crop" then applies to that 16:9 picture.
Writes <backgrounds dir>/<file>.jpg at 3840x2160 and <preview.png> (the first photo, 1280x720).
"""
import hashlib
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

Image.MAX_IMAGE_PIXELS = None          # Webb mosaics are 120+ million pixels; they are trusted NASA/ESA files
W, H = 3840, 2160
S = W / 2560                           # label sizes are set for a 2560-wide screen
# Omarchy fills the screen and crops what does not fit (PreserveAspectCrop), centred. On a 3:2 screen (Framework 13,
# Surface) a 16:9 picture loses (16/9 - 3/2) / (16/9) / 2 = 7.8 % on each side; 16:10 loses 5 %. Labels stay inside
# the 3:2 view so every common laptop shows them whole.
SAFE = 1 - (3 / 2) / (16 / 9)          # the share of the width a 3:2 screen does not show (both sides together)
SANS = "/usr/share/fonts/gsfonts/NimbusSans-{}.otf"


def cache_name(url):
    """The link's own file name; a very long one (a long Cyrillic title is ~400 bytes percent-encoded, past the
    255-byte limit of a file name) keeps its start and gets a short hash of the whole name."""
    name = Path(urllib.parse.urlparse(url).path).name
    if len(name.encode()) <= 200:
        return name
    stem, ext = os.path.splitext(name)
    return f"{stem[:120]}-{hashlib.sha1(name.encode()).hexdigest()[:10]}{ext}"


def fetch(url, dest):
    if dest.exists() and dest.stat().st_size:
        return dest
    print("download", url, file=sys.stderr)
    tmp = dest.with_suffix(dest.suffix + ".part")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"})
    with urllib.request.urlopen(req, timeout=120) as r, open(tmp, "wb") as f:
        while chunk := r.read(1 << 20):
            f.write(chunk)
    tmp.rename(dest)
    return dest


def cut(path, cx, cy, zoom):
    """The 16:9 cut at W x H, and a function taking full-picture pixels to wallpaper pixels."""
    im = Image.open(path)
    w, h = im.size
    cw = min(w, h * W / H) / zoom
    ch = cw * H / W
    x0 = min(max(cx * w - cw / 2, 0), w - cw)
    y0 = min(max(cy * h - ch / 2, 0), h - ch)
    to_wall = lambda x, y: ((x - x0) * W / cw, (y - y0) * H / ch)
    fx = fy = 1.0
    if im.format == "JPEG":            # decode at a smaller size straight away when the cut allows it
        k = max(1, int(cw // W))
        im.draft("RGB", (w // k, h // k))
        # each side scales on its own: the decoder rounds width and height up separately, and one shared factor
        # put the box past the bottom edge of a 12101 x 6546 photo
        fx, fy = im.size[0] / w, im.size[1] / h
    im = im.convert("RGB")
    box = (x0 * fx, y0 * fy, (x0 + cw) * fx, (y0 + ch) * fy)
    return im.resize((W, H), Image.LANCZOS, box=box, reducing_gap=3.0), to_wall


def plate(path, dest):
    """Cut the round dark plate out of a scanned card and set it on a W x H field of the plate's own dark colour, 88 %
    of the height and left of centre so the bottom right stays clear for the label. The plate is found as the largest connected dark area on the cream card, left of the colour
    chart the scan carries on its right (which has black patches too), inside the scanner's black bands."""
    if dest.exists() and dest.stat().st_size:
        return dest
    import numpy as np
    from scipy import ndimage
    im = Image.open(path).convert("RGB")
    a = np.asarray(im).astype(float)
    lum = a.mean(axis=2)
    h, w = lum.shape
    card = lum > 150
    cc = np.where(card.sum(axis=0) > h * 0.3)[0]
    cr = np.where(card.sum(axis=1) > w * 0.2)[0]
    x0, x1, y0, y1 = cc.min() + 25, min(cc.max(), int(w * 0.82)), cr.min() + 25, cr.max() - 25
    dark = np.zeros(lum.shape, bool)
    dark[y0:y1, x0:x1] = lum[y0:y1, x0:x1] < 70
    lab, _ = ndimage.label(dark)
    ys, xs = np.where(lab == np.argmax(np.bincount(lab.ravel())[1:]) + 1)
    cx, cy = (xs.min() + xs.max()) / 2, (ys.min() + ys.max()) / 2
    r = min(xs.max() - xs.min(), ys.max() - ys.min()) / 2 * 0.965   # stay inside the plate's ragged edge
    yy, xx = np.mgrid[0:h, 0:w]
    dist = np.hypot(xx - cx, yy - cy)
    field = tuple(int(v) for v in np.median(a[(dist > r * 0.97) & (dist < r) & dark], axis=0))
    d = int(H * 0.88)
    disc = im.crop((round(cx - r), round(cy - r), round(cx + r), round(cy + r))).resize((d, d), Image.LANCZOS)
    mask = Image.new("L", (d * 4, d * 4), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, d * 4 - 1, d * 4 - 1), fill=255)
    mask = mask.resize((d, d), Image.LANCZOS).filter(ImageFilter.GaussianBlur(d * 0.004))
    out = Image.new("RGB", (W, H), field)
    out.paste(disc, (round(W * 0.41 - d / 2), round(H * 0.47 - d / 2)), mask)
    dest.parent.mkdir(parents=True, exist_ok=True)
    out.save(dest)
    return dest


def fit(path, dest, opt):
    """Set the whole photo (or its "box") on a W x H field of its own edge colour; see "fit" at the top."""
    opt = opt if isinstance(opt, dict) else {}
    im = Image.open(path).convert("RGB")
    w, h = im.size
    if "field" in opt:
        field = tuple(int(opt["field"][i:i + 2], 16) for i in (1, 3, 5))
    else:                              # the median of a thin strip all round: the plain background behind the subject
        b = max(2, round(min(w, h) * 0.02))
        strip = [im.crop(r) for r in ((0, 0, w, b), (0, h - b, w, h), (0, 0, b, h), (w - b, 0, w, h))]
        px = sorted(sum((list(s.resize((64, 4) if s.width > s.height else (4, 64)).get_flattened_data()) for s in strip), []),
                    key=sum)
        field = px[len(px) // 2]
    for x0, y0, x1, y1 in opt.get("hide", []):     # a scale bar on the plain background: painted over with it
        ImageDraw.Draw(im).rectangle((round(x0 * w), round(y0 * h), round(x1 * w), round(y1 * h)), fill=field)
    if "box" in opt:
        x0, y0, x1, y1 = opt["box"]
        im = im.crop((round(x0 * w), round(y0 * h), round(x1 * w), round(y1 * h)))
    w, h = im.size
    k = min(H * opt.get("h", 0.94) / h, W * opt.get("w", 0.96) / w)
    nw, nh = round(w * k), round(h * k)
    im = im.resize((nw, nh), Image.LANCZOS)
    feather = round(min(nw, nh) * opt.get("feather", 0.15))
    mask = Image.new("L", (nw, nh), 0)
    d = ImageDraw.Draw(mask)
    for i in range(feather):           # a smooth fade over the outer 15 % on every side ("feather" to change it)
        t = (i + 1) / feather
        d.rectangle((i, i, nw - 1 - i, nh - 1 - i), outline=round(255 * t * t * (3 - 2 * t)))
    d.rectangle((feather, feather, nw - 1 - feather, nh - 1 - feather), fill=255)
    if opt.get("oval"):                # a round subject on a coloured background: fade along an oval, not the box
        r0, r1 = opt["oval"] if isinstance(opt["oval"], list) else (0.98, 1.15)
        n = 512                        # the oval drawn small and scaled up: smooth, and fast at 4K
        oval = Image.new("L", (n, n), 0)
        od = ImageDraw.Draw(oval)
        steps = 64
        for i in range(steps + 1):     # rings from the outer edge inwards, each a little brighter (smoothstep)
            r = r1 - (r1 - r0) * i / steps
            t = i / steps
            e = n / 2 * r
            od.ellipse((n / 2 - e, n / 2 - e, n / 2 + e, n / 2 + e), fill=round(255 * t * t * (3 - 2 * t)))
        oval = oval.resize((nw, nh), Image.BILINEAR).filter(ImageFilter.GaussianBlur(min(nw, nh) * 0.004))
        mask = ImageChops.multiply(mask, oval)
    out = Image.new("RGB", (W, H), field)
    cx, cy = opt.get("x", 0.42), opt.get("y", 0.5)
    left = min(max(round(W * cx - nw / 2), 0), W - nw)
    top = min(max(round(H * cy - nh / 2), 0), H - nh)
    out.paste(im, (left, top), mask)
    dest.parent.mkdir(parents=True, exist_ok=True)
    out.save(dest)
    return dest


def mark(img, xy, name):
    """A thin tick under the point and its name, like the labels NASA puts on its own copies."""
    x, y = xy
    ov = Image.new("RGBA", img.size)
    d = ImageDraw.Draw(ov)
    d.line((x, y + 16 * S, x, y + 44 * S), fill=(220, 228, 240, 170), width=max(1, round(1.2 * S)))
    d.text((x, y + 52 * S), name, font=font(15), fill=(220, 228, 240, 200), anchor="mt")
    out = img.convert("RGBA")
    out.alpha_composite(ov)
    return out.convert("RGB")


def font(size, bold=False):
    return ImageFont.truetype(SANS.format("Bold" if bold else "Regular"), round(size * S))


def spaced(d, xy, text, f, fill, gap):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=f, fill=fill)
        x += d.textlength(ch, font=f) + gap
    return x


def label(img, p, accent):
    """Bottom right (terminal text keeps to the left, so a see-through terminal rarely covers it): the name in
    spaced capitals, one plain line, then the credit line, right-aligned beside a thin accent bar.
    A soft dark patch behind it keeps it readable on bright nebulae."""
    x_end, y_end = W - round(W * SAFE / 2) - round(60 * S), H - round(64 * S)
    ft, f1, f2 = font(30, True), font(22), font(17)
    rows = [(p["title"], ft, (238, 242, 248), 22 * S), (p["line1"], f1, (214, 221, 232), 12 * S),
            (p["line2"], f2, (160, 170, 186), 0)]
    heights = [f.getbbox("Ag")[3] for _, f, _, _ in rows]
    total = sum(heights) + sum(g for *_, g in rows)
    y = y_end - total
    probe = ImageDraw.Draw(img)
    track = 4 * S                                                  # extra space between the title's letters

    def width(text, f):
        return probe.textlength(text, font=f) + (track * (len(text) - 1) if f is ft else 0)

    x = x_end - max(width(t, f) for t, f, _, _ in rows)

    shade = Image.new("L", img.size, 0)
    if p.get("panel"):                 # a bright photo: a neat dark panel, since a soft patch reads as a smudge there
        ImageDraw.Draw(shade).rounded_rectangle((x - 30 * S, y - 24 * S, x_end + 34 * S, y_end + 20 * S),
                                                radius=12 * S, fill=170 if p["panel"] is True else round(255 * p["panel"]))
        shade = shade.filter(ImageFilter.GaussianBlur(1.2 * S))
    else:
        ImageDraw.Draw(shade).rounded_rectangle((x - 70 * S, y - 50 * S, x_end + 60 * S, y_end + 44 * S),
                                                radius=40 * S, fill=150)
        shade = shade.filter(ImageFilter.GaussianBlur(46 * S))
    img.paste(Image.new("RGB", img.size, (0, 0, 0)), (0, 0), shade)

    glow = Image.new("RGBA", img.size)
    d = ImageDraw.Draw(glow)
    bar_x = x_end + round(19 * S)
    d.rectangle((bar_x, y + 2 * S, bar_x + round(3 * S), y_end), fill=(*accent, 255))
    yy = y
    for (text, f, fill, gap), h in zip(rows, heights):
        tx = x_end - width(text, f)
        if f is ft:
            spaced(d, (tx, yy), text, f, (*fill, 255), track)
        else:
            d.text((tx, yy), text, font=f, fill=(*fill, 255))
        yy += h + gap
    soft = glow.filter(ImageFilter.GaussianBlur(3 * S))           # a faint halo so the letters lift off the photo
    dark = Image.new("RGBA", img.size, (0, 0, 0, 0))
    dark.putalpha(soft.getchannel("A").point(lambda v: v * 0.7))
    out = img.convert("RGBA")
    out.alpha_composite(dark)
    out.alpha_composite(glow)
    return out.convert("RGB")


def main(spec, cache, out, preview):
    cfg = json.loads(spec.read_text())
    accent = tuple(int(cfg["accent"][i:i + 2], 16) for i in (1, 3, 5))
    (cache / "src").mkdir(parents=True, exist_ok=True)
    out.mkdir(parents=True, exist_ok=True)
    photos = [p for p in cfg["wallpapers"] if p.get("format", "jpg") == "jpg"]
    for old in out.glob("*.jpg"):      # the theme's own wallpaper folder: drop pictures no longer on the list
        if old.stem not in {p["file"] for p in photos}:
            old.unlink()
    for i, p in enumerate(photos):
        src = (cache / "src" / p["local"] if "local" in p else
               fetch(p["url"], cache / "src" / cache_name(p["url"])))
        if p.get("plate"):
            src = plate(src, cache / "plates" / f"{src.stem}.png")
        if p.get("fit"):               # named after the settings too, so a changed "fit" is made again
            tag = hashlib.sha1(json.dumps(p["fit"], sort_keys=True).encode()).hexdigest()[:8]
            src = fit(src, cache / "fits" / f"{src.stem}-{tag}.png", p["fit"])
        img, to_wall = cut(src, *p.get("crop", [0.5, 0.5, 1.0]))
        for x, y, name in p.get("marks", []):
            img = mark(img, to_wall(x, y), name)
        own = p.get("accent")
        img = label(img, p, tuple(int(own[i:i + 2], 16) for i in (1, 3, 5)) if own else accent)
        img.save(out / f"{p['file']}.jpg", quality=92, subsampling=0, optimize=True)
        if i == 0:
            img.resize((1280, 720), Image.LANCZOS).save(preview)
        print("wallpaper", p["file"], file=sys.stderr)


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4]))
