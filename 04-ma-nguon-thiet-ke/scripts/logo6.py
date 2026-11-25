import os, json, sys
sys.path.insert(0, "/home/claude")
from logo2 import Font, svg

MUN = "#241B13"; KEM = "#F5EEE2"; DONG = "#BE8A4E"
TILEF = Font("/home/claude/fonts/ArchivoBlack.ttf")
WORDF = Font("/home/claude/fonts/Fredoka-600.ttf")
TAGF = Font("/home/claude/fonts/BeVietnamPro-Bold.ttf")
OUT = "/home/claude/out/logoXE"; os.makedirs(OUT, exist_ok=True)

TILE = 200.0; u = TILE / 2.6
GAP = 0.36 * u; RAD = 0.47 * u
CELLS = ["X", "O", "E", "M"]

def glyphs(font, text, size, track=0.0):
    return font.line(text, size, track)

def mark(x, y, sch):
    out = []
    for i, t in enumerate(CELLS):
        cx = x + (i % 2) * (TILE + GAP); cy = y + (i // 2) * (TILE + GAP)
        bg, fg = sch["tiles"][i]
        out.append(f'<rect x="{cx:.1f}" y="{cy:.1f}" width="{TILE:.1f}" height="{TILE:.1f}" rx="{RAD:.1f}" fill="{bg}"></rect>')
        size = 1.5 * u * (0.78 if t == "NG" else 1.0)
        d, (x0, y0, x1, y1) = glyphs(TILEF, t, size, -0.02)
        cap = 0.70 * size
        tx = cx + TILE / 2 - (x0 + x1) / 2
        ty = cy + TILE / 2 + cap / 2 + (0.10 * size if t in "ÔÊ" else 0)
        out.append(f'<g transform="translate({tx:.2f} {ty:.2f})" fill="{fg}">{d}</g>')
    return "".join(out), 2 * TILE + GAP

def text_block(x, y, sch, align="left", width=None):
    ws = 3.2 * u
    d1, b1 = glyphs(WORDF, "Xo ", ws, -0.01)
    d2, b2 = glyphs(WORDF, "em", ws, -0.01)
    adv1 = WORDF.line("Xo ", ws, -0.01)
    # width of "Xo " incl. trailing space advance
    w_xo = sum(WORDF.glyph(c, ws)[1] for c in "Xo ") - 0.01 * ws * 2
    word_w = w_xo + (b2[2] - b2[0]) + b2[0]
    top = min(b1[1], b2[1]); base_h = -top
    tag_size = 0.72 * u
    dt, bt = glyphs(TAGF, "SLOW COFFEE · COMFY SEATS", tag_size, 0.16)
    tag_w = bt[2] - bt[0]
    colw = max(word_w, tag_w)
    ox = x if align == "left" else x + (width - colw) / 2
    wx = ox if align == "left" else ox + (colw - word_w) / 2
    out = [f'<g transform="translate({wx - b1[0]:.2f} {y + base_h:.2f})" fill="{sch["word"]}">{d1}</g>',
           f'<g transform="translate({wx - b1[0] + w_xo:.2f} {y + base_h:.2f})" fill="{sch["accent"]}">{d2}</g>']
    desc = max(b1[3], b2[3])
    ry = y + base_h + max(desc, 0.05 * ws) + 0.55 * u
    out.append(f'<rect x="{ox:.1f}" y="{ry:.1f}" width="{colw:.1f}" height="{0.13 * u:.1f}" rx="{0.065 * u:.1f}" fill="{sch["accent"]}"></rect>')
    ty = ry + 0.13 * u + 0.5 * u
    tx = ox if align == "left" else ox + (colw - tag_w) / 2
    out.append(f'<g transform="translate({tx - bt[0]:.2f} {ty - bt[1]:.2f})" fill="{sch["word"]}">{dt}</g>')
    h = ty + (bt[3] - bt[1]) - y
    return "".join(out), colw, h

def lockup(sch):
    m, ms = mark(0, 0, sch)
    t, tw, th = text_block(0, 0, sch)
    gx = ms + 1.6 * u
    ty = (ms - th) / 2
    t, tw, th = text_block(gx, ty, sch)
    return svg(gx + tw + 4, ms, m + t)

def stacked(sch):
    _, tw, th = text_block(0, 0, sch)
    W = max(2 * TILE + GAP, tw) + 4
    m, ms = mark((W - (2 * TILE + GAP)) / 2, 0, sch)
    t, _, th = text_block(0, ms + 0.9 * u, sch, "center", W)
    return svg(W, ms + 0.9 * u + th + 4, m + t)

def mark_only(sch):
    m, ms = mark(0, 0, sch)
    return svg(ms, ms, m)

def words_only(sch):
    t, tw, th = text_block(0, 0, sch)
    return svg(tw + 4, th + 4, t)

SCH = {
    "mau":     dict(word=MUN, accent=DONG, tiles=[(MUN, KEM), (DONG, MUN), (DONG, MUN), (MUN, KEM)]),
    "nen-toi": dict(word=KEM, accent=DONG, tiles=[(KEM, MUN), (DONG, MUN), (DONG, MUN), (KEM, MUN)]),
    "den":     dict(word=MUN, accent=MUN, tiles=[(MUN, "#FFFFFF")] * 4),
    "trang":   dict(word="#FFFFFF", accent="#FFFFFF", tiles=[("#FFFFFF", MUN)] * 4),
}
files = []
for sn, sch in SCH.items():
    for name, fn in (("ngang", lockup), ("doc", stacked), ("bieu-tuong", mark_only), ("chu", words_only)):
        p = f"{OUT}/XoEm-logo-{name}-{sn}.svg"; open(p, "w").write(fn(sch)); files.append(p)
json.dump(files, open(f"{OUT}/list.json", "w"))
print(len(files))
