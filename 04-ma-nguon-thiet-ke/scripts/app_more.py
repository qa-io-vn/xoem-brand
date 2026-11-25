from app_common import *
from app_web import files, section, shell, WRAP, field

GREEN_BG = "#EEF3E8"; RED_BG = "#FBEAE6"; WARM = "#FFF8EC"

def overlay(base, sheet):
    return (f'<div style="position: relative; width: 390px; height: 844px; overflow: hidden">{base}'
            f'<div style="position: absolute; inset: 0; background: rgba(43, 29, 22, 0.55)"></div>'
            f'<div role="dialog" aria-modal="true" style="position: absolute; left: 0; right: 0; bottom: 0; background: {CREAM}; border-radius: 26px 26px 0 0; padding: 12px 20px 28px; display: flex; flex-direction: column; gap: 14px">'
            f'<span style="align-self: center; width: 44px; height: 5px; border-radius: 99px; background: {LINE}"></span>{sheet}</div></div>')

def state(img, title, text, actions):
    return (f'<div style="flex-grow: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 10px; text-align: center; padding: 0 12px">'
            f'{img}{D(title, 26, ESP, "margin-top: 8px")}{T(text, 14, 400, MUTED, "max-width: 290px")}'
            f'<div style="display: flex; flex-direction: column; gap: 10px; width: 100%; margin-top: 14px">{actions}</div></div>')

def circle_icon(name, bg, fg, size=96):
    return f'<div style="width: {size}px; height: {size}px; border-radius: 50%; background: {bg}; display: flex; align-items: center; justify-content: center">{ic(name, size // 2, fg, 2.2)}</div>'

def row(icon, title, sub, right="", icolor=TERRA, ibg=CREAM, href=None, unread=False):
    dot = f'<span style="width: 8px; height: 8px; border-radius: 50%; background: {TERRA}; flex-shrink: 0"></span>' if unread else ""
    inner = (f'<div style="display: flex; gap: 12px; align-items: flex-start; padding: 12px 0; border-bottom: 1px solid {LINE}">'
             f'<span style="width: 40px; height: 40px; border-radius: 12px; background: {ibg}; display: flex; align-items: center; justify-content: center; flex-shrink: 0">{ic(icon, 20, icolor)}</span>'
             f'<div style="flex-grow: 1; min-width: 0">{T(title, 14, 700)}{T(sub, 12, 400, MUTED)}</div>{right}{dot}</div>')
    return link(href, inner, "display: block") if href else inner

def toggle(on):
    return (f'<button type="button" aria-pressed="{"true" if on else "false"}" style="all: unset; cursor: pointer; width: 50px; height: 30px; border-radius: 99px; background: {MOSS if on else LINE}; position: relative; flex-shrink: 0">'
            f'<span style="position: absolute; top: 3px; {"right" if on else "left"}: 3px; width: 24px; height: 24px; border-radius: 50%; background: {WHITE}"></span></button>')

# ======================= CUSTOMER: STATES & EXTRA =======================
# C09 Zalo consent
home_dim = screen("Xo em", f'<div style="height: 168px; border-radius: 22px; background: {TERRA}"></div><div style="height: 110px; border-radius: 18px; background: {WHITE}"></div><div style="height: 90px; border-radius: 18px; background: {WHITE}"></div>', CUST_TABS, "home")
perm = "".join(f'<div style="display: flex; gap: 12px; align-items: center; min-height: 52px; border-bottom: 1px solid {LINE}">{ic(i, 20, TERRA)}<div style="flex-grow: 1">{T(a, 14, 700)}{T(b, 12, 400, MUTED)}</div>{ic("check", 18, MOSS)}</div>'
               for i, a, b in (("user", "Tên và ảnh đại diện Zalo", "Để các em gọi đúng tên bạn"), ("phone", "Số điện thoại", "Để tích điểm thẻ thân với em, báo khi món xong")))
sheet = (f'<div style="display: flex; gap: 12px; align-items: center">{boss(64)}<div>{D("Cho em biết bạn là ai nhé?", 21)}{T("Chỉ cần một lần, lần sau vào là em nhớ.", 13, 400, MUTED)}</div></div>'
         f'<div>{perm}</div>{T("Em không gửi tin quảng cáo nếu bạn chưa đồng ý. Xem <u>chính sách dữ liệu</u>.", 12, 400, MUTED)}'
         f'{pbtn("Cho phép", "C01_Home.dc.html")}{pbtn("Để sau, xem thực đơn trước", "C02_Menu.dc.html", WHITE, ESP, border=LINE)}')
files["C09_Consent"] = ("Khách · Xin quyền Zalo lần đầu", overlay(home_dim, sheet), 390, 844, "morec")

# C10 empty cart
body = state(ngo(150), "Giỏ còn trống trơn", "Em Ngơ đứng đợi nãy giờ mà bạn chưa chọn món nào. Xem thực đơn nhé?",
             pbtn("Xem thực đơn", "C02_Menu.dc.html", icon="cup") + pbtn("Gọi lại món quen", "C14_History.dc.html", WHITE, ESP, border=LINE))
files["C10_EmptyCart"] = ("Khách · Giỏ trống", screen("Giỏ của bạn", body, back="C02_Menu.dc.html"), 390, 844, "morec")

# C11 payment failed
info = card("".join(f'<div style="display: flex; justify-content: space-between; min-height: 30px; align-items: center">{T(a, 13, 400, MUTED)}{T(b, 13, 600)}</div>' for a, b in (("Đơn", "#[MÃ] · Bàn 12"), ("Số tiền", "[TỔNG]"), ("Cách trả", "ZaloPay"), ("Lý do", "Bạn đã thoát khỏi trang thanh toán"))), "8px 14px", "width: 100%; text-align: left")
body = state(circle_icon("alert", RED_BG, RED), "Thanh toán chưa xong", "Tiền chưa bị trừ, đơn vẫn giữ cho bạn 10 phút. Nếu thấy đã trừ tiền, bạn báo các em nhé.",
             info + pbtn("Thử lại", "C06_Track.dc.html") + pbtn("Đổi cách trả", "C05_Checkout.dc.html", WHITE, ESP, border=LINE) + link("C06_Track.dc.html", T("Trả tiền mặt tại quầy", 14, 700, TERRA, "text-align: center; padding: 8px")))
files["C11_PayFail"] = ("Khách · Thanh toán thất bại", screen("Thanh toán", body, back="C05_Checkout.dc.html"), 390, 844, "morec")

# C12 notifications
notifs = [("cup", "Món của bạn đã xong", "Cà phê phin sữa đang trên đường ra bàn 12 · 2 phút trước", True, TERRA, CREAM),
          ("star", "Thêm 1 dấu thẻ thân với em", "Còn 5 ly nữa là có ly miễn phí · hôm nay", True, ESP, BUTTER),
          ("gift", "Ưu đãi cuối tuần", "[ƯU ĐÃI] cho khách ghé trước 10h · hôm qua", False, MOSS, GREEN_BG),
          ("cal", "Workshop làm sổ tay", "Còn [SỐ] chỗ cho buổi [NGÀY] · 3 ngày trước", False, TERRA, CREAM),
          ("receipt", "Hóa đơn #[MÃ]", "Đã thanh toán [TỔNG] · 5 ngày trước", False, MUTED, CREAM)]
body = f'''<div style="display: flex; gap: 8px">{chip("Tất cả", True)}{chip("Đơn hàng")}{chip("Ưu đãi")}</div>
{card("".join(row(i, a, b, "", fg, bg, unread=u) for i, a, b, u, fg, bg in notifs), "0 14px")}
{card(f'<div style="display: flex; gap: 12px; align-items: center">{ic("bell", 20, TERRA)}<div style="flex-grow: 1">{T("Nhận tin ưu đãi qua Zalo", 14, 700)}{T("Tối đa 2 tin mỗi tuần", 12, 400, MUTED)}</div>{toggle(True)}</div>', 12)}'''
files["C12_Notify"] = ("Khách · Thông báo", screen("Thông báo", body, back="C01_Home.dc.html"), 390, 844, "morec")

# C13 promotions
def voucher(title, cond, exp, color, on=True):
    return (f'<div style="display: flex; border-radius: 18px; overflow: hidden; border: 1.5px solid {LINE}; background: {WHITE}; opacity: {1 if on else 0.55}">'
            f'<div style="width: 86px; background: {color}; display: flex; align-items: center; justify-content: center; flex-shrink: 0; border-right: 2px dashed {CREAM}">{ic("gift", 30, CREAM)}</div>'
            f'<div style="flex-grow: 1; padding: 12px 14px; display: flex; flex-direction: column; gap: 4px">{T(title, 15, 700)}{T(cond, 12, 400, MUTED)}'
            f'<div style="display: flex; justify-content: space-between; align-items: center; margin-top: 4px">{T(exp, 11, 600, MUTED)}{T("Dùng ngay" if on else "Đã dùng", 13, 700, TERRA if on else MUTED)}</div></div></div>')
body = f'''<div style="display: flex; align-items: center; gap: 10px; height: 46px; border-radius: 14px; background: {WHITE}; border: 1.5px solid {LINE}; padding: 0 14px">{ic("gift", 18, MUTED)}{T("Nhập mã ưu đãi", 14, 400, MUTED, "flex-grow: 1")}{T("Áp dụng", 13, 700, TERRA)}</div>
{voucher("Ly thứ 10 em mời", "Đủ 9 dấu thẻ thân với em", "Không hết hạn", TERRA)}
{voucher("[ƯU ĐÃI] sáng sớm", "Ghé trước 10:00, thứ Hai – thứ Sáu", "Hết hạn [NGÀY]", MOSS)}
{voucher("Mừng tên mới Xo em", "Áp dụng 1 lần cho mỗi khách", "Hết hạn [NGÀY]", BUTTER)}
{voucher("Sinh nhật bạn", "Tặng 1 bánh khi đi từ 2 người", "Đã dùng [NGÀY]", KRAFT, False)}'''
files["C13_Promos"] = ("Khách · Ưu đãi của tôi", screen("Ưu đãi", body, CUST_TABS, "points"), 390, 844, "morec")

# C14 history
def hist(date, items, total, st, color):
    again = link("C04_Cart.dc.html", f'<span style="display: inline-flex; align-items: center; gap: 6px; min-height: 36px; padding: 0 14px; border-radius: 999px; border: 1.5px solid {TERRA}; {SANS}; font-size: 13px; font-weight: 700; color: {TERRA}">{ic("plus", 14, TERRA)}Đặt lại</span>')
    return card(f'<div style="display: flex; justify-content: space-between; align-items: center">{T(date, 12, 600, MUTED)}{badge(st, color, CREAM if color in (MOSS, RED) else ESP)}</div>'
                f'{T(items, 14, 700, ESP, "margin-top: 6px")}<div style="display: flex; justify-content: space-between; align-items: center; margin-top: 8px">{T(total, 14, 700, TERRA)}{again}</div>', 14)
body = f'''<div style="display: flex; gap: 8px">{chip("Tất cả", True)}{chip("Tại bàn")}{chip("Mang đi")}</div>
{hist("Hôm nay · Bàn 12", "Cà phê phin sữa, Bánh chuối nướng", "[TỔNG]", "Đang pha", BUTTER)}
{hist("[NGÀY] · Mang đi", "2× Trà đào cam sả", "[TỔNG]", "Hoàn thành", MOSS)}
{hist("[NGÀY] · Bàn 4", "Bạc xỉu, Croissant bơ", "[TỔNG]", "Hoàn thành", MOSS)}
{hist("[NGÀY] · Bàn 7", "Matcha sữa", "[TỔNG]", "Đã hủy · đã hoàn tiền", RED)}'''
files["C14_History"] = ("Khách · Lịch sử đơn", screen("Đơn đã đặt", body, CUST_TABS, "order"), 390, 844, "morec")

# C15 store closed
body = state(nga(220), "Các em đi ngủ rồi", "Xo em mở cửa từ 07:00 đến 23:00 mỗi ngày. Bạn vẫn xem thực đơn và hẹn giờ lấy món cho sáng mai được.",
             card(f'<div style="display: flex; gap: 10px; align-items: center">{ic("clock", 20, TERRA)}{T("Mở lại lúc 07:00 sáng mai", 14, 700)}</div>', 12, "width: 100%")
             + pbtn("Hẹn lấy món sáng mai", "C02_Menu.dc.html", icon="cal") + pbtn("Xem thực đơn", "C02_Menu.dc.html", WHITE, ESP, border=LINE))
files["C15_Closed"] = ("Khách · Quán đã đóng cửa", screen("Xo em", body, CUST_TABS, "home"), 390, 844, "morec")

# C16 offline
body = state(circle_icon("wifi", SAND, ESP), "Mất kết nối mạng", "Giỏ hàng của bạn vẫn được giữ. Kiểm tra Wi‑Fi hoặc dữ liệu di động rồi thử lại nhé.",
             card(f'<div style="display: flex; gap: 10px; align-items: center">{ic("wifi", 20, TERRA)}<div style="text-align: left">{T("Wi‑Fi của quán", 14, 700)}{T("Tên: [TÊN WIFI] · Mật khẩu: [MẬT KHẨU]", 12, 400, MUTED)}</div></div>', 12, "width: 100%")
             + pbtn("Thử lại", "C02_Menu.dc.html"))
files["C16_Offline"] = ("Khách · Mất mạng", screen("Thực đơn", body, CUST_TABS, "menu"), 390, 844, "morec")

# ======================= STAFF / MANAGER: EXTRA =======================
# S09 login
body = f'''<div style="flex-grow: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 12px; text-align: center">
{boss(130)}{D("Xo em · Nội bộ", 28)}{T("Dành cho nhân viên và quản lý. Đăng nhập bằng tài khoản Zalo đã được chủ quán thêm vào danh sách.", 14, 400, MUTED, "max-width: 300px")}
<div style="width: 100%; margin-top: 10px">{pbtn("Đăng nhập bằng Zalo", "S01_CheckIn.dc.html", "#0068FF", WHITE, icon="user")}</div></div>
{card(f'<div style="display: flex; gap: 10px; align-items: flex-start">{ic("alert", 20, RED)}<div>{T("Tài khoản chưa được cấp quyền", 14, 700, RED)}{T("Nhờ quản lý thêm số Zalo của bạn trong mục Nhân sự, rồi đăng nhập lại.", 12, 400, ESP)}</div></div>', 12, "", RED_BG)}
{T("Trạng thái lỗi ở trên chỉ hiện khi đăng nhập không thành công.", 11, 400, MUTED, "text-align: center")}'''
files["S09_Login"] = ("Nhân viên · Đăng nhập", screen("Xo em", body), 390, 844, "mores")

# S10 staff notifications
sn = [("receipt", "Đơn mới · Bàn 3", "2 món · đã thanh toán ZaloPay · vừa xong", True, CREAM, TERRA, "S03_Order.dc.html"),
      ("bell", "Bàn 6 gọi nhân viên", "1 phút trước", True, BUTTER, ESP, "S04_Tables.dc.html"),
      ("cal", "Yêu cầu giữ chỗ", "[TÊN KHÁCH] · 4 người · [NGÀY] [GIỜ] · cần xác nhận", True, CREAM, TERRA, None),
      ("box", "Sữa tươi sắp hết", "Còn [SỐ] lít · nên đặt hàng hôm nay", False, RED_BG, RED, "S08_MenuAdmin.dc.html"),
      ("users", "Đổi ca", "[NHÂN VIÊN 2] xin đổi ca chiều thứ Bảy với [NHÂN VIÊN 3]", False, GREEN_BG, MOSS, "S07_Shifts.dc.html")]
body = f'''<div style="display: flex; gap: 8px">{chip("Tất cả", True)}{chip("Đơn")}{chip("Kho")}{chip("Nhân sự")}</div>
{card("".join(row(i, a, b, "", fg, bg, h, u) for i, a, b, u, bg, fg, h in sn), "0 14px")}
{card(f'<div style="display: flex; gap: 10px; align-items: center">{ic("cal", 20, TERRA)}<div style="flex-grow: 1">{T("Xác nhận giữ chỗ", 14, 700)}{T("[TÊN KHÁCH] · 4 người", 12, 400, MUTED)}</div></div><div style="display: flex; gap: 8px; margin-top: 10px"><div style="flex: 1">{pbtn("Nhận", None, MOSS, CREAM, s=14)}</div><div style="flex: 1">{pbtn("Đề xuất giờ khác", None, WHITE, ESP, s=14, border=LINE)}</div></div>', 12, "", WARM)}'''
files["S10_Notify"] = ("Nhân viên · Thông báo", screen("Thông báo", body, STAFF_TABS, "orders", back="S02_Queue.dc.html"), 390, 844, "mores")

# S11 payroll by công
prow = lambda n, cong, luong, st, c: (f'<div style="display: grid; grid-template-columns: minmax(0, 1.4fr) 0.7fr 1fr; gap: 6px; align-items: center; min-height: 52px; border-bottom: 1px solid {LINE}">'
                                      f'<div>{T(n, 13, 700)}{T(st, 11, 600, c)}</div>{T(cong, 13, 600, ESP, "text-align: center")}{T(luong, 13, 700, TERRA, "text-align: right")}</div>')
body = f'''<div style="display: flex; justify-content: space-between; align-items: center">{D("Tháng [THÁNG]", 20)}{chip("Đổi tháng")}</div>
{card(f'<div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px"><div>{T("Tổng quỹ lương", 12, 600, MUTED)}{D("[SỐ TIỀN]", 22)}</div><div>{T("Công chuẩn", 12, 600, MUTED)}{D("28 công", 22)}</div></div>', 14)}
{card(f'<div style="display: grid; grid-template-columns: minmax(0, 1.4fr) 0.7fr 1fr; gap: 6px; padding-bottom: 6px; border-bottom: 1.5px solid {LINE}">{T("Nhân viên", 11, 700, MUTED)}{T("Công", 11, 700, MUTED, "text-align: center")}{T("Thực nhận", 11, 700, MUTED, "text-align: right")}</div>'
      + prow("[NHÂN VIÊN 1]", "[SỐ]", "[SỐ TIỀN]", "Đã chốt", MOSS) + prow("[NHÂN VIÊN 2]", "[SỐ]", "[SỐ TIỀN]", "Chờ xác nhận công", RED) + prow("[NHÂN VIÊN 3]", "[SỐ]", "[SỐ TIỀN]", "Đã chốt", MOSS), "10px 14px")}
{T("Thực nhận = lương tháng ÷ 28 × số công thực làm + phụ cấp − khấu trừ. Công lấy từ giờ vào, ra ca đã ghi.", 12, 400, MUTED)}'''
files["S11_Payroll"] = ("Quản lý · Bảng lương theo công", screen("Bảng lương", body, STAFF_TABS, "shift", back="S07_Shifts.dc.html",
                        footer=f'<div style="display: flex; gap: 10px"><div style="flex: 1">{pbtn("Xuất file", None, WHITE, ESP, s=14, border=LINE)}</div><div style="flex: 1">{pbtn("Chốt lương", None, ESP, CREAM, s=14, icon="check")}</div></div>'), 390, 844, "mores")

# S12 weekly report
days = ("T2", "T3", "T4", "T5", "T6", "T7", "CN")
hs = (60, 52, 66, 70, 88, 120, 110)
bars = "".join(f'<div style="display: flex; flex-direction: column; align-items: center; gap: 4px; flex: 1"><div style="width: 100%; height: {h}px; border-radius: 6px 6px 2px 2px; background: {TERRA if d in ("T7", "CN") else SAND}"></div>{T(d, 10, 600, MUTED)}</div>' for d, h in zip(days, hs))
mix = "".join(f'<div style="display: flex; flex-direction: column; gap: 4px"><div style="display: flex; justify-content: space-between">{T(a, 13, 600)}{T("[%]", 12, 700, MUTED)}</div><div style="height: 8px; border-radius: 99px; background: {CREAM}; overflow: hidden"><div style="width: {w}%; height: 100%; background: {c}"></div></div></div>'
              for a, w, c in (("Gọi tại bàn qua Zalo", 55, TERRA), ("Gọi tại quầy", 30, KRAFT), ("Mang đi", 15, MOSS)))
body = f'''<div style="display: flex; gap: 8px">{chip("Tuần này", True)}{chip("Tuần trước")}{chip("Chọn ngày")}</div>
<div style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 8px">''' + "".join(card(f'{T(a, 11, 600, MUTED)}{D("[SỐ]", 19, ESP, "margin-top: 4px")}', 10) for a in ("Doanh thu", "Số đơn", "Giá trị TB/đơn")) + f'''</div>
{card(f'<div style="display: flex; justify-content: space-between">{T("Doanh thu theo ngày", 14, 700)}{T("minh họa", 11, 500, MUTED)}</div><div style="display: flex; align-items: flex-end; gap: 6px; height: 130px; margin-top: 10px">{bars}</div>', 14)}
{card(f'{T("Khách gọi món bằng cách nào", 14, 700, ESP, "margin-bottom: 10px")}<div style="display: flex; flex-direction: column; gap: 10px">{mix}</div>', 14)}
{card(f'<div style="display: flex; gap: 10px; align-items: flex-start">{ic("alert", 18, TERRA)}<div>{T("Điều đáng chú ý", 13, 700)}{T("[GHI CHÚ TỰ ĐỘNG, ví dụ: tối thứ Bảy đông nhất, cần thêm 1 người ca tối]", 12, 400, ESP)}</div></div>', 12, "", WARM)}'''
files["S12_Report"] = ("Quản lý · Báo cáo tuần", screen("Báo cáo tuần", body, STAFF_TABS, "manage", back="S06_Dashboard.dc.html"), 390, 844, "mores")

# S13 promotions admin
def promo(title, rule, used, on, color):
    return card(f'<div style="display: flex; gap: 12px; align-items: center"><span style="width: 44px; height: 44px; border-radius: 12px; background: {color}; display: flex; align-items: center; justify-content: center; flex-shrink: 0">{ic("gift", 22, CREAM)}</span>'
                f'<div style="flex-grow: 1; min-width: 0">{T(title, 14, 700)}{T(rule, 12, 400, MUTED)}{T(used, 11, 600, MOSS if on else MUTED)}</div>{toggle(on)}</div>', 12)
body = f'''<div style="display: flex; gap: 8px">{chip("Đang chạy · 3", True)}{chip("Đã tắt")}{chip("Hết hạn")}</div>
{promo("Thẻ thân với em", "9 ly có dấu, ly thứ 10 miễn phí", "[SỐ] khách đang tích", True, TERRA)}
{promo("Sáng sớm", "[ƯU ĐÃI] trước 10:00, T2–T6", "Đã dùng [SỐ] lần tuần này", True, MOSS)}
{promo("Mừng tên mới Xo em", "1 lần/khách · đến [NGÀY]", "Đã dùng [SỐ] lần", True, BUTTER)}
{promo("Sinh nhật", "Tặng bánh khi đi từ 2 người", "Đang tắt", False, KRAFT)}
{card(f'<div style="display: flex; gap: 10px; align-items: flex-start">{ic("alert", 18, MUTED)}{T("Ưu đãi mới cần quản lý duyệt trước khi khách nhìn thấy. Mỗi khách nhận tối đa 2 tin ưu đãi qua Zalo mỗi tuần.", 12, 400, MUTED)}</div>', 12)}'''
files["S13_PromoAdmin"] = ("Quản lý · Ưu đãi", screen("Ưu đãi", body, STAFF_TABS, "manage", back="S06_Dashboard.dc.html", footer=pbtn("Tạo ưu đãi mới", None, ESP, CREAM, icon="plus")), 390, 844, "mores")

# S14 store switcher
dash_dim = screen("Tổng quan", f'<div style="height: 40px; border-radius: 12px; background: {WHITE}"></div><div style="height: 200px; border-radius: 18px; background: {WHITE}"></div><div style="height: 180px; border-radius: 18px; background: {WHITE}"></div>', STAFF_TABS, "manage")
def store(name, addr, st, on, color):
    dot = f'<span style="width: 12px; height: 12px; border-radius: 50%; background: {TERRA}"></span>' if on else ""
    return card(f'<div style="display: flex; gap: 12px; align-items: center">{thumb(48, color)}<div style="flex-grow: 1">{T(name, 15, 700)}{T(addr, 12, 400, MUTED)}{T(st, 11, 700, MOSS if "Đang mở" in st else MUTED)}</div>'
                f'<span style="width: 22px; height: 22px; border-radius: 50%; border: 2px solid {TERRA if on else LINE}; display: flex; align-items: center; justify-content: center">{dot}</span></div>', 12, f"border-color: {TERRA if on else LINE}")
sheet = (f'{D("Chọn cửa hàng", 22)}{T("Số liệu, đơn và ca làm sẽ đổi theo cửa hàng bạn chọn.", 13, 400, MUTED)}'
         + store("Xo em · 93 Marina", "Ecopark, Văn Giang", "Đang mở · [SỐ] đơn hôm nay", True, TERRA)
         + store("[CỬA HÀNG 2]", "[ĐỊA CHỈ]", "Đang mở · [SỐ] đơn hôm nay", False, MOSS)
         + store("Tất cả cửa hàng", "Xem số liệu gộp", "Chỉ chủ quán", False, ESP)
         + pbtn("Xem cửa hàng này", "S06_Dashboard.dc.html"))
files["S14_Stores"] = ("Quản lý · Đổi cửa hàng", overlay(dash_dim, sheet), 390, 844, "mores")

# ======================= WEBSITE: MORE PAGES =======================
def h1(kicker, title, sub=""):
    return (f'{K(kicker)}<h1 style="margin: 6px 0 0; {DISPLAY}; font-weight: 800; font-size: clamp(44px, 5vw, 64px); line-height: 1">{title}</h1>'
            + (T(sub, 17, 400, MUTED, "margin-top: 12px; max-width: 640px") if sub else ""))
def h2(t, c=ESP):
    return f'<h2 style="margin: 0; {DISPLAY}; font-weight: 800; font-size: 40px; line-height: 1.05; color: {c}">{t}</h2>'
def grid(items, minw=260, gap=20):
    return f'<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax({minw}px, 1fr)); gap: {gap}px">{"".join(items)}</div>'
def tile(color, label, h=190, art=None):
    art = art or sym(int(h * 0.55), body=color if color not in (SAND, CREAM) else TERRA)
    return f'<div style="height: {h}px; border-radius: 16px; background: {SAND if color != SAND else CREAM}; display: flex; align-items: center; justify-content: center; position: relative">{art}<div style="position: absolute; left: 12px; top: 12px">{badge(label, WHITE, MUTED)}</div></div>' if label else f'<div style="height: {h}px; border-radius: 16px; background: {SAND}; display: flex; align-items: center; justify-content: center">{art}</div>'

# W04 shop
prods = [("Sổ da in tên", "Bìa da bò, in tên hoặc chữ ký của bạn", TERRA, "Làm riêng"), ("Sổ kraft Em Ngả", "A5, giấy kem, 120 trang", KRAFT, None),
         ("Bút bi Boss", "Thân gỗ, mực xanh đen", ESP, None), ("Ly sứ Xo em", "350 ml, men kem", TERRA, "Bán chạy"),
         ("Túi vải Có em lo", "Vải canvas dày, quai dài", MOSS, None), ("Cà phê rang xay 250 g", "Gói kraft, hạt rang mộc tại quán", KRAFT, None),
         ("Bộ sticker ba em", "12 hình dán chống nước", BUTTER, None), ("Hộp quà Ngồi xuống", "Sổ + bút + cà phê gói", TERRA, "Quà tặng")]
pc = [card(f'{tile(c, b or "", 200)}<div style="display: flex; justify-content: space-between; align-items: baseline; margin-top: 14px; gap: 10px">{D(n, 21)}{T("[GIÁ]", 15, 700, TERRA, "white-space: nowrap")}</div>{T(d, 14, 400, MUTED)}'
           f'<div style="margin-top: 12px">{pbtn("Đặt in tên" if b == "Làm riêng" else "Giữ hàng qua Zalo", "C01_Home.dc.html", ESP if b == "Làm riêng" else WHITE, CREAM if b == "Làm riêng" else ESP, True, 14, None, None if b == "Làm riêng" else LINE)}</div>', 14) for n, d, c, b in prods]
shop = section(f'''<div style="display: flex; flex-wrap: wrap; gap: 24px; justify-content: space-between; align-items: flex-end; margin-bottom: 28px"><div>{h1("Quà lưu niệm", "Mang em về nhà", "Sổ, bút, ly và cà phê gói mang dấu Xo em. Mua tại quầy, hoặc nhắn Zalo để các em giữ hàng.")}</div>{ngo(150)}</div>
<div style="display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 28px">{"".join(chip(t, t == "Tất cả") for t in ("Tất cả", "Sổ &amp; bút", "Ly &amp; túi", "Cà phê gói", "Hộp quà"))}</div>
{grid(pc, 250)}''', CREAM, "56px 0 64px")
custom = section(f'''<div style="display: flex; flex-wrap: wrap; gap: 40px; align-items: center">
<div style="flex: 1 1 420px; display: flex; flex-direction: column; gap: 14px">{K("Làm riêng cho bạn", BUTTER)}{h2("Sổ da in tên, nhận trong [SỐ] ngày", CREAM)}
{T("Chọn màu da, in tên hoặc một câu ngắn lên bìa. Hợp làm quà sinh nhật, quà cảm ơn đồng nghiệp.", 17, 400, CREAM, "max-width: 520px")}
<div style="display: flex; flex-direction: column; gap: 8px">''' + "".join(f'<div style="display: flex; gap: 10px; align-items: center">{ic("check", 18, BUTTER)}{T(t, 15, 500, CREAM)}</div>' for t in ("Chọn màu: nâu cà phê, đất nung, rêu", "In tối đa [SỐ] ký tự", "Đặt từ 10 cuốn: in logo công ty")) + f'''</div>
<div style="display: flex; flex-wrap: wrap; gap: 12px; margin-top: 6px">{pbtn("Đặt in tên qua Zalo", "C01_Home.dc.html", BUTTER, ESP, False, 16, "edit")}{pbtn("Đăng ký workshop tự làm sổ", "W06_Events.dc.html", TERRA, CREAM, False, 16, None, CREAM)}</div></div>
<div style="flex: 1 1 340px; display: flex; justify-content: center"><div style="width: 300px; height: 380px; border-radius: 18px 28px 28px 18px; background: {TERRA}; border-left: 14px solid #A8432D; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 14px; box-shadow: 0 20px 40px rgba(0,0,0,0.25)">{sym(120, body=BUTTER)}{H("[TÊN CỦA BẠN]", 28, CREAM)}</div></div></div>''', ESP)
ship = section(grid([card(f'{ic(i, 26, TERRA)}{D(a, 22, ESP, "margin-top: 10px")}{T(b, 15, 400, MUTED)}', 22) for i, a, b in
                    (("pin", "Lấy tại quán", "Giữ hàng 3 ngày sau khi nhắn Zalo."), ("bag", "Giao trong Ecopark", "[PHÍ GIAO] · nhận trong ngày."), ("gift", "Gói quà miễn phí", "Kèm thiệp viết tay của các em."))], 260), WHITE, "56px 0")
files["W04_Shop"] = ("Website · Quà lưu niệm", shell("Quà lưu niệm", shop + custom + ship), 1440, 2400, "web")

# W05 story
miles = [("10/2026", "Mở cửa ở 93 Marina", "Hai tầng, sân ngoài trời, rất nhiều sofa."), ("[NGÀY X]", "Đổi tên thành Xo em", "Vẫn quán đó, vẫn các em đó. Chỉ đổi cái tên cho đúng tính mình."),
        ("Sắp tới", "Gọi món qua Zalo", "Quét QR ở bàn, các em mang ra tận nơi."), ("Sắp tới", "Workshop làm sổ", "Tự tay đóng một cuốn sổ da ở quán.")]
tl = "".join(f'<div style="display: flex; gap: 20px; align-items: flex-start"><div style="display: flex; flex-direction: column; align-items: center; flex-shrink: 0; width: 110px">{badge(d, TERRA if i < 2 else SAND, CREAM if i < 2 else ESP)}</div>'
             f'<div style="flex-grow: 1; padding-bottom: 26px; border-left: 2px solid {LINE}; padding-left: 20px">{D(a, 24)}{T(b, 16, 400, MUTED)}</div></div>' for i, (d, a, b) in enumerate(miles))
story = section(f'''<div style="display: flex; flex-wrap: wrap; gap: 40px; align-items: center">
<div style="flex: 1 1 480px">{h1("Câu chuyện", "Bắt đầu từ một chiếc ghế", "Xo em là quán cà phê pha chậm ở Ecopark. Trước đây quán tên Xofa. Bây giờ, quán tự xưng là “em”, vì muốn bạn thấy như được người nhà lo cho.")}</div>
<div style="flex: 1 1 360px; display: flex; justify-content: center; align-items: flex-end; gap: 6px; background: {TERRA}; border-radius: 32px; padding: 40px 20px 28px">{boss(130)}{nga(240)}{ngo(130)}</div></div>''', CREAM, "56px 0 64px")
name_sec = section(f'''<div style="display: flex; flex-wrap: wrap; gap: 40px">
<div style="flex: 1 1 380px; display: flex; flex-direction: column; gap: 14px">{K("Vì sao là Xo em")}{h2("“Xo” là chiếc sofa.<br>“Em” là người lo cho bạn.")}
{T("Ở Xo em, bạn không cần làm gì nhiều. Ghé vào, chọn một chỗ, ngồi xuống. Gọi món, trả tiền, tích điểm, dọn bàn, các em lo hết.", 17, 400, ESP)}</div>
<div style="flex: 1 1 380px">{grid([card(f'{D(a, 26, TERRA)}{T(b, 15, 400, ESP, "margin-top: 6px")}', 20) for a, b in (("Chậm", "Pha phin từng ly, không hối."), ("Mềm", "Ghế êm, đèn dịu, nhạc nhỏ."), ("Thân", "Nhớ món quen, hỏi han như người nhà."))], 200, 14)}</div></div>''', WHITE)
time_sec = section(f'''{K("Hành trình")}<div style="margin: 6px 0 28px">{h2("Từ ngày mở cửa tới giờ")}</div><div style="max-width: 820px">{tl}</div>''')
team = section(f'''<div style="text-align: center; margin-bottom: 28px">{K("Những người pha cho bạn")}<div style="margin-top: 6px">{h2("Đội ngũ Xo em")}</div></div>
{grid([card(f'<div style="height: 220px; border-radius: 16px; background: {c}; display: flex; align-items: center; justify-content: center">{T("[ẢNH NHÂN VIÊN]", 13, 700, CREAM if c in (TERRA, MOSS) else ESP)}</div>{D(n, 22, ESP, "margin-top: 12px")}{T(r, 14, 500, MUTED)}{H(q, 18, TERRA, "margin-top: 6px")}', 14)
       for n, r, q, c in (("[TÊN]", "Pha chế", "“[CÂU YÊU THÍCH]”", TERRA), ("[TÊN]", "Phục vụ", "“[CÂU YÊU THÍCH]”", MOSS), ("[TÊN]", "Quản lý cửa hàng", "“[CÂU YÊU THÍCH]”", BUTTER))], 260)}
<div style="text-align: center; margin-top: 28px">{pbtn("Muốn làm cùng các em? Xem vị trí đang tuyển", "W07_Careers.dc.html", ESP, CREAM, False, 15, "users")}</div>''', WHITE)
files["W05_Story"] = ("Website · Câu chuyện", shell("Câu chuyện", story + name_sec + time_sec + team), 1440, 2800, "web")

# W06 events & workshops
evs = [("Workshop tự đóng sổ da", "[THỨ], [NGÀY] · 09:00–11:30", "Tự cắt, khâu và in tên lên một cuốn sổ da A6. Đã gồm nguyên liệu và 1 đồ uống.", "[GIÁ]/người", "Còn [SỐ] chỗ", TERRA, True),
       ("Pha phin tại nhà cho người mới", "[THỨ], [NGÀY] · 15:00–16:30", "Chọn hạt, xay, ủ phin sao cho đậm mà không đắng. Mang về 100 g cà phê.", "[GIÁ]/người", "Còn [SỐ] chỗ", KRAFT, False),
       ("Tối đọc sách im lặng", "Tối thứ Sáu hằng tuần · 19:30–21:30", "Tắt nhạc, giảm đèn, mỗi người một cuốn. Không cần đăng ký.", "Miễn phí", "Ghé là có chỗ", MOSS, False),
       ("Đêm nhạc mộc trên sân", "[THỨ], [NGÀY] · 20:00", "Guitar, hát nhỏ, gió Ecopark. Gọi món như bình thường.", "Miễn phí", "Nên giữ chỗ", BUTTER, False)]
def ev(t, when, d, price, seats, c, feat):
    return card(f'''<div style="display: flex; flex-wrap: wrap; gap: 20px; align-items: stretch">
<div style="flex: 0 0 150px; border-radius: 16px; background: {c}; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 16px; min-height: 150px">{ic("cal", 34, CREAM if c in (TERRA, MOSS, KRAFT) else ESP)}{T("[NGÀY]", 15, 700, CREAM if c in (TERRA, MOSS, KRAFT) else ESP, "margin-top: 8px")}</div>
<div style="flex: 1 1 320px; display: flex; flex-direction: column; gap: 6px">{("<div style=\"align-self: flex-start\">" + badge("Nổi bật", BUTTER) + "</div>") if feat else ""}{D(t, 26)}{T(when, 14, 700, TERRA)}{T(d, 15, 400, ESP)}
<div style="display: flex; flex-wrap: wrap; gap: 16px; align-items: center; margin-top: 8px">{T(price, 15, 700)}{T(seats, 13, 600, MOSS)}</div></div>
<div style="flex: 0 0 auto; display: flex; align-items: center">{pbtn("Đăng ký" if "Miễn phí" not in price else "Giữ chỗ", "#dang-ky", TERRA if feat else WHITE, CREAM if feat else ESP, False, 15, None, None if feat else LINE)}</div></div>''', 18)
events = section(f'''<div style="display: flex; flex-wrap: wrap; gap: 24px; justify-content: space-between; align-items: flex-end; margin-bottom: 28px"><div>{h1("Sự kiện &amp; workshop", "Ngồi lâu hơn một chút", "Mỗi tháng các em bày vài buổi nhỏ: tự tay làm sổ, học pha phin, đọc sách, nghe nhạc.")}</div>{nga(200)}</div>
<div style="display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 24px">{"".join(chip(t, t == "Tháng [THÁNG]") for t in ("Tháng [THÁNG]", "Workshop", "Miễn phí", "Cuối tuần"))}</div>
<div style="display: flex; flex-direction: column; gap: 16px">{"".join(ev(*e) for e in evs)}</div>''', CREAM, "56px 0 64px")
reg = section(f'''<div id="dang-ky" style="display: flex; flex-wrap: wrap; gap: 32px; align-items: flex-start">
<div style="flex: 1 1 360px; display: flex; flex-direction: column; gap: 12px">{K("Đăng ký")}{h2("Giữ một chỗ trong workshop")}{T("Các em xác nhận qua Zalo và gửi hướng dẫn chuyển khoản. Hủy trước 24 giờ được hoàn tiền.", 16, 400, MUTED)}
{card(f'<div style="display: flex; gap: 12px; align-items: center">{boss(70)}<div>{D("Đi nhóm hoặc công ty?", 20)}{T("Từ 8 người, các em mở buổi riêng theo giờ bạn chọn.", 14, 400, MUTED)}</div></div>', 16, "", WARM)}</div>
<div style="flex: 1 1 460px">{card(f"""<div style="display: flex; flex-direction: column; gap: 14px"><label style="display: flex; flex-direction: column; gap: 6px">{T("Chọn buổi", 14, 700)}<select style="min-height: 48px; border-radius: 12px; border: 1.5px solid {LINE}; padding: 0 12px; {SANS}; font-size: 15px; background: {WHITE}"><option>Workshop tự đóng sổ da · [NGÀY]</option><option>Pha phin tại nhà · [NGÀY]</option></select></label>
<div style="display: flex; flex-wrap: wrap; gap: 14px">{field("Tên của bạn", "Ví dụ: Lan", half=True)}{field("Số điện thoại / Zalo", "09xx xxx xxx", "tel", True)}</div>{field("Số người", "1", "number")}{pbtn("Gửi đăng ký", None, TERRA, CREAM, True, 16, "check")}</div>""", 26)}</div></div>''', WHITE)
files["W06_Events"] = ("Website · Sự kiện và workshop", shell("Sự kiện", events + reg), 1440, 2300, "web")

# W07 careers
jobs = [("Pha chế", "Toàn thời gian · xoay ca sáng / chiều / tối", "Pha phin, máy, trà; giữ quầy sạch; nhớ món quen của khách.", "[MỨC LƯƠNG]"),
        ("Phục vụ", "Toàn thời gian hoặc bán thời gian", "Đón khách, mang món, dọn bàn, hướng dẫn khách gọi qua Zalo.", "[MỨC LƯƠNG]"),
        ("Quản lý cửa hàng", "Toàn thời gian", "Xếp ca, chấm công, kiểm kho, chăm sóc khách và đội ngũ.", "[MỨC LƯƠNG] + thưởng theo kết quả")]
def job(t, kind, d, pay):
    return card(f'''<div style="display: flex; flex-wrap: wrap; gap: 16px; justify-content: space-between; align-items: center"><div style="flex: 1 1 420px; display: flex; flex-direction: column; gap: 6px">{D(t, 26)}{T(kind, 14, 700, TERRA)}{T(d, 15, 400, ESP)}{T("Thu nhập: " + pay, 14, 600, MUTED)}</div>
{pbtn("Ứng tuyển", "#ung-tuyen", ESP, CREAM, False, 15)}</div>''', 22)
perks = [("cup", "Đồ uống miễn phí", "Trong ca và [SỐ] ly mỗi tuần ngoài ca."), ("clock", "Ca linh hoạt", "Đăng ký ca theo tuần ngay trên ứng dụng."),
         ("star", "Được dạy nghề", "Pha phin, pha máy, latte art, phục vụ."), ("wallet", "Lương rõ ràng", "Tính theo công thực làm, xem được từng ngày.")]
careers = section(f'''<div style="display: flex; flex-wrap: wrap; gap: 24px; justify-content: space-between; align-items: flex-end; margin-bottom: 32px"><div>{h1("Tuyển dụng", "Làm “em” ở Xo em", "Các em tìm người thích pha cà phê, thích nói chuyện và thích chăm cho người khác thấy dễ chịu.")}</div>{boss(150)}</div>
{grid([card(f'<div style="width: 48px; height: 48px; border-radius: 14px; background: {CREAM}; display: flex; align-items: center; justify-content: center">{ic(i, 24, TERRA)}</div>{D(a, 22, ESP, "margin-top: 12px")}{T(b, 15, 400, MUTED)}', 20) for i, a, b in perks], 240, 16)}''', CREAM, "56px 0 48px")
openings = section(f'''{K("Vị trí đang tuyển")}<div style="margin: 6px 0 24px">{h2("Ba chỗ còn trống")}</div><div style="display: flex; flex-direction: column; gap: 16px">{"".join(job(*j) for j in jobs)}</div>''', WHITE, "56px 0")
apply = section(f'''<div id="ung-tuyen" style="display: flex; flex-wrap: wrap; gap: 32px; align-items: flex-start">
<div style="flex: 1 1 340px; display: flex; flex-direction: column; gap: 12px">{K("Ứng tuyển")}{h2("Để lại vài dòng cho các em")}{T("Quản lý gọi lại trong [SỐ] ngày làm việc. Không cần kinh nghiệm cho vị trí phục vụ.", 16, 400, MUTED)}</div>
<div style="flex: 1 1 480px">{card(f"""<div style="display: flex; flex-direction: column; gap: 14px"><div style="display: flex; flex-wrap: wrap; gap: 14px">{field("Họ và tên", "", half=True)}{field("Số điện thoại / Zalo", "09xx xxx xxx", "tel", True)}</div>
<div style="display: flex; flex-direction: column; gap: 8px">{T("Vị trí", 14, 700)}<div style="display: flex; flex-wrap: wrap; gap: 8px">{"".join(chip(t, t == "Pha chế") for t in ("Pha chế", "Phục vụ", "Quản lý cửa hàng"))}</div></div>
<div style="display: flex; flex-direction: column; gap: 8px">{T("Ca có thể làm", 14, 700)}<div style="display: flex; flex-wrap: wrap; gap: 8px">{"".join(chip(t, t == "Sáng") for t in ("Sáng", "Chiều", "Tối", "Cuối tuần"))}</div></div>
<label style="display: flex; flex-direction: column; gap: 6px">{T("Kể ngắn về bạn", 14, 700)}<textarea style="min-height: 110px; border-radius: 12px; border: 1.5px solid {LINE}; padding: 12px 14px; {SANS}; font-size: 15px; box-sizing: border-box; width: 100%; resize: vertical"></textarea></label>
{pbtn("Gửi hồ sơ", None, TERRA, CREAM, True, 16, "check")}</div>""", 26)}</div></div>''', CREAM)
files["W07_Careers"] = ("Website · Tuyển dụng", shell("Tuyển dụng", careers + openings + apply), 1440, 2400, "web")

# W08 blog
posts = [("Cà phê", "Pha phin thế nào cho đậm mà không đắng", "Ba thứ quyết định: độ xay, nhiệt độ nước và thời gian ủ.", "[SỐ] phút đọc", TERRA),
         ("Chuyện quán", "Vì sao quán xưng “em”", "Một chữ nhỏ, nhưng đổi cả cách các em đón khách.", "[SỐ] phút đọc", BUTTER),
         ("Sự kiện", "Lịch workshop và sự kiện tháng [THÁNG]", "Làm sổ, học pha phin, tối đọc sách, đêm nhạc mộc.", "[SỐ] phút đọc", MOSS),
         ("Ecopark", "5 góc dạo bộ gần quán", "Đi bộ mười phút, quay về vẫn còn ấm ly cà phê.", "[SỐ] phút đọc", KRAFT),
         ("Cà phê", "Bạc xỉu, nâu đá, cà phê muối khác nhau thế nào", "Bảng so sánh nhanh để lần sau gọi đúng món.", "[SỐ] phút đọc", TERRA),
         ("Chuyện quán", "Một ngày của Em Ngơ ở quầy", "Truyện tranh ngắn: ly cà phê trên sừng và những lần quên.", "[SỐ] phút đọc", MOSS)]
def post(cat, t, d, m, c, big=False):
    return link("#", card(f'{tile(c, cat, 300 if big else 180)}{D(t, 32 if big else 22, ESP, "margin-top: 14px")}{T(d, 16 if big else 14, 400, MUTED, "margin-top: 4px")}{T("[NGÀY] · " + m, 12, 600, MUTED, "margin-top: 10px")}', 14), "display: block")
blog = section(f'''<div style="margin-bottom: 28px">{h1("Góc đọc", "Chuyện cà phê và chuyện quán", "Các em viết về cách pha, về Ecopark và về những ngày ở quầy.")}</div>
<div style="display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 28px">{"".join(chip(t, t == "Tất cả") for t in ("Tất cả", "Cà phê", "Chuyện quán", "Sự kiện", "Ecopark"))}</div>
<div style="display: flex; flex-wrap: wrap; gap: 24px; margin-bottom: 24px"><div style="flex: 2 1 560px">{post(*posts[0], big=True)}</div><div style="flex: 1 1 320px; display: flex; flex-direction: column; gap: 24px">{post(*posts[1])}</div></div>
{grid([post(*p) for p in posts[2:]], 260, 24)}''', CREAM, "56px 0 64px")
sub = section(f'''<div style="display: flex; flex-wrap: wrap; gap: 24px; align-items: center; justify-content: space-between">
<div style="display: flex; gap: 20px; align-items: center">{ngo(110)}<div>{h2("Nhận bài mới qua Zalo", CREAM)}{T("Mỗi tháng một tin, kèm lịch sự kiện. Không quảng cáo dồn dập.", 16, 400, CREAM)}</div></div>
{pbtn("Theo dõi Zalo Xo em", "C01_Home.dc.html", BUTTER, ESP, False, 16, "qr")}</div>''', TERRA, "48px 0")
files["W08_Blog"] = ("Website · Góc đọc", shell("Góc đọc", blog + sub), 1440, 2000, "web")
