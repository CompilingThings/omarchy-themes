# Making the wallpapers

The finished wallpapers are in `themes/*/backgrounds/`, so nobody needs this folder to use the themes. It holds the
scripts that made them, so every picture can be made again and checked.

| Script | What it makes |
|---|---|
| [`build`](build) | Remakes a theme's wallpapers and preview: `src/build <theme>...` or `src/build --all` |
| [`photowall.py`](photowall.py) | Photo wallpapers: downloads each photo once, cuts it to 16:9 at 3840 x 2160, draws the label bottom right inside the 3:2 view; for Snow Crystal it first cuts the round plate out of each museum scan; with `fit` it sets a whole photo of one animal on a field of its own background colour (Pond Drop) |
| [`fractalwall.py`](fractalwall.py), [`fractal.c`](fractal.c) | Seahorse Valley's fractals, drawn from their formulas |
| [`termfractal.py`](termfractal.py) | One of those fractals drawn inside a terminal |
| [`earthspin.py`](earthspin.py) | Low Orbit's turning Earth video |
| [`trippyvid.py`](trippyvid.py), [`trippy.frag`](trippy.frag), [`trippygl.c`](trippygl.c) | Good Trip's moving patterns: the shader runs on the graphics chip without a window and ffmpeg makes each seamless loop |
| [`boardroom/`](boardroom/), [`traceroute/`](traceroute/) | The two board themes, from KiCad board files |
| [`asciiart.py`](asciiart.py) | A wallpaper as braille text art for a theme's `screensaver.txt` (see [`extras/screensaver`](../extras/screensaver/README.md)) |
| [`grain.py`](grain.py) | Measures a photo's grain at screen size, to check it before it goes in |

## What they need

- Python 3.11 or newer with [Pillow](https://pypi.org/project/pillow/); numpy for the fractals, the board themes
  and the Earth; scipy for the Earth and `grain.py`. On Arch: `sudo pacman -S python-pillow python-numpy python-scipy`.
  Or set `PYTHON` to a virtual environment that has them: `PYTHON=.venv/bin/python src/build nordlys`.
- gcc with OpenMP for the fractals; ffmpeg for the Earth; gcc, EGL with OpenGL ES 3.1 (Mesa or a GPU driver) and
  ffmpeg for Good Trip; KiCad 10 (`kicad-cli` and its `pcbnew` Python module) and
  `rsvg-convert` for the board themes.
- The labels use Nimbus Sans (`/usr/share/fonts/gsfonts`, package `gsfonts`) and the board themes JetBrains Mono Nerd
  Font, both installed with Omarchy.

## Examples

```sh
src/build nordlys                 # the photos (~110 MB) download once into ~/.cache/omarchy-themes/nordlys
src/build --all                   # every theme that can be made here (the board themes need BOARDS=<dir>)
python3 tools/unlock.py nordlys   # the boot screen pictures, after a colour change
python3 tools/credits.py          # CREDITS.md and REUSE.toml, after a wallpapers.json change
python3 tools/gallery.py          # docs/images (README pictures), after a preview.png changes

# Low Orbit's turning Earth: about 45 minutes at low priority on a ThinkPad T480 (measured 2026-11-18).
# A lossless master first, then the shipped file from it (H.264, 2560 x 1440, 30 fps, about 42 MB; crf 20
# measured SSIM 0.988 against the master, the same as crf 18 at 58 MB, and under the 50 MB check).
python3 src/earthspin.py ~/.cache/omarchy-themes/earthspin master.mkv --crf 0
ffmpeg -i master.mkv -c:v libx264 -preset slow -crf 20 -pix_fmt yuv420p -movflags +faststart \
  themes/low-orbit/backgrounds/0-earth-turning.mp4
```

Downloads go through each picture's `url` in `wallpapers.json`. Wikimedia Commons answers HTTP 429 (too many
requests) after about ten quick downloads; wait the ten minutes it asks for before trying again.
