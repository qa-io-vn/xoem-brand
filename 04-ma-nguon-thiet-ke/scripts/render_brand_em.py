import asyncio, json
from playwright.async_api import async_playwright
F = "file:///home/claude/fonts/"
css = f"""
@font-face{{font-family:'Baloo 2';src:url({F}Baloo2.ttf);font-weight:400 800}}
@font-face{{font-family:'Patrick Hand';src:url({F}PatrickHand-Regular.ttf)}}
@font-face{{font-family:'Be Vietnam Pro';src:url({F}BeVietnamPro-Regular.ttf);font-weight:400}}
@font-face{{font-family:'Be Vietnam Pro';src:url({F}BeVietnamPro-Medium.ttf);font-weight:500}}
@font-face{{font-family:'Be Vietnam Pro';src:url({F}BeVietnamPro-SemiBold.ttf);font-weight:600}}
@font-face{{font-family:'Be Vietnam Pro';src:url({F}BeVietnamPro-Bold.ttf);font-weight:700}}
body{{margin:0}}
"""
order = json.load(open("/home/claude/xoem-brand/order.json"))
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--allow-file-access-from-files"])
        pg = await b.new_page(viewport={"width": 1600, "height": 1000}, device_scale_factor=1.5)
        for i, f in enumerate(order):
            src = open(f"/home/claude/xoem-brand/project/{f}").read()
            body = src.split("</helmet>",1)[1].split("</x-dc>",1)[0]
            html = f"<!doctype html><html lang='vi'><head><meta charset='utf-8'><style>{css}</style></head><body>{body}</body></html>"
            open("/home/claude/tmp_render.html","w").write(html)
            await pg.goto("file:///home/claude/tmp_render.html")
            await pg.evaluate("document.fonts.ready")
            await pg.wait_for_timeout(300)
            await pg.screenshot(path=f"/home/claude/out/brand-em/XoEm-{i:02d}-{f.replace('.dc.html','')}.png", clip={"x":0,"y":0,"width":1600,"height":1000})
        await b.close()
asyncio.run(main())
