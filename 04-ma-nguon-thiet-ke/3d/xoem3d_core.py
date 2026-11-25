import bpy
import bmesh
import math
import os
import numpy as np
from mathutils import Vector, Matrix, Euler, Quaternion

FPS = 30

PALETTE = {
    "dat_nung": "#C8553D",
    "dat_nung_dam": "#9E3F2C",
    "kem_sua": "#F6EEDF",
    "nau_ca_phe": "#2B1D16",
    "vang_bo": "#F2C14E",
    "vang_bo_dam": "#E0A23A",
    "reu_soi": "#5E7A4A",
    "reu_nhat": "#8AA568",
    "reu_dam": "#46603A",
    "cat_min": "#E8D5B5",
    "hong_ma": "#EC9F8C",
    "go_oc_cho": "#5B3A29",
    "dong_thau": "#D6A443",
    "ca_phe_dac": "#3A2218",
    "rang": "#FBF6EC",
    "hoi_nuoc": "#FFFDF8",
    "bong_bong": "#DDF1FF",
}

OUTLINE_MAIN = 0.0085
OUTLINE_SMALL = 0.0045
OUTLINE_NONE = 0.0

STATE = {"coll": None, "tex_dir": None, "font": None}


def lin(hexstr):
    h = hexstr.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c) + (1.0,)


def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.render.fps = FPS
    scene.unit_settings.system = "METRIC"
    return scene


def begin(name, tex_dir, font_path=None):
    coll = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(coll)
    STATE["coll"] = coll
    STATE["tex_dir"] = tex_dir
    STATE["font"] = font_path
    os.makedirs(tex_dir, exist_ok=True)
    return coll


def link(obj):
    STATE["coll"].objects.link(obj)
    return obj


def _height_to_normal(h, strength):
    dx = (np.roll(h, -1, axis=1) - np.roll(h, 1, axis=1)) * 0.5
    dy = (np.roll(h, -1, axis=0) - np.roll(h, 1, axis=0)) * 0.5
    nx = -dx * strength
    ny = -dy * strength
    nz = np.ones_like(h)
    length = np.sqrt(nx * nx + ny * ny + nz * nz)
    return np.stack([nx / length * 0.5 + 0.5, ny / length * 0.5 + 0.5, nz / length * 0.5 + 0.5], -1)


def _normalize(a):
    a = a - a.min()
    return a / max(a.max(), 1e-9)


def _band_noise(n, rng, lo, hi):
    w = rng.standard_normal((n, n))
    spectrum = np.fft.fft2(w)
    fy = np.fft.fftfreq(n)[:, None]
    fx = np.fft.fftfreq(n)[None, :]
    r = np.sqrt(fx * fx + fy * fy)
    mask = np.exp(-(r / hi) ** 2) * (1.0 - np.exp(-(r / max(lo, 1e-6)) ** 2))
    return _normalize(np.real(np.fft.ifft2(spectrum * mask)))


def height_weave(n=512, threads=48, seed=3):
    rng = np.random.default_rng(seed)
    y, x = np.mgrid[0:n, 0:n] / n * threads
    i = np.floor(x)
    j = np.floor(y)
    u = x - i
    v = y - j
    warp = np.sin(np.pi * u) ** 0.55 * (0.62 + 0.38 * np.sin(np.pi * v))
    weft = np.sin(np.pi * v) ** 0.55 * (0.62 + 0.38 * np.sin(np.pi * u))
    over = ((i + j) % 2) == 0
    h = np.where(over, warp, weft)
    shade_i = rng.uniform(0.85, 1.0, threads)
    shade_j = rng.uniform(0.85, 1.0, threads)
    h = h * np.where(over, shade_i[i.astype(int) % threads], shade_j[j.astype(int) % threads])
    fibre = _band_noise(n, rng, 0.15, 0.45)
    return _normalize(h * 0.85 + fibre * 0.15)


def height_plush(n=512, seed=5):
    rng = np.random.default_rng(seed)
    fine = _band_noise(n, rng, 0.12, 0.35)
    clump = _band_noise(n, rng, 0.01, 0.05)
    return _normalize(fine * 0.55 + clump * 0.45)


def height_scales(n=512, cells=10, seed=7):
    rng = np.random.default_rng(seed)
    jx = rng.uniform(0.15, 0.85, (cells, cells))
    jy = rng.uniform(0.15, 0.85, (cells, cells))
    y, x = np.mgrid[0:n, 0:n] / n * cells
    ci = np.floor(x).astype(int)
    cj = np.floor(y).astype(int)
    f1 = np.full(x.shape, 9.0)
    f2 = np.full(x.shape, 9.0)
    for dj in (-1, 0, 1):
        for di in (-1, 0, 1):
            ni = (ci + di) % cells
            nj = (cj + dj) % cells
            px = ci + di + jx[nj, ni]
            py = cj + dj + jy[nj, ni]
            d = np.sqrt((x - px) ** 2 + (y - py) ** 2)
            f2 = np.where(d < f1, f1, np.minimum(f2, d))
            f1 = np.minimum(f1, d)
    edge = np.clip((f2 - f1) / 0.32, 0.0, 1.0)
    dome = edge * (2 - edge)
    pores = _band_noise(n, rng, 0.2, 0.5)
    return _normalize(dome * 0.9 + pores * 0.1)


TEXTURES = {
    "weave": (height_weave, 7.0),
    "plush": (height_plush, 5.0),
    "scales": (height_scales, 6.0),
}


def texture(name):
    key = "tex_" + name
    if key in bpy.data.images:
        return bpy.data.images[key]
    fn, strength = TEXTURES[name]
    h = fn()
    normal = _height_to_normal(h, strength * h.shape[0] / 512.0)
    n = h.shape[0]
    img = bpy.data.images.new(key, n, n, alpha=False)
    img.colorspace_settings.name = "Non-Color"
    rgba = np.ones((n, n, 4), np.float32)
    rgba[..., :3] = normal
    img.pixels.foreach_set(rgba.ravel())
    path = os.path.join(STATE["tex_dir"], "xoem-" + name + "-normal.png")
    img.filepath_raw = path
    img.file_format = "PNG"
    img.save()
    img.pack()
    return img


MATS = {}


def define(name, color, rough=0.6, sheen=0.0, sheen_tint="#FFFFFF", normal=None, tile=0.1, strength=0.5,
           metal=0.0, coat=0.0, coat_rough=0.1, alpha=1.0, emit=0.0, spec=0.5):
    MATS[name] = dict(color=color, rough=rough, sheen=sheen, sheen_tint=sheen_tint, normal=normal, tile=tile,
                      strength=strength, metal=metal, coat=coat, coat_rough=coat_rough, alpha=alpha, emit=emit,
                      spec=spec)


def material(name):
    if name in bpy.data.materials:
        return bpy.data.materials[name]
    s = MATS[name]
    m = bpy.data.materials.new(name)
    try:
        m.use_nodes = True
    except Exception:
        pass
    nt = m.node_tree
    p = nt.nodes.get("Principled BSDF")
    col = PALETTE.get(s["color"], s["color"])
    p.inputs["Base Color"].default_value = lin(col)
    p.inputs["Roughness"].default_value = s["rough"]
    p.inputs["Metallic"].default_value = s["metal"]
    p.inputs["Specular IOR Level"].default_value = s["spec"]
    if s["sheen"] > 0:
        p.inputs["Sheen Weight"].default_value = s["sheen"]
        p.inputs["Sheen Roughness"].default_value = 0.45
        p.inputs["Sheen Tint"].default_value = lin(PALETTE.get(s["sheen_tint"], s["sheen_tint"]))
    if s["coat"] > 0:
        p.inputs["Coat Weight"].default_value = s["coat"]
        p.inputs["Coat Roughness"].default_value = s["coat_rough"]
    if s["emit"] > 0:
        p.inputs["Emission Color"].default_value = lin(col)
        p.inputs["Emission Strength"].default_value = s["emit"]
    if s["alpha"] < 1.0:
        p.inputs["Alpha"].default_value = s["alpha"]
        if hasattr(m, "surface_render_method"):
            m.surface_render_method = "BLENDED"
        if hasattr(m, "blend_method"):
            try:
                m.blend_method = "BLEND"
            except Exception:
                pass
    if s["normal"]:
        tn = nt.nodes.new("ShaderNodeTexImage")
        tn.image = texture(s["normal"])
        tn.location = (-600, -300)
        nm = nt.nodes.new("ShaderNodeNormalMap")
        nm.inputs["Strength"].default_value = s["strength"]
        nm.location = (-300, -300)
        nt.links.new(tn.outputs["Color"], nm.inputs["Color"])
        nt.links.new(nm.outputs["Normal"], p.inputs["Normal"])
    m.diffuse_color = lin(col)
    m["tile"] = s["tile"]
    m["textured"] = 1 if s["normal"] else 0
    return m


def define_standard_materials():
    define("Vai_DatNung", "dat_nung", rough=0.8, sheen=0.28, sheen_tint="#F2A58C", normal="weave", tile=0.11, strength=0.55)
    define("Vai_DatNungDam", "dat_nung_dam", rough=0.7, sheen=0.25, sheen_tint="#E08A70")
    define("Vai_Kem", "kem_sua", rough=0.85, sheen=0.3, sheen_tint="#FFFFFF", normal="weave", tile=0.09, strength=0.5)
    define("Go_OcCho", "go_oc_cho", rough=0.42, coat=0.4, coat_rough=0.25)
    define("Dong_Thau", "dong_thau", rough=0.28, metal=1.0)
    define("Su_KemSua", "kem_sua", rough=0.18, coat=0.8, coat_rough=0.05)
    define("Su_DatNung", "dat_nung", rough=0.2, coat=0.8, coat_rough=0.05)
    define("Mat_Trang", "kem_sua", rough=0.18, coat=1.0, coat_rough=0.03)
    define("Mat_Den", "nau_ca_phe", rough=0.15, coat=1.0, coat_rough=0.02)
    define("Mat_Mong", "#6A4330", rough=0.2, coat=1.0, coat_rough=0.02)
    define("Mat_Sang", "rang", rough=0.1, emit=0.6)
    define("Net_Ve", "nau_ca_phe", rough=0.6)
    define("Hoi_Nuoc", "hoi_nuoc", rough=0.5, emit=0.15, alpha=0.9)
    define("Long_VangBo", "vang_bo", rough=0.88, sheen=0.42, sheen_tint="#FFD86E", normal="plush", tile=0.22, strength=0.45)
    define("Long_VangBoDam", "vang_bo_dam", rough=0.86, sheen=0.38, sheen_tint="#F7C060", normal="plush", tile=0.22, strength=0.4)
    define("Long_CatMin", "cat_min", rough=0.88, sheen=0.4, sheen_tint="#FFF4E0", normal="plush", tile=0.2, strength=0.4)
    define("Ma_Hong", "hong_ma", rough=0.85, sheen=0.5)
    define("Bong_Bong", "bong_bong", rough=0.05, coat=1.0, coat_rough=0.0, alpha=0.38, spec=0.8)
    define("Da_Reu", "reu_soi", rough=0.62, sheen=0.15, sheen_tint="#B8D898", normal="scales", tile=0.13, strength=0.3)
    define("Da_ReuNhat", "reu_nhat", rough=0.6, sheen=0.15, normal="scales", tile=0.08, strength=0.25)
    define("Da_ReuDam", "reu_dam", rough=0.6)
    define("Bung_CatMin", "cat_min", rough=0.8, sheen=0.5, normal="weave", tile=0.07, strength=0.35)
    define("Sung_CatMin", "cat_min", rough=0.5, coat=0.3, coat_rough=0.3)
    define("Luoi", "dat_nung", rough=0.3, coat=0.6, coat_rough=0.1)
    define("Rang", "rang", rough=0.25, coat=0.6)
    define("Ly_Giay", "kem_sua", rough=0.55)
    define("Ly_Bang", "dat_nung", rough=0.5)
    define("Ca_Phe", "ca_phe_dac", rough=0.08, coat=1.0, coat_rough=0.02)
    define("Bot_Sua", "cat_min", rough=0.4)
    define("Chu_DatNung", "dat_nung", rough=0.45, coat=0.4)
    define("Chu_Nau", "nau_ca_phe", rough=0.5)
    define("Vien_Den", "nau_ca_phe", rough=1.0)


def frame_z(n, up=Vector((0, 0, 1))):
    z = Vector(n).normalized()
    up = Vector(up)
    if abs(z.dot(up.normalized())) > 0.995:
        up = Vector((0, 1, 0)) if abs(z.y) < 0.9 else Vector((1, 0, 0))
    x = up.cross(z).normalized()
    y = z.cross(x).normalized()
    return Matrix((x, y, z)).transposed()


def rot(rx=0.0, ry=0.0, rz=0.0):
    return Euler((math.radians(rx), math.radians(ry), math.radians(rz)), "XYZ").to_matrix()


def to4(m3, t=(0, 0, 0)):
    m = m3.to_4x4()
    m.translation = Vector(t)
    return m


def box_uv(me, tile):
    if not me.uv_layers:
        me.uv_layers.new(name="UVMap")
    uvl = me.uv_layers[0]
    nv = len(me.vertices)
    npoly = len(me.polygons)
    nl = len(me.loops)
    if npoly == 0:
        return
    co = np.empty(nv * 3)
    me.vertices.foreach_get("co", co)
    co = co.reshape(-1, 3)
    lv = np.empty(nl, dtype=np.int64)
    me.loops.foreach_get("vertex_index", lv)
    pn = np.empty(npoly * 3)
    me.polygons.foreach_get("normal", pn)
    pn = pn.reshape(-1, 3)
    lt = np.empty(npoly, dtype=np.int64)
    me.polygons.foreach_get("loop_total", lt)
    poly_of_loop = np.repeat(np.arange(npoly), lt)
    n = pn[poly_of_loop]
    p = co[lv]
    ax = np.argmax(np.abs(n), axis=1)
    sx = np.sign(n[:, 0]) + (n[:, 0] == 0)
    sy = np.sign(n[:, 1]) + (n[:, 1] == 0)
    sz = np.sign(n[:, 2]) + (n[:, 2] == 0)
    u = np.where(ax == 0, -p[:, 1] * sx, np.where(ax == 1, p[:, 0] * sy, p[:, 0] * sz))
    v = np.where(ax == 2, p[:, 1] * sz, p[:, 2])
    uv = np.stack([u, v], 1) / tile
    uvl.data.foreach_set("uv", uv.ravel())


def mesh_object(name, bm, mats, matrix=None, subsurf=0, outline=OUTLINE_MAIN, smooth=True, face_mat=None):
    if face_mat is not None:
        for f in bm.faces:
            f.material_index = face_mat(f)
    bm.normal_update()
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    if matrix is not None:
        me.transform(matrix)
    if not isinstance(mats, (list, tuple)):
        mats = [mats]
    for m in mats:
        me.materials.append(material(m) if isinstance(m, str) else m)
    if smooth:
        me.shade_smooth()
    me.update()
    textured = [m for m in me.materials if m.get("textured")]
    if textured:
        box_uv(me, textured[0]["tile"])
    else:
        box_uv(me, 0.2)
    obj = bpy.data.objects.new(name, me)
    link(obj)
    if subsurf > 0:
        mod = obj.modifiers.new("Subdivision", "SUBSURF")
        mod.levels = subsurf
        mod.render_levels = subsurf + 1
        mod.quality = 3
    obj["outline"] = outline
    return obj


def ellipsoid(name, center, radii, mat, R=None, seg=32, rings=16, deform=None, subsurf=1, outline=OUTLINE_MAIN,
              face_mat=None):
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=rings, radius=1.0)
    if face_mat is not None:
        for f in bm.faces:
            f.material_index = face_mat(f.calc_center_median().normalized())
    for v in bm.verts:
        p = v.co.copy()
        if deform:
            p = Vector(deform(p))
        v.co = Vector((p.x * radii[0], p.y * radii[1], p.z * radii[2]))
    R = R if R is not None else Matrix.Identity(3)
    return mesh_object(name, bm, mat, to4(R, center), subsurf=subsurf, outline=outline)


def deformed_surface(center, radii, deform=None, R=None):
    R = R if R is not None else Matrix.Identity(3)
    c = Vector(center)

    def local(th, ph):
        d = Vector((math.sin(th) * math.cos(ph), math.sin(th) * math.sin(ph), math.cos(th)))
        if deform:
            d = Vector(deform(d))
        return Vector((d.x * radii[0], d.y * radii[1], d.z * radii[2]))

    def at(th, ph, offset=0.0):
        e = 1e-3
        p = local(th, ph)
        t1 = local(th + e, ph) - local(th - e, ph)
        t2 = local(th, ph + e) - local(th, ph - e)
        n = t1.cross(t2)
        if n.length < 1e-12:
            n = p.copy()
        n.normalize()
        if n.dot(p) < 0:
            n = -n
        return c + R @ (p + n * offset), (R @ n).normalized()

    def toward(d, offset=0.0):
        d = Vector(d).normalized()
        th = math.acos(max(-1.0, min(1.0, d.z)))
        ph = math.atan2(d.y, d.x)
        return at(th, ph, offset)

    at.toward = toward
    return at


def ellipsoid_surface(center, radii, R, d):
    R = R if R is not None else Matrix.Identity(3)
    d = Vector(d).normalized()
    k = 1.0 / math.sqrt((d.x / radii[0]) ** 2 + (d.y / radii[1]) ** 2 + (d.z / radii[2]) ** 2)
    pl = d * k
    nl = Vector((pl.x / radii[0] ** 2, pl.y / radii[1] ** 2, pl.z / radii[2] ** 2)).normalized()
    return Vector(center) + R @ pl, (R @ nl).normalized()


def ellipsoid_front(center, radii, x, z, side=-1):
    cx, cy, cz = center
    t = 1.0 - ((x - cx) / radii[0]) ** 2 - ((z - cz) / radii[2]) ** 2
    t = max(t, 0.0)
    y = cy + side * radii[1] * math.sqrt(t)
    p = Vector((x, y, z))
    n = Vector(((x - cx) / radii[0] ** 2, (y - cy) / radii[1] ** 2, (z - cz) / radii[2] ** 2)).normalized()
    return p, n


def ellipsoid_implicit(center, radii, R=None):
    R = R if R is not None else Matrix.Identity(3)
    Ri = R.inverted()
    c = Vector(center)

    def f(p):
        q = Ri @ (Vector(p) - c)
        return (q.x / radii[0]) ** 2 + (q.y / radii[1]) ** 2 + (q.z / radii[2]) ** 2
    return f


def catmull(p0, p1, p2, p3, t):
    t2 = t * t
    t3 = t2 * t
    return 0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3)


def spline(points, per_seg=10, closed=False):
    P = [Vector(p) for p in points]
    m = len(P)
    if m == 2 and not closed:
        return [P[0].lerp(P[1], k / per_seg) for k in range(per_seg + 1)]
    out = []
    segs = m if closed else m - 1
    for i in range(segs):
        if closed:
            p0, p1, p2, p3 = P[(i - 1) % m], P[i], P[(i + 1) % m], P[(i + 2) % m]
        else:
            p0 = P[i - 1] if i > 0 else P[0] * 2 - P[1]
            p1 = P[i]
            p2 = P[i + 1]
            p3 = P[i + 2] if i + 2 < m else P[m - 1] * 2 - P[m - 2]
        for k in range(per_seg):
            out.append(catmull(p0, p1, p2, p3, k / per_seg))
    if not closed:
        out.append(P[-1].copy())
    return out


def _frames(pts, closed):
    n = len(pts)
    T = []
    for i in range(n):
        if closed:
            a, b = pts[(i - 1) % n], pts[(i + 1) % n]
        else:
            a, b = pts[max(i - 1, 0)], pts[min(i + 1, n - 1)]
        d = b - a
        T.append(d.normalized() if d.length > 1e-9 else Vector((0, 0, 1)))
    ref = Vector((0, 0, 1)) if abs(T[0].z) < 0.9 else Vector((1, 0, 0))
    N = [(ref - T[0] * ref.dot(T[0])).normalized()]
    for i in range(1, n):
        q = T[i - 1].rotation_difference(T[i])
        v = q @ N[-1]
        v = (v - T[i] * v.dot(T[i])).normalized()
        N.append(v)
    if closed:
        q = T[-1].rotation_difference(T[0])
        a = q @ N[-1]
        a = (a - T[0] * a.dot(T[0])).normalized()
        ang = math.atan2(T[0].dot(a.cross(N[0])), a.dot(N[0]))
        for i in range(n):
            N[i] = Quaternion(T[i], ang * i / n) @ N[i]
    B = [T[i].cross(N[i]).normalized() for i in range(n)]
    return T, N, B


def tube_bmesh(points, radius, ring=16, per_seg=10, closed=False, caps=True, cap_rings=4, dense=None, bm=None,
               t_mat=None):
    pts = dense if dense is not None else spline(points, per_seg, closed)
    n = len(pts)
    lengths = [0.0]
    for i in range(1, n):
        lengths.append(lengths[-1] + (pts[i] - pts[i - 1]).length)
    total = lengths[-1] if lengths[-1] > 0 else 1.0
    ts = [l / total for l in lengths]
    rfn = radius if callable(radius) else (lambda t, r=radius: r)
    T, N, B = _frames(pts, closed)
    rings = []
    if caps and not closed:
        r0 = rfn(0.0)
        for j in range(cap_rings, 0, -1):
            ph = j / cap_rings * math.pi / 2
            rings.append((pts[0] - T[0] * r0 * math.sin(ph), N[0], B[0], r0 * math.cos(ph), 0.0))
    for i in range(n):
        rings.append((pts[i], N[i], B[i], rfn(ts[i]), ts[i]))
    if caps and not closed:
        r1 = rfn(1.0)
        for j in range(1, cap_rings + 1):
            ph = j / cap_rings * math.pi / 2
            rings.append((pts[-1] + T[-1] * r1 * math.sin(ph), N[-1], B[-1], r1 * math.cos(ph), 1.0))
    bm = bm if bm is not None else bmesh.new()
    vparam = []
    grid = []
    for c, nn, bb, r, t in rings:
        row = []
        if r < 1e-6:
            row = None
            v = bm.verts.new(c)
            vparam.append(t)
            grid.append(v)
            continue
        for k in range(ring):
            th = 2 * math.pi * k / ring
            row.append(bm.verts.new(c + (nn * math.cos(th) + bb * math.sin(th)) * r))
            vparam.append(t)
        grid.append(row)
    count = len(grid)
    pairs = [(i, i + 1) for i in range(count - 1)]
    if closed:
        pairs.append((count - 1, 0))
    ring_t = [r[4] for r in rings]
    new_faces = []
    for a, b in pairs:
        ga, gb = grid[a], grid[b]
        if isinstance(ga, list) and isinstance(gb, list):
            for k in range(ring):
                k2 = (k + 1) % ring
                new_faces.append((bm.faces.new((ga[k], ga[k2], gb[k2], gb[k])), a, b))
        elif isinstance(ga, list):
            for k in range(ring):
                new_faces.append((bm.faces.new((ga[k], ga[(k + 1) % ring], gb)), a, b))
        elif isinstance(gb, list):
            for k in range(ring):
                new_faces.append((bm.faces.new((ga, gb[(k + 1) % ring], gb[k])), a, b))
    if t_mat is not None:
        for f, a, b in new_faces:
            f.material_index = t_mat(0.5 * (ring_t[a] + ring_t[b]))
    bmesh.ops.recalc_face_normals(bm, faces=[f for f, _, _ in new_faces])
    return bm, vparam


def tube(name, points, radius, mat, ring=16, per_seg=10, closed=False, caps=True, outline=OUTLINE_SMALL, subsurf=0,
         dense=None, t_mat=None):
    bm, vparam = tube_bmesh(points, radius, ring, per_seg, closed, caps, dense=dense, t_mat=t_mat)
    obj = mesh_object(name, bm, mat, None, subsurf=subsurf, outline=outline)
    obj["vparam"] = vparam
    return obj


def multi_tube(name, paths, radius, mat, ring=8, caps=True, outline=OUTLINE_NONE, closed=False):
    bm = bmesh.new()
    for path in paths:
        tube_bmesh(None, radius, ring, closed=closed, caps=caps, dense=[Vector(p) for p in path], bm=bm)
    return mesh_object(name, bm, mat, None, subsurf=0, outline=outline)


def multi_ellipsoid(name, items, mat, seg=16, rings=8, subsurf=0, outline=OUTLINE_NONE):
    bm = bmesh.new()
    for center, radii, R in items:
        R = R if R is not None else Matrix.Identity(3)
        M = to4(R, center) @ Matrix.Diagonal((radii[0], radii[1], radii[2], 1.0))
        bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=rings, radius=1.0, matrix=M)
    return mesh_object(name, bm, mat, None, subsurf=subsurf, outline=outline)


def circle_points(center, normal, radius, count=48, up=Vector((0, 0, 1))):
    F = frame_z(normal, up)
    x = F.col[0]
    y = F.col[1]
    return [Vector(center) + (x * math.cos(2 * math.pi * k / count) + y * math.sin(2 * math.pi * k / count)) * radius
            for k in range(count)]


def lathe(name, profile, mat, seg=64, matrix=None, subsurf=0, outline=OUTLINE_MAIN):
    bm = bmesh.new()
    rows = []
    for r, z in profile:
        if r < 1e-6:
            rows.append(bm.verts.new((0, 0, z)))
            continue
        row = []
        for k in range(seg):
            a = 2 * math.pi * k / seg
            row.append(bm.verts.new((r * math.cos(a), r * math.sin(a), z)))
        rows.append(row)
    for i in range(len(rows) - 1):
        ga, gb = rows[i], rows[i + 1]
        if isinstance(ga, list) and isinstance(gb, list):
            for k in range(seg):
                k2 = (k + 1) % seg
                bm.faces.new((ga[k], ga[k2], gb[k2], gb[k]))
        elif isinstance(ga, list):
            for k in range(seg):
                bm.faces.new((ga[k], ga[(k + 1) % seg], gb))
        elif isinstance(gb, list):
            for k in range(seg):
                bm.faces.new((ga, gb[(k + 1) % seg], gb[k]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    return mesh_object(name, bm, mat, matrix, subsurf=subsurf, outline=outline)


def prism(name, outline_pts, depth, mat, matrix=None, subsurf=2, outline=OUTLINE_MAIN):
    bm = bmesh.new()
    front = [bm.verts.new((p[0], p[1], depth / 2)) for p in outline_pts]
    back = [bm.verts.new((p[0], p[1], -depth / 2)) for p in outline_pts]
    bm.faces.new(front)
    bm.faces.new(list(reversed(back)))
    m = len(outline_pts)
    for k in range(m):
        k2 = (k + 1) % m
        bm.faces.new((front[k], back[k], back[k2], front[k2]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    return mesh_object(name, bm, mat, matrix, subsurf=subsurf, outline=outline)


def flat_shape(name, pts2d, thickness, mat, matrix, outline=OUTLINE_NONE):
    return prism(name, pts2d, thickness, mat, matrix, subsurf=0, outline=outline)


def text_mesh(name, s, size, depth, mat, matrix, bevel=0.004, outline=OUTLINE_SMALL):
    cu = bpy.data.curves.new(name + "_txt", "FONT")
    cu.body = s
    if STATE["font"] and os.path.exists(STATE["font"]):
        cu.font = bpy.data.fonts.load(STATE["font"], check_existing=True)
    cu.size = size
    cu.extrude = depth
    cu.bevel_depth = bevel
    cu.bevel_resolution = 3
    cu.align_x = "CENTER"
    cu.align_y = "CENTER"
    cu.resolution_u = 8
    tmp = bpy.data.objects.new(name + "_tmp", cu)
    link(tmp)
    dg = bpy.context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(tmp.evaluated_get(dg))
    bpy.data.objects.remove(tmp)
    bpy.data.curves.remove(cu)
    bm = bmesh.new()
    bm.from_mesh(me)
    bpy.data.meshes.remove(me)
    bmesh.ops.remove_doubles(bm, verts=bm.verts[:], dist=1e-5)
    return mesh_object(name, bm, mat, matrix, subsurf=0, outline=outline, smooth=False)


class RBox:
    def __init__(self, name, center, size, radius, mat, rot_deg=(0, 0, 0), cuts=10, bulge=None, taper=(1.0, 1.0),
                 subsurf=1, outline=OUTLINE_MAIN):
        self.h = Vector(size) / 2
        self.r = radius
        self.i = Vector((max(self.h.x - radius, 0), max(self.h.y - radius, 0), max(self.h.z - radius, 0)))
        self.bulge = {"+x": 0, "-x": 0, "+y": 0, "-y": 0, "+z": 0, "-z": 0}
        if bulge:
            self.bulge.update(bulge)
        self.taper = taper
        self.R = rot(*rot_deg)
        self.M = to4(self.R, center)
        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=2.0)
        bmesh.ops.subdivide_edges(bm, edges=bm.edges[:], cuts=cuts, use_grid_fill=True)
        for v in bm.verts:
            v.co = self.local(v.co.x, v.co.y, v.co.z)
        self.obj = mesh_object(name, bm, mat, self.M, subsurf=subsurf, outline=outline)

    def _taper(self, p):
        if self.taper == (1.0, 1.0):
            return p
        f = (p.z + self.h.z) / (2 * self.h.z)
        f = min(max(f, 0.0), 1.0)
        sx = self.taper[0] + (1 - self.taper[0]) * f
        sy = self.taper[1] + (1 - self.taper[1]) * f
        return Vector((p.x * sx, p.y * sy, p.z))

    def local(self, u, v, w):
        u = max(-1.0, min(1.0, u))
        v = max(-1.0, min(1.0, v))
        w = max(-1.0, min(1.0, w))
        h, i, r = self.h, self.i, self.r
        c = Vector((math.sin(u * math.pi / 2) * h.x, math.sin(v * math.pi / 2) * h.y, math.sin(w * math.pi / 2) * h.z))
        q = Vector((max(-i.x, min(i.x, c.x)), max(-i.y, min(i.y, c.y)), max(-i.z, min(i.z, c.z))))
        d = c - q
        p = q + d.normalized() * r if d.length > 1e-9 else c
        b = self.bulge
        p.x += (b["+x"] if u > 0 else b["-x"]) * (1 if u > 0 else -1) * (1 - v * v) * (1 - w * w) * abs(u) ** 8
        p.y += (b["+y"] if v > 0 else b["-y"]) * (1 if v > 0 else -1) * (1 - u * u) * (1 - w * w) * abs(v) ** 8
        p.z += (b["+z"] if w > 0 else b["-z"]) * (1 if w > 0 else -1) * (1 - u * u) * (1 - v * v) * abs(w) ** 8
        return self._taper(p)

    def _inv(self, a, half):
        return math.asin(max(-1.0, min(1.0, a / half))) * 2 / math.pi

    def _cube(self, face, a, b):
        axis, sign = face[1], (1.0 if face[0] == "+" else -1.0)
        h = self.h
        if axis == "x":
            return sign, self._inv(a, h.y), self._inv(b, h.z)
        if axis == "y":
            return self._inv(a, h.x), sign, self._inv(b, h.z)
        return self._inv(a, h.x), self._inv(b, h.y), sign

    def face_point(self, face, a, b, offset=0.0):
        u, v, w = self._cube(face, a, b)
        p = self.local(u, v, w)
        e = 1e-3
        axis = face[1]
        if axis == "x":
            t1 = self.local(u, v + e, w) - self.local(u, v - e, w)
            t2 = self.local(u, v, w + e) - self.local(u, v, w - e)
        elif axis == "y":
            t1 = self.local(u + e, v, w) - self.local(u - e, v, w)
            t2 = self.local(u, v, w + e) - self.local(u, v, w - e)
        else:
            t1 = self.local(u + e, v, w) - self.local(u - e, v, w)
            t2 = self.local(u, v + e, w) - self.local(u, v - e, w)
        n = t1.cross(t2).normalized()
        out = Vector((1 if axis == "x" else 0, 1 if axis == "y" else 0, 1 if axis == "z" else 0)) * (
            1 if face[0] == "+" else -1)
        if n.dot(out) < 0:
            n = -n
        p = p + n * offset
        return self.M @ p, (self.R @ n).normalized()

    def seam(self, face, per_corner=10, straight=10, offset=0.0):
        axis = "xyz".index(face[1])
        sign = 1.0 if face[0] == "+" else -1.0
        o1, o2 = [a for a in range(3) if a != axis]
        c45 = math.cos(math.pi / 4)
        ia, ib = self.i[o1], self.i[o2]
        rr = self.r * c45
        height = self.i[axis] + self.r * c45
        arcs = []
        for quarter, (ca, cb) in enumerate([(ia, ib), (-ia, ib), (-ia, -ib), (ia, -ib)]):
            arc = []
            for k in range(per_corner + 1):
                ang = math.pi / 2 * (quarter + k / per_corner)
                p = [0.0, 0.0, 0.0]
                n = [0.0, 0.0, 0.0]
                p[axis] = sign * height
                p[o1] = ca + rr * math.cos(ang)
                p[o2] = cb + rr * math.sin(ang)
                n[axis] = sign * c45
                n[o1] = math.cos(ang) * c45
                n[o2] = math.sin(ang) * c45
                arc.append(Vector(p) + Vector(n) * offset)
            arcs.append(arc)
        pts = []
        for j, arc in enumerate(arcs):
            pts.extend(arc)
            nxt = arcs[(j + 1) % 4][0]
            for k in range(1, straight):
                pts.append(arc[-1].lerp(nxt, k / straight))
        return [self.M @ self._taper(p) for p in pts]


def surface_path(fn, count=24):
    return [fn(k / (count - 1)) for k in range(count)]


def bisect(f, lo, hi, iters=40):
    flo = f(lo)
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        fm = f(mid)
        if (fm > 0) == (flo > 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return 0.5 * (lo + hi)


def intersection_ring(inner_center, inner_radii, inner_R, outer_implicit, count=48, lift=0.0015):
    pts = []
    for k in range(count):
        ph = 2 * math.pi * k / count

        def point(th):
            loc = Vector((math.sin(th) * math.cos(ph) * inner_radii[0], math.sin(th) * math.sin(ph) * inner_radii[1],
                          math.cos(th) * inner_radii[2]))
            return Vector(inner_center) + inner_R @ loc

        th = bisect(lambda t: outer_implicit(point(t)) - 1.0, 0.0, math.pi)
        p = point(th)
        loc_n = Vector((math.sin(th) * math.cos(ph) / inner_radii[0], math.sin(th) * math.sin(ph) / inner_radii[1],
                        math.cos(th) / inner_radii[2]))
        n = (inner_R @ loc_n).normalized()
        pts.append(p + n * lift)
    return pts


class Rig:
    def __init__(self, name):
        data = bpy.data.armatures.new(name + "_Rig")
        data.display_type = "STICK"
        self.obj = bpy.data.objects.new(name, data)
        link(self.obj)
        self.obj.show_in_front = True
        self.specs = []
        self.skinned = []

    def bone(self, name, head, parent=None, tail=None, length=0.06):
        h = Vector(head)
        t = Vector(tail) if tail is not None else h + Vector((0, 0, length))
        self.specs.append((name, h, t, parent))

    def build(self):
        bpy.context.view_layer.objects.active = self.obj
        for o in bpy.context.view_layer.objects:
            o.select_set(False)
        self.obj.select_set(True)
        bpy.ops.object.mode_set(mode="EDIT")
        eb = self.obj.data.edit_bones
        for name, h, t, parent in self.specs:
            b = eb.new(name)
            b.head = h
            b.tail = t
            b.roll = 0.0
            if parent:
                b.parent = eb[parent]
                b.use_connect = False
        bpy.ops.object.mode_set(mode="OBJECT")
        for pb in self.obj.pose.bones:
            pb.rotation_mode = "QUATERNION"

    def attach(self, objs, bone):
        if not isinstance(objs, (list, tuple)):
            objs = [objs]
        for o in objs:
            mw = o.matrix_world.copy()
            o.parent = self.obj
            o.parent_type = "BONE"
            o.parent_bone = bone
            bpy.context.view_layer.update()
            o.matrix_world = mw

    def skin(self, obj, bone_params):
        mw = obj.matrix_world.copy()
        obj.parent = self.obj
        obj.parent_type = "OBJECT"
        bpy.context.view_layer.update()
        obj.matrix_world = mw
        params = list(obj["vparam"])
        names = [b for b, _ in bone_params]
        centers = [c for _, c in bone_params]
        groups = {b: obj.vertex_groups.new(name=b) for b in names}
        for vi, t in enumerate(params):
            weights = []
            for j, c in enumerate(centers):
                if j == 0 and t <= c:
                    w = 1.0
                elif j == len(centers) - 1 and t >= c:
                    w = 1.0
                else:
                    left = centers[j - 1] if j > 0 else c
                    right = centers[j + 1] if j < len(centers) - 1 else c
                    if t < c:
                        w = (t - left) / (c - left) if c > left else 0.0
                    else:
                        w = (right - t) / (right - c) if right > c else 0.0
                    w = max(0.0, min(1.0, w))
                weights.append(w)
            s = sum(weights) or 1.0
            for j, w in enumerate(weights):
                if w > 1e-4:
                    groups[names[j]].add([vi], w / s, "REPLACE")
        mod = obj.modifiers.new("Armature", "ARMATURE")
        mod.object = self.obj
        del obj["vparam"]
        self.skinned.append(obj)

    def _pose(self, bname, loc=None, rot_deg=None, scale=None):
        pb = self.obj.pose.bones[bname]
        rest = self.obj.data.bones[bname].matrix_local.to_3x3()
        inv = rest.inverted()
        pb.location = inv @ Vector(loc if loc is not None else (0, 0, 0))
        rw = rot(*(rot_deg if rot_deg is not None else (0, 0, 0)))
        q = (inv @ rw @ rest).to_quaternion()
        pb.rotation_quaternion = q
        s = Matrix.Diagonal(Vector(scale if scale is not None else (1, 1, 1)))
        sl = inv @ s @ rest
        pb.scale = (abs(sl[0][0]), abs(sl[1][1]), abs(sl[2][2]))
        return pb

    def rest_pose(self):
        for pb in self.obj.pose.bones:
            pb.location = (0, 0, 0)
            pb.rotation_quaternion = (1, 0, 0, 0)
            pb.scale = (1, 1, 1)

    def action(self, name, seconds, tracks, step=1):
        ad = self.obj.animation_data or self.obj.animation_data_create()
        act = bpy.data.actions.new(name)
        act.use_fake_user = True
        ad.action = act
        frames = int(round(seconds * FPS))
        bnames = [b.name for b in self.obj.pose.bones]
        for f in list(range(0, frames, step)) + [frames]:
            t = f / FPS
            for b in bnames:
                fn = tracks.get(b)
                d = fn(t) if fn else {}
                pb = self._pose(b, d.get("loc"), d.get("rot"), d.get("scale"))
                pb.keyframe_insert("location", frame=f)
                pb.keyframe_insert("rotation_quaternion", frame=f)
                pb.keyframe_insert("scale", frame=f)
        self.rest_pose()
        track = ad.nla_tracks.new()
        track.name = name
        strip = track.strips.new(name, 0, act)
        if hasattr(strip, "action_slot") and len(act.slots):
            try:
                strip.action_slot = act.slots[0]
            except Exception:
                pass
        track.mute = True
        ad.action = None
        return act


def smooth01(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def bump(t, center, width):
    d = abs(t - center) / width
    return 0.0 if d >= 1 else 0.5 + 0.5 * math.cos(math.pi * d)


def window(t, a, b, c, d):
    return smooth01((t - a) / max(b - a, 1e-6)) * (1 - smooth01((t - c) / max(d - c, 1e-6)))


def wave(t, period, phase=0.0):
    return math.sin(2 * math.pi * t / period + phase)


def export_glb(path, objs, lite=False):
    for o in bpy.context.view_layer.objects:
        o.select_set(False)
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    saved = {}
    if lite:
        for o in objs:
            for m in o.modifiers:
                if m.type == "SUBSURF":
                    saved[(o.name, m.name)] = m.levels
                    m.levels = 0
    bpy.ops.export_scene.gltf(
        filepath=path,
        export_format="GLB",
        use_selection=True,
        export_apply=True,
        export_yup=True,
        export_animations=True,
        export_animation_mode="ACTIONS",
        export_force_sampling=True,
        export_optimize_animation_size=True,
        export_skins=True,
        export_materials="EXPORT",
        export_image_format="AUTO",
        export_def_bones=False,
        export_reset_pose_bones=True,
        export_extras=True,
    )
    for (on, mn), lv in saved.items():
        bpy.data.objects[on].modifiers[mn].levels = lv


def hierarchy(root):
    out = [root]
    for c in root.children_recursive:
        out.append(c)
    return out



def googly_eye(prefix, p, n, radius, depth, look, iris_ratio=0.46, implicit=None, rim_lift=0.12, up=Vector((0, 0, 1))):
    F = frame_z(n, up)
    radii = (radius, radius, depth)
    sclera = ellipsoid(prefix + "_LongTrang", p, radii, "Mat_Trang", R=F, seg=32, rings=16, subsurf=1,
                       outline=OUTLINE_SMALL)
    look_dir = Vector(look).normalized()
    pp, pn = ellipsoid_surface(p, radii, F, look_dir)
    PF = frame_z(pn, F.col[1])
    ir = radius * iris_ratio
    iris = ellipsoid(prefix + "_TrongMat", pp - pn * ir * 0.12, (ir, ir, ir * 0.32), "Mat_Mong", R=PF, seg=24,
                     rings=12, subsurf=1, outline=OUTLINE_NONE)
    pupil = ellipsoid(prefix + "_ConNguoi", pp + pn * ir * 0.1, (ir * 0.62, ir * 0.62, ir * 0.26), "Mat_Den", R=PF,
                      seg=24, rings=12, subsurf=1, outline=OUTLINE_NONE)
    glint_pos = pp + PF @ Vector((-ir * 0.42, ir * 0.42, ir * 0.3))
    glint = ellipsoid(prefix + "_AnhSang", glint_pos, (ir * 0.22, ir * 0.22, ir * 0.12), "Mat_Sang", R=PF, seg=12,
                      rings=6, subsurf=0, outline=OUTLINE_NONE)
    if implicit is not None:
        ring_pts = intersection_ring(p, radii, F, implicit, count=48)
    else:
        lift = depth * rim_lift
        ring_pts = circle_points(p + n * lift, n, radius * math.sqrt(max(1 - rim_lift ** 2, 0.0)), 48, F.col[1])
    rim = tube(prefix + "_VienMat", None, radius * 0.07, "Net_Ve", ring=10, closed=True, caps=False,
               outline=OUTLINE_NONE, dense=ring_pts)
    return dict(sclera=sclera, rim=rim, iris=iris, pupil=pupil, glint=glint, center=p, normal=n)
