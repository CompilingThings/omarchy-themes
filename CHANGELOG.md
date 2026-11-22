# Changelog

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow
[Semantic Versioning](https://semver.org/) (a theme renamed or removed is a major change, a new theme minor, a fixed
picture or colour a patch).

## [Unreleased]

### Added

- Thunderhead: fourteen photos of thunderstorms (lightning at night, shelf clouds, mammatus, a glowing anvil top)
  from Wikimedia Commons with free licences, among them NOIRLab's 1972 Kitt Peak storm; lightning violet and
  electric blue.
- Cold Blood: fourteen close-ups of frogs, lizards, snakes and crocodiles (eyes, heads and scales) from
  Wikimedia Commons with free licences; red-eyed tree frog red and pit viper green.
- Snow Crystal: twelve of Wilson Bentley's snowflake photomicrographs (The Met, CC0), each round plate cut
  from the museum's scan onto a dark field by a new `"plate": true` option in `src/photowall.py`.
- Deep Sea: twelve close photos of jellyfish and comb jellies lit in dark water and a deep-sea isopod from
  900 m, all from Wikimedia Commons with free licences; white-spotted jellyfish blue and bluefire purple.
- Compound Eye: fourteen macro photos of insect faces, twelve from the USGS Bee Inventory and Monitoring Lab (U.S.
  public domain) and two Commons featured pictures; cuckoo wasp green and iridescent blue. Adds the USGS public
  domain licence note.
- Fairy Ring: twelve photos of mushrooms and other fungi from Wikimedia Commons (fly agarics, glowing mushrooms,
  amethyst deceivers, a latticed stinkhorn and more); fly agaric red and amethyst purple. Adds the CC BY-SA 3.0 and
  CC BY-SA 4.0 licence texts.

### Fixed

- `src/photowall.py`: a very large JPEG decoded at reduced size could put the crop box a fraction of a pixel
  past the bottom edge and stop the build; width and height now scale on their own.

## [1.0.0] - 2026-11-18

First release: eleven themes for Omarchy 4.5.

- Themes: Boardroom, Deep Field, Grand Tour, Low Orbit, Nordlys, Red Planet, Seahorse Valley, Solar Max, Stardust,
  Traceroute, Tranquility.
- `install` copies one theme, several, or all of them into `~/.config/omarchy/themes`, and only ever replaces a
  theme it installed itself.
- Every theme ships Omarchy's boot screen files (`unlock.png`, `preview-unlock.png`), made the way Omarchy makes its
  own.
- Every still wallpaper is 3840 x 2160 (Low Orbit's turning Earth is a 2560 x 1440 video), with its label or
  title block inside the part a 3:2 screen shows.
- `tools/check.py` holds every theme to one contract (files, colours, WCAG contrast, terminal and border colours,
  picture sizes, credits); `tools/credits.py` writes CREDITS.md and REUSE.toml from the themes' `wallpapers.json`.
  Both run on GitHub for every push.

[1.0.0]: https://github.com/CompilingThings/omarchy-themes/releases/tag/v1.0.0
