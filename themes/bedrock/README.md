# Bedrock

An Omarchy theme of rock sliced thin enough to see through (a thin section, about 0.03 mm) and photographed under
the microscope, almost all between two crossed polarising filters: a single olivine crystal in basalt, twinned
kyanite, wehrlite, veins of serpentine, worm-like quartz in feldspar, needles of rutile in mica and pink piemontite
from the Apuan Alps. The minerals themselves are mostly pale; between crossed polarisers each crystal shows its own
interference colour, so a grey stone turns into stained glass. All ten are by one photographer, credited on Commons
as Strekeisen. The black between crossed polarisers is the background, the text is warm and pale, the gold of a
serpentine vein is the accent, and the window border turns from that gold into the cyan of an olivine crystal.

Each wallpaper has a small label in the bottom right corner (bottom right because terminal text keeps to the
left): what it is, one line in plain words, when it was photographed, the photographer and the licence.

| Wallpaper | What it shows | Photographed | Photographer, licence | Source |
|---|---|---|---|---|
| `01-olivine` | An olivine crystal in basalt, crossed polarisers, 10x | 21 Apr 2011 | Strekeisen, CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:Olivine_in_basalt.JPG) |
| `02-serpentine-vein` | A yellow serpentine vein in grey serpentine, crossed polarisers, 20x | 6 Nov 2014 | Strekeisen, CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:Yellow_line.JPG) |
| `03-kyanite` | A twinned kyanite crystal, crossed polarisers, 2x | 7 May 2015 | Strekeisen, CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:Twinned_Kyanite.JPG) |
| `04-wehrlite` | Wehrlite (olivine and pyroxene), crossed polarisers, 2x | 7 May 2015 | Strekeisen, CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:Wherlite.JPG) |
| `05-myrmekite` | Myrmekite: rods of quartz in plagioclase, crossed polarisers, 10x | 24 Jul 2014 | Strekeisen, CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:Myrmekite.JPG) |
| `06-piemontite` | Piemontite crystals from the Apuan Alps, plane polarised light, 2x | 5 Jun 2013 | Strekeisen, CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:Piemontite_Epidote.JPG) |
| `07-mylonite` | Peridotite mylonite crossed by a fault, crossed polarisers, 2x | 5 Aug 2014 | Strekeisen, CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:Peridotitic_Mylonite.JPG) |
| `08-rutile-in-biotite` | Needles of rutile in biotite (sagenitic texture) | 21 Apr 2011 | Strekeisen, CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:Sagenitic_biotite.JPG) |
| `09-wehrlite-2` | Wehrlite (olivine and pyroxene), crossed polarisers, 2x | 5 Aug 2014 | Strekeisen, CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:Violet_dot.JPG) |
| `10-serpentine-veins` | Serpentine veins in serpentinite, crossed polarisers, 2x | 6 Nov 2014 | Strekeisen, CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:Serpentine_veins.JPG) |

Facts on the labels come from each photo's Commons page: the rock or mineral, the light (crossed polarisers, "crossed
nicols"; plane polarised light for 06), the magnification and the field of view (how wide the picture is on the
slide: 1, 2 or 7 mm). The date is the one the photo file records. The thickness of a thin section (about 0.03 mm)
is the usual standard, not stated on the pages.

The pictures were chosen from the microscope entries of the European Science Photo Competition 2015 (Italy) on
Wikimedia Commons, then looked at one by one at true screen size. Grain at screen size (`src/grain.py`, Immerkaer
sigma at 2560 x 1440): 0.4 to 3.0; the highest (kyanite 2.5, wehrlite 3.0) are the fine cracks and cleavage lines of
the crystals, sharp at full size, not grain. Left out after the full-size look, from 20: quartz "flowers" and a second
mylonite (fine film grain over flat colour), a quartz-rich marble and a layered serpentinite (soft), a mica schist
(glittery grain all over), zoned tourmaline in plane light (pale, little colour), a peridotite-troctolite contact, a naujaite and a
faulted plagioclase in gabbro (mostly grey), and gregoryite from Ol Doinyo Lengai (soft).

06 is cut from the upper, crystal-filled part of the photo (`crop`); the others fill the screen from their middle.

```
src/build bedrock                # the photos (~80 MB) download once into ~/.cache/omarchy-themes/bedrock
./install bedrock
omarchy theme set bedrock
```

## Credits and licences

Every wallpaper carries its photographer and licence on its label; the table above links each photo's page.

- [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/): free to use and change with credit, a link to
  the licence and a note of changes, and a changed picture must be shared under the same licence.

Changes made to every photo: cut to 16:9 and scaled to 3840 x 2160, and a label added in the bottom right corner.
Every finished wallpaper here is itself shared under CC BY-SA 4.0.
