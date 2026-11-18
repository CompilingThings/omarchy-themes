# Low Orbit

An Omarchy theme made from real photos of Earth taken from the International Space Station, about 420 km up:
the station itself, a train of Starlink satellites, Patagonia's glacier lake,
a category 5 hurricane, sand dunes under the sea in the Bahamas, Mount Everest and the Sahara, plus a turning Earth
video. Deep-ocean dark background, the thin cyan line of the atmosphere as the accent, and the window border fading from that cyan into the warm gold of city lights at night.

Each wallpaper has a small label in the bottom right corner (bottom right because terminal text keeps to the left):
what it is, in plain words, how high up, who took it, when, and the credit.

| Wallpaper | What it shows | Taken by | Source |
|---|---|---|---|
| `0-earth-turning` (video) | One full turn of the Earth in 60 s, looping: day side, the Sun's glint on the sea, city lights on the night side | Made here by `src/earthspin.py`, not a photo: a globe wrapped in NASA's real satellite maps | [Blue Marble](https://science.nasa.gov/earth/earth-observatory/blue-marble-next-generation/) (July 2004 land and sea), [Black Marble 2016](https://science.nasa.gov/earth/earth-observatory/earth-at-night/) (city lights); clouds: [Solar System Scope 8K clouds](https://www.solarsystemscope.com/textures/), CC BY 4.0, brightness matched to NASA's Blue Marble clouds |
| `1-space-station` | The whole station above Earth, from the Soyuz taking its crew home after 197 days | Expedition 56 (Feustel, Arnold, Artemyev), 4 Oct 2018 | [iss056e201235](https://images.nasa.gov/details/iss056e201235) |
| `2-starlink-train` | A line of Starlink satellites rising past the southern lights (aurora australis), marked | ISS Expedition 62, 13 April 2020 | [ISS062-E-148365](https://eol.jsc.nasa.gov/SearchPhotos/photo.pl?mission=ISS062&roll=E&frame=148365), Starlink identification [Marco Langbroek](https://sattrackcam.blogspot.com/2020/04/starlink-train-photographed-from.html) |
| `3-lake-argentino` | Lake Argentino in Los Glaciares National Park, turquoise from glacier-ground rock, ringed by the snowy Andes | ISS Expedition 74, 6 May 2026 (NASA/Jessica Meir) | [iss074e0573516](https://images.nasa.gov/details/iss074e0573516) |
| `4-hurricane-melissa` | Category 5 Hurricane Melissa in the Caribbean Sea, about 80 km (50 miles) south of Jamaica | ISS Expedition 73, 28 Oct 2025 | [iss073e1044319](https://images.nasa.gov/details/iss073e1044319) |
| `5-dunes-under-the-sea` | Sandbars and underwater dunes off Eleuthera in the Bahamas, shaped by currents and waves | ISS Expedition 73, 15 Oct 2025 | [iss073e0880792](https://images.nasa.gov/details/iss073e0880792) |
| `6-mount-everest` | Mount Everest in the middle, clouds on Nepal's side of the Himalayas | ISS outside camera, Expedition 69, 13 April 2023 | [iss069e003192](https://images.nasa.gov/details/iss069e003192) |
| `7-sahara-desert` | Sand dunes, rock and sandstone plateaus in the Sahara, Algeria | ISS Expedition 66, 7 Feb 2022 | [iss066e137392](https://images.nasa.gov/details/iss066e137392) |

Heights are NASA's own numbers, turned from miles into km (the Starlink photo's 428 km is from its NASA astronaut
photo page). The Starlink satellites were spotted by Riccardo Rossi and identified by satellite tracker Marco Langbroek
as objects from the 17 February 2020 launch ("Starlink 4"); NASA's own caption does not name them. In the photo they
are the short sideways dashes in a line (the stars show as short upright streaks);
the small "Starlink train" mark sits under one in the middle of the line, placed from the annotated copy in
Langbroek's post.

## Install

```sh
./install low-orbit
omarchy theme set low-orbit
```

The turning Earth (`0-earth-turning.mp4`, 60 s, 2560 x 1440, looping) is a video wallpaper, played by owe, the video
wallpaper engine Omarchy uses. owe moves it even behind windows by default; to save power, set
`occupied_workspace = true` under `[pause]` in `~/.config/owe/config.toml` (then `owe reload-config`), so it only moves
while no window covers the desktop.

## How the wallpapers are made

- `wallpapers.json` lists each photo: download link, source page, credit and licence, label text, and where to cut it.
- [`src/photowall.py`](../../src/photowall.py) cuts each photo to 16:9 at 3840 x 2160 and draws its label inside the
  part a 3:2 screen shows; the same script makes every photo theme in this repository.
- `src/build low-orbit` makes them again from the photos (~25 MB, downloaded once into `~/.cache/omarchy-themes/low-orbit`).
- [`src/earthspin.py`](../../src/earthspin.py) renders the turning Earth: a globe wrapped in NASA's Blue Marble and
  Black Marble maps and Solar System Scope's clouds, lit by a fixed Sun, with the same label as the photos. One render
  takes about 45 minutes at low priority on a ThinkPad T480 (measured 2026-11-18); see [src/README.md](../../src/README.md).

## Credits

The photos come from NASA. [CREDITS.md](../../CREDITS.md) lists every wallpaper's author, licence and source. NASA
material "generally [is] not subject to copyright in the United States", and "NASA should be acknowledged as the
source of the material" ([NASA media guidelines](https://www.nasa.gov/nasa-brand-center/images-and-media/)). Every
wallpaper says NASA. The turning Earth is made for this theme from NASA's maps and Solar System Scope's
[clouds](https://www.solarsystemscope.com/textures/) (CC BY 4.0), and is itself shared under CC BY 4.0.

- The station photo's NASA page gives the credit as "NASA/Roscosmos" (it was taken from a Soyuz by a NASA and
  Roscosmos crew); the wallpaper prints that credit.
- The Starlink identification is credited to Marco Langbroek on the wallpaper.

## Picture quality

Every photo is checked at true screen size (2560x1440) before it goes in. Night photos of city lights did not pass:
an older frame of Northern Europe (2022) was grainy (grain 12.5 measured at screen size, against about 1 to 2.5 for
the photos kept), and a 2026 aurora over Europe, though far better, still was not crystal clear once cut to 16:9.
Three daytime photos from 2025-2026 (45-megapixel frames, 8256 px wide) replaced older soft ones. The Starlink photo
(2020) is cut to the sky, where the satellites and stars are sharp; its ground was smeared by the long exposure.
