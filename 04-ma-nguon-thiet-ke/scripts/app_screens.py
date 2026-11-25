from app_common import *

files = {}   # name -> (title, html, w, h, kind)

# ======================= CUSTOMER APP =======================
def menu_row(name, desc, color, href="C03_Item.dc.html", tag=None):
    t = badge(tag) if tag else ""
    return link(href, card(f'<div style="display: flex; gap: 12px; align-items: center">{thumb(64, color)}'
                          f'<div style="flex-grow: 1; min-width: 0; display: flex; flex-direction: column; gap: 2px">'
                          f'<div style="display: flex; gap: 6px; align-items: center">{T(name, 15, 700)}{t}</div>{T(desc, 12, 400, MUTED)}{T("[GIÁ]", 13, 700, TERRA)}</div>'
                          f'<span style="width: 34px; height: 34px; border-radius: 12px; background: {TERRA}; display: flex; align-items: center; justify-content: center">{ic("plus", 18, CREAM, 2.4)}</span></div>', 10), "display: block")

# C01 home
body = f'''<div style="background: {TERRA}; border-radius: 22px; padding: 18px; position: relative; overflow: hidden; height: 168px; box-sizing: border-box">
{H("chào bạn, bàn 12 nè", 18, BUTTER)}{D("Ghé vào. Ngồi xuống.<br>Có em lo.", 26, CREAM)}{T("Gọi món tại bàn, em mang ra tận nơi.", 13, 500, CREAM, "margin-top: 6px; max-width: 190px")}
<div style="position: absolute; right: -4px; bottom: -6px">{boss(104)}</div></div>
<div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px">
{link("C02_Menu.dc.html", card(f'{ic("table", 24, TERRA)}{T("Gọi tại bàn", 15, 700, ESP, "margin-top: 8px")}{T("Bàn 12 · tầng 1", 12, 400, MUTED)}', 14), "display: block")}
{link("C02_Menu.dc.html", card(f'{ic("bag", 24, TERRA)}{T("Mang đi", 15, 700, ESP, "margin-top: 8px")}{T("Hẹn giờ lấy", 12, 400, MUTED)}', 14), "display: block")}
</div>
{link("C07_Points.dc.html", card(f'<div style="display: flex; align-items: center; gap: 12px">{nga(78)}<div style="flex-grow: 1">{T("Thẻ thân với em", 15, 700)}{T("Còn 6 ly nữa, ly thứ 10 Em Ngơ mời", 12, 500, MUTED)}<div style="height: 8px; border-radius: 99px; background: {SAND}; margin-top: 8px; overflow: hidden"><div style="width: 40%; height: 100%; background: {TERRA}"></div></div></div>{ic("chev", 18, MUTED)}</div>', 12, "", "#FFF8EC"), "display: block")}
<div style="display: flex; justify-content: space-between; align-items: baseline">{D("Món quen của bạn", 19)}{link("C02_Menu.dc.html", T("Xem thực đơn", 13, 700, TERRA))}</div>
{menu_row("Cà phê phin sữa", "Lần trước: ít đá, ít ngọt", TERRA, tag="Món quen")}
{menu_row("Bánh chuối nướng", "Nướng mới mỗi sáng", KRAFT)}'''
files["C01_Home"] = ("Khách · Trang chủ", screen("Xo em", body, CUST_TABS, "home", right_extra=ic("bell", 22)), 390, 844, "cust")

# C02 menu
cats = "".join(chip(c, c == "Cà phê") for c in ("Cà phê", "Trà &amp; cây", "Bánh", "Đồ lưu niệm"))
rows = "".join(menu_row(n, d, c, tag=("Bán chạy" if n == "Cà phê muối" else None)) for n, d, c, k in MENU[:4])
body = f'''<div style="display: flex; align-items: center; gap: 10px; height: 46px; border-radius: 14px; background: {WHITE}; border: 1.5px solid {LINE}; padding: 0 14px">{ic("search", 18, MUTED)}{T("Tìm món…", 14, 400, MUTED)}</div>
<div style="display: flex; gap: 8px; overflow: hidden">{cats}</div>{rows}'''
foot = link("C04_Cart.dc.html", f'<span style="display: flex; align-items: center; justify-content: space-between; background: {ESP}; color: {CREAM}; border-radius: 14px; padding: 0 16px; min-height: 52px; {SANS}; font-weight: 700; font-size: 15px"><span>2 món · [TỔNG]</span><span style="display: flex; align-items: center; gap: 6px">Xem giỏ {ic("chev", 18, CREAM)}</span></span>', "display: block")
files["C02_Menu"] = ("Khách · Thực đơn", screen("Thực đơn", body, CUST_TABS, "menu", footer=foot), 390, 844, "cust")

# C03 item detail
def opt_group(title, opts, sel):
    return (f'<div style="display: flex; flex-direction: column; gap: 8px">{T(title, 14, 700)}<div style="display: flex; gap: 8px; flex-wrap: wrap">'
            + "".join(chip(o, o == sel) for o in opts) + '</div></div>')
body = f'''<div style="height: 210px; border-radius: 22px; background: {SAND}; display: flex; align-items: center; justify-content: center; position: relative">{sym(150)}
<div style="position: absolute; left: 14px; top: 14px">{badge("Món quen", BUTTER)}</div></div>
<div style="display: flex; justify-content: space-between; align-items: flex-start"><div>{D("Cà phê phin sữa", 24)}{T("Phin nhôm, cà phê rang mộc, sữa đặc vừa đủ ngọt.", 13, 400, MUTED)}</div>{D("[GIÁ]", 18, TERRA)}</div>
{opt_group("Cỡ ly", ["Vừa", "Lớn"], "Vừa")}{opt_group("Đá", ["Bình thường", "Ít đá", "Không đá"], "Ít đá")}{opt_group("Độ ngọt", ["Bình thường", "Ít ngọt", "Không đường"], "Ít ngọt")}
<div style="display: flex; flex-direction: column; gap: 6px">{T("Ghi chú cho các em", 14, 700)}<div style="height: 46px; border-radius: 12px; border: 1.5px solid {LINE}; background: {WHITE}; display: flex; align-items: center; padding: 0 12px">{T("Ví dụ: pha đậm hơn một chút", 13, 400, MUTED)}</div></div>'''
foot = f'<div style="display: flex; gap: 12px; align-items: center">{qty("1")}<div style="flex-grow: 1">{pbtn("Thêm vào giỏ · [GIÁ]", "C02_Menu.dc.html")}</div></div>'
files["C03_Item"] = ("Khách · Chi tiết món", screen("Chi tiết món", body, back="C02_Menu.dc.html", footer=foot), 390, 844, "cust")

# C04 cart
def cart_row(n, o, c):
    return card(f'<div style="display: flex; gap: 12px; align-items: center">{thumb(56, c)}<div style="flex-grow: 1">{T(n, 15, 700)}{T(o, 12, 400, MUTED)}{T("[GIÁ]", 13, 700, TERRA)}</div>{qty("1")}</div>', 10)
body = f'''{card(f'<div style="display: flex; align-items: center; gap: 10px">{ic("table", 22, TERRA)}<div style="flex-grow: 1">{T("Gọi tại bàn 12", 14, 700)}{T("Các em mang ra tận bàn", 12, 400, MUTED)}</div>{T("Đổi", 13, 700, TERRA)}</div>', 12)}
{cart_row("Cà phê phin sữa", "Vừa · ít đá · ít ngọt", TERRA)}{cart_row("Bánh chuối nướng", "1 phần", KRAFT)}
{link("C02_Menu.dc.html", f'<span style="display: flex; align-items: center; gap: 8px; {SANS}; font-weight: 700; font-size: 14px; color: {TERRA}">{ic("plus", 18, TERRA)}Thêm món</span>')}
{card(f'<div style="display: flex; flex-direction: column; gap: 8px">' + "".join(f'<div style="display: flex; justify-content: space-between">{T(a, 14, 400, MUTED)}{T(b, 14, 600)}</div>' for a, b in (("Tạm tính", "[SỐ TIỀN]"), ("Ưu đãi thẻ thân với em", "−[SỐ TIỀN]"))) + f'<div style="border-top: 1.5px dashed {LINE}; padding-top: 8px; display: flex; justify-content: space-between">{T("Tổng", 16, 700)}{D("[TỔNG]", 20, TERRA)}</div></div>', 14)}'''
files["C04_Cart"] = ("Khách · Giỏ hàng", screen("Giỏ của bạn", body, back="C02_Menu.dc.html", footer=pbtn("Đặt món", "C05_Checkout.dc.html")), 390, 844, "cust")

# C05 checkout
def pay(name, sub, on, icon):
    dot = f'<span style="width: 12px; height: 12px; border-radius: 50%; background: {TERRA}"></span>' if on else ""
    return card(f'<div style="display: flex; align-items: center; gap: 12px">{ic(icon, 22, TERRA)}<div style="flex-grow: 1">{T(name, 14, 700)}{T(sub, 12, 400, MUTED)}</div>'
                f'<span style="width: 22px; height: 22px; border-radius: 50%; border: 2px solid {TERRA if on else LINE}; display: flex; align-items: center; justify-content: center">{dot}</span></div>', 12, f"border-color: {TERRA if on else LINE}")
body = f'''{K("Nhận món")}{card(f'<div style="display: flex; gap: 8px">{chip("Tại bàn 12", True)}{chip("Mang đi")}</div>', 10)}
{K("Thanh toán")}{pay("Ví ZaloPay", "Trả ngay trong Zalo", True, "wallet")}{pay("Chuyển khoản QR", "Quét mã QR của quán", False, "qr")}{pay("Trả tại quầy", "Tiền mặt hoặc thẻ", False, "receipt")}
{K("Thông tin")}{card(f'{T("[TÊN KHÁCH] · [SỐ ĐIỆN THOẠI]", 14, 600)}{T("Lấy từ tài khoản Zalo, bấm để sửa", 12, 400, MUTED)}', 12)}
{T("Đặt món là bạn đồng ý với điều khoản của quán. Món làm xong em báo qua Zalo.", 12, 400, MUTED)}'''
files["C05_Checkout"] = ("Khách · Thanh toán", screen("Xác nhận đơn", body, back="C04_Cart.dc.html", footer=pbtn("Thanh toán [TỔNG]", "C06_Track.dc.html")), 390, 844, "cust")

# C06 tracking
steps = [("Đã nhận đơn", "[GIỜ]", True), ("Các em đang pha", "Em Ngơ đang pha ly của bạn", True), ("Đang mang ra bàn 12", "", False), ("Xong, chúc bạn ngon miệng", "", False)]
st = ""
for i, (a, b, done) in enumerate(steps):
    dot = (f'<span style="width: 26px; height: 26px; border-radius: 50%; background: {MOSS if done else WHITE}; border: 2px solid {MOSS if done else LINE}; display: flex; align-items: center; justify-content: center">{ic("check", 14, CREAM, 3) if done else ""}</span>')
    line = f'<span style="width: 2px; flex-grow: 1; background: {MOSS if done and i < 1 else LINE}; margin: 2px 0"></span>' if i < len(steps) - 1 else ""
    st += f'<div style="display: flex; gap: 12px; min-height: 58px"><div style="display: flex; flex-direction: column; align-items: center">{dot}{line}</div><div>{T(a, 15, 700, ESP if done else MUTED)}{T(b, 12, 400, MUTED)}</div></div>'
body = f'''<div style="background: {WHITE}; border: 1.5px solid {LINE}; border-radius: 22px; padding: 16px; display: flex; gap: 12px; align-items: center">{ngo(88)}<div>{K("Đơn #[MÃ ĐƠN]")}{D("Đang pha cho bạn", 22)}{T("Dự kiến: khoảng [SỐ] phút", 13, 500, MUTED)}</div></div>
{card(st, 16)}
{card(f'<div style="display: flex; justify-content: space-between">{T("Cà phê phin sữa ×1", 14)}{T("[GIÁ]", 14, 600)}</div><div style="display: flex; justify-content: space-between; margin-top: 6px">{T("Bánh chuối nướng ×1", 14)}{T("[GIÁ]", 14, 600)}</div>', 14)}'''
foot = f'<div style="display: flex; gap: 10px"><div style="flex: 1">{pbtn("Gọi nhân viên", None, WHITE, ESP, border=LINE, icon="bell")}</div><div style="flex: 1">{pbtn("Gọi thêm", "C02_Menu.dc.html")}</div></div>'
files["C06_Track"] = ("Khách · Theo dõi đơn", screen("Đơn của bạn", body, CUST_TABS, "order", footer=foot), 390, 844, "cust")

# C07 points
stamps = "".join(f'<span style="width: 44px; height: 44px; border-radius: 50%; border: 2px {"solid" if i < 4 or i == 9 else "dashed"} {ESP}; display: flex; align-items: center; justify-content: center; background: {WHITE if i == 9 else "transparent"}">{sym(32, body=TERRA if i < 4 else BUTTER) if i < 4 or i == 9 else ""}</span>' for i in range(10))
offers = [("Ly thứ hai giảm [X]%", "Hạn: [NGÀY]", BUTTER), ("Tặng sticker Em Ngả, Em Ngơ", "Khi gọi từ 2 món", SAND)]
body = f'''<div style="background: {SAND}; border-radius: 22px; padding: 16px; display: flex; flex-direction: column; gap: 12px; align-items: center">
<div style="display: flex; justify-content: space-between; width: 100%; align-items: center">{D("Thẻ thân với em", 20)}{sym(36)}</div>
<div style="display: grid; grid-template-columns: repeat(5, 44px); gap: 12px">{stamps}</div>{H("4/10 ly · ly thứ 10 Em Ngơ mời!", 18)}</div>
<div style="display: flex; justify-content: center">{nga(200)}</div>
{K("Ưu đãi của bạn")}''' + "".join(card(f'<div style="display: flex; gap: 12px; align-items: center"><span style="width: 44px; height: 44px; border-radius: 12px; background: {c}; display: flex; align-items: center; justify-content: center">{ic("gift", 22)}</span><div style="flex-grow: 1">{T(a, 14, 700)}{T(b, 12, 400, MUTED)}</div>{T("Dùng", 13, 700, TERRA)}</div>', 12) for a, b, c in offers)
files["C07_Points"] = ("Khách · Tích điểm", screen("Tích điểm", body, CUST_TABS, "points"), 390, 844, "cust")

# C08 account
items = [("receipt", "Lịch sử đơn"), ("star", "Món yêu thích"), ("cal", "Đặt bàn trước"), ("pin", "Chỉ đường tới quán"), ("phone", "Gọi cho quán"), ("wifi", "Wi‑Fi của quán")]
lst = "".join(f'<div style="display: flex; align-items: center; gap: 12px; min-height: 52px; border-bottom: 1px solid {LINE}">{ic(i, 20, TERRA)}{T(t, 15, 500, ESP, "flex-grow: 1")}{ic("chev", 18, MUTED)}</div>' for i, t in items)
body = f'''<div style="display: flex; gap: 14px; align-items: center">
<div style="width: 64px; height: 64px; border-radius: 50%; background: {TERRA}; display: flex; align-items: center; justify-content: center">{sym(46, body=BUTTER)}</div>
<div>{D("[TÊN KHÁCH]", 22)}{T("Khách thân · 4 ly trong thẻ", 13, 500, MUTED)}</div></div>
{card(lst, "4px 14px")}
{card(f'<div style="display: flex; gap: 12px; align-items: center">{boss(56)}<div>{T("Góp ý cho quán", 14, 700)}{T("Nói với Boss điều bạn chưa ưng, em sửa ngay.", 12, 400, MUTED)}</div></div>', 12)}'''
files["C08_Account"] = ("Khách · Tài khoản", screen("Tôi", body, CUST_TABS, "me"), 390, 844, "cust")

# ======================= STAFF / MANAGER APP =======================
# S01 check-in
body = f'''<div style="display: flex; flex-direction: column; align-items: center; gap: 6px; padding-top: 10px">{boss(110)}{D("Chào [TÊN NHÂN VIÊN]", 24)}{T("Ca sáng · 07:00 – 15:00", 14, 500, MUTED)}</div>
{card(f'<div style="display: flex; flex-direction: column; align-items: center; gap: 6px">{K("Giờ hiện tại")}{D("[GIỜ:PHÚT]", 44, ESP)}{T("Đang ở trong phạm vi quán", 13, 600, MOSS)}</div>', 18)}
{card(f'<div style="display: flex; flex-direction: column; gap: 10px">' + "".join(f'<div style="display: flex; justify-content: space-between">{T(a, 14, 400, MUTED)}{T(b, 14, 600)}</div>' for a, b in (("Vị trí", "Pha chế"), ("Cùng ca", "[NHÂN VIÊN 2], [NHÂN VIÊN 3]"), ("Công tháng này", "[SỐ] / 28"))) + '</div>', 14)}
{card(f'{T("Việc đầu ca", 14, 700)}' + "".join(f'<div style="display: flex; gap: 10px; align-items: center; min-height: 34px">{ic("check", 16, MOSS)}{T(t, 13)}</div>' for t in ("Kiểm tra máy pha, máy xay", "Đếm tiền đầu ca", "Bật đèn biển, nhạc nhỏ")), 14)}'''
files["S01_CheckIn"] = ("Nhân viên · Vào ca", screen("Xo em · Nhân viên", body, footer=pbtn("Vào ca", "S02_Queue.dc.html", icon="clock")), 390, 844, "staff")

# S02 queue
def order_card(no, table, items, status, color, mins, href="S03_Order.dc.html"):
    its = "".join(f'<div style="display: flex; gap: 8px">{T(q, 14, 700, TERRA)}<div>{T(n, 14, 600)}{T(o, 12, 400, MUTED) if o else ""}</div></div>' for q, n, o in items)
    return link(href, card(f'<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px"><div style="display: flex; gap: 8px; align-items: center">{D(table, 18)}{T("#" + no, 12, 600, MUTED)}</div><div style="display: flex; gap: 6px; align-items: center">{ic("clock", 14, RED if mins >= 8 else MUTED)}{T(f"{mins} phút", 12, 700, RED if mins >= 8 else MUTED)}</div></div>'
                           f'<div style="display: flex; flex-direction: column; gap: 6px">{its}</div><div style="margin-top: 10px; display: flex; justify-content: space-between; align-items: center">{badge(status, color, CREAM if color in (TERRA, MOSS) else ESP)}{T("Mở đơn", 13, 700, TERRA)}</div>', 12,
                           f"border-left: 6px solid {color}"), "display: block")
body = f'''<div style="display: flex; gap: 8px">{chip("Mới · 2", True)}{chip("Đang pha · 1")}{chip("Xong · [SỐ]")}</div>
{order_card("[MÃ]", "Bàn 12", [("1×", "Cà phê phin sữa", "Vừa · ít đá · ít ngọt"), ("1×", "Bánh chuối nướng", "")], "Mới", TERRA, 9)}
{order_card("[MÃ]", "Mang đi", [("2×", "Trà đào cam sả", "Lớn · bình thường")], "Mới", TERRA, 3)}
{order_card("[MÃ]", "Bàn 4", [("1×", "Bạc xỉu", "Không đá")], "Đang pha", BUTTER, 5)}'''
files["S02_Queue"] = ("Nhân viên · Hàng đợi pha chế", screen("Đơn cần pha", body, STAFF_TABS, "orders", right_extra=ic("bell", 22)), 390, 844, "staff")

# S03 order detail
body = f'''{card(f'<div style="display: flex; justify-content: space-between; align-items: center">{D("Bàn 12", 26)}{badge("Mới", TERRA, CREAM)}</div>{T("Đơn #[MÃ] · đặt lúc [GIỜ] · qua Zalo", 13, 400, MUTED)}{T("Đã thanh toán ZaloPay", 13, 700, MOSS, "margin-top: 4px")}', 14)}
{card(f'<div style="display: flex; flex-direction: column; gap: 12px">' + "".join(f'<div style="display: flex; gap: 12px; align-items: center">{thumb(52, c)}<div style="flex-grow: 1">{T(n, 15, 700)}{T(o, 12, 500, MUTED)}</div>{D(q, 20, TERRA)}</div>' for n, o, q, c in (("Cà phê phin sữa", "Vừa · ít đá · ít ngọt", "×1", TERRA), ("Bánh chuối nướng", "Hâm nóng", "×1", KRAFT))) + '</div>', 14)}
{card(f'<div style="display: flex; gap: 10px; align-items: flex-start">{ic("edit", 18, TERRA)}<div>{T("Ghi chú của khách", 13, 700)}{T("“Pha đậm hơn một chút”", 13)}</div></div>', 12, "", "#FFF8EC")}
<div style="display: flex; gap: 8px">{chip("Báo hết món")}{chip("In phiếu")}{chip("Gọi khách")}</div>'''
foot = f'<div style="display: flex; gap: 10px"><div style="flex: 1">{pbtn("Bắt đầu pha", "S02_Queue.dc.html", BUTTER, ESP)}</div><div style="flex: 1">{pbtn("Xong, mang ra", "S04_Tables.dc.html", MOSS, CREAM, icon="check")}</div></div>'
files["S03_Order"] = ("Nhân viên · Chi tiết đơn", screen("Chi tiết đơn", body, back="S02_Queue.dc.html", footer=foot), 390, 844, "staff")

# S04 tables
def tbl(n, state):
    cfg = {"trống": (WHITE, ESP, LINE), "có khách": (SAND, ESP, KRAFT), "chờ món": (TERRA, CREAM, TERRA), "gọi nhân viên": (BUTTER, ESP, ESP)}[state]
    return (f'<div style="aspect-ratio: 1 / 1; border-radius: 16px; background: {cfg[0]}; border: 2px solid {cfg[2]}; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 2px">'
            f'{D(n, 22, cfg[1])}{T(state, 10, 700, cfg[1])}</div>')
floor1 = [("1", "có khách"), ("2", "trống"), ("3", "chờ món"), ("4", "chờ món"), ("5", "trống"), ("6", "gọi nhân viên"), ("7", "có khách"), ("8", "trống"), ("9", "trống")]
legend = "".join(f'<div style="display: flex; gap: 6px; align-items: center"><span style="width: 14px; height: 14px; border-radius: 4px; background: {b}; border: 2px solid {bd}"></span>{T(t, 12)}</div>' for b, bd, t in ((WHITE, LINE, "Trống"), (SAND, KRAFT, "Có khách"), (TERRA, TERRA, "Chờ món"), (BUTTER, ESP, "Gọi nhân viên")))
body = f'''<div style="display: flex; gap: 8px">{chip("Tầng 1", True)}{chip("Tầng 2")}{chip("Sân ngoài")}</div>
<div style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 10px">{"".join(tbl(a, b) for a, b in floor1)}</div>
<div style="display: flex; flex-wrap: wrap; gap: 12px">{legend}</div>
{card(f'<div style="display: flex; gap: 10px; align-items: center">{ic("bell", 22, ESP)}<div style="flex-grow: 1">{T("Bàn 6 đang gọi nhân viên", 14, 700)}{T("[SỐ] phút trước", 12, 400, MUTED)}</div>{pbtn("Tới ngay", None, ESP, CREAM, False, 13)}</div>', 12, "", "#FFF8EC")}'''
files["S04_Tables"] = ("Nhân viên · Sơ đồ bàn", screen("Sơ đồ bàn", body, STAFF_TABS, "tables"), 390, 844, "staff")

# S05 stock toggle
def toggle(on):
    return (f'<button type="button" aria-pressed="{"true" if on else "false"}" style="all: unset; cursor: pointer; width: 50px; height: 30px; border-radius: 99px; background: {MOSS if on else LINE}; position: relative; flex-shrink: 0">'
            f'<span style="position: absolute; top: 3px; {"right" if on else "left"}: 3px; width: 24px; height: 24px; border-radius: 50%; background: {WHITE}"></span></button>')
rows = "".join(f'<div style="display: flex; gap: 12px; align-items: center; min-height: 58px; border-bottom: 1px solid {LINE}">{thumb(44, c)}<div style="flex-grow: 1">{T(n, 14, 700)}{T("Còn bán" if on else "Tạm hết", 12, 600, MOSS if on else RED)}</div>{toggle(on)}</div>'
               for (n, d, c, k), on in zip(MENU, (True, True, True, False, True, True, True, False, True)))
body = f'''{T("Tắt một món là món đó ẩn ngay trên ứng dụng của khách.", 13, 400, MUTED)}{card(rows, "2px 14px")}'''
files["S05_Stock"] = ("Nhân viên · Còn / hết món", screen("Còn / hết món", body, STAFF_TABS, "items"), 390, 844, "staff")

# S06 manager dashboard
def kpi(label, icon):
    return card(f'<div style="display: flex; gap: 8px; align-items: center">{ic(icon, 18, TERRA)}{T(label, 12, 600, MUTED)}</div>{D("[SỐ]", 24, ESP, "margin-top: 6px")}{T("so với hôm qua: [±%]", 11, 500, MUTED)}', 12)
bars = "".join(f'<div style="display: flex; flex-direction: column; align-items: center; gap: 4px; flex: 1"><div style="width: 100%; height: {h}px; border-radius: 6px 6px 2px 2px; background: {TERRA if i == 5 else SAND}"></div>{T(l, 10, 600, MUTED)}</div>'
               for i, (h, l) in enumerate(zip((40, 70, 55, 90, 60, 110, 80), ("7h", "9h", "11h", "13h", "15h", "17h", "19h"))))
top = "".join(f'<div style="display: flex; gap: 10px; align-items: center; min-height: 40px">{T(str(i+1), 14, 700, TERRA)}{T(n, 14, 600, ESP, "flex-grow: 1")}{T("[SỐ] ly", 13, 600, MUTED)}</div>' for i, n in enumerate(("Cà phê phin sữa", "Bạc xỉu", "Trà đào cam sả")))
body = f'''<div style="display: flex; gap: 8px">{chip("Hôm nay", True)}{chip("7 ngày")}{chip("Tháng này")}</div>
<div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px">{kpi("Doanh thu", "wallet")}{kpi("Số đơn", "receipt")}{kpi("Khách thân quay lại", "users")}{kpi("Đơn qua Zalo", "qr")}</div>
{card(f'{T("Đơn theo giờ (minh họa)", 14, 700)}<div style="display: flex; align-items: flex-end; gap: 6px; height: 130px; margin-top: 10px">{bars}</div>', 14)}
{card(f'{T("Món bán chạy", 14, 700)}{top}', "12px 14px")}'''
files["S06_Dashboard"] = ("Quản lý · Tổng quan", screen("Tổng quan", body, STAFF_TABS, "manage", right_extra=link("S08_MenuAdmin.dc.html", ic("gear", 22))), 390, 844, "staff")

# S07 shifts
days = ("T2", "T3", "T4", "T5", "T6", "T7", "CN")
def shiftrow(name, cells):
    c = "".join(f'<span style="height: 30px; border-radius: 8px; background: {({"S": BUTTER, "C": TERRA, "T": MOSS, "-": WHITE})[x]}; border: 1.5px solid {LINE}; display: flex; align-items: center; justify-content: center; {SANS}; font-size: 11px; font-weight: 700; color: {CREAM if x in "CT" else ESP}">{x if x != "-" else ""}</span>' for x in cells)
    return f'<div style="display: grid; grid-template-columns: 96px repeat(7, minmax(0, 1fr)); gap: 4px; align-items: center">{T(name, 12, 600)}{c}</div>'
hdr = f'<div style="display: grid; grid-template-columns: 96px repeat(7, minmax(0, 1fr)); gap: 4px">{T("", 11)}' + "".join(T(d, 11, 700, MUTED, "text-align: center") for d in days) + '</div>'
legend = "".join(f'<div style="display: flex; gap: 6px; align-items: center"><span style="width: 14px; height: 14px; border-radius: 4px; background: {b}"></span>{T(t, 12)}</div>' for b, t in ((BUTTER, "S: sáng"), (TERRA, "C: chiều"), (MOSS, "T: tối")))
att = "".join(f'<div style="display: flex; justify-content: space-between; align-items: center; min-height: 40px; border-bottom: 1px solid {LINE}">{T(n, 14, 600)}{T(v, 13, 600, c)}</div>' for n, v, c in (("[NHÂN VIÊN 1]", "Vào ca [GIỜ] · đúng giờ", MOSS), ("[NHÂN VIÊN 2]", "Vào ca [GIỜ] · trễ [SỐ] phút", RED), ("[NHÂN VIÊN 3]", "Chưa vào ca", MUTED)))
body = f'''<div style="display: flex; justify-content: space-between; align-items: center">{D("Tuần [SỐ TUẦN]", 20)}{pbtn("Xếp ca", None, ESP, CREAM, False, 13, "plus")}</div>
{card(hdr + "".join(shiftrow(n, c) for n, c in (("[NHÂN VIÊN 1]", "SSSCC-S"), ("[NHÂN VIÊN 2]", "CC-SSCT"), ("[NHÂN VIÊN 3]", "TTTT-CC"))) , 12, "display: flex; flex-direction: column; gap: 8px")}
<div style="display: flex; gap: 14px">{legend}</div>
{K("Chấm công hôm nay")}{card(att, "2px 14px")}
{card(f'<div style="display: flex; justify-content: space-between; align-items: center">{T("Công tháng này (chuẩn 28 công)", 13, 600)}{T("Xuất bảng lương", 13, 700, TERRA)}</div>', 12)}'''
files["S07_Shifts"] = ("Quản lý · Ca làm và chấm công", screen("Ca làm", body, STAFF_TABS, "shift"), 390, 844, "staff")

# S08 menu admin + stock
inv = [("Cà phê hạt rang", "[SỐ] kg", "Sắp hết", RED), ("Sữa đặc", "[SỐ] hộp", "Đủ dùng", MOSS), ("Sữa tươi", "[SỐ] lít", "Sắp hết", RED), ("Đào ngâm", "[SỐ] hộp", "Đủ dùng", MOSS)]
invr = "".join(f'<div style="display: flex; align-items: center; gap: 10px; min-height: 44px; border-bottom: 1px solid {LINE}">{ic("box", 18, TERRA)}{T(n, 14, 600, ESP, "flex-grow: 1")}{T(q, 13, 500, MUTED)}{badge(s, c, CREAM)}</div>' for n, q, s, c in inv)
mrows = "".join(f'<div style="display: flex; align-items: center; gap: 10px; min-height: 52px; border-bottom: 1px solid {LINE}">{thumb(40, c)}<div style="flex-grow: 1">{T(n, 14, 700)}{T(k, 12, 400, MUTED)}</div>{T("[GIÁ]", 13, 700, TERRA)}{ic("edit", 18, MUTED)}</div>' for n, d, c, k in MENU[:4])
body = f'''<div style="display: flex; gap: 8px">{chip("Thực đơn", True)}{chip("Kho nguyên liệu")}{chip("Ưu đãi")}</div>
{card(mrows, "2px 14px")}{pbtn("Thêm món mới", None, WHITE, ESP, icon="plus", border=LINE)}
{K("Kho nguyên liệu")}{card(f'<div style="display: flex; gap: 8px; align-items: center; margin-bottom: 6px">{ic("alert", 18, RED)}{T("2 nguyên liệu sắp hết, nhớ đặt hàng", 13, 700, RED)}</div>' + invr, "10px 14px")}'''
files["S08_MenuAdmin"] = ("Quản lý · Thực đơn và kho", screen("Thực đơn &amp; kho", body, STAFF_TABS, "manage", back="S06_Dashboard.dc.html"), 390, 844, "staff")
