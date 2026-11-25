import json, os, asyncio, sys
sys.path.insert(0, "/home/claude")
from app_common import ROOT, page
from app_more import files
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
fix = lambda s: s.replace("W01_Home.dc.html", "Main.dc.html")
ONLY = set(sys.argv[1:])
heights = json.load(open(f"{OUTD}/heights.json")) if os.path.exists(f"{OUTD}/heights.json") else {}
async def render():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--allow-file-access-from-files"])
        for name, (title, body, w, h, kind) in files.items():
            if ONLY and name not in ONLY: continue
            web = kind == "web"
            pg = await b.new_page(viewport={"width": w, "height": 900 if web else h}, device_scale_factor=1.25 if web else 2)
            open("/home/claude/tmp_app.html", "w").write(f"<!doctype html><html lang='vi'><head><meta charset='utf-8'><style>{CSS}</style></head><body>{body}</body></html>")
            await pg.goto("file:///home/claude/tmp_app.html"); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(250)
            if web:
                heights[name] = await pg.evaluate("document.documentElement.scrollHeight")
                await pg.screenshot(path=f"{OUTD}/{name}.png", full_page=True)
            else:
                heights[name] = h
                await pg.screenshot(path=f"{OUTD}/{name}.png", clip={"x": 0, "y": 0, "width": w, "height": h})
            await pg.close()
        await b.close()
asyncio.run(render())
json.dump(heights, open(f"{OUTD}/heights.json", "w"))

groups = {}
for name, v in files.items(): groups.setdefault(v[4], []).append(name)
pages = [{"id": "web", "name": "Website"}, {"id": "khach", "name": "Ứng dụng Zalo · Khách"},
         {"id": "nhanvien", "name": "Ứng dụng Zalo · Nhân viên & quản lý"}, {"id": "trangthai", "name": "Trạng thái & màn hình thêm"}]
boards, order, notes = {}, [], {}
def put(name, x, y, pid, web=False):
    title, body, w, h, kind = files[name]
    hh = heights.get(name, h)
    fn = "Main.dc.html" if name == "W01_Home" else name + ".dc.html"
    open(os.path.join(ROOT, fn), "w").write(fix(page(title, fix(body), w, hh)))
    boards[fn] = {"x": x, "y": y, "w": w, "h": hh, "title": title, "page": pid, "is_interactive": True, **({"expand": "fill"} if web else {})}
    order.append(fn)
x = 0
for name in groups["web"]:
    put(name, x, 0, "web", True); x += 1440 + 80
notes["t_web"] = {"x": 0, "y": -300, "text": "Website Xo em · 8 trang", "kind": "title1", "maxW": 3000, "page": "web"}
for gid, pid, label in (("cust", "khach", "Ứng dụng Zalo cho khách · gọi món, thanh toán, tích điểm"), ("staff", "nhanvien", "Ứng dụng Zalo cho nhân viên và quản lý")):
    for i, name in enumerate(groups[gid]): put(name, (i % 4) * 470, (i // 4) * 964, pid)
    notes["t_" + pid] = {"x": 0, "y": -300, "text": label, "kind": "title1", "maxW": 1800, "page": pid}
for i, name in enumerate(groups["morec"]): put(name, i * 470, 0, "trangthai")
for i, name in enumerate(groups["mores"]): put(name, i * 470, 844 + 420, "trangthai")
notes["t_tt"] = {"x": 0, "y": -300, "text": "Khách · lần đầu vào, giỏ trống, lỗi thanh toán, thông báo, ưu đãi, lịch sử, quán đóng, mất mạng", "kind": "title1", "maxW": 3600, "page": "trangthai"}
notes["t_tt2"] = {"x": 0, "y": 844 + 120, "text": "Nhân viên & quản lý · đăng nhập, thông báo, bảng lương theo công, báo cáo tuần, ưu đãi, đổi cửa hàng", "kind": "title1", "maxW": 3600, "page": "trangthai"}
canvas = {"v": 3, "createdOnFiles": {"v": 1, "at": "2026-11-25T07:45:00Z"}, "title": "Xo em – Website & ứng dụng Zalo",
          "launch": {"view": "canvas", "page": "web"}, "pages": pages, "boards": boards, "order": order, "notes": notes, "designSystems": []}
json.dump(canvas, open(os.path.join(ROOT, "canvas.json"), "w"), ensure_ascii=False)
print({k: heights[k] for k in files if k.startswith("W")}, len(order))
