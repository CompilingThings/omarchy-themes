# Viral

An Omarchy theme of viruses under the electron microscope: the coronavirus behind COVID-19 and its Omicron strain,
Ebola, mpox, bird flu, HIV, rabies and hepatitis B. Electron microscopes see in black and white; every picture here
was coloured by hand at NIAID, the US National Institute of Allergy and Infectious Diseases, most of them from
micrographs taken at its Integrated Research Facility in Fort Detrick, Maryland. The background is near black with a
cold blue cast, the text is pale, the red of the Ebola virus is the accent, and the window border turns from that red
into the teal of the cell covered in Omicron.

Each wallpaper has a small label in the bottom right corner (bottom right because terminal text keeps to the
left): what it is, one line in plain words, the date on the picture's page, who made it and the licence.

| Wallpaper | What it shows | Date | Made by, licence | Source |
|---|---|---|---|---|
| `01-covid` | SARS-CoV-2, the virus that causes COVID-19, isolated from a patient in the US, emerging from cells grown in a lab (transmission electron microscope, NIAID Rocky Mountain Laboratories) | 12 Feb 2020 | NIAID, CC BY 2.0 | [Commons](https://commons.wikimedia.org/wiki/File:Novel_Coronavirus_SARS-CoV-2.jpg) |
| `02-covid-bridges` | SARS-CoV-2 (green) on filopodia, the thin arms infected cells stretch to their neighbours (scanning electron microscope) | 12 Jan 2021 | NIAID, CC BY 2.0 | [Commons](https://commons.wikimedia.org/wiki/File:Novel_Coronavirus_SARS-CoV-2_(50835164488).jpg) |
| `03-ebola` | One filamentous Ebola virus (scanning electron microscope) | 13 Oct 2022 | NIAID, CC BY 2.0 | [Commons](https://commons.wikimedia.org/wiki/File:Ebola_Virus_Particle_(52425481714).jpg) |
| `04-mpox` | Immature mpox viruses inside an infected VERO E6 cell (transmission electron microscope) | 29 Apr 2023 | NIAID, CC BY 2.0 | [Commons](https://commons.wikimedia.org/wiki/File:Mpox_Virus_(52863107093).jpg) |
| `05-bird-flu` | Three H5N1 influenza A viruses; two CDC micrographs inverted, put together and coloured by NIAID | 19 Mar 2023 | CDC and NIAID, CC BY 2.0 | [Commons](https://commons.wikimedia.org/wiki/File:Influenza_A_Virus_(H5N1_Bird_Flu)_(52761900537).jpg) |
| `06-omicron` | A cell infected with the Omicron strain of SARS-CoV-2, from a patient sample (scanning electron microscope) | 9 Nov 2022 | NIAID, CC BY 2.0 | [Commons](https://commons.wikimedia.org/wiki/File:Novel_Coronavirus_SARS-CoV-2_(Omicron)_(52488229661).jpg) |
| `07-hiv` | HIV-1 budding from a chronically infected H9 T cell, in all stages of maturing (transmission electron microscope) | 30 Nov 2022 | NIAID, CC BY 2.0 | [Commons](https://commons.wikimedia.org/wiki/File:HIV_Virus_(52538014784).jpg) |
| `08-rabies` | Rabies viruses multiplying in the cytoplasm of an infected VERO E6 cell (transmission electron microscope) | 27 Sep 2024 | NIAID, CC BY 2.0 | [Commons](https://commons.wikimedia.org/wiki/File:Rabies_Virus_-_54025744743.jpg) |
| `09-ebola-loop` | NIAID artwork: one Ebola virus in front of Ebola viruses budding from VERO E6 cells, two micrographs in one | 30 Oct 2022 | NIAID, CC BY 2.0 | [Commons](https://commons.wikimedia.org/wiki/File:Ebola_Virus_(52466947587).jpg) |
| `10-mpox-particle` | One mpox virus, grown in cell culture and purified (transmission electron microscope) | 8 Jul 2024 | NIAID, CC BY 2.0 | [Commons](https://commons.wikimedia.org/wiki/File:Mpox_Virus_Particle.jpg) |
| `11-hepatitis-b` | Hepatitis B viruses; a CDC micrograph coloured by NIAID for Halloween | 19 Oct 2022 | CDC and NIAID, CC BY 2.0 | [Commons](https://commons.wikimedia.org/wiki/File:Hepatitis_B_Virus_(52451177586).jpg) |

Facts on the labels come from each picture's Commons page, which copies NIAID's own caption from its Flickr stream;
the date is the one the page gives (when NIAID published the picture, not when the sample was imaged).

The pictures were chosen from the 1,020 files NIAID has on Wikimedia Commons: 334 are micrographs at least 2400
pixels across, 321 of those were looked at as small pictures (people, 3D models and renderings left out), 26
downloaded whole and looked at one by one at true screen size, and 11 kept. Electron micrographs have a fine grain of
their own, so `src/grain.py` measures them high (0.8 to 10 for the kept ones, Immerkaer sigma at 2560 x 1440); each
was judged by eye at true size instead, and kept only where the grain reads as the sample's texture. Left out: both
Marburg virus pictures, Nipah virus, RSV, HIV budding as two glowing balls, and Omicron on a red cell (all speckled
with grain at screen size), an early Ebola picture, MERS and two mpox viruses on blue (soft and blotchy), coronavirus in a blue mesh (harsh),
coronavirus inside a nose cell (grainy), two near copies of the COVID-19 picture, a second bird flu colouring (the
same picture in blue) and a second rabies colouring (the same picture in teal and purple).

The COVID-19 and bird flu pictures use photowall's `fit`: the whole picture on the black of its own background,
left of the label. The gold Ebola loop is shown whole too, its sides fading into dark red; the rest fill the screen.

```
src/build viral            # the pictures (~65 MB) download once into ~/.cache/omarchy-themes/viral
./install viral
omarchy theme set viral
```

## Credits and licences

Every wallpaper carries its maker and licence on its label; the table above links each picture's page.

- [CC BY 2.0](https://creativecommons.org/licenses/by/2.0/): free to use and change with credit, a link to the
  licence, and a note of changes. NIAID asks for the credit "NIAID"; the bird flu and hepatitis B pictures are
  "CDC and NIAID" (CDC micrographs, coloured by NIAID).

Changes made to every picture: cut or scaled to 16:9 at 3840 x 2160 (three set whole on a dark field with their
edges faded into it), and a label added in the bottom right corner.
