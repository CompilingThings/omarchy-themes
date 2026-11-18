# Nordlys

An Omarchy theme of the northern lights seen from Norway ("nordlys" is Norwegian for northern lights), from
Bergen on the west coast to Kirkenes by the Russian border and Longyearbyen on Svalbard. Polar-night blue, snow-white
text, the green of oxygen glowing 100-300 km up as the accent, and the window border fading from that green into the
purple that nitrogen gives the aurora's lower edge ([Canadian Space Agency: the colours of the northern
lights](https://www.asc-csa.gc.ca/eng/astronomy/northern-lights/colours-of-northern-lights.asp)).

Each wallpaper has a small label in the bottom right corner (bottom right because terminal text keeps to the
left): the place, what it shows in plain words, when it was taken, the photographer and the licence.
Three photos with bright town lights under the label (Reine, Bergen, Svolvær) get a dark panel behind it.

| Wallpaper | What it shows | Taken | Photographer, licence | Source |
|---|---|---|---|---|
| `1-flakstad-lofoten` | Aurora over Flakstad, Lofoten (Commons featured picture) | not given (the date on the page is when it was published on Unsplash) | Johannes Groll (Unsplash), CC0 | [Commons](https://commons.wikimedia.org/wiki/File:Lofoten,_Norway_(Unsplash).jpg) |
| `2-reine-lofoten` | The aurora over Reine and its harbour lights | 11 Mar 2019 | Christoph Strässler, CC BY-SA 2.0 | [Commons](https://commons.wikimedia.org/wiki/File:Aurora_Borealis_(Northern_Light)_over_Reine,_Lofoten,_Norway1.jpg) |
| `3-bergen` | The aurora over Bergen's city lights | 6 Mar 2016 | Sindre Skrede, CC BY 2.0 | [Commons](https://commons.wikimedia.org/wiki/File:Aurora_borealis_over_Bergen,_Norway_(30990582790).jpg) |
| `4-kirkenes` | Blue-green aurora over a cottage at Kirkenes | 6 Apr 2016 | Stefan Stefancik, CC0 | [Commons](https://commons.wikimedia.org/wiki/File:Aurora_Borealis_over_Kirkenes,_Norway.jpg) |
| `5-kjerkfjorden-lofoten` | Green and purple aurora over Kjerkfjorden, Moskenes | 20 Feb 2023 | Eric Kilby, CC BY-SA 2.0 | [Commons](https://commons.wikimedia.org/wiki/File:Green_and_Purple_Aurora.jpg) |
| `6-longyearbyen-svalbard` | The aurora over the mountains by Longyearbyen | 22 Dec 2015 | Frode Ramone, CC BY 2.0 | [Commons](https://commons.wikimedia.org/wiki/File:Svalbard_DSCF1412_(23635947870).jpg) |
| `7-alnes-lighthouse` | The aurora over Alnes lighthouse, Godøya (Giske) | 17 Mar 2013 | Henny stokseth, CC BY-SA 3.0 NO | [Commons](https://commons.wikimedia.org/wiki/File:Alnes_fyr_i_mars_2013-07089.jpg) |
| `8-svolvaer-lofoten` | The aurora over red cabins by Svolvær's harbour | 16 Mar 2019 | Christoph Strässler, CC BY-SA 2.0 | [Commons](https://commons.wikimedia.org/wiki/File:Aurora_Borealis_(Northern_Light)_over_Svolv%C3%A6r,_Lofoten,_Norway1.jpg) |

Facts on the labels come from each photo's Commons page (place, date, description, map position) and:
Reine is a fishing village ([Wikipedia: Reine](https://en.wikipedia.org/wiki/Reine,_Norway)); Kirkenes lies close to the
Russian border ([Wikipedia: Kirkenes](https://en.wikipedia.org/wiki/Kirkenes)); round Longyearbyen's Isfjord the sun
stays below the horizon from 26 October to 15 February
([spitsbergen-svalbard.com](https://www.spitsbergen-svalbard.com/spitsbergen-information/midnight-sun-polar-night.html)),
so the 22 December photo is in the polar night.

Chosen from the 374 photos in Wikimedia Commons' [Aurora in Norway](https://commons.wikimedia.org/wiki/Category:Aurora_in_Norway)
category and its sub-categories: landscape photos at least 4500 pixels wide with a named place and a free
licence, then checked at true screen size. Grain at screen size (`src/grain.py`, Immerkaer sigma at 2560 x 1440;
the space themes looked clean up to about 2.5): Alnes 0.8, Kjerkfjorden 0.9, Kirkenes 1.0, Bergen 1.3,
Reine 1.4, Longyearbyen 1.4, Svolvær 2.3, Flakstad 2.3 (all looked clean in true-size crops). Left out: a 2025
substorm over Kvaløya, Tromsø (grain 4.3, and the people in it wear a company logo), photos with no named place,
and one uploaded by someone other than the photographer.

## Install

```sh
./install nordlys
omarchy theme set nordlys
```

## How the wallpapers are made

- `wallpapers.json` lists each photo: download link, source page, credit and licence, label text, and where to cut it.
- [`src/photowall.py`](../../src/photowall.py) cuts each photo to 16:9 at 3840 x 2160 and draws its label inside the
  part a 3:2 screen shows; the same script makes every photo theme in this repository.
- `src/build nordlys` makes them again from the photos (~110 MB, downloaded once into `~/.cache/omarchy-themes/nordlys`).

## Credits and licences

The photos come from Wikimedia Commons. [CREDITS.md](../../CREDITS.md) lists every wallpaper's author, licence and source. Every wallpaper
carries its photographer and licence on its label; the table above links each photo's page.

- [CC0](https://creativecommons.org/publicdomain/zero/1.0/): public domain, no conditions (credit given anyway).
- [CC BY 2.0](https://creativecommons.org/licenses/by/2.0/), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/):
  free to use and change with credit, a link to the licence, and a note of changes.
- [CC BY-SA 2.0](https://creativecommons.org/licenses/by-sa/2.0/), [CC BY-SA 3.0 NO](https://creativecommons.org/licenses/by-sa/3.0/no/):
  the same, and a changed picture must be shared under the same licence.

Changes made to every photo: cut to 16:9 and scaled to 3840 x 2160, and a label added in the bottom right corner.
A finished wallpaper made from a CC BY-SA photo is itself shared under that photo's CC BY-SA licence.
