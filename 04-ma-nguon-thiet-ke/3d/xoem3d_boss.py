import math
from mathutils import Vector
import xoem3d_core as k

NAME = "Boss"


def saucer(put):
    profile = [(0.0, 0.0), (0.30, 0.0), (0.42, 0.004), (0.50, 0.012), (0.55, 0.026), (0.585, 0.045), (0.602, 0.060),
               (0.600, 0.068), (0.588, 0.071), (0.57, 0.063), (0.53, 0.050), (0.46, 0.038), (0.36, 0.033), (0.0, 0.033)]
    put("root", k.lathe("Boss_DiaLot", profile, "Su_KemSua", seg=96, subsurf=1))
    for r, z, name in ((0.515, 0.0475, "Boss_DiaVienNgoai"), (0.40, 0.0365, "Boss_DiaVienTrong")):
        pts = k.circle_points((0, 0, z), (0, 0, 1), r, 96, up=(0, 1, 0))
        put("root", k.tube(name, None, 0.0042, "Su_DatNung", ring=8, closed=True, caps=False, outline=k.OUTLINE_NONE,
                           dense=pts))


def legs(put):
    profile = [(0.0, 0.0), (0.030, 0.0), (0.043, 0.014), (0.046, 0.034), (0.041, 0.054), (0.031, 0.068),
               (0.028, 0.098), (0.036, 0.108), (0.036, 0.116), (0.0, 0.116)]
    for i, (x, y) in enumerate(((-0.33, -0.24), (0.33, -0.24), (-0.33, 0.24), (0.33, 0.24))):
        put("root", k.lathe("Boss_ChanGo_%d" % i, profile, "Go_OcCho", seg=32, matrix=k.to4(k.rot(), (x, y, 0.034)),
                            subsurf=1))


def base(put):
    b = k.RBox("Boss_ThanDuoi", (0, 0, 0.31), (1.18, 0.84, 0.36), 0.07, "Vai_DatNung", cuts=12,
               bulge={"-y": 0.016, "+y": 0.01, "+x": 0.01, "-x": 0.01}, taper=(0.74, 0.78))
    put("base", b.obj)
    for face, name in (("+z", "Boss_ThanDuoi_VienTren"), ("-z", "Boss_ThanDuoi_VienDuoi")):
        put("base", k.tube(name, None, 0.0085, "Vai_DatNungDam", ring=10, closed=True, caps=False,
                           outline=k.OUTLINE_NONE, dense=b.seam(face, offset=0.002)))
    studs = []
    count = 17
    for i in range(count):
        x = -0.48 + 0.96 * i / (count - 1)
        p, n = b.face_point("-y", x, 0.115, offset=0.0)
        studs.append((p, (0.0125, 0.0125, 0.008), k.frame_z(n)))
    for side in (-1, 1):
        for i in range(9):
            y = -0.30 + 0.60 * i / 8
            p, n = b.face_point("+x" if side > 0 else "-x", y, 0.115)
            studs.append((p, (0.0125, 0.0125, 0.008), k.frame_z(n)))
    put("base", k.multi_ellipsoid("Boss_DinhDong", studs, "Dong_Thau", seg=16, rings=8))
    return b


def seat(put):
    s = k.RBox("Boss_DemNgoi", (0, -0.18, 0.53), (0.76, 0.46, 0.13), 0.05, "Vai_DatNung", cuts=10,
               bulge={"+z": 0.03, "-y": 0.012})
    put("seat", s.obj)
    for face, name in (("+z", "Boss_DemNgoi_VienTren"), ("-z", "Boss_DemNgoi_VienDuoi")):
        put("seat", k.tube(name, None, 0.0075, "Vai_DatNungDam", ring=10, closed=True, caps=False,
                           outline=k.OUTLINE_NONE, dense=s.seam(face, offset=0.002)))
    return s


def armrest(put, side):
    tag = "R" if side < 0 else "L"
    bone = "arm_" + tag
    outer = "+x" if side > 0 else "-x"
    a = k.RBox("Boss_TayVin_" + tag, (0.49 * side, 0.0, 0.665), (0.22, 0.86, 0.41), 0.10, "Vai_DatNung", cuts=10,
               bulge={outer: 0.014, "+z": 0.012})
    put(bone, a.obj)
    put(bone, k.tube("Boss_TayVin_%s_Vien" % tag, None, 0.008, "Vai_DatNungDam", ring=10, closed=True, caps=False,
                     outline=k.OUTLINE_NONE, dense=a.seam("-y", offset=0.002)))
    p, n = a.face_point("-y", 0.0, 0.035)
    F = k.frame_z(n)
    put(bone, k.ellipsoid("Boss_TayVin_%s_Cuon" % tag, p, (0.072, 0.082, 0.02), "Vai_DatNung", R=F, subsurf=1,
                          outline=k.OUTLINE_NONE))
    ring = k.circle_points(p + n * 0.006, n, 0.073, 48)
    ring = [p + F @ Vector(((q - p).dot(F.col[0]), (q - p).dot(F.col[1]) * 1.12, (q - p).dot(F.col[2])))
            for q in ring]
    put(bone, k.tube("Boss_TayVin_%s_CuonVien" % tag, None, 0.0065, "Vai_DatNungDam", ring=10, closed=True,
                     caps=False, outline=k.OUTLINE_NONE, dense=ring))
    put(bone, k.ellipsoid("Boss_TayVin_%s_Nut" % tag, p + n * 0.018, (0.02, 0.02, 0.012), "Vai_DatNungDam", R=F,
                          seg=16, rings=8, subsurf=1, outline=k.OUTLINE_NONE))
    return a


def backrest(put):
    b = k.RBox("Boss_LungTua", (0, 0.22, 0.77), (0.78, 0.36, 0.62), 0.12, "Vai_DatNung", rot_deg=(-5, 0, 0),
               cuts=12, bulge={"-y": 0.045, "+y": 0.02, "+z": 0.015})
    put("back", b.obj)
    for face, name in (("-y", "Boss_LungTua_VienTruoc"), ("+y", "Boss_LungTua_VienSau")):
        put("back", k.tube(name, None, 0.0085, "Vai_DatNungDam", ring=10, closed=True, caps=False,
                           outline=k.OUTLINE_NONE, dense=b.seam(face, offset=0.002)))
    grid = [(-0.2, 0.12), (0.0, 0.12), (0.2, 0.12), (-0.1, 0.0), (0.1, 0.0), (-0.2, -0.12), (0.0, -0.12),
            (0.2, -0.12)]
    buttons = []
    for x, z in grid:
        p, n = b.face_point("+y", -x, z)
        buttons.append((p, (0.019, 0.019, 0.012), k.frame_z(n)))
    put("back", k.multi_ellipsoid("Boss_NutBoc", buttons, "Vai_DatNungDam", subsurf=1))
    creases = [(0, 3), (1, 3), (1, 4), (2, 4), (3, 5), (3, 6), (4, 6), (4, 7)]
    paths = []
    for a, c in creases:
        pa, pc = Vector(grid[a]), Vector(grid[c])
        paths.append([b.face_point("+y", -pa.lerp(pc, s / 8).x, pa.lerp(pc, s / 8).y, offset=-0.002)[0]
                      for s in range(9)])
    put("back", k.multi_tube("Boss_NepBoc", paths, 0.0045, "Vai_DatNungDam", ring=8))
    return b


def face(put, rig_bones, b):
    eyes = {}
    for tag, x, z, r, look in (("R", -0.15, 0.07, 0.118, (0.42, -0.30, 0.86)),
                               ("L", 0.155, 0.045, 0.074, (-0.50, -0.22, 0.84))):
        p, n = b.face_point("-y", x, z)
        e = k.googly_eye("Boss_Mat" + tag, p, n, r, r * 0.55, look)
        eyes[tag] = e
        rig_bones.append(("eye_" + tag, p, "back"))
        rig_bones.append(("pupil_" + tag, p + n * 0.001, "eye_" + tag))
        put("eye_" + tag, e["sclera"], e["rim"])
        put("pupil_" + tag, e["iris"], e["pupil"], e["glint"])
    mouth = []
    for s in range(13):
        u = -1 + 2 * s / 12
        p, n = b.face_point("-y", 0.075 * u + 0.008, -0.075 - 0.022 * (1 - u * u), offset=0.004)
        mouth.append(p)
    mouth_center, _ = b.face_point("-y", 0.008, -0.09)
    rig_bones.append(("mouth", mouth_center, "back"))
    put("mouth", k.tube("Boss_Mieng", None, 0.0095, "Net_Ve", ring=10, caps=True, outline=k.OUTLINE_NONE, dense=mouth))
    for tag, x0, z0, x1, z1, arch in (("R", -0.255, 0.205, -0.075, 0.18, 0.018), ("L", 0.085, 0.152, 0.225, 0.168, 0.012)):
        pts = []
        for s in range(9):
            u = s / 8
            p, n = b.face_point("-y", x0 + (x1 - x0) * u, z0 + (z1 - z0) * u + arch * math.sin(math.pi * u),
                                offset=0.006)
            pts.append(p)
        rig_bones.append(("brow_" + tag, pts[4], "back"))
        put("brow_" + tag, k.tube("Boss_LongMay_" + tag, None, lambda t: 0.0125 * (0.75 + 0.25 * math.sin(math.pi * t)),
                                  "Vai_DatNungDam", ring=12, caps=True, outline=k.OUTLINE_SMALL, dense=k.spline(pts, 4)))
    return eyes


def steam(put, rig_bones):
    for tag, x in (("R", -0.085), ("L", 0.085)):
        y = 0.245
        flip = -1 if tag == "R" else 1
        pts = [(x, y, 1.115), (x + 0.032 * flip, y, 1.185), (x, y, 1.255), (x - 0.032 * flip, y, 1.325),
               (x, y, 1.39)]
        rig_bones.append(("steam_" + tag, Vector((x, y, 1.115)), "back"))
        put("steam_" + tag, k.tube("Boss_HoiNuoc_" + tag, pts,
                                   lambda t: 0.019 * (1.0 - 0.45 * t) * min(1.0, 0.35 + t * 6),
                                   "Hoi_Nuoc", ring=12, per_seg=10, caps=True, outline=k.OUTLINE_SMALL))


def build():
    groups = {}

    def put(bone, *objs):
        groups.setdefault(bone, []).extend(objs)

    saucer(put)
    legs(put)
    b = base(put)
    seat(put)
    armrest(put, -1)
    armrest(put, 1)
    back = backrest(put)
    extra = []
    face(put, extra, back)
    steam(put, extra)

    rig = k.Rig(NAME)
    rig.bone("root", (0, 0, 0), length=0.12)
    rig.bone("base", (0, 0, 0.14), "root")
    rig.bone("seat", (0, -0.18, 0.47), "base")
    rig.bone("arm_R", (-0.49, 0, 0.47), "base")
    rig.bone("arm_L", (0.49, 0, 0.47), "base")
    rig.bone("back", (0, 0.22, 0.47), "base")
    for name, head, parent in extra:
        rig.bone(name, head, parent, length=0.04)
    rig.build()
    for bone, objs in groups.items():
        rig.attach(objs, bone)
    animate(rig)
    return rig


def animate(rig):
    def breath(t, period=2.0):
        return 0.5 - 0.5 * math.cos(2 * math.pi * t / period)

    def steam_track(offset, period):
        def f(t):
            ph = (t / period + offset) % 1.0
            s = math.sin(math.pi * ph) ** 0.8
            return {"loc": (0.008 * k.wave(t, period, offset * 6), 0, 0.09 * ph - 0.02), "scale": (s, s, s)}
        return f

    def blink(t, at):
        return 1.0 - 0.92 * max(k.bump(t, c, 0.11) for c in at)

    rig.action("Idle", 4.0, {
        "back": lambda t: {"rot": (-1.0 * k.wave(t, 4.0), 0, 0), "scale": (1, 1, 1 + 0.012 * breath(t))},
        "seat": lambda t: {"scale": (1, 1, 1 + 0.035 * breath(t))},
        "arm_R": lambda t: {"rot": (0, -1.6 * breath(t), 0)},
        "arm_L": lambda t: {"rot": (0, 1.6 * breath(t), 0)},
        "eye_R": lambda t: {"scale": (1, 1, blink(t, (2.9,)))},
        "eye_L": lambda t: {"scale": (1, 1, blink(t, (2.9,)))},
        "pupil_R": lambda t: {"loc": (0.012 * k.wave(t, 4.0), 0, 0.006 * k.wave(t, 4.0, 1.2))},
        "pupil_L": lambda t: {"loc": (0.008 * k.wave(t, 4.0, 0.5), 0, 0.004 * k.wave(t, 4.0, 1.7))},
        "brow_R": lambda t: {"loc": (0, 0, 0.008 * k.bump(t, 1.3, 0.45)), "rot": (0, -6 * k.bump(t, 1.3, 0.45), 0)},
        "mouth": lambda t: {"scale": (1 + 0.06 * breath(t), 1, 1)},
        "steam_R": steam_track(0.0, 2.0),
        "steam_L": steam_track(0.5, 2.0),
    })

    def pats(t):
        return k.bump(t, 0.62, 0.32) + k.bump(t, 1.32, 0.32)

    def lean(t):
        return k.window(t, 0.1, 0.45, 1.75, 2.3)

    rig.action("Pat", 2.4, {
        "arm_R": lambda t: {"rot": (0, 24 * pats(t), 0)},
        "arm_L": lambda t: {"rot": (0, -24 * pats(t), 0)},
        "back": lambda t: {"rot": (6 * lean(t), 0, 0)},
        "seat": lambda t: {"scale": (1, 1, 1 - 0.09 * (k.bump(t, 0.7, 0.14) + k.bump(t, 1.4, 0.14)))},
        "eye_R": lambda t: {"scale": (1, 1, 1 - 0.45 * lean(t))},
        "eye_L": lambda t: {"scale": (1, 1, 1 - 0.45 * lean(t))},
        "mouth": lambda t: {"scale": (1 + 0.35 * lean(t), 1, 1 + 0.4 * lean(t))},
        "brow_R": lambda t: {"loc": (0, 0, 0.012 * lean(t))},
        "brow_L": lambda t: {"loc": (0, 0, 0.012 * lean(t))},
        "steam_R": steam_track(0.0, 1.2),
        "steam_L": steam_track(0.5, 1.2),
    })
