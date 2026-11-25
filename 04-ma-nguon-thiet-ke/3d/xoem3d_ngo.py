import math
from mathutils import Vector, Matrix
import xoem3d_core as k

NAME = "Em_Ngo"

HEAD_C = Vector((0.0, 0.0, 0.75))
HEAD_R = (0.30, 0.255, 0.25)
BODY_C = Vector((0.0, 0.015, 0.30))
BODY_R = (0.262, 0.232, 0.29)
BELLY_C = Vector((0.0, -0.168, 0.27))
BELLY_R = (0.172, 0.205, 0.085)
BELLY_M = k.frame_z(Vector((0, -1, 0)))
CUP_TILT = k.rot(0, 18, 0) @ k.rot(0, 0, -30)


def body_deform(p):
    s = 1.0 - 0.12 * max(p.z, 0.0)
    z = p.z * (0.92 if p.z < 0 else 1.0)
    return Vector((p.x * s, p.y * s, z))


def body_implicit(q):
    d = Vector(q) - BODY_C
    z = d.z / (BODY_R[2] * (0.92 if d.z < 0 else 1.0))
    s = 1.0 - 0.12 * max(z, 0.0)
    x = d.x / (BODY_R[0] * s)
    y = d.y / (BODY_R[1] * s)
    return x * x + y * y + z * z


HEAD_IMPLICIT = k.ellipsoid_implicit(HEAD_C, HEAD_R)


def side_tag(x):
    return "R" if x < 0 else "L"


def head_front(x, z, offset=0.0):
    p, n = k.ellipsoid_front(HEAD_C, HEAD_R, x, z)
    return p + n * offset, n


def body(put):
    surf = k.deformed_surface(BODY_C, BODY_R, body_deform)
    put("hips", k.ellipsoid("EmNgo_Than", BODY_C, BODY_R, "Da_Reu", seg=36, rings=18, deform=body_deform, subsurf=1))
    put("hips", k.ellipsoid("EmNgo_Bung", BELLY_C, BELLY_R, "Bung_CatMin", R=BELLY_M, seg=32, rings=16, subsurf=1,
                            outline=k.OUTLINE_NONE))
    rim = k.intersection_ring(BELLY_C, BELLY_R, BELLY_M, body_implicit, count=64, lift=0.002)
    put("hips", k.tube("EmNgo_Bung_Vien", None, 0.0068, "Net_Ve", ring=10, closed=True, caps=False,
                       outline=k.OUTLINE_NONE, dense=rim))
    spine = []
    for s in range(15):
        v = 0.86 - 1.72 * s / 14
        p, n = k.ellipsoid_surface(BELLY_C, BELLY_R, BELLY_M, (0.0, v, 1.0))
        spine.append(p + n * 0.003)
    bars = [spine]
    for j, v in enumerate((0.62, 0.32, 0.02, -0.28, -0.58)):
        bar = []
        for s in range(5):
            u = -0.32 + 0.64 * s / 4
            p, n = k.ellipsoid_surface(BELLY_C, BELLY_R, BELLY_M, (u, v, 1.0))
            bar.append(p + n * 0.003)
        bars.append(bar)
    put("hips", k.multi_tube("EmNgo_Bung_DuongKhau", bars, 0.0058, "Net_Ve", ring=8))
    spots = []
    for d, r in (((0.55, 0.75, 0.35), 0.028), ((-0.5, 0.8, 0.1), 0.024), ((0.2, 0.95, -0.2), 0.02),
                 ((-0.75, 0.3, 0.45), 0.022), ((0.8, 0.2, -0.3), 0.02)):
        p, n = surf.toward(d)
        spots.append((p, (r, r, 0.006), k.frame_z(n)))
    put("hips", k.multi_ellipsoid("EmNgo_Than_Dom", spots, "Da_ReuNhat", subsurf=1))
    plates = []
    for i, (d, size) in enumerate((((0, 1, 0.55), 1.0), ((0, 1, 0.15), 0.92), ((0, 1, -0.25), 0.78))):
        p, n = surf.toward(d)
        plates.append(leaf_plate("EmNgo_LaLung_%d" % i, p, n, size))
    put("hips", *plates)
    return surf


def leaf_plate(name, p, n, size):
    tilt = (n + Vector((0, 0.0, -0.35))).normalized()
    F = k.frame_z(tilt, Vector((0, 0, 1)))
    radii = (0.014 * size, 0.05 * size, 0.062 * size)
    return k.ellipsoid(name, p + tilt * (0.062 * size * 0.5 - 0.02), radii, "Da_ReuNhat", R=F, seg=20, rings=12,
                       deform=lambda q: Vector((q.x * (1 - 0.45 * max(q.z, 0)), q.y * (1 - 0.55 * max(q.z, 0)), q.z)),
                       subsurf=1, outline=k.OUTLINE_SMALL)


def feet(put, bones):
    for x in (-0.13, 0.13):
        tag = side_tag(x)
        c = Vector((x, -0.05, 0.048))
        radii = (0.115, 0.15, 0.052)
        R = k.rot(0, 0, 8 if x < 0 else -8)
        bones.append(("foot_" + tag, Vector((x, -0.04, 0.0)), "root"))
        put("foot_" + tag, k.ellipsoid("EmNgo_BanChan_" + tag, c, radii, "Da_Reu", R=R, seg=28, rings=14,
                                       deform=lambda q: Vector((q.x, q.y, q.z * (0.55 if q.z < 0 else 1.0))),
                                       subsurf=1))
        claws = []
        for s in (-1, 0, 1):
            p, n = k.ellipsoid_surface(c, radii, R, (0.42 * s, -1.0, 0.1))
            claws.append((p + n * 0.004, (0.017, 0.017, 0.016), k.frame_z(n)))
        put("foot_" + tag, k.multi_ellipsoid("EmNgo_MongChan_" + tag, claws, "Sung_CatMin", subsurf=1,
                                             outline=k.OUTLINE_SMALL))


def arms(put, bones):
    for sx in (-1, 1):
        tag = side_tag(sx)
        sh = Vector((0.232 * sx, -0.01, 0.43))
        pts = [sh, Vector((0.296 * sx, -0.04, 0.372)), Vector((0.32 * sx, -0.076, 0.298)),
               Vector((0.302 * sx, -0.108, 0.24))]
        bones.append(("arm_" + tag, sh, "hips"))
        hand_c = Vector((0.298 * sx, -0.118, 0.222))
        objs = [k.tube("EmNgo_Tay_" + tag, pts, lambda t: 0.058 - 0.01 * t, "Da_Reu", ring=18, per_seg=8,
                       outline=k.OUTLINE_MAIN),
                k.ellipsoid("EmNgo_BanTay_" + tag, hand_c, (0.062, 0.058, 0.06), "Da_Reu", seg=24, rings=12,
                            subsurf=1)]
        fingers = []
        for s in (-1, 0, 1):
            p, n = k.ellipsoid_surface(hand_c, (0.062, 0.058, 0.06), None, (0.45 * s - 0.25 * sx, -0.75, -0.55))
            fingers.append((p, (0.022, 0.022, 0.02), k.frame_z(n)))
        objs.append(k.multi_ellipsoid("EmNgo_NgonTay_" + tag, fingers, "Da_Reu", subsurf=1, outline=k.OUTLINE_SMALL))
        spot_p, spot_n = k.ellipsoid_surface(hand_c, (0.062, 0.058, 0.06), None, (0.6 * sx, 0.2, 0.75))
        objs.append(k.ellipsoid("EmNgo_BanTay_Dom_" + tag, spot_p, (0.016, 0.016, 0.005), "Da_ReuNhat",
                                R=k.frame_z(spot_n), seg=16, rings=8, subsurf=1, outline=k.OUTLINE_NONE))
        put("arm_" + tag, *objs)


def head(put, bones):
    put("head", k.ellipsoid("EmNgo_Dau", HEAD_C, HEAD_R, "Da_Reu", seg=40, rings=20, subsurf=1))
    for tag, x, z, r, look in (("R", -0.112, 0.802, 0.108, (0.32, -0.24, 0.92)),
                               ("L", 0.126, 0.787, 0.064, (-0.48, -0.1, 0.87))):
        p, n = head_front(x, z)
        e = k.googly_eye("EmNgo_Mat" + tag, p, n, r, r * 0.6, look, implicit=HEAD_IMPLICIT)
        bones.append(("eye_" + tag, p, "head"))
        bones.append(("pupil_" + tag, p + n * 0.001, "eye_" + tag))
        put("eye_" + tag, e["sclera"], e["rim"])
        put("pupil_" + tag, e["iris"], e["pupil"], e["glint"])
    nostrils = []
    for x in (-0.034, 0.03):
        p, n = head_front(x, 0.692)
        nostrils.append((p - n * 0.002, (0.012, 0.012, 0.007), k.frame_z(n)))
    put("head", k.multi_ellipsoid("EmNgo_LoMui", nostrils, "Net_Ve", subsurf=1))
    mouth = []
    for s in range(17):
        u = -1 + 2 * s / 16
        x = 0.118 * u
        z = 0.633 + 0.03 * (u * u) + 0.004 * u
        mouth.append(head_front(x, z, 0.004)[0])
    put("head", k.tube("EmNgo_Mieng", None, lambda t: 0.0085 * (0.65 + 0.35 * math.sin(math.pi * t)), "Net_Ve",
                       ring=10, outline=k.OUTLINE_NONE, dense=mouth))
    tp, tn = head_front(-0.036, 0.618)
    TF = k.frame_z(tn)
    tooth_pts = [(-0.017, 0.006), (0.017, 0.006), (0.018, -0.02), (0.013, -0.034), (-0.013, -0.034), (-0.018, -0.02)]
    put("head", k.prism("EmNgo_Rang", tooth_pts, 0.012, "Rang", matrix=k.to4(TF, tp + tn * 0.003), subsurf=1,
                        outline=k.OUTLINE_SMALL))
    gp, gn = head_front(0.052, 0.624)
    bones.append(("tongue", gp, "head"))
    GF = k.frame_z(gn) @ k.rot(0, 0, -10)
    tongue_c = gp + gn * 0.014 + GF.col[1] * -0.044
    put("tongue", k.ellipsoid("EmNgo_Luoi", tongue_c, (0.037, 0.056, 0.018), "Luoi", R=GF, seg=24, rings=12,
                              deform=lambda q: Vector((q.x * (1.0 + 0.15 * min(q.y, 0)), q.y, q.z)), subsurf=1,
                              outline=k.OUTLINE_SMALL))
    groove = [tongue_c + GF @ Vector((0, 0.036 - 0.06 * s / 4, 0.0185)) for s in range(5)]
    put("tongue", k.tube("EmNgo_Luoi_Ranh", None, 0.0022, "Vai_DatNungDam", ring=6, outline=k.OUTLINE_NONE,
                         dense=groove))
    spots = []
    for x, z, r in ((-0.168, 0.905, 0.032), (0.17, 0.9, 0.03), (-0.215, 0.652, 0.03), (0.226, 0.642, 0.03)):
        p, n = head_front(x, z)
        spots.append((p, (r, r, 0.006), k.frame_z(n)))
    for d, r in (((0.35, 0.55, 0.75), 0.03), ((-0.45, 0.65, 0.55), 0.026), ((0.1, 0.9, 0.3), 0.024),
                 ((-0.2, 0.85, -0.3), 0.022), ((0.6, 0.5, -0.2), 0.024)):
        p, n = k.ellipsoid_surface(HEAD_C, HEAD_R, None, d)
        spots.append((p, (r, r, 0.006), k.frame_z(n)))
    put("head", k.multi_ellipsoid("EmNgo_Dau_Dom", spots, "Da_ReuNhat", subsurf=1))
    for sx in (-1, 1):
        tag = side_tag(sx)
        p, n = k.ellipsoid_surface(HEAD_C, HEAD_R, None, (sx, 0.1, 0.14))
        F = k.rot(0, 0, 16 * sx) @ k.frame_z(Vector((0, -1, 0)))
        out = F.col[0] * sx
        c = p + out * 0.04
        bones.append(("fin_" + tag, p, "head"))
        fin = k.ellipsoid("EmNgo_Vay_" + tag, c, (0.078, 0.066, 0.017), "Da_ReuNhat", R=F, seg=28, rings=14,
                          deform=lambda q, sx=sx: Vector((q.x, q.y * (1 - 0.3 * max(q.x * sx, 0)) + 0.18 * max(q.x * sx, 0)
                                                          , q.z)), subsurf=1)
        ribs = []
        for ang in (-28, 0, 28):
            a = math.radians(ang)
            d = F @ Vector((math.cos(a) * sx, math.sin(a) + 0.1, 0.0))
            ribs.append([c - out * 0.03 + F.col[2] * 0.0165 + d * (0.012 + 0.05 * s / 4) for s in range(5)])
        put("fin_" + tag, fin, k.multi_tube("EmNgo_Vay_Gan_" + tag, ribs, 0.0036, "Da_ReuDam", ring=6))
    plates = []
    for i, (d, size) in enumerate((((0, 0.5, 0.86), 0.85), ((0, 0.82, 0.57), 1.0), ((0, 0.98, 0.18), 0.9))):
        p, n = k.ellipsoid_surface(HEAD_C, HEAD_R, None, d)
        plates.append(leaf_plate("EmNgo_LaDau_%d" % i, p, n, size))
    put("head", *plates)
    horns(put, bones)


def horns(put, bones):
    p, n = k.ellipsoid_surface(HEAD_C, HEAD_R, None, (-0.46, 0.12, 0.88))
    pts = [p - n * 0.035, p + n * 0.06, p + n * 0.06 + Vector((-0.03, 0.022, 0.075)),
           p + n * 0.06 + Vector((-0.022, 0.05, 0.14))]
    bones.append(("horn_R", p, "head"))
    put("horn_R", k.tube("EmNgo_Sung_R", pts, lambda t: 0.05 * (1 - t) + 0.007 * t, "Sung_CatMin", ring=18,
                         per_seg=8, outline=k.OUTLINE_MAIN))
    p, n = k.ellipsoid_surface(HEAD_C, HEAD_R, None, (0.46, 0.12, 0.88))
    p1 = p + n * 0.05
    p2 = p1 + Vector((0.026, 0.012, 0.058))
    bones.append(("cup", p, "head"))
    put("cup", k.tube("EmNgo_Sung_L", [p - n * 0.035, p1, p2], lambda t: 0.047 * (1 - t) + 0.02 * t, "Sung_CatMin",
                      ring=18, per_seg=8, outline=k.OUTLINE_MAIN))
    origin = p1.lerp(p2, 0.25)
    M = k.to4(CUP_TILT, origin)
    cup = [(0.0, 0.0), (0.050, 0.0), (0.0535, 0.006), (0.0745, 0.138), (0.0775, 0.1395), (0.0782, 0.1425),
           (0.0755, 0.1445), (0.0712, 0.1415), (0.0698, 0.133), (0.0505, 0.012), (0.0, 0.012)]
    put("cup", k.lathe("EmNgo_Ly", cup, "Ly_Giay", seg=48, matrix=M, subsurf=1, outline=k.OUTLINE_MAIN))
    band = [(0.0646 + 0.0012, 0.072), (0.0694 + 0.0012, 0.103)]
    band_profile = [(band[0][0] - 0.0004, band[0][1] - 0.0004), band[0], band[1], (band[1][0] - 0.0004, band[1][1] + 0.0004)]
    put("cup", k.lathe("EmNgo_Ly_Bang", band_profile, "Ly_Bang", seg=48, matrix=M, subsurf=0, outline=k.OUTLINE_NONE))
    put("cup", k.lathe("EmNgo_CaPhe", [(0.0, 0.1185), (0.0668, 0.1185), (0.0668, 0.112), (0.0, 0.112)], "Ca_Phe",
                       seg=48, matrix=M, subsurf=0, outline=k.OUTLINE_NONE))
    heart = []
    for s in range(40):
        a = 2 * math.pi * s / 40
        hx = 16 * math.sin(a) ** 3
        hy = 13 * math.cos(a) - 5 * math.cos(2 * a) - 2 * math.cos(3 * a) - math.cos(4 * a)
        heart.append((hx * 0.0016, hy * 0.0016 + 0.002))
    put("cup", k.flat_shape("EmNgo_CaPhe_TraiTim", heart, 0.0012, "Bot_Sua", M @ k.to4(k.rot(0, 0, 30), (0, 0, 0.1192))))
    handle = [(0.068, 0, 0.112), (0.1, 0, 0.106), (0.112, 0, 0.078), (0.098, 0, 0.05), (0.064, 0, 0.048)]
    put("cup", k.tube("EmNgo_Ly_Quai", [M @ Vector(q) for q in handle], 0.0078, "Ly_Giay", ring=12, per_seg=8,
                      outline=k.OUTLINE_SMALL))
    steam_base = M @ Vector((0, 0, 0.165))
    bones.append(("steam", steam_base, "cup"))
    wisp = [(0, 0, 0.165), (0.016, 0, 0.205), (0.0, 0, 0.245), (-0.014, 0, 0.285), (0.0, 0, 0.32)]
    put("steam", k.tube("EmNgo_HoiNuoc", [k.to4(k.rot(0, -18, 0), (0, 0, 0)) @ (M @ Vector(q) - steam_base) + steam_base
                                         for q in wisp],
                        lambda t: 0.0135 * (1 - 0.45 * t) * min(1.0, 0.35 + 6 * t), "Hoi_Nuoc", ring=10, per_seg=8,
                        outline=k.OUTLINE_SMALL))


TAIL_PTS = [(0.1, 0.17, 0.13), (0.26, 0.25, 0.1), (0.43, 0.22, 0.13), (0.54, 0.12, 0.26), (0.56, 0.03, 0.41),
            (0.53, -0.01, 0.52)]
TAIL_JOINTS = [0.0, 0.33, 0.66, 1.0]


def tail(rig, put):
    dense = k.spline(TAIL_PTS, 12)
    lengths = [0.0]
    for i in range(1, len(dense)):
        lengths.append(lengths[-1] + (dense[i] - dense[i - 1]).length)
    total = lengths[-1]

    def at(t):
        target = t * total
        for i in range(1, len(dense)):
            if lengths[i] >= target:
                f = (target - lengths[i - 1]) / max(lengths[i] - lengths[i - 1], 1e-9)
                return dense[i - 1].lerp(dense[i], f)
        return dense[-1].copy()

    obj = k.tube("EmNgo_Duoi", None, lambda t: 0.076 - 0.046 * t, "Da_Reu", ring=20, dense=dense,
                 outline=k.OUTLINE_MAIN)
    heads = [at(max(c - 0.1, 0.0)) for c in TAIL_JOINTS]
    names = ["tail_%d" % i for i in range(len(TAIL_JOINTS))]
    for i, name in enumerate(names):
        tail_end = heads[i + 1] if i + 1 < len(heads) else at(1.0) + (at(1.0) - at(0.95)).normalized() * 0.05
        rig.bone(name, heads[i], names[i - 1] if i > 0 else "hips", tail=tail_end)
    end = at(1.0)
    T = (at(1.0) - at(0.94)).normalized()
    zf = Vector((0, -1, 0))
    zf = (zf - T * zf.dot(T)).normalized()
    xf = T.cross(zf).normalized()
    F = Matrix((xf, T, zf)).transposed()
    spade = [(0.0, 0.125), (0.014, 0.103), (0.072, 0.012), (0.064, -0.008), (0.0, -0.002), (-0.064, -0.008),
             (-0.072, 0.012), (-0.014, 0.103)]
    put("tail_3", k.prism("EmNgo_Duoi_Mui", spade, 0.03, "Chu_DatNung", matrix=k.to4(F, end - T * 0.03), subsurf=2,
                          outline=k.OUTLINE_MAIN))
    return obj, list(zip(names, TAIL_JOINTS))


def question(put, bones):
    p = Vector((0.47, -0.03, 1.02))
    bones.append(("qmark", p, "root"))
    put("qmark", k.text_mesh("EmNgo_DauHoi", "?", 0.26, 0.018, "Chu_DatNung", k.to4(k.rot(0, 10, 0) @ k.rot(90, 0, 0), p),
                             bevel=0.004, outline=k.OUTLINE_SMALL))


def build():
    groups = {}

    def put(bone, *objs):
        groups.setdefault(bone, []).extend(objs)

    extra = []
    body(put)
    feet(put, extra)
    arms(put, extra)
    head(put, extra)
    question(put, extra)
    rig = k.Rig(NAME)
    rig.bone("root", (0, 0, 0), length=0.12)
    rig.bone("hips", (0, 0, 0.1), "root")
    rig.bone("head", (0, 0, 0.52), "hips")
    for name, head_pos, parent in extra:
        rig.bone(name, head_pos, parent, length=0.04)
    tail_obj, joints = tail(rig, put)
    rig.build()
    for bone, objs in groups.items():
        rig.attach(objs, bone)
    rig.skin(tail_obj, joints)
    animate(rig)
    return rig


def animate(rig):
    def blink(t, at):
        return 1.0 - 0.93 * max([k.bump(t, c, 0.09) for c in at] + [0.0])

    def tail_wag(amp, period, phase=0.0):
        return {
            "tail_1": lambda t: {"rot": (0, 0, amp * k.wave(t, period, phase))},
            "tail_2": lambda t: {"rot": (0, 0, amp * 1.4 * k.wave(t, period, phase - 0.7))},
            "tail_3": lambda t: {"rot": (0, 0, amp * 1.8 * k.wave(t, period, phase - 1.4))},
        }

    def steam(period):
        def f(t):
            ph = (t / period) % 1.0
            s = math.sin(math.pi * ph) ** 0.8
            return {"loc": (0.004 * k.wave(t, period), 0, 0.05 * ph - 0.012), "scale": (s, s, s)}
        return f

    idle = {
        "hips": lambda t: {"loc": (0, 0, 0.006 * k.wave(t, 2.0)), "scale": (1 - 0.007 * k.wave(t, 2.0),
                                                                             1 - 0.007 * k.wave(t, 2.0),
                                                                             1 + 0.015 * k.wave(t, 2.0))},
        "head": lambda t: {"rot": (1.5 * k.wave(t, 2.0, 0.5), 3 * k.wave(t, 4.0), 0)},
        "eye_R": lambda t: {"scale": (1, 1, blink(t, (2.4, 2.66)))},
        "eye_L": lambda t: {"scale": (1, 1, blink(t, (2.4, 2.66)))},
        "pupil_R": lambda t: {"loc": (0.01 * k.wave(t, 4.0), 0, 0.006 * k.wave(t, 2.0))},
        "pupil_L": lambda t: {"loc": (-0.006 * k.wave(t, 4.0, 1.0), 0, 0.004 * k.wave(t, 2.0, 0.5))},
        "tongue": lambda t: {"rot": (6 * k.wave(t, 1.0), 0, 0)},
        "fin_R": lambda t: {"rot": (0, 8 * k.wave(t, 2.0), 0)},
        "fin_L": lambda t: {"rot": (0, -8 * k.wave(t, 2.0), 0)},
        "cup": lambda t: {"rot": (0, 4 * k.wave(t, 2.0, 1.0), 0)},
        "steam": steam(1.0),
        "qmark": lambda t: {"loc": (0, 0, 0.02 * k.wave(t, 2.0)), "rot": (0, 10 * k.wave(t, 4.0), 0)},
        "arm_R": lambda t: {"rot": (0, 3 * k.wave(t, 2.0), 0)},
        "arm_L": lambda t: {"rot": (0, -3 * k.wave(t, 2.0), 0)},
    }
    idle.update(tail_wag(10, 2.0))
    rig.action("Idle", 4.0, idle)

    def ph(t):
        return 2 * math.pi * t / 1.0

    walk = {
        "foot_R": lambda t: {"loc": (0, -0.07 * math.sin(ph(t)), 0.038 * max(0.0, math.cos(ph(t)))),
                             "rot": (-14 * max(0.0, math.cos(ph(t))) * math.sin(ph(t)), 0, 0)},
        "foot_L": lambda t: {"loc": (0, -0.07 * math.sin(ph(t) + math.pi), 0.038 * max(0.0, math.cos(ph(t) + math.pi))),
                             "rot": (-14 * max(0.0, math.cos(ph(t) + math.pi)) * math.sin(ph(t) + math.pi), 0, 0)},
        "hips": lambda t: {"loc": (0.012 * math.sin(ph(t)), 0, 0.014 * (0.5 - 0.5 * math.cos(2 * ph(t)))),
                           "rot": (0, 4 * math.sin(ph(t)), 0)},
        "head": lambda t: {"rot": (2 * math.sin(2 * ph(t) - 0.6), -3 * math.sin(ph(t) - 0.4), 0)},
        "arm_R": lambda t: {"rot": (20 * math.sin(ph(t)), 0, 0)},
        "arm_L": lambda t: {"rot": (-20 * math.sin(ph(t)), 0, 0)},
        "cup": lambda t: {"rot": (0, 6 * math.sin(ph(t) - 0.9), 0)},
        "steam": steam(0.5),
        "fin_R": lambda t: {"rot": (0, 10 * math.sin(2 * ph(t)), 0)},
        "fin_L": lambda t: {"rot": (0, -10 * math.sin(2 * ph(t)), 0)},
        "tongue": lambda t: {"rot": (8 * math.sin(2 * ph(t)), 0, 0)},
        "qmark": lambda t: {"loc": (0, 0, 0.015 * math.sin(2 * ph(t)))},
    }
    walk.update(tail_wag(12, 1.0, 0.8))
    rig.action("Walk", 1.0, walk)

    def tilt(t):
        return k.window(t, 0.1, 0.65, 2.2, 2.85)

    forget = {
        "head": lambda t: {"rot": (-6 * tilt(t), 14 * tilt(t), 0)},
        "hips": lambda t: {"loc": (0, 0, 0.01 * tilt(t))},
        "pupil_R": lambda t: {"loc": (0.006 * tilt(t), 0, 0.014 * tilt(t))},
        "pupil_L": lambda t: {"loc": (0.004 * tilt(t), 0, 0.009 * tilt(t))},
        "eye_R": lambda t: {"scale": (1, 1, blink(t, (1.9,)))},
        "eye_L": lambda t: {"scale": (1, 1, blink(t, (1.9,)))},
        "arm_R": lambda t: {"rot": (0, 38 * tilt(t), 0)},
        "arm_L": lambda t: {"rot": (0, -38 * tilt(t), 0)},
        "qmark": lambda t: {"loc": (0, 0, 0.03 * tilt(t)), "scale": [1 + 0.5 * k.bump(t, 0.55, 0.3) + 0.15 * tilt(t)] * 3,
                            "rot": (0, 12 * k.wave(t, 0.75) * tilt(t), 0)},
        "tongue": lambda t: {"rot": (10 * tilt(t), 0, 0)},
        "fin_R": lambda t: {"rot": (0, 14 * tilt(t), 0)},
        "fin_L": lambda t: {"rot": (0, -14 * tilt(t), 0)},
        "cup": lambda t: {"rot": (0, -8 * k.bump(t, 0.7, 0.3), 0)},
        "steam": steam(1.5),
    }
    forget.update(tail_wag(6, 3.0))
    rig.action("Forget", 3.0, forget)
