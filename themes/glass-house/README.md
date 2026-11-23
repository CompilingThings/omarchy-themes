# Glass House

An Omarchy theme of diatoms, single-celled algae that live in shells of glass (silica), under the microscope: round
ones, three-cornered ones, a needle, a honeycomb, and a bunch of them on their stalks. Most are fossils from the
diatomite of Oamaru, New Zealand, 32 to 40 million years old, and from the Ural Mountains; two are the shells of
foraminifera, other single-celled creatures of the sea, and one diatom shell is seen under an electron microscope.
Eight of the twelve photos are by Anatoly Mikhaltsov, and one more is from his Microcosmos lab. A dark blue-violet background, cool pale
text, the violet-blue of the glass in phase contrast as the accent, and the window border turning from it into the
green of the coloured diatom shell.

Each wallpaper has a small label in the bottom right corner (bottom right because terminal text keeps to the
left): what it is, one line in plain words, the date the photo's page gives, the photographer and the licence.

| Wallpaper | What it shows | Date | Photographer, licence | Source |
|---|---|---|---|---|
| `01-arachnoidiscus` | Fossil diatom Arachnoidiscus sp., diatomite from a Russian field; variable phase contrast (micrograph by Irina Klimova, student of the Microcosmos lab) | 16 Nov 2015 | Irina Klimova, Microcosmos lab, CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:Arachnoidiscus_sp.jpg) |
| `02-star-shell` | Shell of the marine foraminifer Baculogypsina sphaerulata | 13 Jun 2016 | Anatoly Mikhaltsov, CC BY 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:Baculogypsina_sphaerulata_2.jpg) |
| `03-lyrella` | Diatom Lyrella hennedyi, reverse contrast, 1500x | 19 Apr 2012 | Massimo Brizzi, CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:Lyrella_hennedy_1600x_contrast_invertion.jpg) |
| `04-triangle` | Fossil diatom Triceratium polycystinorum, Palaeocene-Eocene diatomite from the eastern Urals; bright field, focus stacking | 23 May 2015 | Anatoly Mikhaltsov, CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:Triceratium_polycystinorum.jpg) |
| `05-spiked-shell` | Shell of the marine foraminifer Calcarina spengleri | 13 Jun 2016 | Anatoly Mikhaltsov, CC BY 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:Calcarina_spengleri.jpg) |
| `06-sieve` | Diatom Coscinodiscus oculus-iridis, coloured scanning electron micrograph (TESCAN CLARA, 40 µm field of view) | 14 Sep 2021 | Pavel Somov, CC BY 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:Coscinodiscus_oculus-iridis_(Ehrenberg)_Ehrenberg_1840_diatom_shell._Colored_SEM_image.png) |
| `07-sunburst` | Fossil diatom Actinoptychus maculatus, Oamaru diatomite, 32-40 million years old; bright field | 2 Jan 2015 | Anatoly Mikhaltsov, CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:Actinoptychus_maculatus.jpg) |
| `08-needle` | Diatom Pinnularia major; variable phase contrast | 18 May 2015 | Anatoly Mikhaltsov, CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:Pinnularia_major.jpg) |
| `09-triangle-oamaru` | Fossil diatom Triceratium morlandii var. morlandii, Oamaru, 32-40 million years old; variable phase contrast | 25 Oct 2014 | Anatoly Mikhaltsov, CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:Triceratium_morlandii_var._morlandii.jpg) |
| `10-auliscus` | Fossil diatom Auliscus oamaruensis, Oamaru, 32-40 million years old; bright field, focus stacking | 13 Nov 2015 | Anatoly Mikhaltsov, CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:Auliscus_oamaruensis.jpg) |
| `11-bouquet` | A bunch of Cymbella diatoms | 26 Apr 2019 | Andrei Savitsky, CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:%D0%91%D1%83%D0%BA%D0%B5%D1%82_%D0%B8%D0%B7_%D0%B4%D0%B8%D0%B0%D1%82%D0%BE%D0%BC%D0%BE%D0%B2%D1%8B%D1%85_%D0%B2%D0%BE%D0%B4%D0%BE%D1%80%D0%BE%D1%81%D0%BB%D0%B5%D0%B9_Cymbella.jpg) |
| `12-honeycomb` | Fossil diatom Stephanopyxis grunowii from below, Troublesome Gully, Oamaru, about 40 million years old | 5 Feb 2015 | Anatoly Mikhaltsov, CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:Stephanopyxis_grunowii.jpg) |

Facts on the labels come from each photo's Commons page: the species, where the fossil was found, its age and the
lighting. "Spider disc" is what the name Arachnoidiscus means, not the page's words.

The photos were chosen from the science photo competitions on Wikimedia Commons: 81 large photos of diatoms,
foraminifera and pollen were listed, 14 were downloaded whole and looked at one by one at true screen size, and 12 kept. Grain at screen size
(`src/grain.py`, Immerkaer sigma at 2560 x 1440): 0.1 to 1.1, and 5.0 for the electron micrograph, whose pores are
the fine detail (checked by eye). Left out: a crowd of Navicula diatoms in polarised light and the algae living on a
water plant (both soft at full size).

Every wallpaper is on black. Five photos were taken on black already: each is set whole, left of the label, with a
faded edge (photowall's `fit`). The other seven were taken in transmitted light on a pale grey or white background:
each shell is cut out of it and set alone on black (photowall's `fit` with `cutout`: everything that differs from the
background colour, the largest piece with its holes filled, so the see-through middle of a shell stays as it was
photographed). Six of those had a scale bar beside the shell, painted over first.

```
src/build glass-house            # the photos (~80 MB) download once into ~/.cache/omarchy-themes/glass-house
./install glass-house
omarchy theme set glass-house
```

## Credits and licences

Every wallpaper carries its photographer and licence on its label; the table above links each photo's page.

- [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/): free to use and change with credit, a link to the
  licence, and a note of changes.
- [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/): the same, and changed versions must keep the
  same licence. The wallpapers made from these photos are CC BY-SA 4.0 too.

Changes made to every photo: set whole on black at 3840 x 2160 (the five dark ones with their edges faded into it, the
seven light ones cut out of their background, scale bars painted over), and a label added in the bottom right corner.
