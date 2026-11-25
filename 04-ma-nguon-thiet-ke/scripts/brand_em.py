import json, os

ROOT = "/home/claude/xoem-brand/project"
os.makedirs(ROOT, exist_ok=True)

CREAM = "#F6EEDF"; ESP = "#2B1D16"; TERRA = "#C8553D"; MOSS = "#5E7A4A"
BUTTER = "#F2C14E"; SAND = "#E8D5B5"; KRAFT = "#C9A27A"; BLUSH = "#EBA08C"; LEAF = "#86A266"

DISPLAY = "font-family: 'Baloo 2', 'Be Vietnam Pro', sans-serif"
SANS = "font-family: 'Be Vietnam Pro', system-ui, sans-serif"
HAND = "font-family: 'Patrick Hand', 'Be Vietnam Pro', cursive"
FONTS = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@500;600;700;800'
         '&amp;family=Be+Vietnam+Pro:wght@400;500;600;700&amp;family=Patrick+Hand&amp;display=swap">')
W, H = 1600, 1000

# ---------------------------------------------------------------- marks
def symbol_inner(body=TERRA, ink=ESP, white=CREAM, steam=True):
    e = []
    if steam:
        e.append(f'<path d="M88,46 q-9,-8 0,-16 q9,-8 0,-16" fill="none" stroke="{ink}" stroke-width="7" stroke-linecap="round"></path>')
        e.append(f'<path d="M112,46 q-9,-8 0,-16 q9,-8 0,-16" fill="none" stroke="{ink}" stroke-width="7" stroke-linecap="round"></path>')
    e.append(f'<path d="M26,100 Q26,84 42,84 L50,84 L50,76 Q50,58 70,58 L130,58 Q150,58 150,76 L150,84 L158,84 Q174,84 174,100 '
             f'L174,118 Q174,128 164,130 L154,168 Q151,180 138,180 L62,180 Q49,180 46,168 L36,130 Q26,128 26,118 Z" '
             f'fill="{body}" stroke="{ink}" stroke-width="7" stroke-linejoin="round"></path>')
    e.append(f'<path d="M50,92 L50,130 M150,92 L150,130 M50,130 Q100,142 150,130" fill="none" stroke="{ink}" stroke-width="5" stroke-linecap="round"></path>')
    e.append(f'<circle cx="82" cy="98" r="14" fill="{white}" stroke="{ink}" stroke-width="4.5"></circle>')
    e.append(f'<circle cx="88" cy="101" r="6.5" fill="{ink}"></circle>')
    e.append(f'<circle cx="120" cy="102" r="8.5" fill="{white}" stroke="{ink}" stroke-width="4"></circle>')
    e.append(f'<circle cx="116" cy="103" r="3.8" fill="{ink}"></circle>')
    e.append(f'<path d="M94,118 Q102,124 110,117" fill="none" stroke="{ink}" stroke-width="4.5" stroke-linecap="round"></path>')
    e.append(f'<path d="M36,194 L164,194" stroke="{ink}" stroke-width="7" stroke-linecap="round"></path>')
    return "".join(e)

def symbol(size, **kw):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 200 200" role="img" aria-label="Biểu tượng Xo em" '
            f'style="display: block; flex-shrink: 0">{symbol_inner(**kw)}</svg>')

def wordmark(px, color=ESP):
    return (f'<div style="{DISPLAY}; font-weight: 800; font-size: {px}px; line-height: 0.9; letter-spacing: -0.02em; color: {color}; '
            f'padding-top: {int(px*0.12)}px; white-space: nowrap">xo em</div>')

def lockup(sym, px, body=TERRA, ink=ESP, white=CREAM, tag=True, tagcolor=None, gap=None):
    tagcolor = tagcolor or ink
    g = gap if gap is not None else int(px * 0.18)
    t = (f'<div style="{SANS}; font-weight: 600; font-size: {max(11, int(px*0.13))}px; letter-spacing: 0.22em; color: {tagcolor}; '
         f'margin-top: {int(px*0.06)}px">SLOW COFFEE · COMFY SEATS</div>') if tag else ""
    return (f'<div style="display: flex; align-items: center; gap: {g}px">{symbol(sym, body=body, ink=ink, white=white)}'
            f'<div style="display: flex; flex-direction: column">{wordmark(px, ink)}{t}</div></div>')

def stacked(sym, px, body=TERRA, ink=ESP, white=CREAM, tag=True):
    t = (f'<div style="{SANS}; font-weight: 600; font-size: {max(11, int(px*0.14))}px; letter-spacing: 0.22em; color: {ink}">SLOW COFFEE · COMFY SEATS</div>') if tag else ""
    return (f'<div style="display: flex; flex-direction: column; align-items: center; gap: 6px">{symbol(sym, body=body, ink=ink, white=white)}'
            f'{wordmark(px, ink)}{t}</div>')

# ---------------------------------------------------------------- mascots
def tube(d, w_out, w_in, fill):
    return (f'<path d="{d}" fill="none" stroke="{ESP}" stroke-width="{w_out}" stroke-linecap="round"></path>'
            f'<path d="{d}" fill="none" stroke="{fill}" stroke-width="{w_in}" stroke-linecap="round"></path>')

def nga_inner():
    e = []
    e.append('<ellipse cx="160" cy="226" rx="140" ry="9" fill="rgba(43,29,22,0.12)"></ellipse>')
    e.append(f'<rect x="48" y="214" width="16" height="12" rx="3" fill="{ESP}"></rect><rect x="256" y="214" width="16" height="12" rx="3" fill="{ESP}"></rect>')
    e.append(f'<rect x="52" y="72" width="216" height="96" rx="32" fill="{TERRA}" stroke="{ESP}" stroke-width="6"></rect>')
    e.append(f'<path d="M118,84 L118,150 M202,84 L202,150" stroke="{ESP}" stroke-width="3.5" stroke-linecap="round" opacity="0.5"></path>')
    e.append(f'<rect x="40" y="150" width="240" height="66" rx="24" fill="{TERRA}" stroke="{ESP}" stroke-width="6"></rect>')
    # dragon body
    for cx in (128, 158, 188):
        e.append(f'<path d="M{cx-12},130 Q{cx},100 {cx+12},130 Z" fill="{SAND}" stroke="{ESP}" stroke-width="4" stroke-linejoin="round"></path>')
    e.append(f'<ellipse cx="160" cy="150" rx="88" ry="32" fill="{BUTTER}" stroke="{ESP}" stroke-width="6"></ellipse>')
    e.append(f'<path d="M110,164 Q160,178 210,164" fill="none" stroke="{ESP}" stroke-width="2.5" stroke-dasharray="6 6"></path>')
    e.append(f'<path d="M172,136 q16,-28 38,-14 q-12,4 -10,18 Z" fill="{SAND}" stroke="{ESP}" stroke-width="4" stroke-linejoin="round"></path>')
    # tail over right arm
    e.append(tube("M236,156 Q292,136 294,176 Q296,200 276,206", 24, 14, BUTTER))
    e.append(f'<path d="M266,198 L290,214 L270,220 Z" fill="{TERRA}" stroke="{ESP}" stroke-width="4" stroke-linejoin="round"></path>')
    # arms of sofa
    e.append(f'<rect x="16" y="118" width="58" height="98" rx="26" fill="{TERRA}" stroke="{ESP}" stroke-width="6"></rect>')
    e.append(f'<rect x="246" y="118" width="58" height="98" rx="26" fill="{TERRA}" stroke="{ESP}" stroke-width="6"></rect>')
    e.append(tube("M246,150 Q280,140 286,170", 24, 14, BUTTER))
    # head on left arm
    e.append(f'<path d="M58,86 q-6,-26 10,-32 q6,16 4,32 Z" fill="{SAND}" stroke="{ESP}" stroke-width="4" stroke-linejoin="round"></path>')
    e.append(f'<path d="M90,84 q2,-26 18,-26 q0,16 -6,30 Z" fill="{SAND}" stroke="{ESP}" stroke-width="4" stroke-linejoin="round"></path>')
    e.append(f'<circle cx="78" cy="116" r="42" fill="{BUTTER}" stroke="{ESP}" stroke-width="6"></circle>')
    e.append(f'<ellipse cx="50" cy="130" rx="26" ry="19" fill="{BUTTER}" stroke="{ESP}" stroke-width="6"></ellipse>')
    e.append(f'<circle cx="40" cy="126" r="3" fill="{ESP}"></circle><circle cx="52" cy="124" r="3" fill="{ESP}"></circle>')
    e.append(f'<path d="M64,110 q8,7 16,0 M92,106 q8,7 16,0" fill="none" stroke="{ESP}" stroke-width="4.5" stroke-linecap="round"></path>')
    e.append(f'<ellipse cx="98" cy="126" rx="8" ry="5" fill="{BLUSH}"></ellipse>')
    e.append(f'<path d="M58,142 q6,4 12,0" fill="none" stroke="{ESP}" stroke-width="4" stroke-linecap="round"></path>')
    for x, y, s in ((122, 70, 26), (146, 46, 34), (176, 20, 42)):
        e.append(f'<text x="{x}" y="{y}" font-family="Patrick Hand, cursive" font-size="{s}" fill="{ESP}">z</text>')
    return "".join(e)

def ngo_inner():
    e = []
    e.append('<ellipse cx="130" cy="288" rx="86" ry="9" fill="rgba(43,29,22,0.12)"></ellipse>')
    e.append(tube("M176,246 Q236,256 232,206 Q230,180 248,172", 24, 14, MOSS))
    e.append(f'<path d="M240,178 L256,156 L258,182 Z" fill="{TERRA}" stroke="{ESP}" stroke-width="4" stroke-linejoin="round"></path>')
    e.append(f'<ellipse cx="102" cy="276" rx="28" ry="13" fill="{MOSS}" stroke="{ESP}" stroke-width="5"></ellipse>')
    e.append(f'<ellipse cx="160" cy="276" rx="28" ry="13" fill="{MOSS}" stroke="{ESP}" stroke-width="5"></ellipse>')
    e.append(f'<path d="M130,128 C70,128 58,204 70,250 Q80,282 130,282 Q180,282 190,250 C202,204 190,128 130,128 Z" fill="{MOSS}" stroke="{ESP}" stroke-width="6"></path>')
    e.append(f'<ellipse cx="130" cy="228" rx="40" ry="46" fill="{SAND}" stroke="{ESP}" stroke-width="4"></ellipse>')
    e.append(f'<path d="M130,186 L130,270" stroke="{ESP}" stroke-width="2.5" stroke-dasharray="6 6"></path>')
    for y in (196, 214, 232, 250):
        e.append(f'<path d="M124,{y} L136,{y}" stroke="{ESP}" stroke-width="2"></path>')
    e.append(tube("M80,200 Q54,208 58,232", 22, 13, MOSS))
    e.append(tube("M180,200 Q206,204 208,228", 22, 13, MOSS))
    # horns + cup on horn
    e.append(f'<path d="M86,70 q-14,-40 6,-50 q8,24 16,44 Z" fill="{SAND}" stroke="{ESP}" stroke-width="4" stroke-linejoin="round"></path>')
    e.append(f'<path d="M172,66 q12,-40 -8,-50 q-6,24 -16,44 Z" fill="{SAND}" stroke="{ESP}" stroke-width="4" stroke-linejoin="round"></path>')
    e.append(f'<g transform="rotate(16 168 30)"><path d="M152,14 L184,14 L179,44 Q178,48 174,48 L162,48 Q158,48 157,44 Z" fill="{CREAM}" stroke="{ESP}" stroke-width="3.5" stroke-linejoin="round"></path>'
             f'<rect x="155" y="26" width="26" height="8" fill="{TERRA}"></rect>'
             f'<path d="M184,20 q10,2 8,12 q-2,6 -10,6" fill="none" stroke="{ESP}" stroke-width="3.5"></path>'
             f'<path d="M166,8 q-5,-5 0,-10" fill="none" stroke="{ESP}" stroke-width="3" stroke-linecap="round"></path></g>')
    e.append(f'<ellipse cx="62" cy="96" rx="16" ry="9" fill="{LEAF}" stroke="{ESP}" stroke-width="4" transform="rotate(-30 62 96)"></ellipse>')
    e.append(f'<ellipse cx="198" cy="100" rx="16" ry="9" fill="{LEAF}" stroke="{ESP}" stroke-width="4" transform="rotate(30 198 100)"></ellipse>')
    e.append(f'<ellipse cx="130" cy="112" rx="72" ry="60" fill="{MOSS}" stroke="{ESP}" stroke-width="6"></ellipse>')
    for x, y in ((92, 74), (170, 76), (80, 136), (184, 138)):
        e.append(f'<circle cx="{x}" cy="{y}" r="4" fill="{LEAF}"></circle>')
    e.append(f'<circle cx="104" cy="104" r="23" fill="{CREAM}" stroke="{ESP}" stroke-width="4.5"></circle>')
    e.append(f'<circle cx="112" cy="110" r="9.5" fill="{ESP}"></circle><circle cx="115" cy="106" r="3" fill="{CREAM}"></circle>')
    e.append(f'<circle cx="160" cy="108" r="12" fill="{CREAM}" stroke="{ESP}" stroke-width="4"></circle>')
    e.append(f'<circle cx="155" cy="111" r="5" fill="{ESP}"></circle>')
    e.append(f'<circle cx="124" cy="130" r="3" fill="{ESP}"></circle><circle cx="138" cy="130" r="3" fill="{ESP}"></circle>')
    e.append(f'<path d="M108,142 Q132,160 158,140" fill="none" stroke="{ESP}" stroke-width="5" stroke-linecap="round"></path>')
    e.append(f'<rect x="118" y="146" width="9" height="9" rx="2" fill="{CREAM}" stroke="{ESP}" stroke-width="2.5"></rect>')
    e.append(f'<path d="M136,150 q1,22 14,19 q9,-4 3,-22 Z" fill="{TERRA}" stroke="{ESP}" stroke-width="3.5" stroke-linejoin="round"></path>')
    e.append(f'<text x="214" y="70" font-family="Patrick Hand, cursive" font-size="48" fill="{TERRA}">?</text>')
    return "".join(e)

def nga(w):
    return f'<svg width="{w}" height="{int(w*240/320)}" viewBox="0 0 320 240" role="img" aria-label="Linh vật Em Ngả" style="display: block">{nga_inner()}</svg>'

def ngo(w):
    return f'<svg width="{w}" height="{int(w*300/260)}" viewBox="0 0 260 300" role="img" aria-label="Linh vật Em Ngơ" style="display: block">{ngo_inner()}</svg>'


def boss_inner():
    return symbol_inner()

def boss(w):
    return f'<svg width="{w}" height="{w}" viewBox="0 0 200 200" role="img" aria-label="Linh vật Boss" style="display: block">{boss_inner()}</svg>'

def squiggle(x, y, c, s=1.0, sw=5):
    return f'<path d="M{x},{y} q{8*s},{-10*s} {16*s},0 q{8*s},{10*s} {16*s},0 q{8*s},{-10*s} {16*s},0" fill="none" stroke="{c}" stroke-width="{sw}" stroke-linecap="round"></path>'

def pattern_svg(w, h, bg, body, ink, white, accent, scale=1.0):
    e = [f'<rect width="{w}" height="{h}" fill="{bg}"></rect>']
    step = int(150 * scale)
    r = 0
    for y in range(-20, h + step, step):
        off = (step // 2) if r % 2 else 0
        for x in range(-40 + off, w + step, step):
            k = (x // step + r) % 3
            if k == 0:
                s = 0.42 * scale
                e.append(f'<g transform="translate({x} {y}) scale({s:.3f}) rotate(-8 100 100)">{symbol_inner(body=body, ink=ink, white=white)}</g>')
            elif k == 1:
                e.append(squiggle(x + 20, y + 50, accent, scale, 5))
                e.append(f'<text x="{x+70}" y="{y+40}" font-family="Patrick Hand, cursive" font-size="{int(34*scale)}" fill="{accent}">z</text>')
            else:
                cx, cy = x + 50, y + 50
                e.append(f'<path d="M{cx},{cy-14} L{cx+4},{cy-4} L{cx+14},{cy} L{cx+4},{cy+4} L{cx},{cy+14} L{cx-4},{cy+4} L{cx-14},{cy} L{cx-4},{cy-4} Z" fill="{accent}"></path>')
        r += 1
    return f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" aria-hidden="true" style="display: block">{"".join(e)}</svg>'

# ---------------------------------------------------------------- page shell
def page(title, body):
    props = {"$preview": {"width": W, "height": H}}
    return f'''<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<title>{title}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
{FONTS}
<style>
body{{margin:0}}
a{{color:#8F3A26}}a:hover{{color:#5E2513}}
</style>
</helmet>
{body}
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{json.dumps(props)}'>
class Component extends DCLogic {{
renderVals() {{
return {{}};
}}
}}
</script>
</body>
</html>
'''

def header(num, title, sub="", dark=False):
    c = CREAM if dark else ESP
    k = BUTTER if dark else TERRA
    s = f'<div style="{SANS}; font-size: 17px; line-height: 1.55; color: {c}; opacity: 0.85; max-width: 760px">{sub}</div>' if sub else ""
    return (f'<div style="display: flex; justify-content: space-between; align-items: flex-end; gap: 32px">'
            f'<div style="display: flex; flex-direction: column; gap: 6px">'
            f'<div style="{SANS}; font-size: 14px; font-weight: 700; letter-spacing: 0.2em; color: {k}">{num}</div>'
            f'<h2 style="margin: 0; {DISPLAY}; font-weight: 800; font-size: 56px; line-height: 1; color: {c}">{title}</h2>{s}</div>'
            f'{symbol(54, body=TERRA if not dark else BUTTER, ink=c if not dark else ESP, white=CREAM)}</div>')

def board(inner, bg=CREAM, pad=64, gap=36):
    return (f'<div style="width: {W}px; height: {H}px; box-sizing: border-box; background: {bg}; padding: {pad}px 72px; '
            f'display: flex; flex-direction: column; gap: {gap}px; overflow: hidden">{inner}</div>')

def tile(content, bg, h=None, pad=28, extra=""):
    hh = f"height: {h}px; " if h else ""
    return (f'<div style="background: {bg}; border-radius: 22px; padding: {pad}px; box-sizing: border-box; {hh}'
            f'display: flex; align-items: center; justify-content: center; position: relative; {extra}">{content}</div>')

def cap(t, c=ESP):
    return f'<div style="{SANS}; font-size: 14px; font-weight: 600; color: {c}; position: absolute; left: 20px; top: 16px; opacity: 0.8">{t}</div>'

files = {}

# ================================================================ 01 Cover
cover = f'''<div style="width: {W}px; height: {H}px; box-sizing: border-box; background: {CREAM}; position: relative; overflow: hidden">
<div style="position: absolute; right: -60px; top: 0; width: 760px; height: {H}px; background: {TERRA}; border-radius: 0 0 0 380px"></div>
<div style="position: absolute; left: 80px; top: 72px; {SANS}; font-size: 15px; font-weight: 700; letter-spacing: 0.24em; color: {TERRA}">BỘ NHẬN DIỆN THƯƠNG HIỆU · 2026</div>
<div style="position: absolute; left: 80px; top: 230px; display: flex; flex-direction: column; gap: 28px">
{lockup(170, 150, gap=24)}
<div style="{HAND}; font-size: 42px; color: {TERRA}; line-height: 1.2">Ghé vào. Ngồi xuống. Có em lo.</div>
<div style="{SANS}; font-size: 18px; line-height: 1.6; color: {ESP}; max-width: 620px">Xo em là chỗ quen để ghé: ghế mềm, cà phê pha chậm, và luôn có các em Boss, Em Ngả, Em Ngơ lo cho bạn từ ly đầu tiên tới lúc về. Bộ nhận diện này kể đúng cảm giác đó: thân như người nhà, hơi ngố, và lúc nào cũng có em lo.</div>
</div>
<div style="position: absolute; left: 80px; bottom: 64px; {SANS}; font-size: 15px; color: {ESP}; opacity: 0.75">93 Marina, Ecopark · Văn Giang, Hưng Yên · Mở cửa 07:00–23:00</div>
<div style="position: absolute; right: 96px; top: 150px">{ngo(300)}</div>
<div style="position: absolute; right: 290px; top: 560px">{nga(420)}</div>
</div>'''
files["Main.dc.html"] = page("Xo em – Bìa bộ nhận diện", cover)

# ================================================================ 02 Logo
logo_inner = header("01 — LOGO", "Chiếc ghế cũng là chiếc cốc",
                    "Biểu tượng là một chiếc sofa nhìn chính diện, đặt trên đĩa lót nên đồng thời là một ly cà phê. Hai con mắt lệch to nhỏ là Em Ngơ đang nhìn bạn; hai làn khói trên lưng ghế là hơi cà phê nóng.")
logo_grid = f'''<div style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); grid-template-rows: 300px 300px; gap: 20px; flex-grow: 1">
<div style="grid-column: span 2; display: flex">{tile(cap("Logo chính · ngang") + lockup(150, 120), "#FFFFFF", extra="flex-grow: 1; border: 2px solid " + SAND)}</div>
{tile(cap("Logo dọc", CREAM) + stacked(120, 64, body=BUTTER, ink=ESP, white=CREAM, tag=False), TERRA)}
{tile(cap("Biểu tượng · nền tối", CREAM) + symbol(170, body=TERRA, ink=CREAM, white=ESP), ESP)}
{tile(cap("Biểu tượng · nền rêu", CREAM) + symbol(170, body=BUTTER, ink=ESP, white=CREAM), MOSS)}
<div style="display: grid; grid-template-rows: repeat(2, minmax(0, 1fr)); gap: 20px">
{tile(cap("Chữ logo") + wordmark(84, ESP), BUTTER)}
<div style="background: #FFFFFF; border: 2px solid {SAND}; border-radius: 22px; padding: 18px 22px; box-sizing: border-box; display: flex; gap: 18px; align-items: center">
<div style="position: relative; width: 104px; height: 104px; border: 2px dashed {TERRA}; box-sizing: border-box; display: flex; align-items: center; justify-content: center; flex-shrink: 0">{symbol(70)}</div>
<div style="{SANS}; font-size: 13px; line-height: 1.5; color: {ESP}"><strong>Khoảng trống quanh logo</strong> tối thiểu bằng ¼ chiều cao biểu tượng.<br>Cỡ nhỏ nhất: biểu tượng 12mm khi in, 32px trên màn hình.</div>
</div>
</div>
</div>'''
files["Logo.dc.html"] = page("Xo em – Logo", board(logo_inner + logo_grid))

# ================================================================ 03 Color + type
def cmyk(hexc):
    r, g, b = [int(hexc[i:i+2], 16) / 255 for i in (1, 3, 5)]
    k = 1 - max(r, g, b)
    if k >= 1: return "0 0 0 100"
    c = (1 - r - k) / (1 - k); m = (1 - g - k) / (1 - k); y = (1 - b - k) / (1 - k)
    return " ".join(str(round(v * 100)) for v in (c, m, y, k))

colors = [(TERRA, "Đất Nung", "Màu chính · logo, biển hiệu", CREAM),
          (CREAM, "Kem Sữa", "Màu nền · giấy, tường", ESP),
          (ESP, "Nâu Cà Phê", "Chữ · đường viền", CREAM),
          (BUTTER, "Vàng Bơ", "Điểm nhấn vui · nhà Em Ngả", ESP),
          (MOSS, "Rêu Sồi", "Dòng trà &amp; cây · nhà Em Ngơ", CREAM),
          (SAND, "Cát Mịn", "Màu phụ · bụng linh vật, bao bì", ESP)]
sw = ""
for i, (c, n, role, tc) in enumerate(colors):
    big = i < 3
    sw += (f'<div style="background: {c}; border-radius: 20px; padding: 20px 22px; box-sizing: border-box; display: flex; flex-direction: column; '
           f'justify-content: flex-end; gap: 4px; {"border: 2px solid " + SAND + ";" if c == CREAM else ""} grid-column: span {2 if big else 2}">'
           f'<div style="{DISPLAY}; font-weight: 800; font-size: 30px; color: {tc}; line-height: 1">{n}</div>'
           f'<div style="{SANS}; font-size: 13px; color: {tc}; line-height: 1.5">{role}<br>{c} · CMYK {cmyk(c)}</div></div>')
type_col = f'''<div style="display: flex; flex-direction: column; gap: 16px">
<div style="background: #FFFFFF; border: 2px solid {SAND}; border-radius: 20px; padding: 22px 26px; display: flex; flex-direction: column; gap: 4px">
<div style="{SANS}; font-size: 13px; font-weight: 700; letter-spacing: 0.16em; color: {TERRA}">TIÊU ĐỀ · BALOO 2 EXTRABOLD</div>
<div style="{DISPLAY}; font-weight: 800; font-size: 52px; line-height: 1.05; color: {ESP}">Ngồi xuống, có em lo</div>
<div style="{SANS}; font-size: 13px; color: #5A4A3F">Tròn, mập, đủ dấu tiếng Việt. Dùng cho tên món, khẩu hiệu, tiêu đề.</div>
</div>
<div style="background: #FFFFFF; border: 2px solid {SAND}; border-radius: 20px; padding: 22px 26px; display: flex; flex-direction: column; gap: 6px">
<div style="{SANS}; font-size: 13px; font-weight: 700; letter-spacing: 0.16em; color: {TERRA}">NỘI DUNG · BE VIETNAM PRO</div>
<div style="{SANS}; font-size: 18px; line-height: 1.55; color: {ESP}">Cà phê phin pha chậm, sữa đặc vừa đủ ngọt, đá viên to để tan từ từ. Dùng cho mô tả món, giá, thông báo, bài đăng.</div>
</div>
<div style="background: #FFFFFF; border: 2px solid {SAND}; border-radius: 20px; padding: 22px 26px; display: flex; flex-direction: column; gap: 4px">
<div style="{SANS}; font-size: 13px; font-weight: 700; letter-spacing: 0.16em; color: {TERRA}">CHỮ VIẾT TAY · PATRICK HAND</div>
<div style="{HAND}; font-size: 36px; line-height: 1.15; color: {TERRA}">psst… ly này Em Ngơ pha đấy</div>
<div style="{SANS}; font-size: 13px; color: #5A4A3F">Chỉ dùng cho lời nhắn nhỏ, sticker, ghi chú trên ly. Không dùng cho giá tiền.</div>
</div>
</div>'''
ct_inner = header("02 — MÀU &amp; CHỮ", "Ấm như ghế, ngọt như sữa") + f'''<div style="display: grid; grid-template-columns: minmax(0, 1.15fr) minmax(0, 1fr); gap: 28px; flex-grow: 1">
<div style="display: grid; grid-template-columns: repeat(6, minmax(0, 1fr)); grid-template-rows: 1.3fr 1fr; gap: 14px">{sw}</div>
{type_col}
</div>
<div style="{SANS}; font-size: 14px; color: #5A4A3F">Tỉ lệ dùng màu gợi ý: Kem Sữa 60% · Đất Nung 20% · Nâu Cà Phê 10% · Vàng Bơ, Rêu Sồi, Cát Mịn 10%. Mã CMYK là quy đổi tham khảo, cần in thử để chốt màu.</div>'''
files["ColorType.dc.html"] = page("Xo em – Màu và chữ", board(ct_inner, gap=28))

# ================================================================ 04 Mascots
def profile(rows):
    return "".join(f'<div style="display: flex; gap: 14px; padding: 9px 0; border-top: 1.5px solid {SAND}">'
                   f'<div style="{SANS}; font-size: 13px; font-weight: 700; letter-spacing: 0.1em; color: {TERRA}; width: 104px; flex-shrink: 0">{k}</div>'
                   f'<div style="{SANS}; font-size: 13px; line-height: 1.45; color: {ESP}">{v}</div></div>' for k, v in rows)
nga_rows = [("LOÀI", "Rồng nệm. Sống trên chiếc sofa đỏ đất nung của quán."),
            ("NGOẠI HÌNH", "Vàng bơ, bụng cát mịn có đường khâu, sừng mềm, luôn nhắm mắt."),
            ("TÍNH CÁCH", "Chậm, mềm, chẳng vội gì. Ngủ là chuyên môn chính."),
            ("CÂU CỬA MIỆNG", "“Năm phút nữa thôi…”"),
            ("DÙNG CHO", "Cà phê, bánh, góc ghế sofa, khung giờ chiều")]
ngo_rows = [("LOÀI", "Rồng rêu. Mọc ra từ chậu cây cạnh quầy pha."),
            ("NGOẠI HÌNH", "Xanh rêu, mắt lệch một to một nhỏ, lè lưỡi, một cái răng, ly cà phê mắc trên sừng mà không biết."),
            ("TÍNH CÁCH", "Nhiệt tình, hay quên, không bao giờ cáu."),
            ("CÂU CỬA MIỆNG", "“Ơ… mình vừa định làm gì nhỉ?”"),
            ("DÙNG CHO", "Trà, đồ uống từ cây, sticker, mạng xã hội")]
boss_rows = [("LOÀI", "Chiếc sofa biết nói. Chiếc ghế đầu tiên của quán, cũng chính là biểu tượng trên logo."),
            ("NGOẠI HÌNH", "Thân Đất Nung, hai mắt lệch to nhỏ, miệng cười mỉm, ngồi trên đĩa lót, trên đầu lúc nào cũng bốc khói cà phê."),
            ("TÍNH CÁCH", "Ra vẻ nghiêm nhưng mềm nhất quán. Ai ngồi lên là bị giữ chân, không muốn về."),
            ("CÂU CỬA MIỆNG", "“Ngồi đi, vội gì.”"),
            ("VỚI Em Ngả &amp; Em Ngơ", "Em Ngả ngủ trên lưng Boss, Em Ngơ thì hay quên Boss là sếp.")]
def mcard(img, name, color, rows):
    return (f'<div style="background: #FFFFFF; border: 2px solid {SAND}; border-radius: 24px; padding: 22px 24px; display: flex; flex-direction: column; gap: 10px">'
            f'<div style="height: 250px; display: flex; align-items: flex-end; justify-content: center">{img}</div>'
            f'<div style="{DISPLAY}; font-weight: 800; font-size: 42px; color: {color}; line-height: 1; text-align: center">{name}</div>'
            f'<div style="display: flex; flex-direction: column">{profile(rows)}</div></div>')
masc_inner = header("03 — LINH VẬT", "Em Ngả, Em Ngơ &amp; Boss", "Boss giữ ghế, Em Ngả ngủ, Em Ngơ canh nhưng canh được năm phút là ngủ theo. Ba em nhà Xo em, lúc nào cũng sẵn sàng lo cho khách.") + f'''<div style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 24px; flex-grow: 1">
{mcard(boss(220), "Boss", ESP, boss_rows)}{mcard(nga(300), "Em Ngả", TERRA, nga_rows)}{mcard(ngo(215), "Em Ngơ", MOSS, ngo_rows)}
</div>'''
files["Mascots.dc.html"] = page("Xo em – Linh vật", board(masc_inner))

# ================================================================ 05 Pattern + voice
def sticker(text, bg, fg, size=170, font=30):
    return (f'<div style="width: {size}px; height: {size}px; border-radius: 50%; background: {bg}; border: 4px solid {ESP}; box-sizing: border-box; '
            f'display: flex; align-items: center; justify-content: center; text-align: center; padding: 18px; transform: rotate(-6deg); '
            f'{HAND}; font-size: {font}px; line-height: 1.05; color: {fg}">{text}</div>')
voice = [("“Vui lòng chờ trong giây lát.”", "“Đợi xíu nha, Em Ngơ đang pha.”"),
         ("“Món này đã hết.”", "“Món này Em Ngả ngủ quên, chưa kịp làm. Thử ly khác nha?”"),
         ("“Cảm ơn quý khách.”", "“Cảm ơn bạn đã ghé Xo em. Mai lại ghé nhé!”"),
         ("“Khu vực không hút thuốc.”", "“Ở đây chỉ có khói cà phê thôi.”"),
         ("“Wi‑Fi miễn phí.”", "“Wi‑Fi mạnh, ghế mềm, cứ ngồi lâu, có em lo.”"),
         ("“Quý khách vui lòng tự dọn bàn.”", "“Giúp Em Ngơ dọn ly nha, Em Ngơ hay quên lắm.”")]
vrows = "".join(f'<div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px; padding: 15px 0; border-top: 1.5px solid {SAND}">'
                f'<div style="{SANS}; font-size: 17px; color: #7A6A5F; text-decoration: line-through">{a}</div>'
                f'<div style="{SANS}; font-size: 17px; font-weight: 600; color: {ESP}">{b}</div></div>' for a, b in voice)
pv_inner = header("04 — HỌA TIẾT &amp; GIỌNG NÓI", "Mềm, ngố, chậm rãi") + f'''<div style="display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: 28px; flex-grow: 1">
<div style="display: flex; flex-direction: column; gap: 18px">
<div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px; height: 330px">
<div style="border-radius: 22px; overflow: hidden">{pattern_svg(330, 330, TERRA, BUTTER, ESP, CREAM, CREAM)}</div>
<div style="border-radius: 22px; overflow: hidden">{pattern_svg(330, 330, MOSS, SAND, ESP, CREAM, BUTTER)}</div>
</div>
<div style="display: flex; gap: 20px; align-items: center; justify-content: space-between">
{sticker("có em<br>lo", BUTTER, ESP)}{sticker("đang ngả,<br>đừng gọi", TERRA, CREAM, 160, 27)}{sticker("slow<br>coffee", CREAM, TERRA, 150, 32)}{sticker("ơ?", MOSS, CREAM, 130, 48)}
</div>
<div style="{SANS}; font-size: 14px; line-height: 1.5; color: #5A4A3F">Họa tiết dùng cho giấy gói, ly, túi, tường điểm nhấn. Sticker dán ly, laptop, cửa kính.</div>
</div>
<div style="background: #FFFFFF; border: 2px solid {SAND}; border-radius: 24px; padding: 28px 32px; display: flex; flex-direction: column; gap: 8px">
<div style="{DISPLAY}; font-weight: 800; font-size: 32px; color: {ESP}; line-height: 1.1">Nói như một người bạn hơi lơ đãng</div>
<div style="{SANS}; font-size: 15px; line-height: 1.6; color: {ESP}; margin-bottom: 10px">Quán xưng “em”, gọi khách là “bạn”. Câu ngắn, thân, có chút đùa nhưng không mỉa mai. Được phép lôi Em Ngả và Em Ngơ vào câu chuyện. Không dùng giọng thông báo cứng nhắc.</div>
<div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px; {SANS}; font-size: 12px; font-weight: 700; letter-spacing: 0.14em; color: {TERRA}"><div>THAY VÌ</div><div>XO EM NÓI</div></div>
{vrows}
</div>
</div>'''
files["PatternVoice.dc.html"] = page("Xo em – Họa tiết và giọng nói", board(pv_inner))

# ================================================================ 06 Signage + menu
def awning(w, n=12):
    seg = w / n
    s = ""
    for i in range(n):
        c = TERRA if i % 2 == 0 else CREAM
        x = i * seg
        s += f'<path d="M{x:.1f},0 L{x+seg:.1f},0 L{x+seg:.1f},56 Q{x+seg/2:.1f},86 {x:.1f},56 Z" fill="{c}" stroke="{ESP}" stroke-width="3"></path>'
    return f'<svg width="{w}" height="90" viewBox="0 0 {w} 90" aria-hidden="true" style="display: block">{s}</svg>'

storefront = f'''<div style="position: relative; width: 880px; height: 680px; background: #E9DDC7; border-radius: 24px; overflow: hidden">
<div style="position: absolute; left: 70px; top: 50px; width: 740px; height: 590px; background: {CREAM}; border: 4px solid {ESP}; box-sizing: border-box"></div>
<div style="position: absolute; left: 140px; top: 78px; width: 600px; height: 118px; background: {ESP}; border-radius: 18px; display: flex; align-items: center; justify-content: center">{lockup(84, 66, body=TERRA, ink=CREAM, white=ESP, tagcolor=BUTTER, gap=14)}</div>
<div style="position: absolute; left: 66px; top: 218px">{awning(748)}</div>
<div style="position: absolute; left: 110px; top: 318px; width: 400px; height: 280px; background: #3B2D24; border: 6px solid {ESP}; box-sizing: border-box; border-radius: 6px; overflow: hidden">
<div style="position: absolute; left: 30px; bottom: 0">{nga(250)}</div>
<div style="position: absolute; right: 18px; top: 18px; {HAND}; font-size: 26px; color: {BUTTER}; transform: rotate(-4deg)">còn ghế cho bạn nè!</div>
</div>
<div style="position: absolute; left: 560px; top: 318px; width: 200px; height: 322px; background: {TERRA}; border: 6px solid {ESP}; box-sizing: border-box; border-radius: 100px 100px 0 0; display: flex; align-items: center; justify-content: center">
<div style="width: 120px; height: 120px; border-radius: 50%; background: {CREAM}; border: 4px solid {ESP}; display: flex; align-items: center; justify-content: center">{symbol(88)}</div>
</div>
<div style="position: absolute; left: 0; bottom: 0; width: 880px; height: 40px; background: #B9A88E"></div>
<div style="position: absolute; left: 20px; bottom: 30px">{ngo(110)}</div>
</div>'''
menu_items = [("CÀ PHÊ PHA CHẬM", TERRA, ["Cà phê phin đen", "Cà phê phin sữa", "Bạc xỉu", "Cà phê muối"]),
              ("TRÀ &amp; CÂY · NHÀ NGƠ", MOSS, ["Trà đào cam sả", "Trà sen vàng", "Matcha sữa"]),
              ("BÁNH · NHÀ NGẢ", "#A8741A", ["Bánh chuối nướng", "Croissant bơ"])]
mrows = ""
for sec, c, items in menu_items:
    mrows += f'<div style="{SANS}; font-size: 13px; font-weight: 700; letter-spacing: 0.16em; color: {c}; margin-top: 10px">{sec}</div>'
    for it in items:
        mrows += (f'<div style="display: flex; justify-content: space-between; align-items: baseline; gap: 10px; {SANS}; font-size: 16px; color: {ESP}; '
                  f'border-bottom: 1.5px dotted {SAND}; padding: 5px 0"><span>{it}</span><span style="font-weight: 600">[GIÁ]</span></div>')
menu = f'''<div style="width: 500px; height: 680px; background: #FFFFFF; border: 4px solid {ESP}; border-radius: 24px; box-sizing: border-box; padding: 30px 36px; display: flex; flex-direction: column; gap: 4px; position: relative; overflow: hidden">
<div style="display: flex; justify-content: space-between; align-items: center">{lockup(64, 44, tag=False, gap=10)}<div style="{HAND}; font-size: 24px; color: {TERRA}; transform: rotate(-4deg)">menu chậm</div></div>
{mrows}
<div style="position: absolute; right: 18px; bottom: 10px">{ngo(96)}</div>
<div style="position: absolute; left: 36px; bottom: 26px; {SANS}; font-size: 12px; color: #6A5A4F; width: 300px">Tên món minh họa. Điền món và giá thật trước khi in.</div>
</div>'''
sm_inner = header("05 — BIỂN HIỆU &amp; MENU", "Mặt tiền nhìn là muốn ngồi") + f'''<div style="display: flex; gap: 32px; align-items: flex-start">{storefront}{menu}</div>'''
files["Signage.dc.html"] = page("Xo em – Biển hiệu và menu", board(sm_inner, gap=28))

# ================================================================ 07 Packaging
def hot_cup(w=250, h=340):
    band = f'''<div style="position: absolute; left: 0; bottom: 0; width: 100%; height: 34%; background: {TERRA}"></div>
<div style="position: absolute; left: 0; bottom: 34%; width: 100%; height: 6px; background: {ESP}"></div>'''
    return f'''<div style="display: flex; flex-direction: column; align-items: center">
<div style="width: {w+30}px; height: 30px; background: {ESP}; border-radius: 40px 40px 8px 8px"></div>
<div style="width: {w+12}px; height: 12px; background: {CREAM}; border: 3px solid {ESP}; border-radius: 6px; box-sizing: border-box; margin-top: -2px"></div>
<div style="width: {w}px; height: {h}px; position: relative; overflow: hidden; background: {CREAM}; clip-path: polygon(0 0, 100% 0, 88% 100%, 12% 100%)">
{band}
<div style="position: absolute; left: 0; right: 0; top: 34px; display: flex; flex-direction: column; align-items: center; gap: 4px">{symbol(110)}{wordmark(40)}</div>
<div style="position: absolute; left: 0; right: 0; bottom: 30px; text-align: center; {HAND}; font-size: 22px; color: {CREAM}">có em lo</div>
<div style="position: absolute; inset: 0; background: linear-gradient(90deg, rgba(0,0,0,0.22), rgba(255,255,255,0.12) 40%, rgba(0,0,0,0.04) 60%, rgba(0,0,0,0.25))"></div>
</div></div>'''

def cold_cup(w=240, h=370):
    return f'''<div style="display: flex; flex-direction: column; align-items: center">
<div style="width: 10px; height: 60px; background: {MOSS}; margin-bottom: -10px; transform: rotate(10deg)"></div>
<div style="width: {w+26}px; height: 26px; background: rgba(255,255,255,0.8); border: 3px solid {ESP}; border-radius: 60px 60px 6px 6px; box-sizing: border-box"></div>
<div style="width: {w}px; height: {h}px; position: relative; overflow: hidden; clip-path: polygon(0 0, 100% 0, 88% 100%, 12% 100%); background: rgba(255,255,255,0.55)">
<div style="position: absolute; left: 0; right: 0; bottom: 0; height: 78%; background: linear-gradient(180deg, #C9A27A 0%, #8A5A36 45%, #5A3620 100%)"></div>
<div style="position: absolute; left: 50%; top: 40%; transform: translate(-50%, -50%); width: 130px; height: 130px; border-radius: 50%; background: {BUTTER}; border: 4px solid {ESP}; display: flex; align-items: center; justify-content: center">{symbol(92)}</div>
<div style="position: absolute; left: 0; right: 0; bottom: 26px; text-align: center; {HAND}; font-size: 22px; color: {CREAM}">đá to · tan chậm</div>
</div></div>'''

bag = f'''<div style="width: 300px; height: 380px; position: relative">
<svg width="300" height="80" viewBox="0 0 300 80" aria-hidden="true" style="display: block; position: absolute; top: 0; left: 0"><path d="M90,80 Q90,10 150,10 Q210,10 210,80" fill="none" stroke="{ESP}" stroke-width="10"></path></svg>
<div style="position: absolute; top: 60px; left: 0; width: 300px; height: 320px; background: {KRAFT}; border: 4px solid {ESP}; box-sizing: border-box; border-radius: 6px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 8px">
{symbol(130, body=CREAM, ink=ESP, white=CREAM)}{wordmark(48)}
<div style="{SANS}; font-weight: 600; font-size: 11px; letter-spacing: 0.2em; color: {ESP}">SLOW COFFEE · COMFY SEATS</div>
</div></div>'''

pk_inner = header("06 — BAO BÌ", "Mang em về nhà") + f'''<div style="display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 24px; flex-grow: 1; align-items: center">
<div style="display: flex; flex-direction: column; align-items: center; gap: 14px">{hot_cup()}<div style="{SANS}; font-size: 15px; font-weight: 600; color: {ESP}">Ly giấy nóng</div></div>
<div style="display: flex; flex-direction: column; align-items: center; gap: 14px">{cold_cup()}<div style="{SANS}; font-size: 15px; font-weight: 600; color: {ESP}">Ly nhựa đá + tem tròn</div></div>
<div style="display: flex; flex-direction: column; align-items: center; gap: 14px">{bag}<div style="{SANS}; font-size: 15px; font-weight: 600; color: {ESP}">Túi giấy kraft</div></div>
<div style="display: flex; flex-direction: column; align-items: center; gap: 18px">
<div style="width: 250px; height: 160px; border-radius: 16px; overflow: hidden; border: 4px solid {ESP}; box-sizing: border-box">{pattern_svg(250, 160, TERRA, BUTTER, ESP, CREAM, CREAM, 0.8)}</div>
<div style="{SANS}; font-size: 15px; font-weight: 600; color: {ESP}">Giấy gói bánh</div>
<div style="width: 220px; height: 120px; background: {CREAM}; border: 4px solid {ESP}; border-radius: 14px; box-sizing: border-box; display: flex; align-items: center; gap: 12px; padding: 0 16px">{symbol(64)}<div style="{HAND}; font-size: 22px; line-height: 1.1; color: {ESP}">Em Ngơ đã kiểm tra:<br><span style="color: {TERRA}">ngon ✓</span></div></div>
<div style="{SANS}; font-size: 15px; font-weight: 600; color: {ESP}">Tem niêm phong</div>
</div>
</div>'''
files["Packaging.dc.html"] = page("Xo em – Bao bì", board(pk_inner))

# ================================================================ 08 Staff + stationery
apron = f'''<div style="width: 320px; height: 520px; position: relative">
<svg width="320" height="520" viewBox="0 0 320 520" aria-hidden="true" style="display: block; position: absolute; inset: 0">
<path d="M110,8 Q160,-6 210,8" fill="none" stroke="{SAND}" stroke-width="10"></path>
<path d="M100,10 L220,10 L224,150 Q226,170 250,176 L292,176 L300,500 Q300,516 284,516 L36,516 Q20,516 20,500 L28,176 L70,176 Q94,170 96,150 Z" fill="{ESP}"></path>
<path d="M28,180 L-10,186 M292,180 L330,186" stroke="{SAND}" stroke-width="10"></path>
<rect x="70" y="350" width="180" height="110" rx="10" fill="none" stroke="{TERRA}" stroke-width="4" stroke-dasharray="10 8"></rect>
</svg>
<div style="position: absolute; left: 0; right: 0; top: 190px; display: flex; flex-direction: column; align-items: center; gap: 2px">{symbol(110, body=TERRA, ink=CREAM, white=ESP)}{wordmark(46, CREAM)}</div>
<div style="position: absolute; left: 70px; top: 380px; width: 180px; text-align: center; {HAND}; font-size: 28px; color: {BUTTER}">có em lo</div>
</div>'''
nametag = f'''<div style="width: 260px; height: 110px; background: {CREAM}; border: 4px solid {ESP}; border-radius: 16px; box-sizing: border-box; display: flex; align-items: center; gap: 14px; padding: 0 18px">
{symbol(64)}<div style="display: flex; flex-direction: column"><div style="{SANS}; font-size: 11px; font-weight: 700; letter-spacing: 0.16em; color: {TERRA}">HÔM NAY AI PHA?</div><div style="{DISPLAY}; font-weight: 800; font-size: 34px; color: {ESP}; line-height: 1.1">Tên bạn</div></div></div>'''
card_front = f'''<div style="width: 340px; height: 200px; background: {TERRA}; border-radius: 14px; display: flex; align-items: center; justify-content: center; box-shadow: 0 10px 24px rgba(43,29,22,0.18)">{stacked(90, 40, body=BUTTER, ink=ESP, white=CREAM, tag=False)}</div>'''
card_back = f'''<div style="width: 340px; height: 200px; background: {CREAM}; border: 2px solid {SAND}; border-radius: 14px; box-sizing: border-box; padding: 22px 24px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 10px 24px rgba(43,29,22,0.12)">
<div><div style="{DISPLAY}; font-weight: 800; font-size: 26px; color: {ESP}; line-height: 1">Xo em</div><div style="{SANS}; font-size: 11px; font-weight: 600; letter-spacing: 0.18em; color: {TERRA}; margin-top: 4px">SLOW COFFEE · COMFY SEATS</div></div>
<div style="{SANS}; font-size: 12px; line-height: 1.6; color: {ESP}">93 Marina, Ecopark, Văn Giang, Hưng Yên<br>Mở cửa 07:00–23:00 mỗi ngày<br>[SỐ ĐIỆN THOẠI] · [FACEBOOK / TIKTOK]</div>
</div>'''
stamps = ""
for i in range(10):
    last = i == 9
    inner = symbol(40, body=BUTTER) if last else (symbol(34, body=TERRA) if i < 3 else "")
    stamps += (f'<div style="width: 52px; height: 52px; border-radius: 50%; border: 3px {"solid" if last else "dashed"} {ESP}; box-sizing: border-box; '
               f'background: {"#FFFFFF" if last else "transparent"}; display: flex; align-items: center; justify-content: center">{inner}</div>')
loyalty = f'''<div style="width: 420px; height: 240px; background: {SAND}; border-radius: 16px; box-sizing: border-box; padding: 20px 24px; display: flex; flex-direction: column; gap: 12px; box-shadow: 0 10px 24px rgba(43,29,22,0.12)">
<div style="display: flex; justify-content: space-between; align-items: center"><div style="{DISPLAY}; font-weight: 800; font-size: 26px; color: {ESP}; line-height: 1">Thẻ thân với em</div>{symbol(40)}</div>
<div style="display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 10px; justify-items: center">{stamps}</div>
<div style="{HAND}; font-size: 22px; color: {TERRA}">đủ 9 ly, ly thứ 10 Em Ngơ mời!</div>
</div>'''
st_inner = header("07 — ĐỒNG PHỤC &amp; ẤN PHẨM", "Các em pha cho bạn") + f'''<div style="display: flex; gap: 48px; flex-grow: 1; align-items: center">
<div style="display: flex; flex-direction: column; align-items: center; gap: 20px">{apron}{nametag}</div>
<div style="display: flex; flex-direction: column; gap: 30px; flex-grow: 1">
<div style="{SANS}; font-size: 14px; font-weight: 700; letter-spacing: 0.16em; color: {TERRA}">DANH THIẾP · MẶT TRƯỚC / MẶT SAU</div>
<div style="display: flex; gap: 28px">{card_front}{card_back}</div>
<div style="{SANS}; font-size: 14px; font-weight: 700; letter-spacing: 0.16em; color: {TERRA}; margin-top: 10px">THẺ TÍCH ĐIỂM</div>
<div style="display: flex; gap: 28px; align-items: center">{loyalty}<div style="{SANS}; font-size: 15px; line-height: 1.6; color: {ESP}; max-width: 300px">Mỗi ly đóng một dấu biểu tượng. Ô thứ 10 là quà. Tạp dề màu Nâu Cà Phê, chữ và logo in Kem Sữa, túi trước viền chỉ Đất Nung.</div></div>
</div>
</div>'''
files["Stationery.dc.html"] = page("Xo em – Đồng phục và ấn phẩm", board(st_inner))

# ================================================================ 09 Social
def post(bg, content, label):
    return (f'<div style="display: flex; flex-direction: column; gap: 10px; align-items: center">'
            f'<div style="width: 330px; height: 330px; background: {bg}; border-radius: 18px; position: relative; overflow: hidden; box-shadow: 0 10px 24px rgba(43,29,22,0.15)">{content}</div>'
            f'<div style="{SANS}; font-size: 14px; font-weight: 600; color: {ESP}">{label}</div></div>')
p1 = post(BUTTER, f'''<div style="position: absolute; left: 26px; top: 24px; {DISPLAY}; font-weight: 800; font-size: 46px; line-height: 1; color: {ESP}">Hôm nay<br>ghé em<br>chưa?</div>
<div style="position: absolute; right: -10px; bottom: -14px">{ngo(190)}</div>
<div style="position: absolute; left: 26px; bottom: 22px">{symbol(44)}</div>''', "Bài đăng tương tác")
p2 = post(TERRA, f'''<div style="position: absolute; left: 26px; top: 24px; {SANS}; font-size: 13px; font-weight: 700; letter-spacing: 0.18em; color: {BUTTER}">MÓN MỚI</div>
<div style="position: absolute; left: 26px; top: 48px; {DISPLAY}; font-weight: 800; font-size: 44px; line-height: 1; color: {CREAM}">[Tên món]</div>
<div style="position: absolute; left: 50%; top: 58%; transform: translate(-50%, -50%); width: 170px; height: 170px; border-radius: 50%; background: {CREAM}; border: 4px solid {ESP}; display: flex; align-items: center; justify-content: center; {SANS}; font-size: 14px; color: #6A5A4F; text-align: center">[ẢNH MÓN]</div>
<div style="position: absolute; right: 22px; bottom: 18px; {HAND}; font-size: 24px; color: {CREAM}">Em Ngả thử rồi, ngon!</div>''', "Mẫu giới thiệu món")
p3 = post(ESP, f'''<div style="position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 8px">
{symbol(110, body=TERRA, ink=CREAM, white=ESP)}<div style="{DISPLAY}; font-weight: 800; font-size: 54px; color: {CREAM}; line-height: 1">07:00–23:00</div>
<div style="{HAND}; font-size: 26px; color: {BUTTER}">các em chờ bạn cả ngày</div></div>''', "Thông báo giờ mở cửa")
avatar = f'''<div style="display: flex; flex-direction: column; align-items: center; gap: 10px"><div style="width: 200px; height: 200px; border-radius: 50%; background: {TERRA}; display: flex; align-items: center; justify-content: center; box-shadow: 0 10px 24px rgba(43,29,22,0.15)">{symbol(140, body=BUTTER, ink=ESP, white=CREAM)}</div><div style="{SANS}; font-size: 14px; font-weight: 600; color: {ESP}">Ảnh đại diện</div></div>'''
cover_banner = f'''<div style="display: flex; flex-direction: column; gap: 10px"><div style="width: 820px; height: 312px; border-radius: 18px; overflow: hidden; position: relative; box-shadow: 0 10px 24px rgba(43,29,22,0.15)">
{pattern_svg(820, 312, CREAM, TERRA, ESP, CREAM, SAND, 0.9)}
<div style="position: absolute; left: 40px; top: 50%; transform: translateY(-50%); background: {CREAM}; border: 4px solid {ESP}; border-radius: 20px; padding: 18px 26px">{lockup(90, 70, gap=14)}</div>
<div style="position: absolute; right: 30px; bottom: -6px">{nga(250)}</div>
</div><div style="{SANS}; font-size: 14px; font-weight: 600; color: {ESP}">Ảnh bìa Facebook (820 × 312)</div></div>'''
so_inner = header("08 — MẠNG XÃ HỘI", "Lướt cũng thấy nhớ em") + f'''<div style="display: flex; gap: 40px; align-items: flex-end">{cover_banner}{avatar}</div>
<div style="display: flex; gap: 36px">{p1}{p2}{p3}</div>'''
files["Social.dc.html"] = page("Xo em – Mạng xã hội", board(so_inner, gap=30))

# ---------------------------------------------------------------- write + canvas
order = ["Main.dc.html", "Logo.dc.html", "ColorType.dc.html", "Mascots.dc.html", "PatternVoice.dc.html",
         "Signage.dc.html", "Packaging.dc.html", "Stationery.dc.html", "Social.dc.html"]
titles = ["Bìa", "01 Logo", "02 Màu & chữ", "03 Linh vật Em Ngả & Em Ngơ", "04 Họa tiết & giọng nói",
          "05 Biển hiệu & menu", "06 Bao bì", "07 Đồng phục & ấn phẩm", "08 Mạng xã hội"]
boards = {}
for i, (f, t) in enumerate(zip(order, titles)):
    col, row = i % 3, i // 3
    boards[f] = {"x": col * (W + 80), "y": row * (H + 120), "w": W, "h": H, "title": t}
canvas = {"v": 3, "createdOnFiles": {"v": 1, "at": "2026-11-25T07:05:00Z"}, "title": "Xo em – Bộ nhận diện thương hiệu",
          "launch": {"view": "canvas"}, "pages": [], "boards": boards, "order": order, "notes": {}, "designSystems": []}
for k, v in files.items():
    open(os.path.join(ROOT, k), "w").write(v)
json.dump(canvas, open(os.path.join(ROOT, "canvas.json"), "w"), ensure_ascii=False)
json.dump(order, open("/home/claude/xoem-brand/order.json", "w"))
for k in order:
    print(k, os.path.getsize(os.path.join(ROOT, k)))
