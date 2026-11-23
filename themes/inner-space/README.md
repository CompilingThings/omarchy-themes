# Inner Space

An Omarchy theme of the inside of brains, eyes and cells, made to glow under the microscope with fluorescent dyes,
antibodies and proteins: a mouse hippocampus and cortex, a whole mouse brain slice in blue, nerve fibres and the
growing tips of nerve cells, the retina of a fruit fly and the eye of a baby zebrafish, human kidney cells, and dog
kidney cells caught in the middle of dividing. The photos come from scientists and labs that entered them in the
science photo competitions on Wikimedia Commons. The black the samples glow in is the background, the text is cool
and pale, the pink of the growth cones and the fly retina is the accent, and the window border turns from that pink
into the cyan-green of the growth cones' stalks.

Each wallpaper has a small label in the bottom right corner (bottom right because terminal text keeps to the
left): what it is, one line in plain words, when it was photographed, the photographer and the licence.

| Wallpaper | What it shows | Photographed | Photographer, licence | Source |
|---|---|---|---|---|
| `01-hippocampus` | A slice through a mouse brain at the hippocampus, lit with fluorescent proteins (Cavalieri Ottolenghi Foundation, Turin) | 13 Dec 2019 | Luisa Demarchi, Ilaria Bertocchi, Alessandra Oberto, CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:Hyppocampus_beauty.jpg) |
| `02-nerve-fibres` | Rat hippocampus nerve cells grown in a dish, fibres stained for acetylated tubulin; Zeiss LSM880 confocal | 25 Nov 2025 | MikeRoscopy, CC BY 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:Axons_Al_Dente.png) |
| `03-growth-cones` | The growing tips of two human nerve cells: actin pink, microtubules green | 16 Dec 2025 | Physicl, CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:Neuronal_Growth_Cone.png) |
| `04-fly-retina` | A fruit fly retina; pink (ATF4) in the yellow photoreceptors marks a stress response that can lead to degeneration | 13 Dec 2021 | Guillaume Thuery, CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:Degenerating-drosophila-retina.jpg) |
| `05-zebrafish-eye` | The eye of a four-day-old zebrafish larva, four kinds of retina cell each with its own fluorescent protein (Norden lab, MPI-CBG, Dresden) | 15 Sep 2015 | IchaJaroslav, CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:SOFA-retina.tif) |
| `06-brain-cortex` | Half a mouse brain, cortex layers stained for Tle4 (red) and Ctip2 (green); LSM 780 confocal, SUNY Upstate | 19 Sep 2017 | Mamunur Rashid, CC BY 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:Brain_Cortex.png) |
| `07-kidney-cells` | Human embryonic kidney cells (HEK 293): nuclei red, actin green, phospho-histone H3 (dividing) yellow | 5 Nov 2014 | Iznewton, CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:HEK_293.jpg) |
| `08-mouse-brain` | Every cell nucleus in a mouse brain slice, stained with DAPI | 15 Oct 2025 | Syed07, CC BY 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:Fluorescently_labeled,_DAPI-stained_cell_nuclei_in_a_mouse_coronal_brain_section.jpg) |
| `09-cells-dividing` | Madin-Darby dog kidney cells: phospho-histone H3 red (dividing), actin green, nuclei blue | 11 Nov 2014 | Ian P Newton & Paul L Appleton, CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:Mitotic_MDCKs.jpg) |

Facts on the labels come from each photo's Commons page: what the sample is, what each colour stains (the page's own
words, put plainly) and the date the page gives. "Where memories are made" for the hippocampus is the usual
description of that part of the brain, not the page's words.

The pictures were chosen from about 5,000 microscopy photos in the science photo competitions on Wikimedia Commons:
285 with a medical subject and at least 2000 pixels on each side were looked at as small pictures, 22 were
downloaded whole and looked at one by one at true screen size, and 9 kept. Grain at screen size (`src/grain.py`,
Immerkaer sigma at 2560 x 1440): 0.1 to 2.3 (the growth cones are almost all black and measure nothing). Left out:
two more mouse brain slices by the same photographer as the blue one (flat orange and flat red, no glow), a chick embryo (very grainy), two slices
of testis in dark field (blurry at full size), three zebrafish brain slices (speckled or soft), a wide field of
dividing cells (stitched from tiles, the seams show), cancer cells after a drug (soft), twin cell nuclei (blobby at
full size), a mouse spinal cord (cut off by the photo's edges), and Ebola virus budding from a cell (grainy, and an
electron microscope picture, a different look; NIAID's virus pictures may become a theme of their own).

Every wallpaper but the hippocampus and the kidney cells uses photowall's `fit`: the whole sample, centred left of the
label, on the black of its own photo with a faded edge. The nerve fibres and the dividing cells fill their photos to
the edge, so they are set in a round view, like looking down a microscope (photowall's `oval`). The scale bar and
signature on the black round the brain cortex are painted over with it.

```
src/build inner-space            # the photos (~270 MB) download once into ~/.cache/omarchy-themes/inner-space
./install inner-space
omarchy theme set inner-space
```

## Credits and licences

Every wallpaper carries its photographer and licence on its label; the table above links each photo's page.

- [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/): free to use and change with credit, a link to the
  licence, and a note of changes.
- [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/): the same, and changed versions must keep the
  same licence. The wallpapers made from these photos are CC BY-SA 4.0 too.

Changes made to every photo: cut or scaled to 16:9 at 3840 x 2160 (most set whole on black with their edges faded
into it, two in a round view, a scale bar and signature painted over), and a label added in the bottom right corner.
