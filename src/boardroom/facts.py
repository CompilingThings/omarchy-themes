#!/usr/bin/env python3
"""Board facts for the Boardroom wallpapers, read with KiCad's pcbnew (system python3). Read-only on the boards.

  facts.py scrub <in.kicad_pcb> <out.kicad_pcb> [<text> ...]
      copy of a board without the silkscreen texts named (fp_text / gr_text whose text is exactly one of them), for
      lines that should not appear in a published picture; the board file itself is not changed.

  facts.py facts <hw dir> <out.json> <board> ...      size, copper layers, parts, vias, track length of each board
  facts.py purple <in.kicad_pcb> <out.kicad_pcb> <donor.kicad_pcb>
      copy of a board with the donor's stack-up (colours) added, for a board that has none: the keyboard plate is
      ordered purple / white like the others (hw/keyboard-plate-v1/fab/ORDER.md) but its file keeps no colours.
"""
import json
import sys


def facts(hw, out, boards):
    import pcbnew
    res = {}
    for b in boards:
        bd = pcbnew.LoadBoard(f"{hw}/{b}/{b}.kicad_pcb")
        edge = max((d.GetWidth() for d in bd.GetDrawings() if d.GetLayer() == pcbnew.Edge_Cuts), default=0)
        bb = bd.GetBoardEdgesBoundingBox()
        tracks = list(bd.GetTracks())
        vias = [t for t in tracks if isinstance(t, pcbnew.PCB_VIA)]
        length = sum(t.GetLength() for t in tracks if not isinstance(t, pcbnew.PCB_VIA))
        res[b] = {
            "w": round(pcbnew.ToMM(bb.GetWidth() - edge), 1),
            "h": round(pcbnew.ToMM(bb.GetHeight() - edge), 1),
            "layers": bd.GetCopperLayerCount(),
            "parts": sum(1 for f in bd.GetFootprints() if not f.IsExcludedFromBOM()),
            "vias": len(vias),
            "track_m": round(pcbnew.ToMM(length) / 1000, 2),
        }
        print(b, res[b], file=sys.stderr)
    with open(out, "w") as f:
        json.dump(res, f, indent=1)


def block(text, start):
    """The whole s-expression that opens at text[start] ('(')."""
    depth = 0
    for i in range(start, len(text)):
        depth += {"(": 1, ")": -1}.get(text[i], 0)
        if depth == 0:
            return text[start:i + 1]
    raise SystemExit("unbalanced stack-up")


def purple(src, out, donor):
    text = open(src).read()
    if "(stackup" not in text:
        d = open(donor).read()
        stack = block(d, d.index("(stackup"))
        at = text.index("(setup") + len("(setup")
        text = text[:at] + "\n\t\t" + stack + text[at:]
    open(out, "w").write(text)


def scrub(src, out, texts):
    text = open(src).read()
    for t in texts:
        quoted = '"' + t.replace("\\", "\\\\").replace('"', '\\"') + '"'
        for kind in ("(fp_text user ", "(gr_text "):
            while (i := text.find(kind + quoted)) >= 0:
                text = text[:i] + text[i + len(block(text, i)):]
    open(out, "w").write(text)


if __name__ == "__main__":
    if sys.argv[1] == "scrub":
        scrub(sys.argv[2], sys.argv[3], sys.argv[4:])
    elif sys.argv[1] == "facts":
        facts(sys.argv[2], sys.argv[3], sys.argv[4:])
    elif sys.argv[1] == "purple":
        purple(*sys.argv[2:5])
    else:
        raise SystemExit(__doc__)
