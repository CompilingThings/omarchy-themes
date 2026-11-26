# Contributing

Thank you for helping. Bug reports (a wallpaper label cut off on your screen, a colour hard to read, a wrong credit)
are as welcome as new themes. Please open an issue first for a new theme, so we can agree on the idea and its
pictures' licences before you do the work.

## The theme contract

Every theme in `themes/<slug>/` meets the same rules, and `tools/check.py` checks them all:

```sh
python3 tools/check.py          # every theme; or name some: python3 tools/check.py nordlys
python3 tools/credits.py --check
```

**Files.** A theme folder holds exactly these:

| File | What it is |
|---|---|
| `colors.toml` | The palette: every key Omarchy's stock themes have (`accent`, `selection`, `muted`, four backgrounds, four foregrounds, eight colours and six bright ones), plus `mode` and the two `hyprland_*_border` keys |
| `hyprland.lua` | Window borders (the same colours as `colors.toml`) and, if wanted, a glow |
| `foot.ini` | The terminal: `colors.toml`'s colours in the slots Omarchy's own foot template uses; `blur=yes` when `alpha` is below 1 |
| `shell.bar.toml`, `shell.controls.toml`, `shell.launcher.toml`, `shell.menu.toml` | Omarchy shell sections, using only palette colours |
| `icons.theme` | The icon theme's name (a Yaru colour) |
| `preview.png` | 16:9, shown by Omarchy's theme picker |
| `unlock.png`, `preview-unlock.png` | Boot screen logo and its preview, made by `tools/unlock.py` |
| `backgrounds/` | The wallpapers: 3840 x 2160 `.jpg` or `.png`, or an `.mp4` video |
| `wallpapers.json` | One entry per wallpaper: `file`, `by`, `licence` (SPDX), and `page` (its source) or `made_with` (the script in `src/` that made it) |
| `README.md` | Starts with `# <Theme Name>`: what the theme is, a table of its wallpapers, how they are made, credits |

Optional, when the theme takes them unchanged from an Omarchy theme: `neovim.lua`, `vscode.json`. Optional too:
`screensaver.txt`, the theme's text art for the screensaver, made from one of its wallpapers with `src/asciiart.py`
(shown by [`extras/screensaver`](extras/screensaver/README.md)); its `wallpapers.json` then names that wallpaper and
the settings as `"screensaver": {"from": ..., "args": [...]}`, so the art can be made again and carries its photo's
credit and licence. No other files: Omarchy ignores them, and an
unexpected file is usually a leftover.

**Colours.** Contrast is measured as in [WCAG 2.2](https://www.w3.org/TR/WCAG22/#dfn-contrast-ratio) against
`background`: `foreground` at least 7:1 (level AAA for body text); `accent` and the twelve terminal colours (`red`
to `magenta` and their bright forms) at least 4.5:1 (level AA). `muted`, `brown` and the dimmed foregrounds are for
quiet text and are not held to it.

**Wallpapers.**
- 3840 x 2160 (16:9). Omarchy fills the screen and crops what does not fit, from the centre, so text and anything
  that must be seen whole stay inside the middle 3240 x 2160, the part a 3:2 screen shows (16:10 shows more).
- Labels go bottom right: a terminal's text starts at the top left, so a see-through terminal rarely covers them.
- Each picture is checked at true screen size before it goes in: no visible grain (`src/grain.py` measures it;
  photos kept so far measure up to about 2.5), no blur, no stretched or upscaled source.
- No file is larger than 50 MB (GitHub warns above that).

**Credits.** A picture goes in only with a licence that allows sharing it, and its credit printed on the picture
when the licence asks for one. `tools/credits.py` writes [CREDITS.md](CREDITS.md) and [REUSE.toml](REUSE.toml) from
the `wallpapers.json` files; run it after any change to them. Every licence used has its full text in `LICENSES/`.

## Making the wallpapers

See [src/README.md](src/README.md). In short: `src/build <theme>` remakes a theme's wallpapers and preview from its
`wallpapers.json`, then `tools/unlock.py <theme>` remakes its boot screen pictures.

## Before a pull request

```sh
python3 tools/check.py && python3 tools/credits.py --check
shellcheck install src/build src/*/build
```

The same checks run on GitHub for every push and pull request ([.github/workflows/check.yml](.github/workflows/check.yml)).
Install the theme with `./install <theme>`, apply it with `omarchy theme set <theme>`, and look at every wallpaper
on a real screen.

By contributing you agree that your code is shared under the MIT licence and your own pictures under CC BY 4.0, as
in [README.md](README.md#licence).
