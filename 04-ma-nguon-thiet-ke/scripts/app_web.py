from app_common import *
from app_screens import files

WRAP = "width: 100%; max-width: 1200px; margin: 0 auto; padding: 0 32px; box-sizing: border-box"

def nav(active):
    items = [("Thực đơn", "W02_Menu.dc.html"), ("Quà lưu niệm", "W04_Shop.dc.html"), ("Sự kiện", "W06_Events.dc.html"),
             ("Câu chuyện", "W05_Story.dc.html"), ("Góc đọc", "W08_Blog.dc.html"), ("Đặt bàn", "W03_Booking.dc.html")]
    links = "".join(link(h, f'<span style="{SANS}; font-size: 15px; font-weight: {700 if t.startswith(active) else 500}; color: {TERRA if t.startswith(active) else ESP}; padding: 10px 4px; display: inline-block">{t}</span>') for t, h in items)
    return (f'<header style="background: {CREAM}; border-bottom: 1px solid {LINE}"><div style="{WRAP}; display: flex; flex-wrap: wrap; gap: 12px 28px; align-items: center; justify-content: space-between; min-height: 76px">'
            f'{link("W01_Home.dc.html", B.lockup(40, 30, tag=False, gap=8))}<nav aria-label="Trang web" style="display: flex; flex-wrap: wrap; gap: 6px 22px; align-items: center">{links}'
            f'{pbtn("Gọi món qua Zalo", "C01_Home.dc.html", TERRA, CREAM, False, 14, "qr")}</nav></div></header>')

def footer():
    cols = [("Ghé quán", ["93 Marina, Ecopark", "Văn Giang, Hưng Yên", "07:00–23:00 mỗi ngày"]),
            ("Liên hệ", ["[SỐ ĐIỆN THOẠI]", "Zalo: Xo em", "@xoem.ecopark"]),
            ("Khám phá", [link("W04_Shop.dc.html", "Quà lưu niệm"), link("W06_Events.dc.html", "Sự kiện &amp; workshop"), link("W05_Story.dc.html", "Câu chuyện"), link("W07_Careers.dc.html", "Tuyển dụng")])]
    c = "".join(f'<div style="display: flex; flex-direction: column; gap: 8px; min-width: 180px">{K(t, BUTTER)}' + "".join(T(x, 14, 400, CREAM) for x in xs) + '</div>' for t, xs in cols)
    return (f'<footer style="background: {ESP}; padding: 56px 0 40px"><div style="{WRAP}; display: flex; flex-wrap: wrap; gap: 40px; justify-content: space-between">'
            f'<div style="display: flex; flex-direction: column; gap: 10px; max-width: 320px">{B.lockup(52, 40, body=TERRA, ink=CREAM, white=ESP, tagcolor=BUTTER, gap=10)}{H("Ghé vào. Ngồi xuống. Có em lo.", 20, BUTTER)}</div>{c}</div>'
            f'<div style="{WRAP}; margin-top: 36px">{T("© Xo em · Ecopark", 12, 400, "#BFAF9E")}</div></footer>')

def section(inner, bg=CREAM, pad="72px 0"):
    return f'<section style="background: {bg}; padding: {pad}"><div style="{WRAP}">{inner}</div></section>'

def shell(active, inner):
    return f'<div style="width: 100%; background: {CREAM}; {SANS}; color: {ESP}">{nav(active)}{inner}{footer()}</div>'

# ---------------- W01 home ----------------
hero = section(f'''<div style="display: flex; flex-wrap: wrap; gap: 32px; align-items: center">
<div style="flex: 1 1 420px; display: flex; flex-direction: column; gap: 18px">{K("Quán cà phê pha chậm · Ecopark")}
<h1 style="margin: 0; {DISPLAY}; font-weight: 800; font-size: clamp(44px, 6vw, 76px); line-height: 1; color: {ESP}">Ghé vào.<br>Ngồi xuống.<br><span style="color: {TERRA}">Có em lo.</span></h1>
{T("Ghế mềm, cà phê pha phin, Wi‑Fi mạnh và ba em Boss, Em Ngả, Em Ngơ lo cho bạn từ ly đầu tiên tới lúc về.", 18, 400, ESP, "max-width: 520px")}
<div style="display: flex; flex-wrap: wrap; gap: 12px">{pbtn("Gọi món qua Zalo", "C01_Home.dc.html", TERRA, CREAM, False, 16, "qr")}{pbtn("Chỉ đường", None, WHITE, ESP, False, 16, "pin", LINE)}</div>
{T("Mở cửa 07:00–23:00 mỗi ngày · 93 Marina, Ecopark", 14, 600, MUTED)}</div>
<div style="flex: 1 1 420px; position: relative; min-height: 420px; border-radius: 36px; overflow: hidden; background: {TERRA}; display: flex; align-items: flex-end; justify-content: center">
<div style="position: absolute; inset: 0; opacity: 0.35">{pat(620, 460, TERRA, BUTTER, ESP, CREAM, CREAM, 1.0)}</div>
<div style="position: relative; display: flex; align-items: flex-end; gap: 4px; padding-bottom: 28px">{boss(130)}{nga(300)}{ngo(130)}</div></div></div>''', CREAM, "56px 0 72px")

vals = [("Chậm", "Pha phin từng ly. Không ai hối, ngồi bao lâu cũng được.", "clock"),
        ("Mềm", "Ghế sofa, ánh sáng dịu, nhạc nhỏ. Chỗ để ngồi lâu không mỏi.", "home"),
        ("Thân", "Quán xưng em, nhớ món quen của bạn, hỏi han như người nhà.", "users")]
values = section(f'''<div style="display: flex; flex-direction: column; gap: 28px">{K("Ba điều ở Xo em")}<h2 style="margin: 0; {DISPLAY}; font-weight: 800; font-size: 44px; line-height: 1.05">Chậm, mềm và thân</h2>
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 20px">''' + "".join(
    card(f'<div style="width: 52px; height: 52px; border-radius: 16px; background: {CREAM}; display: flex; align-items: center; justify-content: center">{ic(i, 26, TERRA)}</div>{D(a, 30, TERRA, "margin-top: 14px")}{T(b, 16, 400, ESP, "margin-top: 6px")}', 24) for a, b, i in vals) + '</div></div>', WHITE)

feat = "".join(link("W02_Menu.dc.html", card(f'<div style="height: 180px; border-radius: 14px; background: {SAND}; display: flex; align-items: center; justify-content: center">{sym(110, body=c)}</div>'
                                            f'<div style="display: flex; justify-content: space-between; align-items: baseline; margin-top: 14px">{D(n, 22)}{T("[GIÁ]", 15, 700, TERRA)}</div>{T(d, 14, 400, MUTED)}', 14), "display: block")
               for n, d, c, k in (MENU[1], MENU[3], MENU[4], MENU[7]))
menu_sec = section(f'''<div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: flex-end; gap: 16px; margin-bottom: 28px"><div>{K("Thực đơn")}<h2 style="margin: 6px 0 0; {DISPLAY}; font-weight: 800; font-size: 44px">Món các em hay pha</h2></div>{link("W02_Menu.dc.html", T("Xem cả thực đơn →", 16, 700, TERRA))}</div>
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 20px">{feat}</div>''')

zones = [("Góc sofa", "Ghế êm, đèn vàng, hợp ngồi đọc sách", TERRA), ("Bàn dài làm việc", "Ổ cắm từng chỗ, Wi‑Fi mạnh", MOSS),
         ("Tầng 2 yên tĩnh", "Nhạc nhỏ hơn, hợp học bài, họp nhóm", BUTTER), ("Sân ngoài trời", "Gió Ecopark, hợp đi cùng thú cưng", KRAFT)]
zone_html = "".join(card(f'<div style="height: 150px; border-radius: 14px; background: {c}; display: flex; align-items: center; justify-content: center">{T("[ẢNH GÓC NGỒI]", 13, 700, CREAM if c in (TERRA, MOSS) else ESP)}</div>{D(a, 22, ESP, "margin-top: 12px")}{T(b, 14, 400, MUTED)}', 14) for a, b, c in zones)
zones_sec = section(f'''{K("Góc ngồi")}<h2 style="margin: 6px 0 28px; {DISPLAY}; font-weight: 800; font-size: 44px">Chọn chỗ hợp với bạn</h2>
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 20px">{zone_html}</div>''', WHITE)

mascots = [(boss(150), "Boss", "Chiếc ghế đầu tiên của quán. Ai ngồi lên là bị giữ chân.", "“Ngồi đi, vội gì.”"),
           (nga(230), "Em Ngả", "Rồng nệm ngủ trên ghế sofa, chuyên trông ca chiều.", "“Năm phút nữa thôi…”"),
           (ngo(150), "Em Ngơ", "Rồng rêu phụ quầy, hay quên ly cà phê trên sừng.", "“Ơ… mình vừa định làm gì nhỉ?”")]
masc_html = "".join(card(f'<div style="height: 190px; display: flex; align-items: flex-end; justify-content: center">{img}</div>{D(n, 28, TERRA, "margin-top: 12px; text-align: center")}{T(d, 15, 400, ESP, "text-align: center")}{H(q, 20, MUTED, "text-align: center; margin-top: 6px")}', 22) for img, n, d, q in mascots)
masc_sec = section(f'''<div style="text-align: center">{K("Gặp các em")}<h2 style="margin: 6px 0 28px; {DISPLAY}; font-weight: 800; font-size: 44px">Ba em nhà Xo em</h2></div>
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px">{masc_html}</div>''')

app_sec = section(f'''<div style="display: flex; flex-wrap: wrap; gap: 40px; align-items: center">
<div style="flex: 1 1 380px; display: flex; flex-direction: column; gap: 16px">{K("Gọi món không cần đứng dậy", BUTTER)}<h2 style="margin: 0; {DISPLAY}; font-weight: 800; font-size: 44px; color: {CREAM}; line-height: 1.05">Quét QR ở bàn,<br>gọi món qua Zalo</h2>
{T("Không cần tải ứng dụng. Gọi món, trả tiền, tích điểm thẻ thân với em ngay trong Zalo.", 17, 400, CREAM, "max-width: 480px")}
<div style="display: flex; flex-wrap: wrap; gap: 12px">{pbtn("Mở trong Zalo", "C01_Home.dc.html", BUTTER, ESP, False, 16, "qr")}</div></div>
<div style="flex: 1 1 320px; display: flex; justify-content: center; gap: 20px; align-items: center">
<div style="width: 180px; height: 180px; border-radius: 24px; background: {CREAM}; border: 4px dashed {BUTTER}; display: flex; align-items: center; justify-content: center">{T("[MÃ QR ZALO]", 13, 700, MUTED)}</div>{nga(220)}</div></div>''', TERRA)

visit = section(f'''<div style="display: flex; flex-wrap: wrap; gap: 28px; align-items: stretch">
<div style="flex: 1 1 340px; display: flex; flex-direction: column; gap: 14px">{K("Ghé quán")}<h2 style="margin: 0; {DISPLAY}; font-weight: 800; font-size: 44px">93 Marina, Ecopark</h2>
{T("Văn Giang, Hưng Yên · đối diện sân bóng Edison", 16, 500, MUTED)}
{card("".join(f'<div style="display: flex; gap: 12px; align-items: center; min-height: 44px">{ic(i, 20, TERRA)}{T(t, 15, 500)}</div>' for i, t in (("clock", "Mở cửa 07:00–23:00 mỗi ngày"), ("phone", "[SỐ ĐIỆN THOẠI]"), ("wifi", "Wi‑Fi miễn phí, ổ cắm điện"))), "10px 18px")}
<div style="display: flex; flex-wrap: wrap; gap: 12px">{pbtn("Chỉ đường Google Maps", None, TERRA, CREAM, False, 15, "pin")}{pbtn("Đặt bàn", "W03_Booking.dc.html", WHITE, ESP, False, 15, "cal", LINE)}</div></div>
<div style="flex: 1 1 460px; min-height: 340px; border-radius: 28px; overflow: hidden; background: #E9E4D6; position: relative; border: 1.5px solid {LINE}">
<svg width="100%" height="100%" viewBox="0 0 600 340" preserveAspectRatio="xMidYMid slice" aria-hidden="true" style="position: absolute; inset: 0"><path d="M0,230 Q240,180 600,250" stroke="#FFFFFF" stroke-width="26" fill="none"></path><path d="M170,0 L250,340" stroke="#FFFFFF" stroke-width="18"></path><path d="M440,0 Q400,170 480,340" stroke="#FFFFFF" stroke-width="14" fill="none"></path><rect x="40" y="40" width="90" height="70" rx="10" fill="#CFE0C3"></rect><rect x="480" y="50" width="90" height="100" rx="12" fill="#BFD7EA"></rect></svg>
<div style="position: absolute; left: 50%; top: 42%; transform: translate(-50%, -50%); display: flex; flex-direction: column; align-items: center; gap: 6px"><div style="width: 74px; height: 74px; border-radius: 50%; background: {TERRA}; border: 4px solid {ESP}; display: flex; align-items: center; justify-content: center">{sym(52, body=BUTTER)}</div>{badge("Xo em", ESP, CREAM)}</div>
<div style="position: absolute; left: 16px; bottom: 16px">{badge("Bản đồ minh họa · nhúng Google Maps khi làm thật", WHITE, MUTED)}</div></div></div>''', WHITE)

home = shell("Trang chủ", hero + values + menu_sec + zones_sec + masc_sec + app_sec + visit)
files["W01_Home"] = ("Website · Trang chủ", home, 1440, 3900, "web")

# ---------------- W02 menu ----------------
def mcard(n, d, c):
    return card(f'<div style="display: flex; gap: 16px; align-items: center">{thumb(88, c)}<div style="flex-grow: 1; min-width: 0">{D(n, 21)}{T(d, 14, 400, MUTED)}</div>{T("[GIÁ]", 16, 700, TERRA, "white-space: nowrap")}</div>', 16)
groups = ""
for cat, label in (("Cà phê", "Cà phê pha chậm"), ("Trà", "Trà &amp; cây · nhà Em Ngơ"), ("Bánh", "Bánh · nhà Em Ngả")):
    items = "".join(mcard(n, d, c) for n, d, c, k in MENU if k == cat)
    groups += f'<div style="display: flex; flex-direction: column; gap: 16px; margin-bottom: 40px"><h2 style="margin: 0; {DISPLAY}; font-weight: 800; font-size: 34px; color: {ESP}">{label}</h2><div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(340px, 1fr)); gap: 16px">{items}</div></div>'
tabs = "".join(chip(t, t == "Tất cả") for t in ("Tất cả", "Cà phê", "Trà &amp; cây", "Bánh", "Đồ lưu niệm"))
menu_page = section(f'''<div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: flex-end; gap: 20px; margin-bottom: 24px">
<div>{K("Thực đơn")}<h1 style="margin: 6px 0 0; {DISPLAY}; font-weight: 800; font-size: 60px; line-height: 1">Hôm nay uống gì?</h1>{T("Giá và món đang để minh họa, điền thực đơn thật trước khi đưa lên.", 15, 400, MUTED, "margin-top: 8px")}</div>
<div style="display: flex; align-items: center; gap: 10px; min-height: 48px; min-width: 280px; border-radius: 14px; background: {WHITE}; border: 1.5px solid {LINE}; padding: 0 16px">{ic("search", 18, MUTED)}<label style="{SANS}; font-size: 14px; color: {MUTED}">Tìm món <input type="search" style="border: none; outline: none; background: transparent; width: 160px"></label></div></div>
<div style="display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 36px">{tabs}</div>{groups}
{card(f'<div style="display: flex; flex-wrap: wrap; gap: 20px; align-items: center; justify-content: space-between"><div style="display: flex; gap: 16px; align-items: center">{ngo(90)}<div>{D("Ngồi ở quán? Gọi qua Zalo nhé", 24)}{T("Quét QR trên bàn, các em mang ra tận nơi.", 15, 400, MUTED)}</div></div>{pbtn("Mở ứng dụng gọi món", "C02_Menu.dc.html", TERRA, CREAM, False, 15, "qr")}</div>', 22, "", "#FFF8EC")}''', CREAM, "56px 0 72px")
files["W02_Menu"] = ("Website · Thực đơn", shell("Thực đơn", menu_page), 1440, 2050, "web")

# ---------------- W03 booking ----------------
def field(label, ph, kind="text", half=False):
    return (f'<label style="display: flex; flex-direction: column; gap: 6px; {"flex: 1 1 220px" if half else "width: 100%"}">{T(label, 14, 700)}'
            f'<input type="{kind}" placeholder="{ph}" style="min-height: 48px; border-radius: 12px; border: 1.5px solid {LINE}; background: {WHITE}; padding: 0 14px; {SANS}; font-size: 15px; color: {ESP}; box-sizing: border-box; width: 100%"></label>')
zone_pick = "".join(chip(z, z == "Góc sofa") for z in ("Góc sofa", "Bàn dài làm việc", "Tầng 2 yên tĩnh", "Sân ngoài trời", "Để các em chọn"))
form = card(f'''<div style="display: flex; flex-direction: column; gap: 16px">{D("Giữ chỗ trước", 30)}{T("Các em xác nhận qua Zalo trong vòng [SỐ] phút.", 14, 400, MUTED)}
<div style="display: flex; flex-wrap: wrap; gap: 14px">{field("Tên của bạn", "Ví dụ: Lan", half=True)}{field("Số điện thoại / Zalo", "09xx xxx xxx", "tel", True)}</div>
<div style="display: flex; flex-wrap: wrap; gap: 14px">{field("Ngày", "dd/mm/yyyy", "text", True)}{field("Giờ", "hh:mm", "text", True)}{field("Số người", "2", "number", True)}</div>
<div style="display: flex; flex-direction: column; gap: 8px">{T("Khu vực muốn ngồi", 14, 700)}<div style="display: flex; flex-wrap: wrap; gap: 8px">{zone_pick}</div></div>
<label style="display: flex; flex-direction: column; gap: 6px">{T("Ghi chú", 14, 700)}<textarea placeholder="Sinh nhật, cần ổ cắm, đi cùng thú cưng…" style="min-height: 96px; border-radius: 12px; border: 1.5px solid {LINE}; padding: 12px 14px; {SANS}; font-size: 15px; box-sizing: border-box; width: 100%; resize: vertical"></textarea></label>
{pbtn("Gửi yêu cầu giữ chỗ", None, TERRA, CREAM, True, 16, "check")}</div>''', 28)
faqs = [("Có chỗ đỗ xe không?", "[THÔNG TIN CHỖ ĐỖ XE]"), ("Mang thú cưng được không?", "[CHÍNH SÁCH THÚ CƯNG]"), ("Có tổ chức sinh nhật, họp nhóm không?", "Có. Bạn ghi chú khi giữ chỗ, các em chuẩn bị bàn phù hợp."),
        ("Ngồi làm việc cả ngày được không?", "Được. Wi‑Fi mạnh, có ổ cắm, cứ ngồi lâu, có em lo.")]
faq = "".join(f'<details style="border-bottom: 1px solid {LINE}; padding: 14px 0"><summary style="{SANS}; font-size: 16px; font-weight: 700; color: {ESP}; cursor: pointer">{q}</summary>{T(a, 15, 400, MUTED, "margin-top: 8px")}</details>' for q, a in faqs)
side = (f'<div style="display: flex; flex-direction: column; gap: 20px; flex: 1 1 340px">'
        + card(f'<div style="display: flex; gap: 14px; align-items: center">{boss(80)}<div>{D("Thích ghé luôn?", 22)}{T("Không cần giữ chỗ, cứ tới là có ghế.", 14, 400, MUTED)}</div></div>'
               + "".join(f'<div style="display: flex; gap: 12px; align-items: center; min-height: 44px">{ic(i, 20, TERRA)}{T(t, 15, 500)}</div>' for i, t in (("pin", "93 Marina, Ecopark, Văn Giang, Hưng Yên"), ("clock", "07:00–23:00 mỗi ngày"), ("phone", "[SỐ ĐIỆN THOẠI]"), ("qr", "Zalo: Xo em"))), 22)
        + card(f'{D("Câu hỏi hay gặp", 22)}{faq}', 22) + '</div>')
booking = section(f'''{K("Đặt bàn &amp; liên hệ")}<h1 style="margin: 6px 0 28px; {DISPLAY}; font-weight: 800; font-size: 60px; line-height: 1">Để em giữ chỗ cho bạn</h1>
<div style="display: flex; flex-wrap: wrap; gap: 24px; align-items: flex-start"><div style="flex: 2 1 520px; min-width: 0">{form}</div>{side}</div>''', CREAM, "56px 0 72px")
files["W03_Booking"] = ("Website · Đặt bàn và liên hệ", shell("Đặt bàn", booking), 1440, 1500, "web")
