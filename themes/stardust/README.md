# Stardust

An Omarchy theme made from the clearest nebula pictures of 2026: stars being born and stars dying, from the
James Webb Space Telescope, Hubble and Euclid. A violet-black sky, starlight text, the rose of glowing hydrogen
as the accent, and the window border fading from that rose into the gold of the Helix Nebula's dust.

Each wallpaper has a small label in the bottom right corner (bottom right because terminal text keeps to the
left): what it is, in plain words, how far away, who took it, when, and the credit.

| Wallpaper | What it shows | Taken by | Source |
|---|---|---|---|
| `1-helix-nebula` | Comet-shaped knots of gas round a dying star, 650 light-years away ("the clearest infrared look at this familiar object") | Webb, 20 Jan 2026 | [weic2601a](https://esawebb.org/images/weic2601a/), facts [weic2601](https://esawebb.org/news/weic2601/) |
| `2-cats-head-nebula` | A dust pillar in the Carina Nebula, 7,500 light-years away | Webb NIRCam, 29 Oct 2026 | [weic2622c](https://esawebb.org/images/weic2622c/), facts [weic2622](https://esawebb.org/news/weic2622/) |
| `3-cats-eye-nebula` | NGC 6543, a dying star's shells and its halo of gas fragments, 4,400 light-years away | Euclid + Hubble, 3 Mar 2026 | [potm2602c](https://esahubble.org/images/potm2602c/), facts [potm2602a](https://esahubble.org/images/potm2602a/) |
| `4-ngc-7129` | A young cluster lighting golden gas, protostar jets in the cold red cloud, 3,300 light-years away | Webb, 6 Oct 2026 | [weic2620a](https://esawebb.org/images/weic2620a/) |
| `5-lion-nebula` | NGC 2392: the bubble is the face, the white dwarf the nose, a lit dust shell the mane; in Gemini | Webb, 10 Aug 2026 | [weic2616a](https://esawebb.org/images/weic2616a/), facts [weic2616](https://esawebb.org/news/weic2616/) |
| `6-exposed-cranium-nebula` | PMR 1, a dying star shedding its layers; the dark lane may be twin jets; in Vela | Webb NIRCam, 25 Feb 2026 | [weic2605c](https://esawebb.org/images/weic2605c/), facts [weic2605](https://esawebb.org/news/weic2605/) |
| `7-ic-348` | A star nursery with brown dwarfs of about twice Jupiter's mass, 1,000 light-years away | Webb, 15 Sep 2026 | [weic2619a](https://esawebb.org/images/weic2619a/) (publication JPEG; the full mosaic is 30866 x 38204) |

The release pages give no distance for the Lion and the Exposed Cranium, so their labels name the constellation.

Left out, after a look at full screen size: the Crab Nebula (heic2607a, Hubble, 23 Mar 2026; the cut that avoids
the mosaic's black corners shows colour grain), the Trifid Nebula (heic2608a, Hubble's 36th-birthday picture,
20 Apr 2026; grain 2.5 with a faint fine texture in its blue sky; G took it out), the Egg Nebula (heic2604a; only
1668 x 1552 pixels), and the Cat's Head collage (weic2622a) in favour of Webb's single view. Grain at screen size
(Immerkaer sigma, 2560 x 1440): 0.5 to 0.9 for most; Exposed Cranium 3.1 and Cat's Eye 2.8 are fine detail (gas
threads, thousands of faint galaxies), not grain.

## Install

```sh
./install stardust
omarchy theme set stardust
```

## How the wallpapers are made

- `wallpapers.json` lists each photo: download link, source page, credit and licence, label text, and where to cut it.
- [`src/photowall.py`](../../src/photowall.py) cuts each photo to 16:9 at 3840 x 2160 and draws its label inside the
  part a 3:2 screen shows; the same script makes every photo theme in this repository.
- `src/build stardust` makes them again from the photos (~101 MB, downloaded once into `~/.cache/omarchy-themes/stardust`).

## Credits and licences

The photos come from ESA/Webb and ESA/Hubble. [CREDITS.md](../../CREDITS.md) lists every wallpaper's author, licence and source.

- Pictures from esawebb.org and esahubble.org are published under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
  with the credit shown on each picture (NASA, ESA, CSA, STScI, the Euclid Consortium and the named image processors).
  The credit is printed on every wallpaper, exactly as the image page gives it.
