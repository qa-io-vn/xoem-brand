import json, os, asyncio, sys
sys.path.insert(0, "/home/claude")
from app_common import ROOT, page
from app_web import files
from playwright.async_api import async_playwright

OUTD = "/home/claude/out/app"; os.makedirs(OUTD, exist_ok=True)
F = "file:///home/claude/fonts/"
CSS = f"""
@font-face{{font-family:'Baloo 2';src:url({F}Baloo2.ttf);font-weight:400 800}}
@font-face{{font-family:'Patrick Hand';src:url({F}PatrickHand-Regular.ttf)}}
@font-face{{font-family:'Be Vietnam Pro';src:url({F}BeVietnamPro-Regular.ttf);font-weight:400}}
@font-face{{font-family:'Be Vietnam Pro';src:url({F}BeVietnamPro-Medium.ttf);font-weight:500}}
@font-face{{font-family:'Be Vietnam Pro';src:url({F}BeVietnamPro-SemiBold.ttf);font-weight:600}}
@font-face{{font-family:'Be Vietnam Pro';src:url({F}BeVietnamPro-Bold.ttf);font-weight:700}}
body{{margin:0}}
"""
heights = {}
async def render():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--allow-file-access-from-files"])
        for name, (title, body, w, h, kind) in files.items():
            pg = await b.new_page(viewport={"width": w, "height": h if kind != "web" else 900}, device_scale_factor=2 if kind != "web" else 1.25)
            open("/home/claude/tmp_app.html", "w").write(f"<!doctype html><html lang='vi'><head><meta charset='utf-8'><style>{CSS}</style></head><body>{body}</body></html>")
            await pg.goto("file:///home/claude/tmp_app.html"); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(250)
            if kind == "web":
                hh = await pg.evaluate("document.documentElement.scrollHeight"); heights[name] = hh
                await pg.screenshot(path=f"{OUTD}/{name}.png", full_page=True)
            else:
                heights[name] = h
                await pg.screenshot(path=f"{OUTD}/{name}.png", clip={"x": 0, "y": 0, "width": w, "height": h})
            await pg.close()
        await b.close()
asyncio.run(render())

# write artboards + canvas index
boards, order = {}, []
groups = {"web": [], "cust": [], "staff": []}
for name, v in files.items():
    groups[v[4]].append(name)
pages = [{"id": "web", "name": "Website"}, {"id": "khach", "name": "Ứng dụng Zalo · Khách"}, {"id": "nhanvien", "name": "Ứng dụng Zalo · Nhân viên & quản lý"}]
notes = {}
x = 0
for name in groups["web"]:
    title, body, w, h, kind = files[name]
    hh = heights[name]
    open(os.path.join(ROOT, name + ".dc.html"), "w").write(page(title, body, w, hh))
    boards[name + ".dc.html"] = {"x": x, "y": 0, "w": w, "h": hh, "title": title, "page": "web", "expand": "fill", "is_interactive": True}
    order.append(name + ".dc.html"); x += w + 80
notes["t_web"] = {"x": 0, "y": -300, "text": "Website Xo em · trang chủ, thực đơn, đặt bàn", "kind": "title1", "maxW": x - 80, "page": "web"}
for gid, pid, label in (("cust", "khach", "Ứng dụng Zalo cho khách · gọi món, thanh toán, tích điểm"), ("staff", "nhanvien", "Ứng dụng Zalo cho nhân viên và quản lý")):
    for i, name in enumerate(groups[gid]):
        title, body, w, h, kind = files[name]
        open(os.path.join(ROOT, name + ".dc.html"), "w").write(page(title, body, w, h))
        boards[name + ".dc.html"] = {"x": (i % 4) * (390 + 80), "y": (i // 4) * (844 + 120), "w": 390, "h": 844, "title": title, "page": pid, "is_interactive": True}
        order.append(name + ".dc.html")
    notes["t_" + pid] = {"x": 0, "y": -300, "text": label, "kind": "title1", "maxW": 4 * 390 + 3 * 80, "page": pid}
canvas = {"v": 3, "createdOnFiles": {"v": 1, "at": "2026-11-25T07:45:00Z"}, "title": "Xo em – Website & ứng dụng Zalo",
          "launch": {"view": "canvas", "page": "web"}, "pages": pages, "boards": boards, "order": order, "notes": notes, "designSystems": []}
json.dump(canvas, open(os.path.join(ROOT, "canvas.json"), "w"), ensure_ascii=False)
json.dump({k: heights[k] for k in heights}, open("/home/claude/out/app/heights.json", "w"))
print(heights)
