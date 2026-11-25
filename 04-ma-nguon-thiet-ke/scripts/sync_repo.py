import os, re, shutil, sys, glob, html
sys.path.insert(0, "/home/claude")
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    from app_more import files
R = "/home/claude/repo/xoem-brand"
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@500;600;700;800&family=Be+Vietnam+Pro:wght@400;500;600;700&family=Patrick+Hand&display=swap">'
def fname(n): return "Main" if n == "W01_Home" else n
def fix(s): return re.sub(r'([A-Z]\d\d_[A-Za-z]+)\.dc\.html', lambda m: fname(m.group(1)) + ".html", s)
D = f"{R}/docs"; os.makedirs(D, exist_ok=True)
for f in glob.glob(f"{D}/*.html"): os.remove(f)
groups = {"web": [], "cust": [], "morec": [], "staff": [], "mores": []}
for n, (title, body, w, h, kind) in files.items():
    groups[kind].append((n, title))
    center = "" if kind == "web" else "<style>body{display:flex;justify-content:center;background:#E8D5B5;padding:24px 0}</style>"
    open(f"{D}/{fname(n)}.html", "w").write(f'<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{title}</title>{FONTS}<style>body{{margin:0}}a{{color:#8F3A26}}</style>{center}</head><body>\n{fix(body)}\n</body></html>')
sec = [("Website", "web"), ("Ứng dụng Zalo · Khách", "cust"), ("Khách · Trạng thái & màn hình thêm", "morec"), ("Ứng dụng Zalo · Nhân viên & quản lý", "staff"), ("Nhân viên · Màn hình thêm", "mores")]
lists = "".join(f"<h2>{t}</h2><ul>" + "".join(f'<li><a href="{fname(n)}.html">{html.escape(ti, quote=False)}</a></li>' for n, ti in groups[k]) + "</ul>" for t, k in sec)
open(f"{D}/index.html", "w").write(f'<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Xo em – Bản thiết kế bấm thử</title>{FONTS}<style>body{{margin:0;background:#F6EEDF;color:#2B1D16;font-family:\'Be Vietnam Pro\',sans-serif}}main{{max-width:760px;margin:0 auto;padding:48px 24px}}h1{{font-family:\'Baloo 2\',sans-serif;font-size:44px;margin:0 0 8px}}h2{{font-family:\'Baloo 2\',sans-serif;margin:28px 0 4px}}li{{margin:8px 0;font-size:17px}}a{{color:#C8553D;font-weight:600}}</style></head><body><main><h1>Xo em · Bản thiết kế bấm thử</h1><p>{len(files)} màn hình: website, ứng dụng Zalo cho khách và cho nhân viên/quản lý. Bấm nút trong từng màn hình để đi tiếp.</p>{lists}</main></body></html>')
# source
S = f"{R}/04-ma-nguon-thiet-ke"
for f in glob.glob(f"{S}/*.py"): os.remove(f)
for f in ["app_common.py", "app_screens.py", "app_web.py", "app_more.py", "app_build.py", "app_build2.py", "brand.py", "brand_em.py", "merch.py", "xoem_extra.py", "kit.py", "logo2.py", "logo5.py", "logo6.py", "compare.py", "render_brand_em.py", "sync_repo.py"]:
    if os.path.exists(f"/home/claude/{f}"): shutil.copy(f"/home/claude/{f}", f"{S}/scripts/")
W = f"{S}/website-zalo-app"; shutil.rmtree(W); shutil.copytree("/home/claude/xoem-app/project", W)
for sub, pat in (("website", "W0*.png"), ("app-khach", "C*.png"), ("app-nhan-vien", "S*.png")):
    for f in glob.glob(f"/home/claude/out/app/{pat}"): shutil.copy(f, f"{R}/03-website-zalo-app/{sub}/")
print(len(files), "pages")
