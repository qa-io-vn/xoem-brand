import os, json, io, contextlib, sys
sys.path.insert(0, "/home/claude")
with contextlib.redirect_stdout(io.StringIO()):
    import brand_em as B
CREAM, ESP, TERRA, MOSS, BUTTER, SAND, KRAFT, BLUSH = B.CREAM, B.ESP, B.TERRA, B.MOSS, B.BUTTER, B.SAND, B.KRAFT, B.BLUSH
SANS, DISPLAY, HAND = B.SANS, B.DISPLAY, B.HAND
sym, wm, lockup, nga, ngo, boss, pat = B.symbol, B.wordmark, B.lockup, B.nga, B.ngo, B.boss, B.pattern_svg
ROOT = B.ROOT
MUTED = "#6A5A4F"
HANDLE = "@xoem.ecopark"
ADDR = "93 Marina, Ecopark, Văn Giang, Hưng Yên"

def T(t, s=15, w=400, c=ESP, extra=""):
    return f'<div style="{SANS}; font-size: {s}px; font-weight: {w}; color: {c}; line-height: 1.45; {extra}">{t}</div>'
def D(t, s=28, c=ESP, extra=""):
    return f'<div style="{DISPLAY}; font-weight: 800; font-size: {s}px; color: {c}; line-height: 1.05; {extra}">{t}</div>'
def H(t, s=20, c=TERRA, extra=""):
    return f'<div style="{HAND}; font-size: {s}px; color: {c}; line-height: 1.15; {extra}">{t}</div>'
def K(t, c=TERRA):
    return f'<div style="{SANS}; font-size: 12px; font-weight: 700; letter-spacing: 0.16em; color: {c}">{t}</div>'
def box(inner, bg="#FFFFFF", pad="20px 22px", extra=""):
    bd = f"border: 2px solid {SAND};" if bg in ("#FFFFFF", CREAM) else ""
    return f'<div style="background: {bg}; {bd} border-radius: 20px; padding: {pad}; box-sizing: border-box; display: flex; flex-direction: column; gap: 10px; {extra}">{inner}</div>'
def cell(content, t, sub="", extra=""):
    s = T(sub, 12, 400, MUTED, "text-align: center") if sub else ""
    return (f'<div style="background: #FFFFFF; border: 2px solid {SAND}; border-radius: 20px; padding: 16px; display: flex; flex-direction: column; '
            f'align-items: center; justify-content: space-between; gap: 10px; overflow: hidden; {extra}">'
            f'<div style="flex-grow: 1; display: flex; align-items: center; justify-content: center; gap: 14px; width: 100%">{content}</div>'
            f'<div style="display: flex; flex-direction: column; align-items: center; gap: 2px">{T(t, 14, 700, ESP, "text-align: center")}{s}</div></div>')
def grid(items, cols=3, rows=None, gap=18):
    r = f"grid-template-rows: {rows};" if rows else "grid-auto-rows: minmax(0, 1fr);"
    return f'<div style="display: grid; grid-template-columns: repeat({cols}, minmax(0, 1fr)); {r} gap: {gap}px; flex-grow: 1; min-height: 0">{"".join(items)}</div>'
def phone(inner, w=230, h=470, bg=CREAM):
    return (f'<div style="width: {w}px; height: {h}px; border: 8px solid {ESP}; border-radius: 34px; background: {bg}; overflow: hidden; '
            f'box-sizing: border-box; position: relative; flex-shrink: 0">{inner}</div>')
def btn(t, bg=TERRA, fg=CREAM, s=13):
    return f'<div style="background: {bg}; color: {fg}; {SANS}; font-weight: 700; font-size: {s}px; border-radius: 999px; padding: 8px 14px; text-align: center; border: 2px solid {ESP}">{t}</div>'
def qr(s=90):
    return (f'<div style="width: {s}px; height: {s}px; border: 3px dashed {ESP}; border-radius: 8px; display: flex; align-items: center; justify-content: center; '
            f'{SANS}; font-size: 11px; font-weight: 700; color: {MUTED}; text-align: center; background: #FFFFFF; flex-shrink: 0">[MÃ QR]</div>')
def tiles(size=46, gap=6, cols=(ESP, TERRA, TERRA, ESP), fgs=(CREAM, CREAM, CREAM, CREAM)):
    out = ""
    for i, ch in enumerate("XOEM"):
        out += (f'<div style="width: {size}px; height: {size}px; border-radius: {int(size*0.18)}px; background: {cols[i]}; display: flex; align-items: center; '
                f'justify-content: center; {DISPLAY}; font-weight: 800; font-size: {int(size*0.62)}px; color: {fgs[i]}; padding-top: {int(size*0.08)}px; box-sizing: border-box">{ch}</div>')
    return f'<div style="display: grid; grid-template-columns: repeat(2, {size}px); gap: {gap}px">{out}</div>'

pages = []

# ---------------- 12: câu chuyện ----------------
vals = [("Chậm", "Cà phê pha phin, pha chậm. Không ai hối khách, không ai hối nhân viên."),
        ("Mềm", "Ghế mềm, ánh sáng dịu, nhạc nhỏ. Chỗ để ngồi lâu mà không mỏi."),
        ("Thân", "Quán xưng em, nhớ món quen của khách, hỏi han như người nhà.")]
vcards = "".join(box(D(a, 30, TERRA) + T(b, 15), "#FFFFFF") for a, b in vals)
aud = [("Cư dân Ecopark", "đi dạo, dắt chó, ghé ly sáng"), ("Người làm việc", "cần góc yên, Wi‑Fi mạnh, ổ cắm"),
       ("Gia đình, nhóm bạn", "cuối tuần, cần bàn rộng, ghế sofa")]
acards = "".join(f'<div style="display: flex; flex-direction: column; gap: 2px; padding: 10px 0; border-top: 1.5px solid {SAND}">{T(a, 15, 700)}{T(b, 14, 400, MUTED)}</div>' for a, b in aud)
p = B.header("12 — CÂU CHUYỆN THƯƠNG HIỆU", "Có em lo") + f'''<div style="display: grid; grid-template-columns: minmax(0, 1.15fr) minmax(0, 1fr); gap: 28px; flex-grow: 1; min-height: 0">
<div style="display: flex; flex-direction: column; gap: 18px">
{box(K("SỨ MỆNH") + D("Một chỗ quen để ghé, ngồi xuống và để các em lo phần còn lại.", 30) + T("Xo em là tên mới của quán ở 93 Marina, Ecopark. Vẫn ghế mềm, vẫn cà phê pha chậm, thêm một lời hứa rõ ràng: khách chỉ việc ngồi, mọi thứ khác có em lo.", 16), CREAM, "24px 28px")}
<div style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px">{vcards}</div>
<div style="display: flex; align-items: flex-end; justify-content: space-around; flex-grow: 1; background: #FFFFFF; border: 2px solid {SAND}; border-radius: 20px; padding: 16px">{boss(130)}{nga(210)}{ngo(130)}</div>
</div>
<div style="display: flex; flex-direction: column; gap: 18px">
{box(K("LỜI HỨA THƯƠNG HIỆU", BUTTER) + D("Ghé vào.<br>Ngồi xuống.<br>Có em lo.", 40, CREAM) + T("Câu này đi cùng logo ở biển hiệu, ly, bài đăng và lời chào của nhân viên.", 14, 500, CREAM), TERRA, "24px 28px")}
{box(K("KHÁCH CỦA XO EM (GỢI Ý)") + acards)}
{box(K("TÍNH CÁCH") + f'<div style="display: flex; flex-wrap: wrap; gap: 8px">{btn("Thân thiện", CREAM, ESP)}{btn("Chu đáo", BUTTER, ESP)}{btn("Hơi ngố", MOSS)}{btn("Không vội", TERRA)}</div>', "#FFFFFF", "20px 22px", "flex-grow: 1")}
</div></div>'''
pages.append(("Story.dc.html", "Câu chuyện thương hiệu", "12 Câu chuyện", p))

# ---------------- 13: logo system ----------------
def mark_ok(ok):
    if ok:
        return f'<svg width="26" height="26" viewBox="0 0 26 26" aria-hidden="true"><circle cx="13" cy="13" r="12" fill="{MOSS}"></circle><path d="M7,13 L11,17 L19,9" fill="none" stroke="{CREAM}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"></path></svg>'
    return f'<svg width="26" height="26" viewBox="0 0 26 26" aria-hidden="true"><circle cx="13" cy="13" r="12" fill="#B8382A"></circle><path d="M8,8 L18,18 M18,8 L8,18" stroke="{CREAM}" stroke-width="3" stroke-linecap="round"></path></svg>'
def rule(inner, ok, label, bg=CREAM):
    return (f'<div style="display: flex; flex-direction: column; gap: 8px; align-items: center">'
            f'<div style="width: 100%; height: 190px; background: {bg}; border: 2px solid {SAND}; border-radius: 14px; display: flex; align-items: center; justify-content: center; overflow: hidden; position: relative">{inner}</div>'
            f'<div style="display: flex; gap: 6px; align-items: center">{mark_ok(ok)}{T(label, 13, 600)}</div></div>')
small = lockup(46, 34, tag=False, gap=8)
rules = "".join([
    rule(small, True, "Đúng: nền sáng, đủ khoảng trống"),
    rule(f'<div style="transform: scaleX(1.5)">{small}</div>', False, "Kéo giãn, bóp méo"),
    rule(lockup(46, 34, body="#3B6FB6", ink=ESP, tag=False, gap=8), False, "Tự đổi màu"),
    rule(f'<div style="filter: drop-shadow(5px 5px 3px rgba(0,0,0,0.5))">{small}</div>', False, "Đổ bóng, hiệu ứng"),
    rule(f'<div style="position: absolute; inset: 0">{pat(300, 120, TERRA, BUTTER, ESP, CREAM, CREAM, 0.7)}</div><div style="position: relative">{small}</div>', False, "Đặt trên nền rối"),
    rule(f'<div style="transform: rotate(-14deg)">{small}</div>', False, "Xoay nghiêng"),
])
icons = (f'<div style="display: flex; align-items: flex-end; gap: 18px">'
         f'<div style="width: 120px; height: 120px; border-radius: 28px; background: {TERRA}; display: flex; align-items: center; justify-content: center; border: 3px solid {ESP}">{sym(92, body=BUTTER)}</div>'
         f'<div style="width: 64px; height: 64px; border-radius: 16px; background: {TERRA}; display: flex; align-items: center; justify-content: center">{sym(50, body=BUTTER)}</div>'
         f'<div style="width: 32px; height: 32px; border-radius: 8px; background: {TERRA}; display: flex; align-items: center; justify-content: center">{sym(26, body=BUTTER, steam=False)}</div></div>')
p = B.header("13 — HỆ THỐNG LOGO", "Một logo, nhiều cỡ", "Logo chính dùng cho mọi nơi. Logo 4 ô dùng cho tường quầy, tem, con dấu. Biểu tượng vuông dùng làm ảnh đại diện, biểu tượng ứng dụng và biểu tượng trình duyệt.") + grid([
    cell(lockup(140, 104), "Logo chính", "Biểu tượng + chữ + khẩu hiệu"),
    cell(f'<div style="display: flex; align-items: center; gap: 16px">{tiles(78)}{D("xo em", 60)}</div>', "Logo 4 ô X·O·E·M", "Tường quầy, tem dán, con dấu"),
    cell(icons, "Biểu tượng ứng dụng &amp; trình duyệt", "120 · 64 · 32 px, bo góc"),
], 3, "300px") + f'<div style="display: grid; grid-template-columns: repeat(6, minmax(0, 1fr)); gap: 14px">{rules}</div>'
pages.append(("LogoRules.dc.html", "Hệ thống logo và quy tắc", "13 Hệ thống logo", p))

# ---------------- 14: biển báo ----------------
wifi = (f'<div style="width: 220px; height: 170px; background: {CREAM}; border: 3px solid {ESP}; border-radius: 14px; padding: 14px; box-sizing: border-box; position: relative">'
        f'{K("WI‑FI")}{D("[TÊN MẠNG]", 22)}{T("Mật khẩu: [MẬT KHẨU]", 13, 600)}{H("ngồi lâu cũng được,<br>có em lo", 17)}'
        f'<div style="position: absolute; right: -6px; bottom: -8px">{ngo(70)}</div></div>')
table_no = (f'<div style="display: flex; gap: 16px; align-items: center">'
            f'<div style="width: 120px; height: 120px; border-radius: 50%; background: {TERRA}; border: 3px solid {ESP}; display: flex; flex-direction: column; align-items: center; justify-content: center">'
            f'{K("BÀN", CREAM)}{D("12", 46, CREAM)}</div>{sym(70)}</div>')
wc = (f'<div style="width: 170px; height: 190px; background: {MOSS}; border: 3px solid {ESP}; border-radius: 14px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 8px">'
      f'<svg width="90" height="70" viewBox="0 0 90 70" aria-hidden="true"><circle cx="24" cy="12" r="8" fill="{CREAM}"></circle><rect x="16" y="24" width="16" height="40" rx="6" fill="{CREAM}"></rect>'
      f'<circle cx="66" cy="12" r="8" fill="{CREAM}"></circle><path d="M66,22 L80,52 L52,52 Z" fill="{CREAM}"></path><rect x="60" y="50" width="12" height="16" fill="{CREAM}"></rect>'
      f'<rect x="44" y="4" width="2" height="62" fill="{CREAM}"></rect></svg>{D("Nhà vệ sinh", 22, CREAM)}{T("đi thẳng, rẽ trái", 13, 600, CREAM)}</div>')
door = (f'<div style="width: 220px; height: 190px; background: rgba(255,255,255,0.6); border: 3px solid {ESP}; border-radius: 6px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 6px">'
        f'{sym(56)}{D("Mở cửa mỗi ngày", 20)}{D("07:00–23:00", 30, TERRA)}{T("cả lễ Tết, có em lo", 12, 600, MUTED)}</div>')
aframe = (f'<div style="position: relative; width: 200px; height: 240px">'
          f'<div style="position: absolute; left: 10px; top: 0; width: 180px; height: 210px; background: #2E2A26; border: 8px solid {KRAFT}; border-radius: 6px; box-sizing: border-box; padding: 14px; display: flex; flex-direction: column; gap: 6px">'
          f'{H("hôm nay", 18, BUTTER)}{D("Có em lo", 30, CREAM)}{H("món của ngày:", 17, BUTTER)}{T("[TÊN MÓN]", 14, 700, CREAM)}{T("[GIÁ]", 13, 600, BUTTER)}</div>'
          f'<div style="position: absolute; left: 22px; bottom: 0; width: 8px; height: 40px; background: {KRAFT}; transform: rotate(10deg)"></div>'
          f'<div style="position: absolute; right: 22px; bottom: 0; width: 8px; height: 40px; background: {KRAFT}; transform: rotate(-10deg)"></div></div>')
water = (f'<div style="width: 200px; height: 150px; background: {BUTTER}; border: 3px solid {ESP}; border-radius: 14px; padding: 14px; box-sizing: border-box; display: flex; flex-direction: column; gap: 4px">'
         f'{K("TỰ PHỤC VỤ", ESP)}{D("Nước lọc", 26)}{T("cứ lấy thoải mái, hết thì gọi em", 13, 600)}</div>')
qr_tent = (f'<div style="width: 180px; height: 220px; background: {CREAM}; border: 3px solid {ESP}; border-radius: 14px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 8px; padding: 10px; box-sizing: border-box">'
           f'{D("Quét Zalo", 22)}{qr(96)}{T("gọi món tại bàn, em mang ra", 12, 600, MUTED, "text-align: center")}</div>')
p = B.header("14 — BIỂN BÁO TRONG QUÁN", "Đi đâu cũng có em chỉ") + grid([
    cell(wifi, "Thẻ Wi‑Fi để bàn"), cell(table_no, "Số bàn"), cell(wc, "Biển nhà vệ sinh"), cell(door, "Dán cửa kính · giờ mở cửa"),
    cell(aframe, "Bảng đứng trước quán"), cell(water, "Khu tự phục vụ nước"), cell(qr_tent, "Thẻ QR gọi món"),
    cell(f'<div style="display: flex; gap: 10px; align-items: center">{sym(60)}{T("Mũi tên, biển cấm hút thuốc, biển ổ cắm điện… dùng cùng khung và màu này.", 13, 400, MUTED, "max-width: 190px")}</div>', "Quy tắc chung"),
], 4)
pages.append(("Wayfinding.dc.html", "Biển báo trong quán", "14 Biển báo", p))

# ---------------- 15: bao bì mở rộng ----------------
sleeve = (f'<div style="width: 280px; height: 90px; border: 3px solid {ESP}; border-radius: 10px; overflow: hidden; position: relative">'
          f'{pat(280, 90, TERRA, BUTTER, ESP, CREAM, CREAM, 0.55)}<div style="position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%); background: {CREAM}; border: 3px solid {ESP}; border-radius: 10px; padding: 2px 12px">{H("có em lo", 20)}</div></div>')
napkin = (f'<div style="width: 150px; height: 150px; background: #FFFFFF; border: 3px solid {ESP}; box-sizing: border-box; position: relative; transform: rotate(-4deg)">'
          f'<div style="position: absolute; inset: 8px; border: 2px dashed {SAND}"></div><div style="position: absolute; right: 14px; bottom: 14px">{sym(46)}</div></div>')
straw = (f'<div style="display: flex; flex-direction: column; gap: 14px">'
         + "".join(f'<div style="width: 250px; height: 22px; background: {c}; border: 2px solid {ESP}; border-radius: 4px; display: flex; align-items: center; justify-content: center; {DISPLAY}; font-weight: 800; font-size: 13px; color: {fc}">xo em · có em lo · xo em</div>' for c, fc in ((CREAM, TERRA), (TERRA, CREAM)))
         + '</div>')
cake = (f'<div style="position: relative; width: 210px; height: 150px; background: {CREAM}; border: 3px solid {ESP}; border-radius: 8px; box-sizing: border-box">'
        f'<div style="position: absolute; left: 30px; right: 30px; top: 24px; height: 60px; border: 2px solid {ESP}; border-radius: 8px; background: rgba(255,255,255,0.7); display: flex; align-items: center; justify-content: center">{T("ô nhìn bánh", 12, 600, MUTED)}</div>'
        f'<div style="position: absolute; left: 0; right: 0; bottom: 14px; display: flex; justify-content: center; gap: 8px; align-items: center">{sym(32)}{D("xo em", 20)}</div></div>')
carrier = (f'<div style="display: flex; gap: 6px; align-items: flex-end">'
           f'<div style="width: 230px; height: 70px; background: {KRAFT}; border: 3px solid {ESP}; border-radius: 8px 8px 16px 16px; display: flex; align-items: center; justify-content: center; gap: 10px">{sym(44, body=CREAM)}{T("2 ly · có em lo", 13, 700)}</div></div>')
lid = (f'<div style="display: flex; gap: 14px">'
       + "".join(f'<div style="width: 90px; height: 90px; border-radius: 50%; background: {b}; border: 3px solid {ESP}; display: flex; align-items: center; justify-content: center; text-align: center; {HAND}; font-size: 16px; line-height: 1; color: {c}">{t}</div>'
                 for b, c, t in ((BUTTER, ESP, "ít đá"), (TERRA, CREAM, "ít ngọt"), (MOSS, CREAM, "mang đi")))
       + '</div>')
p = B.header("15 — BAO BÌ MỞ RỘNG", "Từng món nhỏ cũng có em") + grid([
    cell(sleeve, "Ống giấy bọc ly", "Chống nóng tay"), cell(napkin, "Khăn giấy", "In một góc"), cell(straw, "Giấy bọc ống hút"),
    cell(cake, "Hộp bánh", "Có ô nhìn bánh"), cell(carrier, "Khay giấy 2 ly"), cell(lid, "Tem ghi chú trên nắp", "Đánh dấu nhanh khi pha"),
])
pages.append(("PackagingPlus.dc.html", "Bao bì mở rộng", "15 Bao bì mở rộng", p))

# ---------------- 16: khuyến mãi & đổi tên ----------------
poster = (f'<div style="width: 300px; height: 424px; background: {TERRA}; border: 3px solid {ESP}; border-radius: 10px; box-sizing: border-box; padding: 22px; display: flex; flex-direction: column; gap: 8px; position: relative; overflow: hidden">'
          f'{K("THÔNG BÁO", BUTTER)}{D("Xofa giờ là<br>Xo em", 40, CREAM)}{T("Vẫn chỗ ngồi đó, vẫn ly cà phê đó. Chỉ đổi tên thôi, còn lại có em lo.", 14, 500, CREAM)}'
          f'{T("Từ ngày [NGÀY ĐỔI TÊN]", 13, 700, BUTTER)}<div style="position: absolute; right: 14px; bottom: 14px">{boss(120)}</div>'
          f'<div style="position: absolute; left: 22px; bottom: 22px">{T(ADDR.replace(", ", "<br>", 1), 11, 500, CREAM)}</div></div>')
voucher = (f'<div style="display: flex; width: 330px; height: 140px; border: 3px solid {ESP}; border-radius: 12px; overflow: hidden">'
           f'<div style="flex-grow: 1; background: {BUTTER}; padding: 14px; display: flex; flex-direction: column; gap: 4px">{K("PHIẾU QUÀ", ESP)}{D("Ly thứ hai<br>giảm [X]%", 26)}{T("Hạn dùng: [NGÀY]", 12, 600)}</div>'
           f'<div style="width: 90px; background: {CREAM}; border-left: 3px dashed {ESP}; display: flex; align-items: center; justify-content: center">{sym(60)}</div></div>')
flyer = (f'<div style="width: 230px; height: 320px; background: {CREAM}; border: 3px solid {ESP}; border-radius: 10px; padding: 16px; box-sizing: border-box; display: flex; flex-direction: column; gap: 6px; position: relative; overflow: hidden">'
         f'{lockup(40, 30, tag=False, gap=6)}{H("tuần lễ chào tên mới", 20)}{T("• Ly thứ hai giảm [X]%<br>• Tặng sticker Em Ngả, Em Ngơ<br>• Check‑in nhận thẻ tích điểm", 13, 500)}'
         f'<div style="position: absolute; right: -10px; bottom: -6px">{nga(170)}</div></div>')
post = (f'<div style="width: 220px; height: 220px; background: {BUTTER}; border: 3px solid {ESP}; border-radius: 14px; padding: 16px; box-sizing: border-box; position: relative; overflow: hidden">'
        f'{D("Tụi em<br>đổi tên<br>rồi nè!", 30)}<div style="position: absolute; right: -6px; bottom: -8px">{ngo(110)}</div></div>')
p = B.header("16 — KHUYẾN MÃI &amp; ĐỔI TÊN", "Tên mới, chỗ ngồi cũ") + f'''<div style="display: flex; gap: 24px; flex-grow: 1; align-items: stretch">
{cell(poster, "Áp phích thông báo đổi tên (A3)", "Dán cửa, quầy thu ngân", "flex: 1.1")}
<div style="display: flex; flex-direction: column; gap: 18px; flex: 1.2">{cell(voucher, "Phiếu quà tặng", "", "flex: 1")}{cell(post, "Bài đăng thông báo", "", "flex: 1.3")}</div>
{cell(flyer, "Tờ rơi tuần lễ tên mới", "Nội dung khuyến mãi minh họa", "flex: 1")}
</div>'''
pages.append(("Promo.dc.html", "Khuyến mãi và đổi tên", "16 Khuyến mãi & đổi tên", p))

# ---------------- 17: mạng xã hội mở rộng ----------------
fb = (f'<div style="width: 100%; max-width: 560px; border: 2px solid {SAND}; border-radius: 14px; overflow: hidden; background: #FFFFFF">'
      f'<div style="height: 150px; position: relative">{pat(560, 150, CREAM, TERRA, ESP, CREAM, SAND, 0.8)}<div style="position: absolute; right: 20px; bottom: -4px">{nga(170)}</div></div>'
      f'<div style="display: flex; align-items: flex-end; gap: 14px; padding: 0 18px 14px; margin-top: -40px; position: relative">'
      f'<div style="width: 96px; height: 96px; border-radius: 50%; background: {TERRA}; border: 4px solid #FFFFFF; display: flex; align-items: center; justify-content: center">{sym(66, body=BUTTER)}</div>'
      f'<div style="flex-grow: 1; padding-bottom: 6px">{D("Xo em", 24)}{T("Quán cà phê · Ecopark", 12, 500, MUTED)}</div>{btn("Nhắn tin")}</div></div>')
ig_tiles = ""
ig = [(TERRA, sym(60, body=BUTTER)), (CREAM, nga(90)), (BUTTER, D("có em<br>lo", 20)), (MOSS, ngo(56)), (ESP, sym(60)), (CREAM, H("món mới<br>thứ 6", 18)),
      (BUTTER, boss(62)), (TERRA, D("07:00<br>23:00", 18, CREAM)), (SAND, T("[ẢNH MÓN]", 11, 700, MUTED))]
for bg, inner in ig:
    ig_tiles += f'<div style="aspect-ratio: 1 / 1; background: {bg}; display: flex; align-items: center; justify-content: center; text-align: center; overflow: hidden">{inner}</div>'
igg = f'<div style="width: 250px; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 3px; border: 2px solid {SAND}">{ig_tiles}</div>'
vids = "".join(f'<div style="aspect-ratio: 3 / 4; background: {bg}; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 2px; padding: 4px; box-sizing: border-box; text-align: center">{img}{T(t, 9, 700, fc)}</div>'
               for bg, img, t, fc in ((CREAM, ngo(40), "Em Ngơ quên ly trên sừng", ESP), (TERRA, boss(40), "Boss giữ chân khách", CREAM),
                                      (BUTTER, nga(56), "Em Ngả ngủ ca chiều", ESP), (MOSS, sym(38, body=BUTTER), "Pha phin cùng em", CREAM),
                                      (ESP, sym(38), "Một ngày ở quán", CREAM), (SAND, T("[VIDEO]", 10, 700, MUTED), "Món mới", ESP)))
tiktok = phone(f'<div style="padding: 18px 12px; display: flex; flex-direction: column; align-items: center; gap: 6px">'
               f'<div style="width: 70px; height: 70px; border-radius: 50%; background: {TERRA}; display: flex; align-items: center; justify-content: center">{sym(48, body=BUTTER)}</div>'
               f'{T(HANDLE, 13, 700)}{T("Ghé vào. Ngồi xuống. Có em lo.", 11, 500, MUTED, "text-align: center")}'
               f'<div style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 3px; width: 100%; margin-top: 6px">{vids}</div></div>', 220, 430)
story = phone(f'<div style="position: absolute; inset: 0; background: {TERRA}"></div>'
              f'<div style="position: relative; padding: 26px 16px; display: flex; flex-direction: column; gap: 8px; height: 100%; box-sizing: border-box">'
              f'{K("HÔM NAY Ở XO EM", BUTTER)}{D("Món của ngày", 26, CREAM)}<div style="height: 150px; border-radius: 14px; background: {CREAM}; display: flex; align-items: center; justify-content: center">{T("[ẢNH MÓN]", 12, 700, MUTED)}</div>'
              f'{T("[TÊN MÓN] · [GIÁ]", 13, 700, CREAM)}<div style="margin-top: auto; display: flex; justify-content: space-between; align-items: flex-end">{H("vuốt lên<br>gọi món", 16, BUTTER)}{boss(70)}</div></div>', 220, 430)
hl = "".join(f'<div style="display: flex; flex-direction: column; align-items: center; gap: 4px"><div style="width: 52px; height: 52px; border-radius: 50%; background: {b}; border: 2px solid {ESP}; display: flex; align-items: center; justify-content: center">{i}</div>{T(t, 11, 600)}</div>'
             for b, i, t in ((CREAM, sym(34), "Thực đơn"), (BUTTER, nga(46), "Góc ngồi"), (MOSS, ngo(30), "Sự kiện"), (TERRA, boss(32), "Đánh giá")))
p = B.header("17 — MẠNG XÃ HỘI", "Lướt cũng thấy nhớ em", f"Tên tài khoản thống nhất trên mọi kênh: {HANDLE} (kiểm tra còn trống trước khi tạo).") + f'''<div style="display: grid; grid-template-columns: minmax(0, 1fr) 294px 252px 252px; gap: 18px; flex-grow: 1; min-height: 0">
<div style="display: flex; flex-direction: column; gap: 16px">{box(K("TRANG FACEBOOK") + fb)}{box(K("ẢNH NỔI BẬT TRÊN TRANG CÁ NHÂN") + f'<div style="display: flex; gap: 18px">{hl}</div>')}</div>
{box(K("INSTAGRAM · LƯỚI 9 Ô") + igg + T("Xen kẽ: logo, linh vật, chữ, ảnh món. Không đăng 2 ô cùng màu cạnh nhau.", 12, 400, MUTED), "#FFFFFF", "20px 22px", "align-items: center")}
{box(K("TIKTOK") + tiktok, "#FFFFFF", "16px", "align-items: center")}{box(K("TIN 24 GIỜ") + story, "#FFFFFF", "16px", "align-items: center")}
</div>'''
pages.append(("SocialPlus.dc.html", "Mạng xã hội mở rộng", "17 Mạng xã hội", p))

# ---------------- 18: google maps ----------------
listing = (f'<div style="width: 360px; border: 2px solid {SAND}; border-radius: 16px; overflow: hidden; background: #FFFFFF">'
           f'<div style="height: 130px; background: {CREAM}; display: flex; align-items: flex-end; justify-content: center; position: relative; overflow: hidden">{pat(360, 130, CREAM, TERRA, ESP, CREAM, SAND, 0.7)}<div style="position: absolute; bottom: -6px">{nga(170)}</div></div>'
           f'<div style="padding: 14px 18px; display: flex; flex-direction: column; gap: 6px">{D("Xo em", 26)}'
           f'{T("[ĐIỂM ĐÁNH GIÁ] · [SỐ LƯỢT ĐÁNH GIÁ] · Quán cà phê", 12, 500, MUTED)}'
           f'<div style="display: flex; gap: 6px; flex-wrap: wrap; margin: 6px 0">{btn("Chỉ đường", TERRA, CREAM, 12)}{btn("Gọi", CREAM, ESP, 12)}{btn("Lưu", CREAM, ESP, 12)}{btn("Chia sẻ", CREAM, ESP, 12)}</div>'
           f'{T(ADDR, 13)}{T("Mở cửa · 07:00–23:00 mỗi ngày", 13, 700, MOSS)}{T("[SỐ ĐIỆN THOẠI] · [TRANG WEB]", 13, 500, MUTED)}</div></div>')
pin = (f'<div style="position: relative; width: 300px; height: 230px; border-radius: 16px; overflow: hidden; border: 2px solid {SAND}; background: #E9E4D6">'
       f'<svg width="300" height="230" viewBox="0 0 300 230" aria-hidden="true" style="position: absolute; inset: 0"><path d="M0,150 Q120,120 300,170" stroke="#FFFFFF" stroke-width="16" fill="none"></path>'
       f'<path d="M90,0 L130,230" stroke="#FFFFFF" stroke-width="12"></path><path d="M210,0 Q190,120 240,230" stroke="#FFFFFF" stroke-width="10" fill="none"></path>'
       f'<rect x="20" y="20" width="50" height="40" rx="6" fill="#CFE0C3"></rect><rect x="230" y="30" width="56" height="60" rx="8" fill="#BFD7EA"></rect></svg>'
       f'<svg width="70" height="90" viewBox="0 0 70 90" aria-hidden="true" style="position: absolute; left: 120px; top: 40px"><path d="M35,88 C35,88 4,52 4,32 A31,31 0 1 1 66,32 C66,52 35,88 35,88 Z" fill="{TERRA}" stroke="{ESP}" stroke-width="4"></path></svg>'
       f'<div style="position: absolute; left: 133px; top: 52px">{sym(44, body=BUTTER)}</div></div>')
photos = [("Ảnh bìa", "Mặt tiền ban ngày, thấy rõ biển Xo em"), ("Logo", "Biểu tượng vuông nền Đất Nung"), ("Bên trong", "Góc sofa, quầy pha, ánh sáng tự nhiên"),
          ("Món", "Ảnh chụp thật từng món, nền gọn"), ("Đội ngũ", "Các em pha chế mặc tạp dề quán")]
prow = "".join(f'<div style="display: grid; grid-template-columns: 90px minmax(0, 1fr); gap: 10px; padding: 7px 0; border-top: 1.5px solid {SAND}">{T(a, 13, 700, TERRA)}{T(b, 13)}</div>' for a, b in photos)
replies = [("5 sao", "Cảm ơn bạn đã ghé Xo em! Lần sau ghé, báo em món quen là có em lo liền nha."),
           ("4 sao", "Cảm ơn bạn đã ghé! Bạn chỉ em điều gì chưa ưng nhất để lần sau em lo chu đáo hơn nha."),
           ("Chưa hài lòng", "Em xin lỗi vì lần ghé vừa rồi chưa như ý. Bạn nhắn Zalo quán cho em để em xin lỗi trực tiếp và mời bạn ly kế tiếp nhé."),
           ("Hỏi chỗ đỗ xe", "Dạ, [THÔNG TIN CHỖ ĐỖ XE]. Bạn cần em chỉ đường cứ nhắn Zalo quán nha."),
           ("Hỏi giờ mở cửa", "Dạ, Xo em mở cửa 07:00–23:00 mỗi ngày, cả cuối tuần. Bạn ghé lúc nào cũng có em lo.")]
rrow = "".join(f'<div style="display: flex; flex-direction: column; gap: 3px; padding: 8px 0; border-top: 1.5px solid {SAND}">{K(a.upper())}{T("“" + b + "”", 13)}</div>' for a, b in replies)
p = B.header("18 — GOOGLE MAPS", "Tìm là thấy em", "Tên trên Google Maps để đúng chữ “Xo em” như biển hiệu, không chèn thêm từ khóa như “cà phê Ecopark” vào tên, để tránh hồ sơ bị Google gỡ hoặc hạn chế.") + f'''<div style="display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr) minmax(0, 1.1fr); gap: 20px; flex-grow: 1; min-height: 0">
<div style="display: flex; flex-direction: column; gap: 16px">{box(K("HỒ SƠ QUÁN TRÊN GOOGLE MAPS") + listing, "#FFFFFF", "18px", "align-items: center")}
{box(K("MÔ TẢ QUÁN (GỢI Ý)") + T("Xo em là quán cà phê pha chậm ở 93 Marina, Ecopark. Ghế mềm, Wi‑Fi mạnh, mở cửa 07:00–23:00 mỗi ngày. Ghé vào, ngồi xuống, có em lo.", 13), "#FFFFFF", "18px 22px", "flex-grow: 1")}</div>
<div style="display: flex; flex-direction: column; gap: 16px">{box(K("GHIM BẢN ĐỒ &amp; ẢNH ĐẠI DIỆN") + pin, "#FFFFFF", "18px", "align-items: center")}{box(K("ẢNH NÊN ĐĂNG") + prow, "#FFFFFF", "18px 22px", "flex-grow: 1")}</div>
<div style="display: flex; flex-direction: column; gap: 16px">{box(K("MẪU TRẢ LỜI ĐÁNH GIÁ") + rrow, "#FFFFFF", "18px 22px", "flex-grow: 1")}</div>
</div>'''
pages.append(("GoogleMaps.dc.html", "Google Maps", "18 Google Maps", p))

# ---------------- 19: zalo ----------------
oa = (f'<div style="width: 100%; border: 2px solid {SAND}; border-radius: 14px; overflow: hidden; background: #FFFFFF">'
      f'<div style="height: 110px; position: relative; background: {TERRA}; overflow: hidden">{pat(420, 110, TERRA, BUTTER, ESP, CREAM, CREAM, 0.6)}</div>'
      f'<div style="display: flex; gap: 12px; align-items: center; padding: 0 16px 14px; margin-top: -30px; position: relative">'
      f'<div style="width: 76px; height: 76px; border-radius: 50%; background: {CREAM}; border: 4px solid #FFFFFF; display: flex; align-items: center; justify-content: center">{sym(54)}</div>'
      f'<div style="flex-grow: 1; padding-top: 26px">{D("Xo em", 20)}{T("Trang quán trên Zalo · Ecopark", 11, 500, MUTED)}</div><div style="padding-top: 26px">{btn("Quan tâm", TERRA, CREAM, 12)}</div></div></div>')
welcome = box(K("TIN NHẮN CHÀO KHI KHÁCH QUAN TÂM") + T("“Chào bạn, em là Boss của Xo em đây! Bạn có thể gọi món tại bàn, đặt mang đi hoặc xem điểm tích lũy ngay trong Zalo. Cần gì cứ nhắn, có em lo.”", 13)
              + f'<div style="display: flex; gap: 8px; flex-wrap: wrap">{btn("Gọi món", TERRA, CREAM, 12)}{btn("Thực đơn", CREAM, ESP, 12)}{btn("Điểm của tôi", CREAM, ESP, 12)}</div>')
home = phone(f'<div style="padding: 16px 12px; display: flex; flex-direction: column; gap: 10px">'
             f'<div style="display: flex; justify-content: space-between; align-items: center">{lockup(30, 22, tag=False, gap=6)}{T("Bàn 12", 11, 700, TERRA)}</div>'
             f'<div style="background: {TERRA}; border-radius: 16px; padding: 12px; position: relative; overflow: hidden; height: 110px; box-sizing: border-box">{H("chào bạn,", 16, BUTTER)}{D("Có em lo", 24, CREAM)}<div style="position: absolute; right: -4px; bottom: -6px">{boss(64)}</div></div>'
             f'<div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 8px">{btn("Gọi tại bàn", BUTTER, ESP, 12)}{btn("Mang đi", CREAM, ESP, 12)}{btn("Tích điểm", MOSS, CREAM, 12)}{btn("Ưu đãi", CREAM, ESP, 12)}</div>'
             f'{K("MÓN QUEN CỦA BẠN")}<div style="display: flex; gap: 8px">' + "".join(f'<div style="flex: 1; background: #FFFFFF; border: 2px solid {SAND}; border-radius: 12px; padding: 8px; display: flex; flex-direction: column; gap: 4px; align-items: center">{sym(34, body=c)}{T("[TÊN MÓN]", 10, 700)}</div>' for c in (TERRA, BUTTER)) + '</div></div>')
menu_items = ["Cà phê phin sữa", "Bạc xỉu", "Trà đào cam sả", "Bánh chuối nướng"]
menu = phone(f'<div style="padding: 16px 12px; display: flex; flex-direction: column; gap: 8px">{D("Thực đơn", 22)}'
             f'<div style="display: flex; gap: 6px">{btn("Cà phê", TERRA, CREAM, 11)}{btn("Trà", CREAM, ESP, 11)}{btn("Bánh", CREAM, ESP, 11)}</div>'
             + "".join(f'<div style="display: flex; gap: 8px; align-items: center; background: #FFFFFF; border: 2px solid {SAND}; border-radius: 12px; padding: 8px">'
                       f'<div style="width: 42px; height: 42px; border-radius: 10px; background: {CREAM}; display: flex; align-items: center; justify-content: center">{sym(30)}</div>'
                       f'<div style="flex-grow: 1">{T(m, 12, 700)}{T("[GIÁ]", 11, 600, TERRA)}</div>'
                       f'<div style="width: 26px; height: 26px; border-radius: 50%; background: {TERRA}; color: {CREAM}; {SANS}; font-weight: 700; display: flex; align-items: center; justify-content: center">+</div></div>' for m in menu_items)
             + f'<div style="margin-top: 4px">{btn("Gửi món cho các em · [TỔNG]", ESP, CREAM, 12)}</div></div>')
stamps = "".join(f'<div style="width: 30px; height: 30px; border-radius: 50%; border: 2px {"solid" if i < 3 or i == 9 else "dashed"} {ESP}; display: flex; align-items: center; justify-content: center; background: {"#FFFFFF" if i == 9 else "transparent"}">{sym(22, body=TERRA if i < 3 else BUTTER) if i < 3 or i == 9 else ""}</div>' for i in range(10))
points = phone(f'<div style="padding: 16px 12px; display: flex; flex-direction: column; gap: 10px; align-items: center">{D("Thẻ thân với em", 20)}'
               f'<div style="background: {SAND}; border-radius: 16px; padding: 12px; width: 100%; box-sizing: border-box; display: flex; flex-direction: column; gap: 8px; align-items: center">'
               f'<div style="display: grid; grid-template-columns: repeat(5, 30px); gap: 8px">{stamps}</div>{H("còn 6 ly nữa, ly thứ 10 Em Ngơ mời!", 15)}</div>'
               f'{nga(170)}{T("Đưa mã này cho các em khi thanh toán", 11, 500, MUTED)}{qr(70)}</div>')
p = B.header("19 — ZALO", "Gọi món không cần đứng dậy", "Trang quán trên Zalo để nhắn tin và gửi ưu đãi. Ứng dụng nhỏ trong Zalo để khách quét QR ở bàn, gọi món và tích điểm.") + f'''<div style="display: grid; grid-template-columns: minmax(0, 1.05fr) minmax(0, 2fr); gap: 20px; flex-grow: 1; min-height: 0">
<div style="display: flex; flex-direction: column; gap: 16px">{box(K("TRANG QUÁN TRÊN ZALO") + oa)}{welcome}</div>
{box(K("ỨNG DỤNG NHỎ TRONG ZALO · TRANG CHỦ · THỰC ĐƠN · TÍCH ĐIỂM") + f'<div style="display: flex; gap: 18px; justify-content: center; align-items: center; flex-grow: 1">{home}{menu}{points}</div>', "#FFFFFF")}
</div>'''
pages.append(("Zalo.dc.html", "Zalo", "19 Zalo", p))

# ---------------- 20: web & link ----------------
web = (f'<div style="width: 100%; border: 3px solid {ESP}; border-radius: 14px; overflow: hidden; background: {CREAM}">'
       f'<div style="height: 26px; background: {SAND}; display: flex; align-items: center; gap: 6px; padding: 0 12px">' + "".join(f'<div style="width: 9px; height: 9px; border-radius: 50%; background: {c}"></div>' for c in (TERRA, BUTTER, MOSS)) + f'{T("xoem.vn (gợi ý, cần kiểm tra còn trống)", 11, 500, MUTED, "margin-left: 10px")}</div>'
       f'<div style="display: flex; justify-content: space-between; align-items: center; padding: 14px 22px">{lockup(34, 26, tag=False, gap=6)}<div style="display: flex; gap: 16px">{T("Thực đơn", 13, 600)}{T("Góc ngồi", 13, 600)}{T("Đồ lưu niệm", 13, 600)}{T("Liên hệ", 13, 600)}</div></div>'
       f'<div style="display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); padding: 10px 22px 22px; gap: 10px; align-items: center">'
       f'<div style="display: flex; flex-direction: column; gap: 10px">{D("Ghé vào.<br>Ngồi xuống.<br>Có em lo.", 40)}{T("Quán cà phê pha chậm ở 93 Marina, Ecopark. Mở cửa 07:00–23:00 mỗi ngày.", 14)}'
       f'<div style="display: flex; gap: 10px">{btn("Chỉ đường", TERRA, CREAM, 13)}{btn("Xem thực đơn", CREAM, ESP, 13)}</div></div>'
       f'<div style="display: flex; align-items: flex-end; justify-content: center; gap: 6px">{boss(110)}{nga(220)}{ngo(110)}</div></div></div>')
links = phone(f'<div style="padding: 20px 14px; display: flex; flex-direction: column; gap: 9px; align-items: center">'
              f'<div style="width: 70px; height: 70px; border-radius: 50%; background: {TERRA}; display: flex; align-items: center; justify-content: center">{sym(48, body=BUTTER)}</div>'
              f'{D("Xo em", 22)}{T("Ghé vào. Ngồi xuống. Có em lo.", 11, 500, MUTED)}'
              + "".join(f'<div style="width: 100%">{btn(t, b, f, 12)}</div>' for t, b, f in (("Thực đơn hôm nay", TERRA, CREAM), ("Chỉ đường Google Maps", CREAM, ESP), ("Gọi món qua Zalo", MOSS, CREAM),
                                                                                       ("TikTok · Facebook · Instagram", CREAM, ESP), ("Đồ lưu niệm", BUTTER, ESP)))
              + '</div>', 230, 470)
sig = (f'<div style="display: flex; gap: 14px; align-items: center; padding: 14px; border: 2px solid {SAND}; border-radius: 12px; background: #FFFFFF">'
       f'{sym(56)}<div style="border-left: 2px solid {TERRA}; padding-left: 14px">{T("[HỌ TÊN]", 14, 700)}{T("[CHỨC VỤ] · Xo em", 12, 500, MUTED)}{T("[SỐ ĐIỆN THOẠI] · " + HANDLE, 12, 500, MUTED)}{H("có em lo", 16)}</div></div>')
wifiqr = (f'<div style="display: flex; gap: 14px; align-items: center">{qr(90)}<div>{D("Quét để vào Wi‑Fi", 18)}{T("Mã QR chứa tên mạng và mật khẩu, khách khỏi phải gõ.", 12, 400, MUTED, "max-width: 200px")}</div></div>')
p = B.header("20 — TRANG WEB &amp; TRANG LIÊN KẾT", "Một chạm là tới em") + f'''<div style="display: grid; grid-template-columns: minmax(0, 2.2fr) minmax(0, 1fr); gap: 20px; flex-grow: 1; min-height: 0">
<div style="display: flex; flex-direction: column; gap: 16px">{box(K("TRANG WEB · TRANG ĐẦU") + web)}
<div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px">{box(K("CHỮ KÝ EMAIL") + sig)}{box(K("QR WI‑FI") + wifiqr)}</div></div>
{box(K("TRANG LIÊN KẾT (DÁN VÀO TIỂU SỬ MẠNG XÃ HỘI)") + links, "#FFFFFF", "18px", "align-items: center")}
</div>'''
pages.append(("Web.dc.html", "Trang web và trang liên kết", "20 Web & liên kết", p))

# ---------------- 21: thông số ----------------
specs = [("Logo", "SVG (in, làm biển) · PNG nền trong suốt (mạng xã hội, tài liệu)", "Màu chính · nền tối · đen · trắng"),
         ("Linh vật", "PNG nền trong suốt: Boss, Em Ngả, Em Ngơ", "Không kéo giãn, không đổi màu"),
         ("Màu", "Đất Nung #C8553D · Kem Sữa #F6EEDF · Nâu Cà Phê #2B1D16 · Vàng Bơ #F2C14E · Rêu Sồi #5E7A4A · Cát Mịn #E8D5B5", "In thử để chốt màu CMYK"),
         ("Phông chữ", "Baloo 2 (tiêu đề) · Be Vietnam Pro (nội dung) · Patrick Hand (viết tay)", "Miễn phí trên Google Fonts, giấy phép mở OFL"),
         ("Facebook", "Ảnh bìa 820 × 312 · ảnh đại diện vuông", "Ảnh đại diện: biểu tượng nền Đất Nung"),
         ("Instagram", "Bài 1080 × 1080 hoặc 1080 × 1350 · tin 24 giờ 1080 × 1920", "Xen kẽ màu theo lưới 9 ô"),
         ("TikTok", "Video dọc 1080 × 1920 · ảnh đại diện vuông", "Tên " + HANDLE),
         ("Google Maps", "Logo vuông · ảnh bìa ngang · ảnh thật của quán", "Kích thước chuẩn xem trong trang quản lý hồ sơ"),
         ("Zalo", "Ảnh đại diện vuông · ảnh bìa ngang · ứng dụng nhỏ theo khung Zalo", "Kích thước chuẩn xem trong trang quản lý Zalo"),
         ("In ấn", "File in thêm 3mm tràn lề · chữ cách mép ≥ 5mm", "Gửi xưởng bản SVG/PDF, không gửi ảnh chụp màn hình")]
srow = "".join(f'<div style="display: grid; grid-template-columns: 140px minmax(0, 1.6fr) minmax(0, 1fr); gap: 18px; padding: 11px 0; border-top: 1.5px solid {SAND}">{T(a, 15, 700, TERRA)}{T(b, 14)}{T(c, 13, 400, MUTED)}</div>' for a, b, c in specs)
p = B.header("21 — THÔNG SỐ &amp; BỘ FILE", "Gửi xưởng là làm được ngay") + box(
    f'<div style="display: grid; grid-template-columns: 140px minmax(0, 1.6fr) minmax(0, 1fr); gap: 18px">{K("HẠNG MỤC")}{K("FILE &amp; KÍCH THƯỚC")}{K("GHI CHÚ")}</div>' + srow, "#FFFFFF", "22px 28px", "flex-grow: 1")
pages.append(("Specs.dc.html", "Thông số và bộ file", "21 Thông số & bộ file", p))

# ---------------- write + extend canvas ----------------
cj = os.path.join(ROOT, "canvas.json")
c = json.load(open(cj))
for i, (f, t) in enumerate((("Merch1.dc.html", "09 Sổ & văn phòng phẩm"), ("Merch2.dc.html", "10 Quà lưu niệm"), ("Merch3.dc.html", "11 Cà phê & hộp quà"))):
    n = 9 + i
    c["boards"][f] = {"x": (n % 3) * (B.W + 80), "y": (n // 3) * (B.H + 120), "w": B.W, "h": B.H, "title": t}
    if f not in c["order"]:
        c["order"].append(f)
base_n = 12
for i, (f, title, short, inner) in enumerate(pages):
    open(os.path.join(ROOT, f), "w").write(B.page("Xo em – " + title, B.board(inner)))
    n = base_n + i
    c["boards"][f] = {"x": (n % 3) * (B.W + 80), "y": (n // 3) * (B.H + 120), "w": B.W, "h": B.H, "title": short}
    if f not in c["order"]:
        c["order"].append(f)
json.dump(c, open(cj, "w"), ensure_ascii=False)
json.dump(c["order"], open(os.path.join(os.path.dirname(ROOT), "order.json"), "w"))
print(len(c["order"]))
