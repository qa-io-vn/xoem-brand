import os, math, json
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.transformPen import TransformPen

DONG = "#9A6A33"; KEM = "#F5EEE2"; MUN = "#241B13"
OUT = "/home/claude/out/logo2"; os.makedirs(OUT, exist_ok=True)

class Font:
    def __init__(self, p):
        self.f = TTFont(p); self.gs = self.f.getGlyphSet(); self.cm = self.f.getBestCmap()
        self.upm = self.f["head"].unitsPerEm; self.hm = self.f["hmtx"]
    def glyph(self, ch, size):
        g = self.cm[ord(ch)]; s = size / self.upm
        pen = SVGPathPen(self.gs); bp = BoundsPen(self.gs)
        t = (s, 0, 0, -s, 0, 0)
        self.gs[g].draw(TransformPen(pen, t)); self.gs[g].draw(TransformPen(bp, t))
        return pen.getCommands(), self.hm[g][0] * s, bp.bounds
    def line(self, text, size, track=0.0):
        ds, x = [], 0.0; xmin = ymin = 1e9; xmax = ymax = -1e9
        for ch in text:
            d, adv, b = self.glyph(ch, size)
            if d:
                ds.append(f'<path transform="translate({x:.2f} 0)" d="{d}"></path>')
                xmin = min(xmin, x + b[0]); xmax = max(xmax, x + b[2]); ymin = min(ymin, b[1]); ymax = max(ymax, b[3])
            x += adv + track * size
        return "".join(ds), (xmin, ymin, xmax, ymax)

BAL = Font("/home/claude/fonts/Baloo2-ExtraBold-static.ttf")
SEMI = Font("/home/claude/fonts/BeVietnamPro-SemiBold.ttf")

def sofa(x, y, w, body, line, cushion):
    s = w / 200.0
    return (f'<g transform="translate({x:.1f} {y:.1f}) scale({s:.4f})" stroke="{line}" stroke-width="9" stroke-linejoin="round" stroke-linecap="round">'
            f'<rect x="42" y="14" width="116" height="66" rx="20" fill="{body}"></rect>'
            f'<rect x="42" y="70" width="116" height="36" rx="10" fill="{cushion}"></rect>'
            f'<path d="M100,74 L100,104" fill="none"></path>'
            f'<rect x="10" y="48" width="44" height="72" rx="20" fill="{body}"></rect>'
            f'<rect x="146" y="48" width="44" height="72" rx="20" fill="{body}"></rect>'
            f'<path d="M34,122 L30,138 M166,122 L170,138" fill="none"></path></g>')

def svg(w, h, body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" height="{h:.0f}">{body}</svg>'

# ---------- A: gạch chữ 3x2 ----------
def tiles(sch):
    T, G = 150, 8
    cells = [("SOFA",), ("X",), ("Ô",), ("N",), ("G",), ("Ơ",)]
    fills = sch["tiles"]
    out = []
    for i, c in enumerate(cells):
        cx, cy = (i % 3) * (T + G), (i // 3) * (T + G)
        bg, fg = fills[i]
        out.append(f'<rect x="{cx}" y="{cy}" width="{T}" height="{T}" rx="14" fill="{bg}"></rect>')
        if c[0] == "SOFA":
            out.append(sofa(cx + 17, cy + 34, 116, fg, bg, fg))
        else:
            d, adv, (x0, y0, x1, y1) = BAL.glyph(c[0], 150)
            tx = cx + T / 2 - (x0 + x1) / 2; ty = cy + T / 2 - (y0 + y1) / 2 + (6 if c[0] in "ÔƠ" else 0)
            out.append(f'<path transform="translate({tx:.2f} {ty:.2f})" d="{d}" fill="{fg}"></path>')
    W = 3 * T + 2 * G; H = 2 * T + G
    tg, (a, b, c2, d2) = SEMI.line("SLOW COFFEE · COMFY SEATS", 19.5, 0.2)
    tw = c2 - a
    out.append(f'<g transform="translate({(W - tw) / 2 - a:.2f} {H + 30 - b:.2f})" fill="{sch["text"]}">{tg}</g>')
    return svg(W, H + 30 + (d2 - b) + 4, "".join(out))

# ---------- B: ngang ----------
def horiz(sch):
    S = 200
    wm, (x0, y0, x1, y1) = BAL.line("Xô Ngơ", 150, -0.01)
    tg, (a, b, c, d) = SEMI.line("SLOW COFFEE · COMFY SEATS", 22, 0.22)
    wx = S + 36
    wm_h = y1 - y0
    block_h = wm_h + 18 + (d - b)
    H = max(150, block_h)
    out = [sofa(0, (H - 150) / 2 + 8, S, sch["body"], sch["line"], sch["cushion"])]
    oy = (H - block_h) / 2
    out.append(f'<g transform="translate({wx - x0:.2f} {oy - y0:.2f})" fill="{sch["text"]}">{wm}</g>')
    out.append(f'<g transform="translate({wx + 4 - a:.2f} {oy + wm_h + 18 - b:.2f})" fill="{sch["text"]}">{tg}</g>')
    W = wx + max(x1 - x0, c - a + 4)
    return svg(W + 4, H, "".join(out))

# ---------- C: con dấu tròn ----------
def arc_text(font, text, size, r, cx, cy, top=True, track=0.12):
    items = []; total = 0.0
    for ch in text:
        d, adv, b = font.glyph(ch, size)
        items.append((d, adv)); total += adv + track * size
    total -= track * size
    out = []; cum = 0.0
    for d, adv in items:
        mid = cum + adv / 2
        if top:
            ang = math.degrees(-total / (2 * r) + mid / r)
            tr = f"translate({cx} {cy}) rotate({ang:.3f}) translate({-adv / 2:.2f} {-r})"
        else:
            ang = math.degrees(total / (2 * r) - mid / r)
            tr = f"translate({cx} {cy}) rotate({ang:.3f}) translate({-adv / 2:.2f} {r})"
        if d:
            out.append(f'<path transform="{tr}" d="{d}"></path>')
        cum += adv + track * size
    return "".join(out)

def badge(sch):
    R = 240; cx = cy = R + 6
    out = [f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="{sch["disc"]}" stroke="{sch["line"]}" stroke-width="10"></circle>',
           f'<circle cx="{cx}" cy="{cy}" r="{R - 26}" fill="none" stroke="{sch["line"]}" stroke-width="3"></circle>',
           f'<circle cx="{cx}" cy="{cy}" r="{R - 96}" fill="{sch["inner"]}" stroke="{sch["line"]}" stroke-width="5"></circle>']
    out.append(f'<g fill="{sch["ring"]}">{arc_text(BAL, "XÔ NGƠ", 70, R - 82, cx, cy, True, 0.16)}</g>')
    out.append(f'<g fill="{sch["ring"]}">{arc_text(SEMI, "SLOW COFFEE · COMFY SEATS", 24, R - 54, cx, cy, False, 0.18)}</g>')
    for sx in (-1, 1):
        x = cx + sx * (R - 61)
        out.append(f'<circle cx="{x}" cy="{cy}" r="7" fill="{sch["ring"]}"></circle>')
    out.append(sofa(cx - 95, cy - 70, 190, sch["body"], sch["line"], sch["cushion"]))
    return svg(2 * cx, 2 * cy, "".join(out))

SCHEMES = {
  "mau": dict(text=MUN, body=DONG, line=MUN, cushion=KEM, disc=KEM, inner=KEM, ring=MUN,
              tiles=[(MUN, KEM), (DONG, KEM), (MUN, KEM), (DONG, KEM), (MUN, KEM), (DONG, KEM)]),
  "nen-toi": dict(text=KEM, body=DONG, line=KEM, cushion=MUN, disc=MUN, inner=MUN, ring=KEM,
              tiles=[(KEM, MUN), (DONG, KEM), (KEM, MUN), (DONG, KEM), (KEM, MUN), (DONG, KEM)]),
  "den": dict(text=MUN, body="none", line=MUN, cushion="none", disc="none", inner="none", ring=MUN,
              tiles=[(MUN, "#FFFFFF")] * 6),
}
# mono tiles: black squares with letters knocked out to white; keep simple

files = []
for name, fn in (("gach-chu", tiles), ("ngang", horiz), ("con-dau", badge)):
    for sn, sch in SCHEMES.items():
        p = f"{OUT}/XoNgo-logo-{name}-{sn}.svg"
        open(p, "w").write(fn(sch)); files.append(p)
json.dump(files, open(f"{OUT}/list.json", "w"))
print(len(files))
