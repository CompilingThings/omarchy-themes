# Screensaver

Omarchy's screensaver draws a text picture (`~/.config/omarchy/branding/screensaver.txt`) with a random animated
effect from [ttfx](https://github.com/ChrisBuilds/terminaltexteffects), in ttfx's own colours. These two small
scripts make it follow the theme: each theme's own picture, in the theme's colours.

| File | What it does | Install |
|---|---|---|
| [`theme-set`](theme-set) | Omarchy hook: on a theme change, copies the theme's `screensaver.txt` to the file the screensaver reads (the picture that was there first is kept and put back for a theme without one) | `cp theme-set ~/.config/omarchy/hooks/theme-set.d/20-omarchy-themes-screensaver` |
| [`ttfx`](ttfx) | Stands in for ttfx in the screensaver's call only: picks one of nine techie effects (decrypt, matrix rain, laser etch, synth grid, beams, binary path, VHS glitch, error correct, rings), colours it with the theme's two border colours, its bright text and its muted grey, and holds the finished picture 12 s. Every other ttfx call goes straight to `/usr/bin/ttfx` | `sudo install -m 755 ttfx /usr/local/bin/ttfx` |

Each works without the other: the hook alone gives each theme its picture in ttfx's colours; the stand-in alone
colours whatever picture is there. Undo: delete the two files.

The pictures are braille text art (each character a 2 x 4 grid of dots) made from one of the theme's wallpapers:

```sh
python3 src/asciiart.py themes/spore-garden/backgrounds/07-hazel-mildew.jpg themes/spore-garden/screensaver.txt \
  --cols 100 --rows 24 --box 0.14,0.0,0.70,0.9 --level 0.3 --gamma 0.7 --title "Spore Garden"
```

Omarchy's screensaver window (JetBrains Mono at 18 pt, full screen) is 111 x 27 characters on a 2560 x 1440 screen at
scale 1.6, so a picture of at most 100 x 24 plus the name fits.
