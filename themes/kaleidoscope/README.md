# Kaleidoscope

An Omarchy theme of chemicals crystallising on a microscope slide, seen between two crossed polarising filters: each
crystal turns the light by its own amount, so it shows as its own band of colour. The fans of malic acid, a thin film
growing out from one seed point, vanillin (the taste of vanilla), Epsom salt on violet, a liquid crystal in its
layered phase, and the seed point of nicotinic acid. The near-black of crossed polarisers as the background, pale text, the violet of the
Epsom salt as the accent, and the window border turning from it into the gold of malic acid.

Each wallpaper has a small label in the bottom right corner (bottom right because terminal text keeps to the
left): what it is, one line in plain words, the date the photo's page gives, the photographer and the licence.

| Wallpaper | What it shows | Date | Photographer, licence | Source |
|---|---|---|---|---|
| `01-malic-acid` | Crystals of malic acid (the sour of apples), polarised light at 100x | 13 Dec 2018 | MarekMiś, CC BY 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:Kwas_jab%C5%82kowy.jpg) |
| `02-nucleation` | A thin crystalline chemical film growing outward from one nucleation point, between crossed polarisers | 27 Jul 2024 | KarlGaff, CC BY 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:Nucleation.jpg) |
| `03-vanillin` | Vanillin crystals, polarised light; the photographer's title is "Knight Shield" | 2 Oct 2016 | Photon 400 750, CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:01_Vanillin_Crystals.jpg) |
| `04-magnesium-sulfate` | Magnesium sulfate (Epsom salt) crystals dissolving and growing again in solution, compensated polarised light | 18 Dec 2021 | KarlGaff, CC BY 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:Magnesium_sulfate_crystals.jpg) |
| `05-smectic-phase` | A liquid crystal material in its smectic A phase (molecules in layers), between crossed polarisers at 4x | 11 Mar 2022 | Alexander Kurilov, CC BY 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:SmA_phase.jpg) |
| `06-nicotinic-acid` | The nucleation point of a thin crystalline film of nicotinic acid (vitamin B3), polarised light | 10 Feb 2020 | KarlGaff, CC BY 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:Nicotinic_acid.jpg) |
Facts on the labels come from each photo's Commons page: the chemical, the light and the magnification. "The sour of
apples", "the taste of vanilla" and "Epsom salt" are the everyday words for malic acid, vanillin and magnesium sulfate.

The photos were chosen from the science photo competitions and the crystal categories on Wikimedia Commons: 243
photos of crystals in polarised light were listed and looked at as small pictures, 42 downloaded whole and looked at
one by one at true screen size, and 18 kept for three themes of six (this one: the full-frame rainbow ones). Every
chemical here is new to these themes: vitamin C, aspirin, citric acid, sulfur and beta-alanine, all in Prism already,
were left out, however good the photo. Grain at screen size (`src/grain.py`, Immerkaer sigma at 2560 x 1440): 0.9 to
2.7. Left out too: noisy photos (grain 6.8 to 11.3), a second vanillin photo with harsh, noisy colour, crystals that
sit as shapes on black (kept for their own theme), and bubbles (also their own theme).

```
src/build kaleidoscope          # the photos (~60 MB) download once into ~/.cache/omarchy-themes/kaleidoscope
./install kaleidoscope
omarchy theme set kaleidoscope
```

## Credits and licences

Every wallpaper carries its photographer and licence on its label; the table above links each photo's page.

- [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/): free to use and change with credit, a link to the
  licence, and a note of changes.
- [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/): the same, and changed versions must keep the
  same licence. The wallpaper made from that photo (`03-vanillin`) is CC BY-SA 4.0 too.

Changes made to every photo: cut to 16:9 at 3840 x 2160 (the vanillin cut from its top, to leave out the scale bar),
and a label added in the bottom right corner.
