import asyncio
from playwright.async_api import async_playwright

MUN = "#241B13"; KEM = "#F5EEE2"; DONG = "#BE8A4E"
F = "file:///home/claude/fonts/"
brands = [
    ("Xofa", "Tên cũ", "/home/claude/out/logoXF/Xofa-logo-"),
    ("Xô Ngơ", "Phương án 1", "/home/claude/out/logoXN/XoNgo-logo-"),
    ("Xo em", "Phương án 2", "/home/claude/out/logoXE/XoEm-logo-"),
]
rows = [
    ("Ý nghĩa tên", ["Chơi chữ từ “sofa”", "Gợi “ngả ngơ”: ngả lưng, ngơ ngẩn thư giãn; gắn với linh vật Ngả &amp; Ngơ", "“Em”: cách xưng hô thân mật; các em Boss, Ngả, Ngơ lo cho khách"]),
    ("Khớp khẩu hiệu Slow coffee · Comfy seats", ["Khớp: sofa ↔ comfy seats", "Khớp phần “slow”: chậm, thư thả", "Khớp tinh thần chăm khách: “có em lo”"]),
    ("Đọc, gõ, tìm trên mạng", ["Không dấu, dễ gõ", "2 dấu (ô, ơ); khách hay gõ “xo ngo”", "Không dấu, dễ gõ và tìm"]),
    ("Bộ 4 ô vuông", ["X · O · F · A", "X · Ô · NG · Ơ (NG ghép chung một ô)", "X · O · E · M (không dấu trong ô, vừa khít 4 chữ)"]),
    ("Phông chữ", ["Phông gốc", "Phải đổi phông: phông gốc không có chữ “ơ”", "Giữ được phông gốc"]),
    ("Pháp lý tên", ["Đang có bên khác nhắn trùng tên", "Cần tra cứu nhãn hiệu trước khi dùng", "Cần tra cứu nhãn hiệu trước khi dùng"]),
]

def img(path, h, extra=""):
    return f"<img src='file://{path}' style='max-height:{h}px;max-width:100%;{extra}'>"

def cup(path):
    return (f"<div style='display:flex;flex-direction:column;align-items:center'>"
            f"<div style='width:150px;height:18px;background:{MUN};border-radius:30px 30px 4px 4px'></div>"
            f"<div style='width:132px;height:170px;background:{KEM};clip-path:polygon(0 0,100% 0,88% 100%,12% 100%);display:flex;align-items:center;justify-content:center;position:relative'>"
            f"<img src='file://{path}' style='width:74px'>"
            f"<div style='position:absolute;inset:0;background:linear-gradient(90deg,rgba(0,0,0,.18),rgba(255,255,255,.1) 40%,rgba(0,0,0,.2))'></div></div></div>")

def avatar(path):
    return f"<div style='width:150px;height:150px;border-radius:50%;background:{KEM};border:2px solid #D9CDB8;display:flex;align-items:center;justify-content:center'><img src='file://{path}' style='width:86px'></div>"

cols = ""
for name, label, p in brands:
    cols += f"""<div style='display:flex;flex-direction:column;gap:18px'>
<div style='display:flex;align-items:baseline;gap:14px'><div style="font-family:'Fredoka';font-weight:600;font-size:52px;color:{MUN}">{name}</div><div style="font-family:'BVP';font-weight:700;font-size:15px;letter-spacing:.16em;color:{DONG};text-transform:uppercase">{label}</div></div>
<div style='background:{KEM};border-radius:18px;height:230px;display:flex;align-items:center;justify-content:center;padding:24px'>{img(p+'ngang-mau.png', 150)}</div>
<div style='background:{MUN};border-radius:18px;height:230px;display:flex;align-items:center;justify-content:center;padding:24px'>{img(p+'ngang-nen-toi.png', 150)}</div>
<div style='background:#FFFFFF;border-radius:18px;height:260px;display:flex;align-items:center;justify-content:space-around;padding:20px'>{avatar(p+'bieu-tuong-mau.png')}{cup(p+'bieu-tuong-mau.png')}</div>
</div>"""

table = ""
for r, vals in rows:
    table += (f"<div style='display:grid;grid-template-columns:260px repeat(3,1fr);gap:28px;padding:16px 0;border-top:1.5px solid #D9CDB8'>"
              f"<div style=\"font-family:'BVP';font-weight:700;font-size:16px;color:{DONG}\">{r}</div>"
              + "".join(f"<div style=\"font-family:'BVP';font-size:18px;line-height:1.5;color:{MUN}\">{v}</div>" for v in vals) + "</div>")

html = f"""<html><head><meta charset='utf-8'><style>
@font-face{{font-family:'Fredoka';src:url({F}Fredoka-600.ttf);font-weight:600}}
@font-face{{font-family:'BVP';src:url({F}BeVietnamPro-Regular.ttf);font-weight:400}}
@font-face{{font-family:'BVP';src:url({F}BeVietnamPro-Bold.ttf);font-weight:700}}
body{{margin:0;background:#EFE7DA}}
</style></head><body>
<div style='width:2000px;box-sizing:border-box;padding:70px 80px;display:flex;flex-direction:column;gap:40px'>
<div><div style="font-family:'BVP';font-weight:700;font-size:16px;letter-spacing:.2em;color:{DONG}">SO SÁNH LOGO · CÙNG PHONG CÁCH, KHÁC TÊN</div>
<div style="font-family:'Fredoka';font-weight:600;font-size:64px;color:{MUN};line-height:1.1">Xofa · Xô Ngơ · Xo em</div></div>
<div style='display:grid;grid-template-columns:260px repeat(3,1fr);gap:28px'>
<div style="display:flex;flex-direction:column;gap:18px;font-family:'BVP';font-weight:700;font-size:16px;color:{DONG}"><div style='height:70px'></div><div style='height:230px;display:flex;align-items:center'>Logo ngang · nền sáng</div><div style='height:230px;display:flex;align-items:center'>Logo ngang · nền tối</div><div style='height:260px;display:flex;align-items:center'>Ảnh đại diện · ly giấy</div></div>
{cols}</div>
<div>{table}</div>
</div></body></html>"""
open("/home/claude/out/compare.html", "w").write(html)

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--allow-file-access-from-files"])
        pg = await b.new_page(viewport={"width": 2000, "height": 1200}, device_scale_factor=1.2)
        await pg.goto("file:///home/claude/out/compare.html")
        await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(400)
        await pg.screenshot(path="/home/claude/out/So-sanh-logo-Xofa-XoNgo-Xoem.png", full_page=True)
        await b.close()
asyncio.run(main())
