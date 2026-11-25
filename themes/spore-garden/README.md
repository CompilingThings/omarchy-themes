# Spore Garden

An Omarchy theme of moulds and other fungi under the microscope: fungus threads growing over the eyes of insects
(two of them coloured by the photographers after the electron microscope), spores of Sordaria lined up in their sacs,
Penicillium on a slide, colonies close up, the web of a bread mould, and the spore case of a powdery mildew from a
hazel leaf. A near-black background with a hint of violet, cool pale text, the green of the fungus threads as the
accent, and the window border turning from it into the magenta of the eye they grow on.

Each wallpaper has a small label in the bottom right corner (bottom right because terminal text keeps to the
left): what it is, one line in plain words, the date the photo's page gives, the photographer and the licence.

| Wallpaper | What it shows | Date | Photographer, licence | Source |
|---|---|---|---|---|
| `01-eye-colony` | A fungus colonising the eye of an insect, scanning electron micrograph, digitally coloured | 9 Jul 2023 | Brandon Antonio Segura Torres & Priscilla Vieto Bonilla, CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:Un_hongo_colonizando_el_ojo_de_un_Insecto.jpg) |
| `02-spore-rosettes` | Ascospores of Sordaria macrospora in rows in their asci; a parent heterozygous for spore colour gives yellow and black spores, and the patterns show DNA recombination in meiosis | 8 Aug 2017 | Aurora Storlazzi, CC BY 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:Linear_arrangement_of_ascospores_in_the_asci_of_the_fungus_Sordaria_macrospora.jpg) |
| `03-mycelium-on-an-eye` | Fungal mycelium on a compound eye, scanning electron micrograph | 13 Sep 2025 | Brandon Antonio Segura Torres & Priscilla Vieto Bonilla, CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:Micelio_de_hongo_sobre_ojo_compuesto_SEM.jpg) |
| `04-penicillium` | The mould Penicillium, light microscope | 22 Dec 2023 | Hafid1412, CC BY 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:Pinicillium_Sp.jpg) |
| `05-colonies` | Fungus colonies close up: The parallel microscopic Universe IV | 22 Jun 2015 | Sofia Vini, CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:The_parallel_microscopic_Universe_IV.jpg) |
| `06-bread-mould` | Mould on bread, scanning electron micrograph (Tescan S9251G) | 6 Nov 2019 | Pavel.Somov, CC BY 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:Mold_on_bread_2.png) |
| `07-hazel-mildew` | Cleistothecium (spore case) of the powdery mildew Phyllactinia guttata on a common hazel leaf, Donetsk | 30 Nov 2017 | Gubin Olexander, CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:Cleistothecium_of_powdery_mildew_fungi_Phyllactinia_guttata_on_the_leave_of_common_hazel.jpg) |
| `08-moth-eye` | Penicillium spreading over the compound eye of the moth Mythimna loreyi, scanning electron micrograph | 10 Mar 2023 | Brandon Antonio Segura Torres & Priscilla Vieto Bonilla, CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:Proliferaci%C3%B3n_de_hongo_penicillium_sobre_ojo_compuesto_de_polilla.jpg) |

Facts on the labels come from each photo's Commons page: the species, the microscope, where the leaf was found.
"Yellow or black by the genes each one got" is the plain-words version of the Sordaria page's own explanation.

The photos were chosen from the science photo competitions on Wikimedia Commons: 479 photos of fungi were listed, 200
looked at as small pictures, 29 downloaded whole and looked at one by one at true screen size, and 8 kept. Grain at
screen size (`src/grain.py`, Immerkaer sigma at 2560 x 1440): 0.5 to 3.0. Left out: soft or noisy photos (mould heads
on a dark ground, grain 3.6; a coloured moth eye, 4.6; two Aspergillus heads, glowing threads under fluorescence and
two dark-field sporangia, all soft at screen size), a halftone print, a sharp but flat grey electron micrograph,
photos on a white slide that cannot be cut out cleanly (blue-stained moulds, a mildew case with see-through arms), and
a slime mould, which is not a fungus.

The Penicillium slide and the hazel mildew are set whole on black with photowall's `fit`; the mildew is cut out of
its light background (`"cutout"`). The mycelium photo is cut a little higher to leave out its scale bar. Five labels
sit on a neat dark panel (photowall's `panel`) where the photo behind them is bright or busy.

```
src/build spore-garden          # the photos (~110 MB) download once into ~/.cache/omarchy-themes/spore-garden
./install spore-garden
omarchy theme set spore-garden
```

## Credits and licences

Every wallpaper carries its photographer and licence on its label; the table above links each photo's page.

- [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/): free to use and change with credit, a link to the
  licence, and a note of changes.
- [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/): the same, and changed versions must keep the
  same licence. The wallpapers made from these photos are CC BY-SA 4.0 too.

Changes made to every photo: cut to 16:9 (the Penicillium slide and the hazel mildew set whole on black instead) at
3840 x 2160, and a label added in the bottom right corner.
