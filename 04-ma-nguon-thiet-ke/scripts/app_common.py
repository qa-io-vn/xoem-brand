import json, os, io, contextlib, sys
sys.path.insert(0, "/home/claude")
with contextlib.redirect_stdout(io.StringIO()):
    import brand_em as B

ROOT = "/home/claude/xoem-app/project"
os.makedirs(ROOT, exist_ok=True)
CREAM, ESP, TERRA, MOSS, BUTTER, SAND, KRAFT = B.CREAM, B.ESP, B.TERRA, B.MOSS, B.BUTTER, B.SAND, B.KRAFT
MUTED = "#6A5A4F"; LINE = "#E6D8C0"; WHITE = "#FFFFFF"; RED = "#B8382A"; DEEPT = "#A8432D"
SANS = "font-family: 'Be Vietnam Pro', system-ui, sans-serif"
DISPLAY = "font-family: 'Baloo 2', 'Be Vietnam Pro', sans-serif"
HAND = "font-family: 'Patrick Hand', 'Be Vietnam Pro', cursive"
sym, nga, ngo, boss, pat = B.symbol, B.nga, B.ngo, B.boss, B.pattern_svg
FONTS = B.FONTS

ICONS = {
    "home": "M3 11l9-8 9 8v9a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z",
    "cup": "M4 8h13v6a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5zM17 10h1.5a2.5 2.5 0 0 1 0 5H17M8 3v2M12 3v2",
    "receipt": "M6 3h12v18l-3-2-3 2-3-2-3 2zM9 8h6M9 12h6",
    "star": "M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1L3.2 9.5l6.1-.9z",
    "user": "M12 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM4 21a8 8 0 0 1 16 0",
    "plus": "M12 5v14M5 12h14", "minus": "M5 12h14",
    "clock": "M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18zM12 7v5l3 2",
    "check": "M5 12l5 5 9-10",
    "chart": "M4 20V10M10 20V4M16 20v-7M22 20H2",
    "cal": "M4 6h16v15H4zM4 10h16M8 3v4M16 3v4",
    "box": "M3 7l9-4 9 4-9 4zM3 7v10l9 4 9-4V7M12 11v10",
    "gear": "M12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM19.4 15a1.7 1.7 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.8-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1.1-1.5 1.7 1.7 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.8 1.7 1.7 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.5-1.1 1.7 1.7 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 1.8.3H9a1.7 1.7 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.8V9a1.7 1.7 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1z",
    "bell": "M6 16V11a6 6 0 0 1 12 0v5l2 2H4zM10 20a2 2 0 0 0 4 0",
    "search": "M11 18a7 7 0 1 0 0-14 7 7 0 0 0 0 14zM21 21l-5-5",
    "pin": "M12 21s-7-6.5-7-12a7 7 0 0 1 14 0c0 5.5-7 12-7 12zM12 11a2 2 0 1 0 0-4 2 2 0 0 0 0 4z",
    "phone": "M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z",
    "chev": "M9 6l6 6-6 6", "back": "M15 6l-6 6 6 6",
    "table": "M3 9h18M5 9v10M19 9v10M8 5h8",
    "gift": "M4 10h16v10H4zM3 7h18v3H3zM12 7v13M12 7c-2-4-6-3-5 0M12 7c2-4 6-3 5 0",
    "bag": "M5 8h14l-1 12H6zM9 8V6a3 3 0 0 1 6 0v2",
    "qr": "M4 4h6v6H4zM14 4h6v6h-6zM4 14h6v6H4zM14 14h2v2h-2zM18 18h2v2h-2zM14 18h2",
    "list": "M8 6h12M8 12h12M8 18h12M4 6h.01M4 12h.01M4 18h.01",
    "alert": "M12 3l10 18H2zM12 10v5M12 18h.01",
    "wallet": "M3 7h18v12H3zM3 7l3-3h12l3 3M16 13h2",
    "edit": "M4 20h4L19 9l-4-4L4 16zM14 6l4 4",
    "users": "M9 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM2 21a7 7 0 0 1 14 0M17 11a3 3 0 1 0 0-6M22 21a6 6 0 0 0-5-6",
    "wifi": "M2 8a16 16 0 0 1 20 0M5 12a11 11 0 0 1 14 0M8.5 15.5a6 6 0 0 1 7 0M12 19h.01",
    "x": "M6 6l12 12M18 6L6 18",
    "logout": "M15 4h4v16h-4M10 17l5-5-5-5M15 12H3",
}

def ic(name, size=22, color=ESP, sw=2):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" aria-hidden="true" style="display: block; flex-shrink: 0">'
            f'<path d="{ICONS[name]}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"></path></svg>')

def T(t, s=14, w=400, c=ESP, extra=""):
    return f'<div style="{SANS}; font-size: {s}px; font-weight: {w}; color: {c}; line-height: 1.45; {extra}">{t}</div>'
def D(t, s=24, c=ESP, extra=""):
    return f'<div style="{DISPLAY}; font-weight: 800; font-size: {s}px; color: {c}; line-height: 1.08; {extra}">{t}</div>'
def H(t, s=18, c=TERRA, extra=""):
    return f'<div style="{HAND}; font-size: {s}px; color: {c}; line-height: 1.15; {extra}">{t}</div>'
def K(t, c=TERRA, s=11):
    return f'<div style="{SANS}; font-size: {s}px; font-weight: 700; letter-spacing: 0.14em; color: {c}; text-transform: uppercase">{t}</div>'

def link(href, inner, style=""):
    return f'<a href="{href}" style="text-decoration: none; color: inherit; {style}">{inner}</a>'
def pbtn(t, href=None, bg=TERRA, fg=CREAM, full=True, s=15, icon=None, border=None):
    bd = f"border: 2px solid {border};" if border else "border: none;"
    inner = (f'<span style="display: flex; align-items: center; justify-content: center; gap: 8px; {"width: 100%;" if full else ""} min-height: 48px; padding: 0 18px; box-sizing: border-box; '
             f'background: {bg}; color: {fg}; {bd} border-radius: 14px; {SANS}; font-weight: 700; font-size: {s}px">{ic(icon, 18, fg) if icon else ""}{t}</span>')
    if href:
        return f'<a href="{href}" style="text-decoration: none; display: {"block" if full else "inline-block"}; {"width: 100%;" if full else ""}">{inner}</a>'
    return f'<button type="button" style="all: unset; display: {"block" if full else "inline-block"}; {"width: 100%;" if full else ""} cursor: pointer">{inner}</button>'
def chip(t, on=False, href=None):
    st = (f'display: inline-flex; align-items: center; min-height: 36px; padding: 0 14px; border-radius: 999px; {SANS}; font-size: 13px; font-weight: 600; '
          f'background: {ESP if on else WHITE}; color: {CREAM if on else ESP}; border: 1.5px solid {ESP if on else LINE}; white-space: nowrap')
    return link(href, f'<span style="{st}">{t}</span>') if href else f'<button type="button" style="all: unset; cursor: pointer"><span style="{st}">{t}</span></button>'
def card(inner, pad=14, extra="", bg=WHITE):
    pad = pad if isinstance(pad, str) else f"{pad}px"
    return f'<div style="background: {bg}; border: 1.5px solid {LINE}; border-radius: 18px; padding: {pad}; box-sizing: border-box; {extra}">{inner}</div>'
def thumb(size=64, body=TERRA, bg=CREAM, s=None):
    s = s or int(size * 0.68)
    return f'<div style="width: {size}px; height: {size}px; border-radius: {int(size*0.22)}px; background: {bg}; display: flex; align-items: center; justify-content: center; flex-shrink: 0">{sym(s, body=body)}</div>'
def badge(t, bg=BUTTER, fg=ESP):
    return f'<span style="display: inline-block; padding: 3px 9px; border-radius: 999px; background: {bg}; color: {fg}; {SANS}; font-size: 11px; font-weight: 700">{t}</span>'
def qty(n="1"):
    b = lambda name, lbl: f'<button type="button" aria-label="{lbl}" style="all: unset; cursor: pointer; width: 32px; height: 32px; border-radius: 10px; border: 1.5px solid {LINE}; display: flex; align-items: center; justify-content: center; background: {WHITE}">{ic(name, 16)}</button>'
    return f'<div style="display: flex; align-items: center; gap: 10px">{b("minus", "Bớt")}{T(n, 15, 700)}{b("plus", "Thêm")}</div>'

MENU = [("Cà phê phin đen", "Đậm, đắng nhẹ, pha phin tại chỗ", TERRA, "Cà phê"), ("Cà phê phin sữa", "Sữa đặc vừa đủ ngọt", TERRA, "Cà phê"),
        ("Bạc xỉu", "Nhiều sữa, ít cà phê", BUTTER, "Cà phê"), ("Cà phê muối", "Kem muối béo mặn nhẹ", BUTTER, "Cà phê"),
        ("Trà đào cam sả", "Thanh mát, nhiều miếng đào", MOSS, "Trà"), ("Trà sen vàng", "Hương sen, hạt sen bùi", MOSS, "Trà"),
        ("Matcha sữa", "Matcha đánh tay, sữa tươi", MOSS, "Trà"), ("Bánh chuối nướng", "Nướng mới mỗi sáng", KRAFT, "Bánh"),
        ("Croissant bơ", "Giòn vỏ, mềm ruột", KRAFT, "Bánh")]

# -------- phone shell (Zalo mini app) --------
def mini_header(title, back=None, right_extra=""):
    b = (link(back, f'<span style="display: flex; width: 36px; height: 36px; align-items: center; justify-content: center" aria-label="Quay lại">{ic("back", 22)}</span>')
         if back else '<span style="display: block; width: 36px"></span>')
    capsule = (f'<div style="display: flex; align-items: center; gap: 10px; height: 30px; padding: 0 12px; border-radius: 999px; border: 1.5px solid {LINE}; background: {WHITE}" aria-hidden="true">'
               f'<div style="display: flex; gap: 3px"><span style="width: 4px; height: 4px; border-radius: 50%; background: {ESP}"></span><span style="width: 4px; height: 4px; border-radius: 50%; background: {ESP}"></span><span style="width: 4px; height: 4px; border-radius: 50%; background: {ESP}"></span></div>'
               f'<span style="width: 1px; height: 14px; background: {LINE}"></span>{ic("x", 14)}</div>')
    return (f'<div style="height: 56px; flex-shrink: 0; display: flex; align-items: center; justify-content: space-between; padding: 0 12px 0 8px; background: {CREAM}; border-bottom: 1px solid {LINE}">'
            f'<div style="display: flex; align-items: center; gap: 4px; min-width: 0">{b}{D(title, 19)}</div><div style="display: flex; align-items: center; gap: 10px">{right_extra}{capsule}</div></div>')

def tabbar(tabs, active):
    out = ""
    for key, label, icon, href in tabs:
        on = key == active
        c = TERRA if on else MUTED
        out += link(href, f'<span style="display: flex; flex-direction: column; align-items: center; gap: 3px; min-width: 56px; padding-top: 8px">{ic(icon, 22, c, 2.2 if on else 1.8)}'
                          f'<span style="{SANS}; font-size: 11px; font-weight: {700 if on else 500}; color: {c}">{label}</span></span>', "flex: 1; display: flex; justify-content: center")
    return f'<nav aria-label="Điều hướng chính" style="height: 72px; flex-shrink: 0; display: flex; background: {WHITE}; border-top: 1px solid {LINE}">{out}</nav>'

CUST_TABS = [("home", "Trang chủ", "home", "C01_Home.dc.html"), ("menu", "Thực đơn", "cup", "C02_Menu.dc.html"),
             ("order", "Đơn hàng", "receipt", "C06_Track.dc.html"), ("points", "Tích điểm", "star", "C07_Points.dc.html"),
             ("me", "Tôi", "user", "C08_Account.dc.html")]
STAFF_TABS = [("orders", "Đơn", "receipt", "S02_Queue.dc.html"), ("tables", "Bàn", "table", "S04_Tables.dc.html"),
              ("items", "Món", "cup", "S05_Stock.dc.html"), ("shift", "Ca làm", "clock", "S07_Shifts.dc.html"),
              ("manage", "Quản lý", "chart", "S06_Dashboard.dc.html")]

def screen(title, body, tabs=None, active=None, back=None, footer=None, right_extra="", bg=CREAM):
    tb = tabbar(tabs, active) if tabs else ""
    ft = f'<div style="flex-shrink: 0; padding: 12px 16px 18px; background: {WHITE}; border-top: 1px solid {LINE}">{footer}</div>' if footer else ""
    return (f'<div style="width: 390px; height: 844px; box-sizing: border-box; background: {bg}; display: flex; flex-direction: column; overflow: hidden; {SANS}; color: {ESP}">'
            f'{mini_header(title, back, right_extra)}<main style="flex-grow: 1; overflow: hidden; padding: 16px; display: flex; flex-direction: column; gap: 14px">{body}</main>{ft}{tb}</div>')

def page(title, body, w, h):
    props = {"$preview": {"width": w, "height": h}}
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
