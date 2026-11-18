#!/usr/bin/env python3
"""How grainy a photo will look as a wallpaper, measured at true screen size.

Usage: grain.py <photo> [<photo> ...]          (needs numpy, scipy, Pillow)

Each photo is cut to 16:9 round its middle and scaled to 2560x1440 (a 1440p laptop screen), then the noise is
estimated with Immerkaer's method (J. Immerkaer, "Fast Noise Variance Estimation", Computer Vision and Image
Understanding 64(2), 1996): the image filtered with a Laplacian-difference kernel, where real edges are left out
(the 10 % strongest gradients, so stars and sharp edges do not count as noise).
Printed: luminance sigma and colour (chroma) sigma, both in 8-bit steps.
From the space themes (2026-11-17/18), judged by eye at true size: up to about 2.5 looks clean; real fine detail
(gas threads, fields of faint galaxies, snow texture) can also score 2.5-3, so every photo above 2.5 still needs a
look at a true-size crop before it goes in or out; the Crab mosaic scored 4.1 and showed colour speckle.
"""
import sys

import numpy as np
from PIL import Image
from scipy.ndimage import convolve, sobel

K = np.array([[1, -2, 1], [-2, 4, -2], [1, -2, 1]], float)


def sigma(ch, keep):
    r = np.abs(convolve(ch, K, mode="reflect"))[1:-1, 1:-1]
    k = keep[1:-1, 1:-1]
    return float(np.sqrt(np.pi / 2) * r[k].mean() / 6)


def measure(path):
    im = Image.open(path).convert("RGB")
    w, h = im.size
    if w / h > 16 / 9:
        cw, ch = round(h * 16 / 9), h
    else:
        cw, ch = w, round(w * 9 / 16)
    im = im.crop(((w - cw) // 2, (h - ch) // 2, (w - cw) // 2 + cw, (h - ch) // 2 + ch))
    a = np.asarray(im.resize((2560, 1440), Image.LANCZOS), float)
    y = a @ [0.299, 0.587, 0.114]
    g = np.hypot(sobel(y, 0), sobel(y, 1))
    keep = g < np.percentile(g, 90)
    cb, cr = a[..., 2] - y, a[..., 0] - y
    return sigma(y, keep), (sigma(cb, keep) + sigma(cr, keep)) / 2, (w, h)


if __name__ == "__main__":
    for p in sys.argv[1:]:
        lum, col, (w, h) = measure(p)
        print(f"{lum:5.2f} luma  {col:5.2f} colour  {w}x{h}  {p}")
