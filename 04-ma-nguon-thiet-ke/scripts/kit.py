import os, sys, io, contextlib, asyncio, shutil, glob
sys.path.insert(0, "/home/claude")
with contextlib.redirect_stdout(io.StringIO()):
    import brand_em as B
    from logo2 import Font
from playwright.async_api import async_playwright
OUT = "/home/claude/out/Xoem-Brand-Kit"; shutil.rmtree(OUT, ignore_errors=True)
for d in ("1-Logo/SVG", "1-Logo/PNG", "2-Logo-4-o", "3-Linh-vat", "4-Hoa-tiet", "5-Bo-nhan-dien"):
    os.makedirs(f"{OUT}/{d}", exist_ok=True)
WMF = Font("/home/claude/fonts/Baloo2-ExtraBold-static.ttf"); TGF = Font("/home/claude/fonts/BeVietnamPro-SemiBold.ttf")
def svg(w, h, body): return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" height="{h:.0f}">{body}</svg>'
S = {"mau": dict(body=B.TERRA, ink=B.ESP, white=B.CREAM, text=B.ESP),
     "nen-toi": dict(body=B.TERRA, ink=B.CREAM, white=B.ESP, text=B.CREAM),
     "den": dict(body="none", ink=B.ESP, white="none", text=B.ESP),
     "trang": dict(body="none", ink="#FFFFFF", white="none", text="#FFFFFF")}
def mark(sc, x, y, size):
    return f'<g transform="translate({x:.1f} {y:.1f}) scale({size/200:.4f})">{B.symbol_inner(body=sc["body"], ink=sc["ink"], white=sc["white"])}</g>'
def words(sc, x, y, tag=True, center_w=None):
    d, (x0, y0, x1, y1) = WMF.line("xo em", 200, -0.02); ww, wh = x1 - x0, y1 - y0
    out = f'<g transform="translate({x - x0 + ((center_w - ww) / 2 if center_w else 0):.1f} {y - y0:.1f})" fill="{sc["text"]}">{d}</g>'
    h = wh; w = ww
    if tag:
        t, (a, b, c, e) = TGF.line("SLOW COFFEE · COMFY SEATS", 34, 0.22); tw = c - a
        tx = x + (((center_w - tw) / 2) if center_w else 4)
        out += f'<g transform="translate({tx - a:.1f} {y + wh + 34 - b:.1f})" fill="{sc["text"]}">{t}</g>'
        h = wh + 34 + (e - b); w = max(ww, tw + 4)
    return out, w, h
files = {}
for n, sc in S.items():
    files[f"Xoem-bieu-tuong-{n}"] = svg(200, 200, mark(sc, 0, 0, 200))
    t, w, h = words(sc, 0, 0); files[f"Xoem-chu-{n}"] = svg(w + 8, h + 8, t)
    t, w, h = words(sc, 300, 0); H = max(280, h); t, w, h = words(sc, 300, (H - h) / 2)
    files[f"Xoem-logo-ngang-{n}"] = svg(300 + w + 8, H, mark(sc, 0, (H - 280) / 2, 280) + t)
    _, w, h = words(sc, 0, 0); W = max(w, 300) + 40
    t, _, h = words(sc, 0, 330, True, W); files[f"Xoem-logo-doc-{n}"] = svg(W, 330 + h + 8, mark(sc, (W - 300) / 2, 0, 300) + t)
for k, v in files.items(): open(f"{OUT}/1-Logo/SVG/{k}.svg", "w").write(v)
def wrap(inner, vb, w, h): return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" width="{w}" height="{h}">{inner}</svg>'
import re as _re
PH = Font("/home/claude/fonts/PatrickHand-Regular.ttf")
def outline_text(svgtxt):
    def rep(m):
        x, y, size, fill, ch = float(m.group(1)), float(m.group(2)), float(m.group(3)), m.group(4), m.group(5)
        d, _ = PH.line(ch, size, 0)
        return f'<g transform="translate({x} {y})" fill="{fill}">{d}</g>'
    return _re.sub(r'<text x="([\d.]+)" y="([\d.]+)" font-family="Patrick Hand, cursive" font-size="([\d.]+)" fill="([^"]+)">([^<]+)</text>', rep, svgtxt)
mascots = {"Boss": wrap(B.symbol_inner(), "0 0 200 200", 1600, 1600), "Em-Nga": wrap(outline_text(B.nga_inner()), "0 0 320 240", 2000, 1500),
           "Em-Ngo": wrap(outline_text(B.ngo_inner()), "0 0 260 300", 1560, 1800)}
pats = {"Hoa-tiet-Dat-Nung": outline_text(B.pattern_svg(2000, 2000, B.TERRA, B.BUTTER, B.ESP, B.CREAM, B.CREAM, 2.0)),
        "Hoa-tiet-Kem": outline_text(B.pattern_svg(2000, 2000, B.CREAM, B.TERRA, B.ESP, B.CREAM, B.SAND, 2.0)),
        "Hoa-tiet-Reu": outline_text(B.pattern_svg(2000, 2000, B.MOSS, B.SAND, B.ESP, B.CREAM, B.BUTTER, 2.0))}
FONT_CSS = "@font-face{font-family:'Patrick Hand';src:url(file:///home/claude/fonts/PatrickHand-Regular.ttf)}body{margin:0;background:transparent}"
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--allow-file-access-from-files"]); pg = await b.new_page()
        async def shot(svgtxt, path, scale_to=2400):
            import re
            w, h = [float(v) for v in re.search(r'viewBox="[\d.\-]+ [\d.\-]+ ([\d.]+) ([\d.]+)"', svgtxt).groups()]
            sc = scale_to / max(w, h); W, Hh = int(w * sc), int(h * sc)
            s2 = re.sub(r'width="[\d.]+" height="[\d.]+"', f'width="{W}" height="{Hh}"', svgtxt, count=1)
            await pg.set_viewport_size({"width": W, "height": Hh})
            await pg.set_content(f"<html><head><style>{FONT_CSS}</style></head><body>{s2}</body></html>"); await pg.wait_for_timeout(150)
            await pg.screenshot(path=path, omit_background=True, clip={"x": 0, "y": 0, "width": W, "height": Hh})
        for k, v in files.items(): await shot(v, f"{OUT}/1-Logo/PNG/{k}.png")
        for k, v in mascots.items():
            open(f"{OUT}/3-Linh-vat/{k}.svg", "w").write(v); await shot(v, f"{OUT}/3-Linh-vat/{k}.png", 2000)
        for k, v in pats.items():
            v = v.replace('<svg ', '<svg xmlns="http://www.w3.org/2000/svg" ', 1); open(f"{OUT}/4-Hoa-tiet/{k}.svg", "w").write(v); await shot(v, f"{OUT}/4-Hoa-tiet/{k}.png", 2000)
        await b.close()
asyncio.run(main())
for f in glob.glob("/home/claude/out/logoXE/XoEm-logo-*"):
    if f.endswith((".svg", ".png")) and "tong-hop" not in f:
        shutil.copy(f, f"{OUT}/2-Logo-4-o/" + os.path.basename(f).replace("XoEm-", "Xoem-"))
shutil.copy("/home/claude/out/Xoem-Bo-nhan-dien.pdf", f"{OUT}/5-Bo-nhan-dien/")
open(f"{OUT}/DOC-TRUOC.txt", "w").write("""BỘ FILE THƯƠNG HIỆU XO EM

1-Logo        Logo chính (biểu tượng ghế-ly + chữ "xo em"): ngang, dọc, chỉ biểu tượng, chỉ chữ.
              4 bản màu: mau (nền sáng), nen-toi (nền tối), den (in một màu đen), trang (in một màu trắng).
              SVG: gửi xưởng in, làm biển, khắc, phóng to không vỡ. Chữ đã chuyển thành nét, không cần cài phông.
              PNG: nền trong suốt, dùng cho mạng xã hội, tài liệu, thiết kế nhanh.
2-Logo-4-o    Logo 4 ô X-O-E-M (bảng chữ trên tường quầy, tem, con dấu).
3-Linh-vat    Boss, Em Ngả, Em Ngơ: SVG và PNG nền trong suốt.
4-Hoa-tiet    3 mẫu họa tiết lặp (Đất Nung, Kem, Rêu): giấy gói, ly, túi, tường.
5-Bo-nhan-dien  Cẩm nang thương hiệu đầy đủ (PDF).

MÀU
Đất Nung   #C8553D   (màu chính)
Kem Sữa    #F6EEDF   (màu nền)
Nâu Cà Phê #2B1D16   (chữ, đường viền)
Vàng Bơ    #F2C14E   (điểm nhấn)
Rêu Sồi    #5E7A4A   (dòng trà, cây)
Cát Mịn    #E8D5B5   (màu phụ)
Mã CMYK trong cẩm nang chỉ là quy đổi tham khảo, cần in thử để chốt màu.

PHÔNG CHỮ (miễn phí, Google Fonts, giấy phép mở OFL)
Baloo 2 ExtraBold   tiêu đề, tên món
Be Vietnam Pro      nội dung, giá
Patrick Hand        chữ viết tay, sticker

TÊN TÀI KHOẢN GỢI Ý: @xoem.ecopark (kiểm tra còn trống trước khi tạo)
""")
shutil.make_archive("/home/claude/out/Xoem-Brand-Kit", "zip", "/home/claude/out", "Xoem-Brand-Kit")
print(sum(len(f) for _, _, f in os.walk(OUT)))
