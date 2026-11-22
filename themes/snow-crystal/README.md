# Snow Crystal

An Omarchy theme of single snowflakes as Wilson Bentley photographed them through a microscope in Jericho, Vermont:
fern-like stars, flat hexagons, needles, a triangle, one shaped like a flower. Bentley "photographed his first
snowflake on January 15, 1885" and "captured more than 5,000 images of crystals"
([Wikipedia: Wilson Bentley](https://en.wikipedia.org/wiki/Wilson_Bentley)). These twelve are his own small prints,
now in the Metropolitan Museum of Art in New York, which shares them free for any use. The warm black of his plates,
the cream of the old prints as text, an icy blue accent, and the window border fading from that blue into the cream.

Each print is a round dark plate on a cream card. For the wallpapers the plate is cut out of the museum's scan
(`src/photowall.py`, `"plate": true`) and set, a little left of centre, on a field of its own dark colour, so the
snowflake floats in the dark and the label in the bottom right corner never covers it (bottom right because terminal
text keeps to the left). The label gives the crystal's shape, one fact about Bentley or snow, and the credit.

| Wallpaper | What it shows | The Met's image | Source |
|---|---|---|---|
| `01-fern-star` | Six fern-like arms | DP351918 | [Commons](https://commons.wikimedia.org/wiki/File:-Snow_Crystal-_MET_DP351918.jpg) |
| `02-hexagonal-plate` | A six-sided plate with ridges | DP351906 | [Commons](https://commons.wikimedia.org/wiki/File:-Snow_Crystal-_MET_DP351906.jpg) |
| `03-triangle` | A three-sided crystal | DP351930 | [Commons](https://commons.wikimedia.org/wiki/File:-Snow_Crystal-_MET_DP351930.jpg) |
| `04-needle-star` | Six needles, each with small plates on it | DP351922 | [Commons](https://commons.wikimedia.org/wiki/File:-Snow_Crystal-_MET_DP351922.jpg) |
| `05-six-petals` | Six rounded lobes like petals | DP351912 | [Commons](https://commons.wikimedia.org/wiki/File:-Snow_Crystal-_MET_DP351912.jpg) |
| `06-branched-star` | Six branching arms round a tiny hexagon | DP351909 | [Commons](https://commons.wikimedia.org/wiki/File:-Snow_Crystal-_MET_DP351909.jpg) |
| `07-hexagon` | A plain hexagon with a scalloped inner line | DP351916 | [Commons](https://commons.wikimedia.org/wiki/File:-Snow_Crystal-_MET_DP351916.jpg) |
| `08-six-pointed-star` | A six-pointed star plate | DP351910 | [Commons](https://commons.wikimedia.org/wiki/File:-Snow_Crystal-_MET_DP351910.jpg) |
| `09-ribbed-plate` | A plate with ribs to each side | DP351932 | [Commons](https://commons.wikimedia.org/wiki/File:-Snow_Crystal-_MET_DP351932.jpg) |
| `10-star-and-hexagon` | A star with a hexagon at its heart | DP351911 | [Commons](https://commons.wikimedia.org/wiki/File:-Snow_Crystal-_MET_DP351911.jpg) |
| `11-plate-with-arms` | A plate with short broad arms | DP351914 | [Commons](https://commons.wikimedia.org/wiki/File:-Snow_Crystal-_MET_DP351914.jpg) |
| `12-broad-armed-star` | A star with broad, plate-tipped arms | DP351907 | [Commons](https://commons.wikimedia.org/wiki/File:-Snow_Crystal-_MET_DP351907.jpg) |

All twelve: Wilson A. Bentley, *[Snow Crystal]*, 1890s–1920s, gelatin silver print, each about 7 to 8 cm across; The
Metropolitan Museum of Art, Purchase, Alfred Stieglitz Society Gifts, 2015 (for example accession numbers 2015.188 and 2015.194).
Released by the Met as CC0 (Open Access) and uploaded to Wikimedia Commons from the Met's own files.

Facts on the labels: Bentley's first snowflake photo, his 5,000 crystals, how he worked ("Each crystal was caught on
a blackboard and transferred rapidly to a microscope slide"; he "attached a bellows camera to a compound
microscope"), that he "argued that no two snow crystals were alike", his name "Snowflake Bentley" and his years
(born in Jericho, Vermont, 1865; died 1931) all come from [Wikipedia: Wilson Bentley](https://en.wikipedia.org/wiki/Wilson_Bentley).
Six sides "arising from the hexagonal crystalline structure of ice", the shape "determined primarily by the
temperature and humidity at which it is formed", the arms called dendrites and the plate as a basic shape come from
[Wikipedia: Snowflake](https://en.wikipedia.org/wiki/Snowflake). Date, medium, size and credit come from each
picture's Commons page (copied from the Met's record). The shape names in the titles are plain descriptions.

Chosen from the Met's 24 Bentley prints on Commons (about 4000 x 2500 pixels each) for as many different shapes as
possible. Grain at screen size (`src/grain.py`, Immerkaer sigma at 2560 x 1440): 1.4 to 1.9 for all twelve; true-size
crops of two of them show the fine ice detail sharp, and each plate is a little smaller on the wallpaper than in the scan (no enlarging).
Also on Commons and looked at, but left out to keep one look: modern snowflake photos by Janek Lass, Alexey
Kljatov and others (free licences, but on white, pink or blue backgrounds, and some only 2048 pixels wide).

```
src/build snow-crystal           # the scans (~25 MB) download once into ~/.cache/omarchy-themes/snow-crystal
./install snow-crystal
omarchy theme set snow-crystal
```

Building needs numpy and scipy as well as Pillow, to find and cut the round plates.

## Credits and licences

Every wallpaper carries the photographer and licence on its label; the table above links each picture's page.

- [CC0](https://creativecommons.org/publicdomain/zero/1.0/): public domain, no conditions (credit given anyway, to
  Bentley and the Met).

Changes made to every picture: the round plate cut out of the scan of the card, set on a dark field of the plate's
own colour at 3840 x 2160, and a label added in the bottom right corner.
