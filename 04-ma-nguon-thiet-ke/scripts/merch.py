"""Merch pages for Xô Ngơ / Xo em. Usage: python3 merch.py ngo|em"""
import sys, os, json, importlib, io, contextlib
which = sys.argv[1]
sys.path.insert(0, "/home/claude")
with contextlib.redirect_stdout(io.StringIO()):
    B = importlib.import_module("brand" if which == "ngo" else "brand_em")
NAME = "Xô Ngơ" if which == "ngo" else "Xo em"
TAG = "ngơ một chút" if which == "ngo" else "có em lo"
POST = "gửi bạn một<br>chút ngơ…" if which == "ngo" else "gửi bạn,<br>từ các em…"
PRICE = "Ngả đã ngủ thử, êm thật!" if which == "ngo" else "Em Ngả ngủ thử rồi, mềm lắm!"
ROOT = B.ROOT
CREAM, ESP, TERRA, MOSS, BUTTER, SAND, KRAFT = B.CREAM, B.ESP, B.TERRA, B.MOSS, B.BUTTER, B.SAND, B.KRAFT
SANS, DISPLAY, HAND = B.SANS, B.DISPLAY, B.HAND
sym, wm, nga, ngo = B.symbol, B.wordmark, B.nga, B.ngo
DEEP = "#9E3F2B"

def cap(t, sub=""):
    s = f'<div style="{SANS}; font-size: 13px; color: #6A5A4F; text-align: center; line-height: 1.4">{sub}</div>' if sub else ""
    return f'<div style="display: flex; flex-direction: column; gap: 2px; align-items: center"><div style="{SANS}; font-size: 15px; font-weight: 700; color: {ESP}; text-align: center">{t}</div>{s}</div>'

def cell(content, t, sub="", span=1):
    return (f'<div style="grid-column: span {span}; background: #FFFFFF; border: 2px solid {SAND}; border-radius: 22px; padding: 20px 16px 16px; '
            f'display: flex; flex-direction: column; align-items: center; justify-content: space-between; gap: 12px; overflow: hidden">'
            f'<div style="flex-grow: 1; display: flex; align-items: center; justify-content: center; gap: 18px">{content}</div>{cap(t, sub)}</div>')

def grid(cells, cols=3):
    return (f'<div style="display: grid; grid-template-columns: repeat({cols}, minmax(0, 1fr)); grid-auto-rows: minmax(0, 1fr); gap: 20px; flex-grow: 1">'
            + "".join(cells) + '</div>')

# ---------------- page 09: sổ & văn phòng phẩm ----------------
notebook = f'''<div style="position: relative; width: 190px; height: 260px; background: {TERRA}; border-radius: 10px 16px 16px 10px; border: 3px solid {ESP}; box-sizing: border-box; box-shadow: 6px 8px 0 rgba(43,29,22,0.15)">
<div style="position: absolute; inset: 10px; border: 2px dashed rgba(246,238,223,0.6); border-radius: 8px"></div>
<div style="position: absolute; left: 50%; top: 62px; transform: translateX(-50%)">{sym(86, body=TERRA, ink=DEEP, white=TERRA)}</div>
<div style="position: absolute; left: 0; right: 0; bottom: 34px; text-align: center; {SANS}; font-size: 11px; font-weight: 700; letter-spacing: 0.2em; color: {BUTTER}">TÊN CỦA BẠN</div>
<div style="position: absolute; right: 22px; top: -3px; bottom: -3px; width: 10px; background: {ESP}"></div>
</div>'''
dots = "".join(f'<circle cx="{x}" cy="{y}" r="1.4" fill="#C9B79A"></circle>' for x in range(14, 160, 14) for y in range(16, 200, 14))
page_svg = f'<svg width="160" height="210" viewBox="0 0 160 210" aria-hidden="true" style="display: block">{dots}</svg>'
spread = f'''<div style="display: flex; border: 3px solid {ESP}; border-radius: 8px; overflow: hidden; box-shadow: 6px 8px 0 rgba(43,29,22,0.12)">
<div style="position: relative; width: 170px; height: 220px; background: {CREAM}; border-right: 2px solid {SAND}">{page_svg}
<div style="position: absolute; left: 14px; top: 16px; {HAND}; font-size: 20px; color: {TERRA}; line-height: 1.1">hôm nay<br>mình ghé {NAME}…</div>
<div style="position: absolute; left: 10px; bottom: 6px">{nga(120)}</div></div>
<div style="position: relative; width: 170px; height: 220px; background: {CREAM}">{page_svg}
<div style="position: absolute; right: 10px; bottom: 8px">{sym(30)}</div></div></div>'''
def pen(color, clip, label_color, w=250):
    return (f'<div style="position: relative; width: {w}px; height: 26px">'
            f'<div style="position: absolute; left: 0; top: 0; width: {w-30}px; height: 26px; background: {color}; border: 3px solid {ESP}; border-radius: 13px 4px 4px 13px; box-sizing: border-box"></div>'
            f'<div style="position: absolute; right: 0; top: 6px; width: 34px; height: 14px; background: {SAND}; border: 3px solid {ESP}; border-radius: 2px 14px 14px 2px; box-sizing: border-box"></div>'
            f'<div style="position: absolute; left: 22px; top: -10px; width: 70px; height: 10px; background: {clip}; border: 3px solid {ESP}; border-bottom: none; border-radius: 6px 6px 0 0; box-sizing: border-box"></div>'
            f'<div style="position: absolute; left: 110px; top: 3px; {DISPLAY}; font-weight: 800; font-size: 15px; color: {label_color}">{NAME.lower()}</div></div>')
pens = f'<div style="display: flex; flex-direction: column; gap: 30px">{pen(TERRA, ESP, CREAM)}{pen(MOSS, BUTTER, CREAM)}{pen(BUTTER, TERRA, ESP, 210)}</div>'
bookmark = (f'<div style="display: flex; gap: 18px; align-items: flex-end">'
            f'<div style="position: relative; width: 70px; height: 230px; background: {MOSS}; border: 3px solid {ESP}; border-radius: 6px; box-sizing: border-box; overflow: hidden">'
            f'<div style="position: absolute; left: -16px; top: -12px">{ngo(100)}</div>'
            f'<div style="position: absolute; bottom: 12px; left: 0; right: 0; text-align: center; {HAND}; font-size: 17px; line-height: 1; color: {CREAM}">đọc<br>chậm<br>thôi</div></div>'
            f'<div style="position: relative; width: 70px; height: 230px; background: {BUTTER}; border: 3px solid {ESP}; border-radius: 6px; box-sizing: border-box; overflow: hidden">'
            f'<div style="position: absolute; left: 4px; bottom: 10px">{sym(56)}</div>'
            f'<div style="position: absolute; top: 12px; left: 0; right: 0; text-align: center; {DISPLAY}; font-weight: 800; font-size: 18px; color: {ESP}; line-height: 1">{NAME.lower().replace(" ", "<br>")}</div></div></div>')
def stk(inner, bg, size=78, rot=-6):
    return (f'<div style="width: {size}px; height: {size}px; border-radius: 50%; background: {bg}; border: 3px solid {ESP}; box-sizing: border-box; '
            f'display: flex; align-items: center; justify-content: center; transform: rotate({rot}deg); text-align: center; {HAND}; font-size: 17px; line-height: 1; color: {ESP}">{inner}</div>')
sticker_sheet = (f'<div style="width: 290px; height: 210px; background: #FFFFFF; border: 2px dashed #C9B79A; border-radius: 12px; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); place-items: center; padding: 8px; box-sizing: border-box">'
                 f'{stk(sym(54), CREAM)}{stk(TAG.replace(" ", "<br>", 1), BUTTER, 82, 5)}{stk("ơ?", MOSS, 70, -10)}'
                 f'{stk("slow<br>coffee", TERRA, 80, 8)}{stk(sym(50, body=BUTTER), TERRA, 74, -4)}{stk("zzz", SAND, 66, 6)}</div>')
postcard = (f'<div style="display: flex; gap: 14px"><div style="width: 200px; height: 140px; border-radius: 10px; overflow: hidden; border: 3px solid {ESP}; position: relative">'
            f'{B.pattern_svg(200, 140, TERRA, BUTTER, ESP, CREAM, CREAM, 0.7)}'
            f'<div style="position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%); background: {CREAM}; border: 3px solid {ESP}; border-radius: 10px; padding: 4px 12px">{wm(28)}</div></div>'
            f'<div style="width: 200px; height: 140px; border-radius: 10px; border: 3px solid {ESP}; background: {CREAM}; box-sizing: border-box; position: relative">'
            f'<div style="position: absolute; left: 14px; top: 12px; {HAND}; font-size: 18px; color: {TERRA}; line-height: 1.2">{POST}</div>'
            f'<div style="position: absolute; right: 12px; top: 10px; width: 38px; height: 46px; border: 2px dashed {TERRA}; display: flex; align-items: center; justify-content: center">{sym(28)}</div>'
            f'<div style="position: absolute; left: 104px; right: 14px; top: 78px; border-top: 1.5px solid {SAND}"></div><div style="position: absolute; left: 104px; right: 14px; top: 100px; border-top: 1.5px solid {SAND}"></div></div></div>')
p9 = B.header("09 — SỔ &amp; VĂN PHÒNG PHẨM", "Viết chậm thôi") + grid([
    cell(notebook, "Sổ da A5", "Dập chìm biểu tượng, in tên theo yêu cầu"),
    cell(spread, "Ruột sổ chấm bi", "Giấy kem, góc trang có linh vật"),
    cell(pens, "Bút bi &amp; bút chì", "3 màu thương hiệu, in chữ logo"),
    cell(bookmark, "Kẹp sách", "Ngơ ló đầu · bản logo"),
    cell(sticker_sheet, "Tờ sticker", "Tặng kèm sổ hoặc bán lẻ"),
    cell(postcard, "Bưu thiếp", "Mặt họa tiết · mặt viết thư"),
])
# ---------------- page 10: quà lưu niệm ----------------
mug = (f'<div style="position: relative; width: 210px; height: 200px">'
       f'<div style="position: absolute; left: 150px; top: 50px; width: 60px; height: 90px; border: 14px solid {CREAM}; border-left: none; border-radius: 0 40px 40px 0; box-sizing: border-box; outline: 3px solid {ESP}; outline-offset: -3px"></div>'
       f'<div style="position: absolute; left: 0; top: 10px; width: 170px; height: 180px; background: {CREAM}; border: 3px solid {ESP}; border-radius: 10px 10px 26px 26px; box-sizing: border-box; overflow: hidden">'
       f'<div style="position: absolute; left: 0; right: 0; bottom: 0; height: 40px; background: {TERRA}; border-top: 3px solid {ESP}"></div>'
       f'<div style="position: absolute; left: 50%; top: 22px; transform: translateX(-50%)">{sym(92)}</div></div></div>')
tumbler = (f'<div style="display: flex; flex-direction: column; align-items: center">'
           f'<div style="width: 96px; height: 26px; background: {ESP}; border-radius: 10px 10px 4px 4px"></div>'
           f'<div style="width: 110px; height: 230px; background: {MOSS}; border: 3px solid {ESP}; border-radius: 8px 8px 30px 30px; box-sizing: border-box; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 4px">'
           f'{sym(60, body=BUTTER)}<div style="{DISPLAY}; font-weight: 800; font-size: 22px; color: {CREAM}; line-height: 0.95; text-align: center">{NAME.lower().replace(" ", "<br>")}</div></div></div>')
tote = (f'<div style="position: relative; width: 230px; height: 260px">'
        f'<svg width="230" height="80" viewBox="0 0 230 80" aria-hidden="true" style="display: block; position: absolute; top: 0"><path d="M60,80 Q60,8 115,8 Q170,8 170,80" fill="none" stroke="{SAND}" stroke-width="14"></path></svg>'
        f'<div style="position: absolute; top: 60px; left: 0; width: 230px; height: 200px; background: #EFE6D3; border: 3px solid {ESP}; box-sizing: border-box; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 2px">'
        f'{nga(170)}<div style="{SANS}; font-weight: 700; font-size: 10px; letter-spacing: 0.2em; color: {ESP}">SLOW COFFEE · COMFY SEATS</div></div></div>')
def acrylic(inner, w):
    return (f'<div style="display: flex; flex-direction: column; align-items: center">'
            f'<div style="width: 26px; height: 26px; border: 4px solid #A9A39A; border-radius: 50%"></div>'
            f'<div style="width: 6px; height: 14px; background: #A9A39A"></div>'
            f'<div style="background: rgba(255,255,255,0.7); border: 3px solid {ESP}; border-radius: 26px; padding: 8px">{inner}</div></div>')
keychains = f'<div style="display: flex; gap: 22px; align-items: flex-start">{acrylic(nga(130), 130)}{acrylic(ngo(90), 90)}</div>'
def badge(inner, bg, s=92):
    return (f'<div style="width: {s}px; height: {s}px; border-radius: 50%; background: {bg}; border: 3px solid {ESP}; box-sizing: border-box; '
            f'box-shadow: inset -6px -6px 0 rgba(0,0,0,0.08); display: flex; align-items: center; justify-content: center; {HAND}; font-size: 22px; line-height: 1; text-align: center; color: {ESP}">{inner}</div>')
badges = (f'<div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px">{badge(sym(62), CREAM)}{badge("ơ?", MOSS)}'
          f'{badge(TAG.replace(" ", "<br>", 1), BUTTER)}{badge(sym(62, body=BUTTER), TERRA)}</div>')
tee = (f'<div style="position: relative; width: 250px; height: 240px">'
       f'<svg width="250" height="240" viewBox="0 0 250 240" aria-hidden="true" style="display: block"><path d="M80,10 Q125,40 170,10 L240,44 L214,96 L190,84 L190,232 L60,232 L60,84 L36,96 L10,44 Z" fill="{CREAM}" stroke="{ESP}" stroke-width="4" stroke-linejoin="round"></path>'
       f'<path d="M98,14 Q125,32 152,14" fill="none" stroke="{ESP}" stroke-width="3"></path></svg>'
       f'<div style="position: absolute; left: 136px; top: 62px">{sym(40)}</div>'
       f'<div style="position: absolute; left: 0; right: 0; top: 140px; text-align: center; {HAND}; font-size: 24px; color: {TERRA}">{TAG}</div></div>')
p10 = B.header("10 — QUÀ LƯU NIỆM", "Mang về một chút ấm") + grid([
    cell(mug, "Cốc sứ", "Đáy viền Đất Nung · 350ml"),
    cell(tumbler, "Ly giữ nhiệt", "Thép không gỉ, sơn Rêu Sồi"),
    cell(tote, "Túi vải canvas", "In Ngả ngủ trên sofa"),
    cell(keychains, "Móc khóa Ngả &amp; Ngơ", "Mica trong, in hai mặt"),
    cell(badges, "Huy hiệu cài áo", "Bộ 4 cái · 44mm"),
    cell(tee, "Áo thun", "Logo ngực trái · chữ viết tay"),
])
# ---------------- page 11: cà phê & hộp quà ----------------
coffee_bag = (f'<div style="position: relative; width: 200px; height: 290px; background: {KRAFT}; border: 3px solid {ESP}; border-radius: 8px 8px 18px 18px; box-sizing: border-box">'
              f'<div style="position: absolute; left: 0; right: 0; top: 18px; border-top: 3px dashed rgba(43,29,22,0.35)"></div>'
              f'<div style="position: absolute; left: 82px; top: 36px; width: 30px; height: 30px; border-radius: 50%; border: 3px solid {ESP}; background: {SAND}"></div>'
              f'<div style="position: absolute; left: 18px; right: 18px; top: 84px; bottom: 22px; background: {CREAM}; border: 3px solid {ESP}; border-radius: 10px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 4px; padding: 8px; box-sizing: border-box">'
              f'{sym(58)}{wm(26)}<div style="{SANS}; font-size: 11px; font-weight: 700; letter-spacing: 0.14em; color: {TERRA}; text-align: center">CÀ PHÊ PHA PHIN</div>'
              f'<div style="{SANS}; font-size: 11px; color: {ESP}; text-align: center">[NGUỒN GỐC HẠT] · 250g</div></div></div>')
def drip(bg, label, tc):
    return (f'<div style="width: 104px; height: 140px; background: {bg}; border: 3px solid {ESP}; border-radius: 8px; box-sizing: border-box; '
            f'display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 6px; position: relative">'
            f'<div style="position: absolute; left: 0; right: 0; top: 12px; border-top: 2px dashed rgba(43,29,22,0.4)"></div>'
            f'{sym(48, body=CREAM if bg != CREAM else TERRA)}<div style="{HAND}; font-size: 17px; color: {tc}; text-align: center; line-height: 1">{label}</div></div>')
drips = f'<div style="display: flex; gap: 14px">{drip(TERRA, "đậm", CREAM)}{drip(BUTTER, "sữa", ESP)}{drip(MOSS, "nhẹ", CREAM)}</div>'
gift_box = (f'<div style="display: flex; gap: 40px; align-items: center">'
            f'<div style="position: relative; width: 300px; height: 210px">'
            f'<div style="position: absolute; left: 0; top: 0; width: 300px; height: 70px; border: 3px solid {ESP}; border-radius: 10px; overflow: hidden; box-sizing: border-box">{B.pattern_svg(300, 70, TERRA, BUTTER, ESP, CREAM, CREAM, 0.6)}</div>'
            f'<div style="position: absolute; left: 10px; top: 64px; width: 280px; height: 146px; background: {TERRA}; border: 3px solid {ESP}; border-radius: 0 0 12px 12px; box-sizing: border-box"></div>'
            f'<div style="position: absolute; left: 132px; top: 0; width: 36px; height: 210px; background: {BUTTER}; border-left: 3px solid {ESP}; border-right: 3px solid {ESP}; box-sizing: border-box"></div>'
            f'<div style="position: absolute; left: 50%; top: 104px; transform: translateX(-50%); background: {CREAM}; border: 3px solid {ESP}; border-radius: 10px; padding: 6px 14px; display: flex; flex-direction: column; align-items: center">'
            f'{wm(30)}<div style="{SANS}; font-size: 10px; font-weight: 700; letter-spacing: 0.18em; color: {TERRA}">HỘP QUÀ</div></div></div>'
            f'<div style="display: flex; flex-direction: column; gap: 8px; {SANS}; font-size: 15px; color: {ESP}; line-height: 1.5">'
            f'<div style="{SANS}; font-size: 13px; font-weight: 700; letter-spacing: 0.16em; color: {TERRA}">TRONG HỘP GỢI Ý</div>'
            f'<div>1 túi cà phê 250g</div><div>5 túi lọc pha nhanh</div><div>1 cốc sứ hoặc ly giữ nhiệt</div><div>1 sổ da in tên</div><div>1 tờ sticker Ngả &amp; Ngơ</div></div></div>')
price_tag = (f'<div style="display: flex; gap: 16px; align-items: center">'
             f'<div style="position: relative; width: 150px; height: 200px; background: {CREAM}; border: 3px solid {ESP}; border-radius: 12px 12px 12px 12px; box-sizing: border-box; display: flex; flex-direction: column; align-items: center; padding-top: 34px; gap: 6px">'
             f'<div style="position: absolute; top: 10px; width: 14px; height: 14px; border-radius: 50%; border: 3px solid {ESP}"></div>'
             f'{sym(56)}<div style="{DISPLAY}; font-weight: 800; font-size: 20px; color: {ESP}">[TÊN MÓN]</div><div style="{SANS}; font-size: 14px; font-weight: 700; color: {TERRA}">[GIÁ]</div></div>'
             f'<div style="{HAND}; font-size: 22px; color: {TERRA}; max-width: 140px; line-height: 1.1">{PRICE}</div></div>')
p11 = B.header("11 — CÀ PHÊ ĐÓNG GÓI &amp; HỘP QUÀ", "Cà phê để dành") + grid([
    cell(coffee_bag, "Túi cà phê hạt / bột", "Túi đứng giấy kraft, van một chiều"),
    cell(drips, "Túi lọc pha nhanh", "3 vị, mỗi vị một màu"),
    cell(price_tag, "Thẻ giá quầy lưu niệm", "Treo hoặc dán kệ"),
    cell(gift_box, "Hộp quà", "Nắp in họa tiết, đai Vàng Bơ", span=3),
])

if which == "em":
    import re as _re
    def _em(x):
        x = _re.sub(r'(?<!Em )\bNgả\b', 'Em Ngả', x)
        return _re.sub(r'(?<!Em )\bNgơ\b', 'Em Ngơ', x)
    p9, p10, p11 = _em(p9), _em(p10), _em(p11)
pages = {"Merch1.dc.html": (f"{NAME} – Sổ và văn phòng phẩm", p9, "09 Sổ & văn phòng phẩm"),
         "Merch2.dc.html": (f"{NAME} – Quà lưu niệm", p10, "10 Quà lưu niệm"),
         "Merch3.dc.html": (f"{NAME} – Cà phê đóng gói và hộp quà", p11, "11 Cà phê & hộp quà")}
for f, (title, inner, _) in pages.items():
    open(os.path.join(ROOT, f), "w").write(B.page(title, B.board(inner)))
# extend canvas index: new row under existing 3x3 grid
cj = os.path.join(ROOT, "canvas.json")
c = json.load(open(cj))
for i, (f, (_, _, t)) in enumerate(pages.items()):
    c["boards"][f] = {"x": i * (B.W + 80), "y": 3 * (B.H + 120), "w": B.W, "h": B.H, "title": t}
    if f not in c["order"]:
        c["order"].append(f)
json.dump(c, open(cj, "w"), ensure_ascii=False)
order_path = os.path.join(os.path.dirname(ROOT), "order.json")
json.dump(c["order"], open(order_path, "w"))
print("ok", which, list(pages))
