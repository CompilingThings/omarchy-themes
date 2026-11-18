# Grand Tour

An Omarchy theme made from real photos of the outer solar system: Saturn and its rings from Cassini,
Jupiter and its moons Io and Europa from Juno, and Pluto from New Horizons. The name comes from
the Voyager probes' "Grand Tour" of the outer planets. Deep-space teal-black, Jupiter-cream text, a
Neptune teal accent, and the window border fading from that teal into the ochre of Jupiter's cloud belts.

Each wallpaper has a small label in the bottom right corner (bottom right because terminal text keeps
to the left): what it is, in plain words, how far away, who took it, when, and the credit.

| Wallpaper | What it shows | Taken by | Source |
|---|---|---|---|
| `1-saturn` | Saturn and its rings, 126 pictures joined into one natural-colour view, from 6.3 million km | Cassini, 6 Oct 2004 | [PIA06193](https://science.nasa.gov/photojournal/the-greatest-saturn-portrait-yet/) |
| `2-great-red-spot` | The Great Red Spot and the cloud bands of Jupiter's south, from 16,535 km above the clouds (colours enhanced) | Juno, 10 July 2017 | [PIA21778](https://science.nasa.gov/photojournal/jupiter-a-new-point-of-view/) |
| `3-blue-rays` | Pluto's night side with layers of blue haze lit from behind, close to true colour, from 200,000 km | New Horizons, 14 July 2015 | [PIA21590](https://science.nasa.gov/photojournal/blue-rays-new-horizons-high-res-farewell-to-pluto/) |
| `4-io` | Io's north polar region: low sunlight shows mountains up to 9.8 km high | Juno, 30 Dec 2023 | [PIA26484](https://science.nasa.gov/photojournal/juno-captures-north-polar-region-of-io/) |
| `5-farewell-to-saturn` | Cassini's last full picture of Saturn and its rings, two days before it plunged into the planet | Cassini, 13 Sept 2017 | [PIA17218](https://science.nasa.gov/photojournal/a-farewell-to-saturn/) |
| `6-europa` | Europa from 1,521 km up during Juno's close flyby: ridges and bands in the cracked ice, colours enhanced | Juno, 29 Sept 2022 | [PIA25334](https://science.nasa.gov/photojournal/junocam-image-of-europa-from-flyby/) |
| `7-string-of-pearls` | Jupiter's southern half with a white oval of the "String of Pearls" storms, from 33,115 km (colours enhanced) | Juno, 24 Oct 2017 | [PIA21970](https://science.nasa.gov/photojournal/jupiters-stunning-southern-hemisphere/) |
| `8-sunset-on-pluto` | Near sunset on Pluto: icy mountains up to 3,500 m, ice plains and more than a dozen haze layers | New Horizons, 14 July 2015 | [PIA19948](https://science.nasa.gov/photojournal/plutos-majestic-mountains-frozen-plains-and-foggy-hazes/) |

The Cassini farewell date is worked out from its page: "two days before" the end of the mission on 15 September 2017.
Europa's picture is 2300 px wide, a little under the 2560 px the others start from; at 2560x1440 it still looks sharp.

Uranus, Neptune, Titan and Enceladus are not in the pack: no NASA or ESA/Webb picture of them found was big
enough for a sharp 16:9 cut at 2560 px (biggest found: Voyager's Neptune PIA01492 at 2188 px, Webb's Uranus and
Neptune at 2058 and 1680 px, Cassini's single frames of Titan and Enceladus at about 1000 px; checked November 2026).

## Install

```sh
./install grand-tour
omarchy theme set grand-tour
```

## How the wallpapers are made

- `wallpapers.json` lists each photo: download link, source page, credit and licence, label text, and where to cut it.
- [`src/photowall.py`](../../src/photowall.py) cuts each photo to 16:9 at 3840 x 2160 and draws its label inside the
  part a 3:2 screen shows; the same script makes every photo theme in this repository.
- `src/build grand-tour` makes them again from the photos (~60 MB, downloaded once into `~/.cache/omarchy-themes/grand-tour`).

## Credits and licences

The photos come from NASA's Photojournal. [CREDITS.md](../../CREDITS.md) lists every wallpaper's author, licence and source.

- NASA pictures (Cassini, New Horizons, Juno) "generally are not subject to copyright in the United
  States", and "NASA should be acknowledged as the source"
  ([NASA media guidelines](https://www.nasa.gov/nasa-brand-center/images-and-media/)). Each wallpaper prints the
  credit from its Photojournal page: NASA/JPL/Space Science Institute and NASA/JPL-Caltech/Space Science Institute
  (Cassini), NASA/Johns Hopkins APL/Southwest Research Institute (New Horizons), NASA/JPL-Caltech/SwRI/MSSS
  (Juno).
- The Juno pictures are made by citizen scientists from raw JunoCam data, and NASA credits them by name:
  - `4-io`: image processing by Gerald Eichstädt (no licence mark on the page).
  - `2-great-red-spot` and `7-string-of-pearls`: Gerald Eichstädt and Seán Doran. Their pages mark these
    "© CC NC SA" ([Creative Commons BY-NC-SA](https://creativecommons.org/licenses/by-nc-sa/3.0/)): fine for a
    personal desktop with the credit shown, not for selling; a shared copy of the labelled wallpaper would carry
    the same licence.
  - `6-europa`: Björn Jónsson; the page marks it "CC BY-NC-SA 2.0", the same terms.
