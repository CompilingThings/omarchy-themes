# Changelog

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow
[Semantic Versioning](https://semver.org/) (a theme renamed or removed is a major change, a new theme minor, a fixed
picture or colour a patch).

## [Unreleased]

### Added

- Heartstone: six colour electron micrographs by Sergio Bertazzo from Wikimedia Commons, where colour shows how
  dense each part is (mineral grains in heart tissue, kidney-stone crystals, calcified heart tissue mirrored);
  fibre pink and kidney-stone orange, with its own screensaver
- Stowaway: six parasites of fish in dark-field light by Brandon Antonio Segura Torres and Priscilla Vieto Bonilla,
  from Wikimedia Commons (flukes from perch and puyen, gill worms), each laid on its side; fluke magenta and womb gold,
  with its own screensaver
- `src/photowall.py`: "turn" in "fit" lays a long, thin subject on its side
- Green Room: six photos of leaf cells under the microscope from Wikimedia Commons (tulip stomata in polarised light,
  Canadian pondweed packed with chloroplasts, leaf cells glowing in fluorescence, a leaf's structural cells);
  chlorophyll green and polarised magenta, with its own screensaver
- Colony: six bacterial colonies growing across agar, photographed through a microscope's eyepiece by Korinna, from
  Wikimedia Commons (a Bacillus subtilis fractal, blue Bacillus, tree-like colonies, a red colony); Bacillus blue and
  colony red, with its own screensaver
- Bone White: six animal skulls photographed on black by Didier Descouens (a babirusa, a mandrill, a yellow baboon, a
  warthog, a Siberian musk deer, an eastern woolly lemur), from Wikimedia Commons' featured pictures; bone ivory and
  tusk amber, with its own screensaver
- Mother Lode: six mineral specimens photographed in the studio by Ivar Leidus (azurite, wulfenite, gypsum with green
  herbertsmithite, celestine, mimetite, vanadinite), from Wikimedia Commons' featured pictures; ultramarine and
  wulfenite orange, with its own screensaver
- Surface Tension: six photos of bubbles under the microscope (soap islands on a soap bubble's film, air bubbles in
  melted, dried and squeezed polyvinyl alcohol, the walls of a foam, packed soap bubbles), from the science photo
  competitions on Wikimedia Commons; foam blue and soap-film magenta, with its own screensaver
- Sceptre: six crystals standing alone on black (potassium dichromate sceptres, ammonium nitrate needles, sugar,
  methylene violet, potato starch, a star of sea minerals), all new to these themes, from the science photo
  competitions on Wikimedia Commons; dichromate orange and ice cyan, with its own screensaver
- Kaleidoscope: six chemicals crystallising in polarised light (malic acid, a film growing from one seed point,
  vanillin, Epsom salt, a liquid crystal's smectic phase, nicotinic acid), all new to these themes, from the science
  photo competitions on Wikimedia Commons; Epsom violet and malic gold
- Spore Garden: eight moulds and other fungi under the microscope (fungus threads on insect eyes, spore rosettes,
  Penicillium, colonies, bread mould, a powdery mildew's spore case), from the science photo competitions on Wikimedia
  Commons.
- Eight Eyes: twelve spiders and mites up close (jumping-spider eyes, two tarantulas, water mites, a mite's skin under
  the electron microscope), from the science photo competitions on Wikimedia Commons.
- Glass House: twelve diatoms, single-celled algae in shells of glass, and two foraminifera shells, most of them
  fossils from Oamaru (New Zealand) and the Ural Mountains, from the science photo competitions on Wikimedia Commons;
  all on black: the seven photographed on a light background are cut out of it.
- photowall: `"cutout"` in `fit` cuts a subject out of its plain background (the largest piece, holes filled) and
  sets it alone on the field colour.
- Scale Wing: eleven butterfly and moth wings up close, scale by scale (a painted lady, the large blue, the green
  hairstreak, a Patagonian moth with sunflower pollen), from the science photo competitions on Wikimedia Commons;
  blue and orange.
- Front Line: eleven immune cells and the germs they meet under the electron microscope, coloured by NIAID
  (natural killer cells, T cells, B cells, an HIV-infected T cell, MRSA, Klebsiella, malaria); green and violet.
- Viral: eleven viruses under the electron microscope, coloured by NIAID (the coronavirus behind COVID-19 and
  Omicron, Ebola, mpox, bird flu, HIV, rabies, hepatitis B), from NIAID's pictures on Wikimedia Commons; red and teal.
- Inner Space: nine brains, eyes and cells glowing under the microscope (a mouse hippocampus, cortex and whole
  brain slice, nerve fibres, growth cones, a fruit fly retina, a zebrafish eye, human kidney cells, dividing dog
  kidney cells), from the science photo competitions on Wikimedia Commons; pink and cyan-green.
- Stem Glow: eleven plant stems, stalks and a pine needle cut across under the microscope, most glowing under blue
  or ultraviolet light, three in polarised light (butcher's broom, bracken, rye, a rose, banana, red pepper, grape,
  peach, mulberry), by five photographers from Wikimedia Commons; gold and glow green. `src/photowall.py`'s `fit`
  gains `"oval"`: the fade follows an oval round a round slice, so a coloured photo background shows only as a glow.
- Die Shot: eight bare chip dies under the microscope, whole on black (a Soviet op-amp, a Fairchild video switch,
  a Holtek RS-232 driver, Winbond clock chips, a keyboard controller), all by VektorF from Wikimedia Commons;
  gold and pale cyan.
- Bedrock: ten thin slices of rock under the microscope, most between crossed polarisers (olivine, kyanite,
  wehrlite, serpentine, myrmekite, piemontite), all by Strekeisen from Wikimedia Commons; gold and cyan.
- Neon Pond: eleven pond animals glowing in colour on black (water fleas, a copepod, phantom midge and mosquito
  larvae, a diving beetle's foot) in dark field and polarised light, all by Andrei Savitsky from Wikimedia Commons;
  cyan and yellow.
- Lantern: fourteen insect heads glowing on their own under a fluorescence microscope (ants, flies, a moth, a
  ladybird, a green shield bug, a soldier beetle, a scorpionfly), all by Alexander Klepnev from Wikimedia Commons;
  eye green and shell gold.
- Prism: fourteen photos of crystals under the microscope in polarised light (citric acid, vitamin C, aspirin,
  sulfur, succinic acid, beta-alanine, caesium chloride, a glycerol film) from Wikimedia Commons featured pictures
  and science photo competitions; sulfur magenta and citric yellow.
- Pond Drop: thirteen Commons featured pictures of the animals in a drop of pond water under the microscope
  (water fleas, copepods, seed shrimp, water mites, midge larvae, a moss animal's statoblast), ten of them by Janek
  Lass from ponds in Rakvere, Estonia; dark-field black, water-flea teal and brood amber. `src/photowall.py` gains a
  `fit` option that sets a photo of one subject on a plain background whole on a field of its own colour, and can
  paint over a scale bar.
- Thunderhead: fourteen photos of thunderstorms (lightning at night, shelf clouds, mammatus, a glowing anvil top)
  from Wikimedia Commons with free licences, among them NOIRLab's 1972 Kitt Peak storm; lightning violet and
  electric blue.
- Cold Blood: fourteen close-ups of frogs, lizards, snakes and crocodiles (eyes, heads and scales) from
  Wikimedia Commons with free licences; red-eyed tree frog red and pit viper green.
- Snow Crystal: twelve of Wilson Bentley's snowflake photomicrographs (The Met, CC0), each round plate cut
  from the museum's scan onto a dark field by a new `"plate": true` option in `src/photowall.py`.
- Deep Sea: twelve close photos of jellyfish and comb jellies lit in dark water and a deep-sea isopod from
  900 m, all from Wikimedia Commons with free licences; white-spotted jellyfish blue and bluefire purple.
- Compound Eye: fourteen macro photos of insect faces, twelve from the USGS Bee Inventory and Monitoring Lab (U.S.
  public domain) and two Commons featured pictures; cuckoo wasp green and iridescent blue. Adds the USGS public
  domain licence note.
- Fairy Ring: twelve photos of mushrooms and other fungi from Wikimedia Commons (fly agarics, glowing mushrooms,
  amethyst deceivers, a latticed stinkhorn and more); fly agaric red and amethyst purple. Adds the CC BY-SA 3.0 and
  CC BY-SA 4.0 licence texts.

### Fixed

- `src/photowall.py`: a download whose file name is too long for the file system (a long Cyrillic title is about
  400 bytes once percent-encoded) is kept under a shortened name with a hash; shorter names are unchanged.
- `src/photowall.py`: a very large JPEG decoded at reduced size could put the crop box a fraction of a pixel
  past the bottom edge and stop the build; width and height now scale on their own.

## [1.0.0] - 2026-11-18

First release: eleven themes for Omarchy 4.5.

- Themes: Boardroom, Deep Field, Grand Tour, Low Orbit, Nordlys, Red Planet, Seahorse Valley, Solar Max, Stardust,
  Traceroute, Tranquility.
- `install` copies one theme, several, or all of them into `~/.config/omarchy/themes`, and only ever replaces a
  theme it installed itself.
- Every theme ships Omarchy's boot screen files (`unlock.png`, `preview-unlock.png`), made the way Omarchy makes its
  own.
- Every still wallpaper is 3840 x 2160 (Low Orbit's turning Earth is a 2560 x 1440 video), with its label or
  title block inside the part a 3:2 screen shows.
- `tools/check.py` holds every theme to one contract (files, colours, WCAG contrast, terminal and border colours,
  picture sizes, credits); `tools/credits.py` writes CREDITS.md and REUSE.toml from the themes' `wallpapers.json`.
  Both run on GitHub for every push.

[1.0.0]: https://github.com/CompilingThings/omarchy-themes/releases/tag/v1.0.0
