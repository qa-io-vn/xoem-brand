import math
from mathutils import Vector, Matrix
import xoem3d_core as k

NAME = "Em_Nga"

BODY_C = Vector((0.12, 0.0, 0.236))
BODY_R = (0.50, 0.30, 0.236)
HEAD_C = Vector((-0.49, -0.07, 0.262))
HEAD_R = (0.248, 0.26, 0.234)
HEAD_M = k.rot(0, 0, 30) @ k.rot(0, -5, 0) @ k.rot(9, 0, 0)
HEAD_UP = HEAD_M @ Vector((0, 0, 1))
SNOUT_C = HEAD_C + HEAD_M @ Vector((-0.222, 0.0, -0.058))
SNOUT_R = (0.148, 0.178, 0.124)
BELLY_RING = 10


def body_deform(p):
    s = 1.0 + 0.09 * p.x
    z = p.z * (0.9 if p.z < 0 else 1.0)
    return Vector((p.x, p.y * s, z * s))


def head_point(local_dir, offset=0.0):
    return k.ellipsoid_surface(HEAD_C, HEAD_R, HEAD_M, local_dir) if offset == 0 else _offset(
        k.ellipsoid_surface(HEAD_C, HEAD_R, HEAD_M, local_dir), offset)


def _offset(pn, d):
    return pn[0] + pn[1] * d, pn[1]


def project_head(q, offset):
    d = HEAD_M.inverted() @ (Vector(q) - HEAD_C)
    p, n = k.ellipsoid_surface(HEAD_C, HEAD_R, HEAD_M, d)
    return p + n * offset, n


def body(put):
    surf = k.deformed_surface(BODY_C, BODY_R, body_deform)
    put("body", k.ellipsoid("EmNga_Than", BODY_C, BODY_R, ["Long_VangBo", "Long_CatMin"], seg=40, rings=16,
                            deform=body_deform, subsurf=1,
                            face_mat=lambda u: 1 if u.z < math.cos(math.pi * BELLY_RING / 16) else 0))
    th = math.pi * BELLY_RING / 16
    dashes = []
    count = 46
    for i in range(count):
        a0 = 2 * math.pi * i / count
        a1 = a0 + 2 * math.pi / count * 0.55
        dashes.append([surf(th, a0 + (a1 - a0) * s / 3, 0.0085)[0] for s in range(4)])
    put("body", k.multi_tube("EmNga_DuongKhau", dashes, 0.0058, "Net_Ve", ring=8))
    spines = []
    for i, (x, size) in enumerate(((-0.42, 0.85), (-0.16, 1.05), (0.1, 1.1), (0.36, 0.95), (0.6, 0.75))):
        p, n = surf.toward((x, 0.0, math.sqrt(max(1 - x * x, 0.05))))
        tilt = (n + Vector((0.5, 0, 0))).normalized()
        F = k.frame_z(tilt, Vector((1, 0, 0)))
        spines.append(k.ellipsoid("EmNga_GaiMem_%d" % i, p + tilt * (0.03 * size - 0.028), (0.034 * size, 0.056 * size,
                                                                                            0.07 * size),
                                  "Long_VangBoDam", R=F, seg=24, rings=12,
                                  deform=lambda q: Vector((q.x * (1 - 0.55 * max(q.z, 0)), q.y * (1 - 0.35 * max(q.z, 0)),
                                                           q.z)),
                                  subsurf=1, outline=k.OUTLINE_SMALL))
    put("body", *spines)
    tag(put, surf)
    return surf


def tag(put, surf):
    p, n = surf.toward((0.46, -0.78, 0.42))
    F = k.frame_z(n, Vector((0, 0, 1))) @ k.rot(0, 0, 16)
    w, h, r = 0.07, 0.048, 0.012
    outline = []
    for quarter, (cx, cy) in enumerate(((w - r, h - r), (-w + r, h - r), (-w + r, -h + r), (w - r, -h + r))):
        for s in range(5):
            a = math.pi / 2 * (quarter + s / 4)
            outline.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    M = k.to4(F, p + n * 0.004)
    put("body", k.prism("EmNga_NhanGoi", outline, 0.006, "Long_CatMin", matrix=M, subsurf=1, outline=k.OUTLINE_SMALL))
    stitch = []
    inset = 0.007
    for quarter, (cx, cy) in enumerate(((w - r, h - r), (-w + r, h - r), (-w + r, -h + r), (w - r, -h + r))):
        for s in range(5):
            a = math.pi / 2 * (quarter + s / 4)
            stitch.append(M @ Vector((cx + (r - inset) * math.cos(a), cy + (r - inset) * math.sin(a), 0.0042)))
    put("body", k.tube("EmNga_NhanGoi_Chi", None, 0.0016, "Chu_DatNung", ring=6, closed=True, caps=False,
                       outline=k.OUTLINE_NONE, dense=stitch))
    bean_c = M @ Vector((0, 0, 0.0035))
    BF = F @ k.rot(0, 0, 35)
    put("body", k.ellipsoid("EmNga_NhanGoi_HatCaPhe", bean_c, (0.015, 0.022, 0.005), "Vai_DatNungDam", R=BF, seg=16,
                            rings=8, subsurf=1, outline=k.OUTLINE_NONE))
    groove = [bean_c + BF @ Vector((0.003 * math.sin(math.pi * s / 4 * 2), -0.014 + 0.007 * s, 0.0038)) for s in
              range(5)]
    put("body", k.tube("EmNga_NhanGoi_RanhHat", None, 0.0012, "Net_Ve", ring=6, caps=True, outline=k.OUTLINE_NONE,
                       dense=groove))


def head(put, bones):
    put("head", k.ellipsoid("EmNga_Dau", HEAD_C, HEAD_R, "Long_VangBo", R=HEAD_M, seg=36, rings=18, subsurf=1))
    put("head", k.ellipsoid("EmNga_Mom", SNOUT_C, SNOUT_R, "Long_VangBo", R=HEAD_M, seg=32, rings=16, subsurf=1))
    nostrils = []
    bubble_anchor = None
    for side in (-1, 1):
        p, n = k.ellipsoid_surface(SNOUT_C, SNOUT_R, HEAD_M, (-1.0, 0.38 * side, 0.26))
        nostrils.append((p - n * 0.002, (0.017, 0.023, 0.008), k.frame_z(n, HEAD_UP)))
        if side < 0:
            bubble_anchor = (p, n)
    put("head", k.multi_ellipsoid("EmNga_LoMui", nostrils, "Net_Ve", subsurf=1))
    bp, bn = bubble_anchor
    bones.append(("bubble", bp, "head"))
    put("bubble", k.ellipsoid("EmNga_BongMui", bp + bn * 0.046, (0.05, 0.05, 0.05), "Bong_Bong", seg=32, rings=16,
                              subsurf=1, outline=k.OUTLINE_NONE))
    put("bubble", k.ellipsoid("EmNga_BongMui_AnhSang", bp + bn * 0.046 + Vector((-0.018, -0.03, 0.03)),
                              (0.011, 0.007, 0.011), "Mat_Sang", R=k.frame_z(Vector((-0.4, -0.8, 0.4))), seg=12,
                              rings=6, subsurf=0, outline=k.OUTLINE_NONE))
    mouth = []
    for s in range(11):
        u = -1 + 2 * s / 10
        p, n = k.ellipsoid_surface(SNOUT_C, SNOUT_R, HEAD_M, (-0.6, 0.5 * u, -0.8 + 0.22 * u * u))
        mouth.append(p + n * 0.003)
    put("head", k.tube("EmNga_Mieng", None, lambda t: 0.0065 * (0.6 + 0.4 * math.sin(math.pi * t)), "Net_Ve", ring=8,
                       outline=k.OUTLINE_NONE, dense=mouth))
    lids = []
    lashes = []
    for side in (-1, 1):
        p, n = head_point((-0.6, 0.6 * side, 0.32))
        F = k.frame_z(n, HEAD_UP)
        arc = []
        for s in range(11):
            u = -1 + 2 * s / 10
            q = p + F.col[0] * 0.056 * u + F.col[1] * (-0.019 * (1 - u * u))
            arc.append(project_head(q, 0.004)[0])
        lids.append(arc)
        ends = [arc[0], arc[-1]]
        back = max(ends, key=lambda e: (HEAD_M.inverted() @ (e - HEAD_C)).x)
        tangent = (back - (arc[1] if back is arc[0] else arc[-2])).normalized()
        for j, lift in enumerate((0.55, -0.1)):
            d = (tangent + F.col[1] * lift).normalized()
            q1 = back + d * 0.024
            lashes.append([back, back.lerp(q1, 0.5) + n * 0.003, q1 + n * 0.004])
        cheek, cn = head_point((-0.4, 0.8 * side, -0.14))
        put("head", k.ellipsoid("EmNga_MaHong_%s" % ("L" if side < 0 else "R"), cheek - cn * 0.001,
                                (0.05, 0.032, 0.008), "Ma_Hong", R=k.frame_z(cn, HEAD_UP), seg=24, rings=12,
                                subsurf=1, outline=k.OUTLINE_NONE))
    put("head", k.multi_tube("EmNga_MatNham", lids, 0.0078, "Net_Ve", ring=10))
    put("head", k.multi_tube("EmNga_LongMi", lashes, 0.0042, "Net_Ve", ring=6))
    for side in (-1, 1):
        tag = "L" if side < 0 else "R"
        p, n = head_point((0.04, 0.5 * side, 0.86))
        p0 = p - n * 0.035
        p1 = p + n * 0.05
        p2 = p1 + HEAD_M @ Vector((0.05, 0.022 * side, 0.05))
        p3 = p2 + HEAD_M @ Vector((0.068, 0.016 * side, 0.004))
        bones.append(("horn_" + tag, p, "head"))
        put("horn_" + tag, k.tube("EmNga_Sung_" + tag, [p0, p1, p2, p3],
                                  lambda t: 0.054 * (1 - t) + 0.015 * t, "Long_CatMin", ring=18, per_seg=8,
                                  outline=k.OUTLINE_MAIN))
    top, tn = head_point((0.1, 0.0, 1.0))
    curls = []
    for j, (dx, dy, h) in enumerate(((-0.03, -0.012, 0.05), (0.0, 0.0, 0.062), (0.028, 0.012, 0.046))):
        b = project_head(top + HEAD_M @ Vector((dx, dy, 0)), -0.01)[0]
        c1 = b + tn * h * 0.6 + HEAD_M @ Vector((-0.012, 0, 0))
        c2 = b + tn * h + HEAD_M @ Vector((0.016, 0, 0))
        c3 = c2 + HEAD_M @ Vector((0.018, 0, -0.012))
        curls.append(k.tube("EmNga_ChomLong_%d" % j, [b, c1, c2, c3], lambda t: 0.013 * (1 - 0.75 * t),
                            "Long_VangBoDam", ring=10, per_seg=6, outline=k.OUTLINE_SMALL))
    put("head", *curls)


def paws(put, bones):
    front = [("FL", Vector((-0.69, -0.29, 0.045)), 20), ("FR", Vector((-0.6, 0.1, 0.045)), 26)]
    for tag, c, yaw in front:
        R = k.rot(0, 0, yaw)
        radii = (0.105, 0.07, 0.05)
        bones.append(("paw_" + tag, c, "root"))
        put("paw_" + tag, k.ellipsoid("EmNga_Chan_" + tag, c, radii, "Long_VangBo", R=R, seg=24, rings=12,
                                      deform=lambda q: Vector((q.x, q.y, q.z * (0.7 if q.z < 0 else 1.0))), subsurf=1))
        creases = []
        for s in (-0.3, 0.3):
            path = []
            for j in range(6):
                u = j / 5
                d = Vector((-1.0 + 0.5 * u, s, 0.2 + 0.7 * u))
                p, n = k.ellipsoid_surface(c, radii, R, d)
                path.append(p + n * 0.003)
            creases.append(path)
        put("paw_" + tag, k.multi_tube("EmNga_NgonChan_" + tag, creases, 0.0045, "Net_Ve", ring=6))
    back = [("BL", Vector((0.5, -0.235, 0.05)), -24), ("BR", Vector((0.5, 0.235, 0.05)), 24)]
    for tag, c, yaw in back:
        R = k.rot(0, 0, yaw)
        radii = (0.1, 0.072, 0.056)
        bones.append(("paw_" + tag, c, "root"))
        put("paw_" + tag, k.ellipsoid("EmNga_Chan_" + tag, c, radii, "Long_VangBo", R=R, seg=24, rings=12,
                                      deform=lambda q: Vector((q.x, q.y, q.z * (0.75 if q.z < 0 else 1.0))), subsurf=1))
        pads = []
        p, n = k.ellipsoid_surface(c, radii, R, (1.0, 0.0, -0.12))
        pads.append((p, (0.03, 0.034, 0.008), k.frame_z(n)))
        for s in (-0.42, 0.0, 0.42):
            p, n = k.ellipsoid_surface(c, radii, R, (0.8, s, 0.5))
            pads.append((p, (0.0135, 0.0135, 0.006), k.frame_z(n)))
        put("paw_" + tag, k.multi_ellipsoid("EmNga_DemChan_" + tag, pads, "Ma_Hong", subsurf=1))


TAIL_PTS = [(0.56, 0.06, 0.16), (0.73, 0.05, 0.12), (0.86, -0.06, 0.085), (0.86, -0.24, 0.065), (0.74, -0.37, 0.058),
            (0.57, -0.41, 0.062)]
TAIL_JOINTS = [0.0, 0.33, 0.66, 1.0]


def tail(rig):
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

    obj = k.tube("EmNga_Duoi", None, lambda t: 0.09 - 0.042 * t, ["Long_VangBo", "Long_CatMin"], ring=20,
                 dense=dense, outline=k.OUTLINE_MAIN, t_mat=lambda t: 1 if t > 0.86 else 0)
    heads = [at(max(c - 0.1, 0.0)) for c in TAIL_JOINTS]
    names = ["tail_%d" % i for i in range(len(TAIL_JOINTS))]
    for i, name in enumerate(names):
        tail_end = heads[i + 1] if i + 1 < len(heads) else at(1.0) + (at(1.0) - at(0.95)).normalized() * 0.05
        rig.bone(name, heads[i], names[i - 1] if i > 0 else "root", tail=tail_end)
    return obj, list(zip(names, TAIL_JOINTS))


def zzz(put, bones):
    letters = [(Vector((-0.42, -0.12, 0.64)), 0.12, -8), (Vector((-0.28, -0.14, 0.8)), 0.155, 6),
               (Vector((-0.1, -0.16, 0.99)), 0.2, -4)]
    for i, (p, size, tilt) in enumerate(letters):
        name = "z_%d" % (i + 1)
        bones.append((name, p, "root"))
        M = k.to4(k.rot(0, tilt, 0) @ k.rot(90, 0, 0), p)
        put(name, k.text_mesh("EmNga_Z%d" % (i + 1), "z", size, 0.012, "Chu_Nau", M, bevel=0.003,
                              outline=k.OUTLINE_NONE))


def build():
    groups = {}

    def put(bone, *objs):
        groups.setdefault(bone, []).extend(objs)

    extra = []
    body(put)
    head(put, extra)
    paws(put, extra)
    zzz(put, extra)
    rig = k.Rig(NAME)
    rig.bone("root", (0, 0, 0), length=0.12)
    rig.bone("body", (0.12, 0, 0.02), "root")
    rig.bone("head", (-0.3, -0.03, 0.12), "root")
    for name, head_pos, parent in extra:
        rig.bone(name, head_pos, parent, length=0.04)
    tail_obj, joints = tail(rig)
    rig.build()
    for bone, objs in groups.items():
        rig.attach(objs, bone)
    rig.skin(tail_obj, joints)
    animate(rig)
    return rig


def animate(rig):
    def breath(t):
        return 0.5 - 0.5 * math.cos(2 * math.pi * t / 2.0)

    def z_track(offset, period=4.0, drift=(0.08, 0.0, 0.2)):
        def f(t):
            ph = (t / period + offset) % 1.0
            s = math.sin(math.pi * ph) ** 0.7
            return {"loc": (drift[0] * ph + 0.01 * k.wave(t, 2.0, offset * 5), 0, drift[2] * ph - 0.06),
                    "rot": (0, 10 * k.wave(t, 2.0, offset * 4), 0), "scale": (s, s, s)}
        return f

    def twitch(t, at):
        return 18 * (k.bump(t, at, 0.07) + 0.6 * k.bump(t, at + 0.16, 0.06))

    rig.action("Sleep", 4.0, {
        "body": lambda t: {"scale": (1, 1 + 0.02 * breath(t), 1 + 0.04 * breath(t))},
        "head": lambda t: {"loc": (0, 0, 0.007 * breath(t)), "rot": (1.2 * breath(t), 0, 0)},
        "bubble": lambda t: {"scale": [0.45 + 0.75 * breath(t)] * 3},
        "horn_L": lambda t: {"rot": (twitch(t, 1.5), 0, 0)},
        "tail_1": lambda t: {"rot": (0, 0, 5 * k.wave(t, 4.0))},
        "tail_2": lambda t: {"rot": (0, 0, 8 * k.wave(t, 4.0, -0.6))},
        "tail_3": lambda t: {"rot": (0, 0, 12 * k.wave(t, 4.0, -1.2))},
        "z_1": z_track(0.0),
        "z_2": z_track(1 / 3),
        "z_3": z_track(2 / 3),
    })

    def lift(t):
        return k.window(t, 0.25, 0.9, 1.9, 2.7)

    def stretch(t):
        return k.bump(t, 1.25, 0.5)

    rig.action("Stir", 3.0, {
        "body": lambda t: {"scale": (1 + 0.06 * stretch(t), 1, 1 - 0.02 * stretch(t))},
        "head": lambda t: {"loc": (-0.02 * lift(t), 0, 0.05 * lift(t)), "rot": (6 * lift(t), 0, 10 * lift(t))},
        "bubble": lambda t: {"scale": [max(0.0, 0.45 + 0.6 * k.bump(t, 0.3, 0.3) - 1.05 * k.window(t, 0.45, 0.5, 2.5,
                                                                                                    2.95))] * 3},
        "horn_L": lambda t: {"rot": (twitch(t, 0.9), 0, 0)},
        "horn_R": lambda t: {"rot": (-twitch(t, 1.0), 0, 0)},
        "tail_1": lambda t: {"rot": (0, 0, 14 * stretch(t))},
        "tail_2": lambda t: {"rot": (0, 0, 22 * stretch(t) - 6 * k.bump(t, 2.2, 0.3))},
        "tail_3": lambda t: {"rot": (0, 0, 28 * stretch(t) - 10 * k.bump(t, 2.3, 0.3))},
        "paw_FL": lambda t: {"loc": (-0.035 * stretch(t), 0, 0.01 * stretch(t))},
        "paw_FR": lambda t: {"loc": (-0.03 * stretch(t), 0, 0.008 * stretch(t))},
        "z_1": lambda t: {"scale": (0, 0, 0)},
        "z_2": lambda t: {"scale": (0, 0, 0)},
        "z_3": lambda t: {"scale": (0, 0, 0)},
    })
