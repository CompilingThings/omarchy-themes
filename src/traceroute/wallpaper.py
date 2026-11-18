"""Traceroute wallpaper: a real KiCad board drawn in copper on blue-black, with one net
traced hop by hop (pads and vias) like `traceroute`, distances in mm instead of ms.

    python3 wallpaper.py <board.kicad_pcb> <net name> <out.svg> [title]
    (build draws both wallpapers: see src/traceroute/build)

Needs KiCad's pcbnew Python module. Reads the board only; never saves it.
"""
import heapq
import html
import math
import sys

import pcbnew

W, H = 3840, 2160
BG = "#070C12"
MASK = "#0B1724"
COPPER = "#C9824C"
COPPER_HI = "#E8A56C"
BLUE = "#7FC8F8"
ICE = "#CFE6F5"
TRACE = "#9FDCFF"
FONT = "JetBrainsMono Nerd Font, monospace"

board_path, net_name, out_path = sys.argv[1:4]
title = sys.argv[4] if len(sys.argv) > 4 else ""
bd = pcbnew.LoadBoard(board_path)

MM = 1e6
bbox = bd.GetBoardEdgesBoundingBox()
bx, by, bw, bh = bbox.GetX() / MM, bbox.GetY() / MM, bbox.GetWidth() / MM, bbox.GetHeight() / MM
# Omarchy crops a wallpaper to fill the screen. Everything drawn stays inside what a 3:2 screen shows (7.8 % off each
# side of a 16:9 picture), so the terminal and the board are whole on every common laptop.
SAFE_X = round(W * (1 - (3 / 2) / (16 / 9)) / 2)
BOX_W = 1180  # terminal box on the left; the board sits to its right
area_x0, area_x1 = SAFE_X + BOX_W - 20, W - SAFE_X - 40
s = min((area_x1 - area_x0) / bw, H * 0.80 / bh)
ox = area_x0 + ((area_x1 - area_x0) - bw * s) / 2
oy = (H - bh * s) / 2


def scr(x_mm, y_mm):
    return ox + (x_mm - bx) * s, oy + (y_mm - by) * s


def f(v):
    return ("%.3f" % v).rstrip("0").rstrip(".")


def poly_path(ps):
    """SVG path data (board mm) for a SHAPE_POLY_SET, holes included (draw with evenodd)."""
    parts = []

    def chain(c):
        n = c.PointCount()
        if n < 2:
            return
        pts = [c.CPoint(j) for j in range(n)]
        parts.append("M" + " ".join("%s %s" % (f(p.x / MM), f(p.y / MM)) for p in pts) + "Z")

    for i in range(ps.OutlineCount()):
        chain(ps.Outline(i))
        for h in range(ps.HoleCount(i)):
            chain(ps.Hole(i, h))
    return "".join(parts)


def item_poly(item, layer):
    ps = pcbnew.SHAPE_POLY_SET()
    if item.GetClass() in ("PCB_TEXT", "PCB_FIELD"):
        item.TransformTextToPolySet(ps, 0, 2000, pcbnew.ERROR_INSIDE)  # the letters, not their box
    else:
        item.TransformShapeToPolygon(ps, layer, 0, 2000, pcbnew.ERROR_INSIDE)
    return ps


cu = list(bd.GetEnabledLayers().CuStack())
F, B = pcbnew.F_Cu, pcbnew.B_Cu
lname = {l: bd.GetLayerName(l) for l in cu}
tracks = [t for t in bd.GetTracks() if t.GetClass() == "PCB_TRACK"]
arcs = [t for t in bd.GetTracks() if t.GetClass() == "PCB_ARC"]
vias = [t for t in bd.GetTracks() if t.GetClass() == "PCB_VIA"]
pads = [p for fp in bd.GetFootprints() for p in fp.Pads()]


# ---- trace the net: the longest pad-to-pad path through tracks and vias ----
def key(layer, p):
    return (layer, int(round(p.x / 1000)), int(round(p.y / 1000)))


graph = {}


def link(a, b, w):
    graph.setdefault(a, []).append((b, w))
    graph.setdefault(b, []).append((a, w))


net_tracks = [t for t in tracks + arcs if t.GetNetname() == net_name]
net_vias = [v for v in vias if v.GetNetname() == net_name]
net_pads = [p for p in pads if p.GetNetname() == net_name]
if not net_tracks:
    sys.exit("no tracks on net %r" % net_name)
ends = []
for t in net_tracks:
    a, b = key(t.GetLayer(), t.GetStart()), key(t.GetLayer(), t.GetEnd())
    link(a, b, t.GetLength() / MM)
    ends += [(a, t.GetStart(), t.GetLayer()), (b, t.GetEnd(), t.GetLayer())]
# T-joins: a track that ends on the middle of another track on the same layer
for k, p, layer in ends:
    for t in net_tracks:
        if t.GetClass() != "PCB_TRACK" or t.GetLayer() != layer:
            continue
        a, b = t.GetStart(), t.GetEnd()
        ka, kb = key(layer, a), key(layer, b)
        if k in (ka, kb):
            continue
        dx, dy = b.x - a.x, b.y - a.y
        l2 = float(dx * dx + dy * dy) or 1.0
        u = max(0.0, min(1.0, ((p.x - a.x) * dx + (p.y - a.y) * dy) / l2))
        if math.hypot(a.x + u * dx - p.x, a.y + u * dy - p.y) <= t.GetWidth() / 2:
            link(k, ka, u * t.GetLength() / MM)
            link(k, kb, (1 - u) * t.GetLength() / MM)
for i, v in enumerate(net_vias):
    node = ("via", i)
    r = v.GetWidth(pcbnew.F_Cu) / 2
    c = v.GetPosition()
    for k, p, layer in ends:
        if math.hypot(p.x - c.x, p.y - c.y) <= r + 1000:
            link(node, k, 0.0)
for i, p in enumerate(net_pads):
    node = ("pad", i)
    for k, pt, layer in ends:
        if p.IsOnLayer(layer) and p.HitTest(pt):
            link(node, k, 0.0)


def dijkstra(src):
    dist, prev, q = {src: 0.0}, {}, [(0.0, 0, src)]
    n = 1
    while q:
        d, _, u = heapq.heappop(q)
        if d > dist.get(u, 1e18):
            continue
        for v, w in graph.get(u, []):
            nd = d + w
            if nd < dist.get(v, 1e18):
                dist[v], prev[v] = nd, u
                heapq.heappush(q, (nd, n, v))
                n += 1
    return dist, prev


best = None
for i in range(len(net_pads)):
    dist, prev = dijkstra(("pad", i))
    for j in range(len(net_pads)):
        d = dist.get(("pad", j))
        if j != i and d is not None and (best is None or d > best[0]):
            best = (d, i, j, prev)
if best is None:
    sys.exit("net %r has no routed pad-to-pad path" % net_name)
total, src, dst, prev = best
path = [("pad", dst)]
while path[-1] != ("pad", src):
    path.append(prev[path[-1]])
path.reverse()

hops, run, last = [], 0.0, None
for idx, node in enumerate(path):
    if last is not None:
        run += next(w for v, w in graph[last] if v == node)
    last = node
    if node[0] == "pad":
        p = net_pads[node[1]]
        hops.append(("%s.%s" % (p.GetParentFootprint().GetReference(), p.GetNumber()), "", run, p.GetPosition()))
    elif node[0] == "via":
        before = path[idx - 1][0] if idx else None
        after = path[idx + 1][0] if idx + 1 < len(path) else None
        names = [lname.get(before, "?"), lname.get(after, "?")]
        names = [n.replace(".Cu", "") for n in names]
        hops.append(("via", "%s \u2192 %s" % tuple(names), run, net_vias[node[1]].GetPosition()))
lit_tracks = net_tracks  # the whole net lights up; the hops are the route through it


# ---- draw ----
out = []
w = out.append
w('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">' % (W, H, W, H))
w("""<defs>
<radialGradient id="bg" cx="60%%" cy="48%%" r="75%%">
  <stop offset="0" stop-color="#0B1622"/><stop offset=".55" stop-color="%s"/><stop offset="1" stop-color="#020406"/>
</radialGradient>
<radialGradient id="vig" cx="55%%" cy="50%%" r="78%%">
  <stop offset=".6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".8"/>
</radialGradient>
<pattern id="grid" width="%s" height="%s" patternUnits="userSpaceOnUse" x="%s" y="%s">
  <circle cx="1.5" cy="1.5" r="1.5" fill="%s" fill-opacity=".10"/>
</pattern>
<filter id="glow" x="-20%%" y="-20%%" width="140%%" height="140%%">
  <feGaussianBlur stdDeviation="9" result="b"/>
  <feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
<filter id="glowmm" x="-5%%" y="-5%%" width="110%%" height="110%%">
  <feGaussianBlur stdDeviation="%s" result="b"/>
  <feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
<filter id="soft" x="-20%%" y="-20%%" width="140%%" height="140%%">
  <feGaussianBlur stdDeviation="4" result="b"/>
  <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
</defs>
<rect width="100%%" height="100%%" fill="url(#bg)"/>
<rect width="100%%" height="100%%" fill="url(#grid)"/>""" % (
    BG, f(2.54 * s), f(2.54 * s), f(ox % (2.54 * s)), f(oy % (2.54 * s)), BLUE, f(8 / s)))

w('<g transform="translate(%s %s) scale(%s) translate(%s %s)">' % (f(ox), f(oy), f(s), f(-bx), f(-by)))

outline = pcbnew.SHAPE_POLY_SET()
bd.GetBoardPolygonOutlines(outline, True)
w('<path d="%s" fill="%s" fill-rule="evenodd" stroke="%s" stroke-opacity=".45" stroke-width="%s"/>'
  % (poly_path(outline), MASK, BLUE, f(1.6 / s)))


def zones(layer, color, op):
    for z in bd.Zones():
        if z.IsOnLayer(layer) and not z.GetIsRuleArea():
            d = poly_path(z.GetFilledPolysList(layer))
            if d:
                w('<path d="%s" fill="%s" fill-opacity="%s" fill-rule="evenodd"/>' % (d, color, op))


def track_lines(layer, color, op, extra=1.0):
    w('<g stroke="%s" stroke-opacity="%s" stroke-linecap="round" fill="none">' % (color, op))
    for t in tracks:
        if t.GetLayer() == layer:
            a, b = t.GetStart(), t.GetEnd()
            w('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke-width="%s"/>' % (
                f(a.x / MM), f(a.y / MM), f(b.x / MM), f(b.y / MM), f(t.GetWidth() / MM * extra)))
    for t in arcs:
        if t.GetLayer() == layer:
            ps = item_poly(t, layer)
            w('<path d="%s" fill="%s" fill-opacity="%s" stroke="none"/>' % (poly_path(ps), color, op))
    w("</g>")


def silk(layer, color, op):
    """Every silkscreen line, circle and label on one side, as the board would print them."""
    w('<g fill="%s" fill-opacity="%s">' % (color, op))
    items = [it for it in bd.GetDrawings()]
    for fp in bd.GetFootprints():
        items += list(fp.GraphicalItems()) + list(fp.GetFields())
    for it in items:
        if it.GetLayer() != layer or (hasattr(it, "IsVisible") and not it.IsVisible()):
            continue
        d = poly_path(item_poly(it, layer))
        if d:
            w('<path d="%s"/>' % d)
    w("</g>")


inner = [l for l in cu if l not in (F, B)]
zones(B, BLUE, ".035")
for l in inner:
    track_lines(l, BLUE, ".10")
track_lines(B, BLUE, ".20")
w('<g fill="%s" fill-opacity=".22">' % BLUE)
for p in pads:
    if p.IsOnLayer(B) and not p.IsOnLayer(F):
        w('<path d="%s"/>' % poly_path(item_poly(p, B)))
w("</g>")
silk(pcbnew.B_SilkS, BLUE, ".20")  # the back's printing, seen through the board (mirrored)
zones(F, COPPER, ".07")
track_lines(F, COPPER, ".62")
w('<g fill="%s" fill-opacity=".82">' % COPPER_HI)
for p in pads:
    if p.IsOnLayer(F):
        w('<path d="%s"/>' % poly_path(item_poly(p, F)))
w("</g>")
for v in vias:
    c = v.GetPosition()
    r = v.GetWidth(F) / MM / 2
    dr = v.GetDrillValue() / MM / 2
    w('<circle cx="%s" cy="%s" r="%s" fill="none" stroke="%s" stroke-opacity=".75" stroke-width="%s"/>' % (
        f(c.x / MM), f(c.y / MM), f((r + dr) / 2), COPPER, f(r - dr)))

silk(pcbnew.F_SilkS, ICE, ".62")

# the traced net, lit
w('<g filter="url(#glowmm)" stroke="%s" stroke-linecap="round" fill="none">' % TRACE)
for t in lit_tracks:
    if t.GetClass() == "PCB_TRACK":
        a, b = t.GetStart(), t.GetEnd()
        w('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke-width="%s"/>' % (
            f(a.x / MM), f(a.y / MM), f(b.x / MM), f(b.y / MM), f(max(t.GetWidth() / MM * 1.4, 0.22))))
    else:
        w('<path d="%s" fill="%s" stroke="none"/>' % (poly_path(item_poly(t, t.GetLayer())), TRACE))
w("</g>")
w("</g>")

# hop numbers beside the board's pads and vias
w('<g font-family="%s" font-size="26" font-weight="700" fill="%s" filter="url(#soft)">' % (FONT, TRACE))
for n, (name, via, d, pos) in enumerate(hops, 1):
    x, y = scr(pos.x / MM, pos.y / MM)
    w('<circle cx="%s" cy="%s" r="11" fill="none" stroke="%s" stroke-width="3"/>' % (f(x), f(y), TRACE))
    w('<text x="%s" y="%s">%d</text>' % (f(x + 16), f(y - 14), n))
w("</g>")

# silkscreen-style caption under the board
nlayers = len(cu)
cap = "%s  ·  %d LAYERS  ·  %d TRACES  ·  %d VIAS" % (
    title.upper() or "BOARD", nlayers, len(tracks) + len(arcs), len(vias))
w('<text x="%s" y="%s" font-family="%s" font-size="30" letter-spacing="6" fill="%s" fill-opacity=".45">%s</text>' % (
    f(ox), f(oy + bh * s + 70), FONT, ICE, html.escape(cap)))

# the terminal
lines = [("dim", "// TRACEROUTE :: copper, not packets"),
         ("cmd", "$ traceroute %s" % net_name.split("/")[-1]),
         ("dim", "traceroute to %s (%s), 30 hops max" % (hops[-1][0], net_name.split("/")[-1]))]
for n, (name, via, d, pos) in enumerate(hops, 1):
    lines.append(("hop", "%2d  %-10s %-9s %7.2f mm" % (n, name, via, d)))
lines.append(("blank", ""))
tx, ty, lh = SAFE_X + 110, 0, 46
box_h = 90 + lh * (len(lines) + 1)
ty = H - 170 - box_h
w('<rect x="%d" y="%d" width="%d" height="%d" fill="#03070B" fill-opacity=".86"/>' % (tx - 50, ty, BOX_W - 120, box_h))
w('<rect x="%d" y="%d" width="%d" height="%d" fill="none" stroke="%s" stroke-opacity=".5" stroke-width="2"/>' % (
    tx - 50, ty, BOX_W - 120, box_h, COPPER))
w('<g font-family="%s" font-size="32" xml:space="preserve">' % FONT)
y = ty + 70
for kind, text in lines:
    color, op, weight = {"dim": ("#6F8EA3", 1, 400), "cmd": (COPPER_HI, 1, 700),
                         "hop": (ICE, .92, 400), "blank": (ICE, 1, 400)}[kind]
    w('<text x="%d" y="%d" fill="%s" fill-opacity="%s" font-weight="%d">%s</text>' % (
        tx, y, color, op, weight, html.escape(text)))
    y += lh
w('<text x="%d" y="%d" fill="%s" font-weight="700" filter="url(#soft)">root@deck:~#</text>' % (tx, y, TRACE))
w('<rect x="%d" y="%d" width="20" height="36" fill="%s"/>' % (tx + 250, y - 30, TRACE))
w("</g>")

w('<rect width="100%" height="100%" fill="url(#vig)"/>')
w("</svg>")
with open(out_path, "w") as fh:
    fh.write("\n".join(out))
xs = [h[3].x / MM for h in hops]; ys = [h[3].y / MM for h in hops]
print("%s: %d hops, %.1f mm, %d lit tracks, spread %.0f x %.0f mm" % (net_name, len(hops), total, len(lit_tracks), max(xs) - min(xs), max(ys) - min(ys)), file=sys.stderr)
