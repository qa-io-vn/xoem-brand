import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import bmesh
import bpy
import numpy as np
from mathutils import Vector, Matrix, Euler

import xoem3d_core as k

FILES = {"boss": "Boss", "nga": "Em-Nga", "ngo": "Em-Ngo", "sofa": "Sofa-Em-Nga"}
ROOTS = {"boss": "Boss", "nga": "Em_Nga", "ngo": "Em_Ngo", "sofa": "Sofa_Em_Nga"}
LABELS = {"boss": "Boss", "nga": "Em Ngả", "ngo": "Em Ngơ"}


def args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    return dict(out_root=os.path.abspath(argv[0]), mode=argv[1], which=argv[2] if len(argv) > 2 else "all",
                dest=os.path.abspath(argv[3]) if len(argv) > 3 else None,
                font=os.path.abspath(argv[4]) if len(argv) > 4 else None)


def setup_cycles(samples):
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    prefs = bpy.context.preferences.addons["cycles"].preferences
    try:
        prefs.compute_device_type = "METAL"
        prefs.get_devices()
        for d in prefs.devices:
            d.use = True
        sc.cycles.device = "GPU"
    except Exception:
        sc.cycles.device = "CPU"
    sc.cycles.samples = samples
    sc.cycles.use_adaptive_sampling = True
    sc.cycles.use_denoising = True
    try:
        sc.cycles.denoiser = "OPENIMAGEDENOISE"
    except Exception:
        pass
    sc.cycles.transparent_max_bounces = 48
    sc.cycles.max_bounces = 8
    sc.render.film_transparent = False
    vs = sc.view_settings
    for vt in ("Khronos PBR Neutral", "Standard"):
        try:
            vs.view_transform = vt
            break
        except Exception:
            continue
    vs.look = "None"
    vs.exposure = -0.4
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGBA"


def append_character(out_root, which):
    path = os.path.join(out_root, "blend", FILES[which] + ".blend")
    with bpy.data.libraries.load(path, link=False) as (src, dst):
        dst.collections = [c for c in src.collections]
    for c in dst.collections:
        if c.name not in bpy.context.scene.collection.children:
            bpy.context.scene.collection.children.link(c)
    root = bpy.data.objects[ROOTS[which]]
    if root.animation_data:
        for tr in root.animation_data.nla_tracks:
            tr.mute = True
        root.animation_data.action = None
    return root


def outline_material():
    if "VienNgoai" in bpy.data.materials:
        return bpy.data.materials["VienNgoai"]
    m = bpy.data.materials.new("VienNgoai")
    try:
        m.use_nodes = True
    except Exception:
        pass
    nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    mix = nt.nodes.new("ShaderNodeMixShader")
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = k.lin(k.PALETTE["nau_ca_phe"])
    em.inputs["Strength"].default_value = 1.0
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    nt.links.new(geo.outputs["Backfacing"], mix.inputs["Fac"])
    nt.links.new(em.outputs["Emission"], mix.inputs[1])
    nt.links.new(tr.outputs["BSDF"], mix.inputs[2])
    nt.links.new(mix.outputs["Shader"], out.inputs["Surface"])
    m.use_backface_culling = True
    return m


def add_outlines(root, scale=1.2):
    mat = outline_material()
    dg = bpy.context.evaluated_depsgraph_get()
    hulls = []
    for o in [root] + list(root.children_recursive):
        if o.type != "MESH":
            continue
        w = float(o.get("outline", 0.0)) * scale
        if w <= 0:
            continue
        skinned = any(m.type == "ARMATURE" for m in o.modifiers)
        if skinned:
            me = o.data.copy()
        else:
            me = bpy.data.meshes.new_from_object(o.evaluated_get(dg))
        bm = bmesh.new()
        bm.from_mesh(me)
        bm.normal_update()
        for v in bm.verts:
            v.co += v.normal * w
        bmesh.ops.reverse_faces(bm, faces=bm.faces[:])
        bm.to_mesh(me)
        bm.free()
        me.materials.clear()
        me.materials.append(mat)
        hull = bpy.data.objects.new(o.name + "_Vien", me)
        for c in o.users_collection:
            c.objects.link(hull)
        hull.parent = o.parent
        hull.parent_type = o.parent_type
        if o.parent_type == "BONE":
            hull.parent_bone = o.parent_bone
        hull.matrix_parent_inverse = o.matrix_parent_inverse.copy()
        hull.matrix_basis = o.matrix_basis.copy()
        if skinned:
            for vg in o.vertex_groups:
                hull.vertex_groups.new(name=vg.name)
            mod = hull.modifiers.new("Armature", "ARMATURE")
            mod.object = [m for m in o.modifiers if m.type == "ARMATURE"][0].object
        hull.visible_shadow = False
        hull.visible_diffuse = False
        hull.visible_glossy = False
        hull.visible_transmission = False
        hull.visible_volume_scatter = False
        hulls.append(hull)
    return hulls


def studio(shadow_catcher=False):
    sc = bpy.context.scene
    world = bpy.data.worlds.new("Studio")
    sc.world = world
    try:
        world.use_nodes = True
    except Exception:
        pass
    wn = world.node_tree
    bg = wn.nodes.get("Background")
    bg.inputs["Color"].default_value = k.lin("#FBF1E2")
    bg.inputs["Strength"].default_value = 0.32
    cam_bg = wn.nodes.new("ShaderNodeBackground")
    cam_bg.inputs["Color"].default_value = k.lin("#F1E4CF")
    cam_bg.inputs["Strength"].default_value = 1.0
    lp = wn.nodes.new("ShaderNodeLightPath")
    mix = wn.nodes.new("ShaderNodeMixShader")
    wout = wn.nodes.get("World Output")
    wn.links.new(lp.outputs["Is Camera Ray"], mix.inputs["Fac"])
    wn.links.new(bg.outputs["Background"], mix.inputs[1])
    wn.links.new(cam_bg.outputs["Background"], mix.inputs[2])
    wn.links.new(mix.outputs["Shader"], wout.inputs["Surface"])
    bm = bmesh.new()
    prof = []
    for i in range(12):
        prof.append((-8.0 + i * 0.9, 0.0))
    for i in range(1, 17):
        a = i / 16 * math.pi / 2
        prof.append((2.0 + math.sin(a) * 2.5, 2.5 - math.cos(a) * 2.5))
    prof.append((4.5, 8.0))
    rows = []
    for x in (-12.0, -4.0, 0.0, 4.0, 12.0):
        rows.append([bm.verts.new((x, y, z)) for y, z in prof])
    for a in range(len(rows) - 1):
        for j in range(len(prof) - 1):
            bm.faces.new((rows[a][j], rows[a + 1][j], rows[a + 1][j + 1], rows[a][j + 1]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    for f in bm.faces:
        if f.normal.z < -0.1 or (abs(f.normal.z) < 0.1 and f.normal.y > 0):
            f.normal_flip()
    me = bpy.data.meshes.new("Phong")
    bm.to_mesh(me)
    bm.free()
    me.shade_smooth()
    floor = bpy.data.objects.new("Phong", me)
    sc.collection.objects.link(floor)
    mat = bpy.data.materials.new("Phong")
    try:
        mat.use_nodes = True
    except Exception:
        pass
    p = mat.node_tree.nodes.get("Principled BSDF")
    p.inputs["Base Color"].default_value = k.lin("#F4E9D6")
    p.inputs["Roughness"].default_value = 0.92
    p.inputs["Emission Color"].default_value = k.lin("#F4E9D6")
    p.inputs["Emission Strength"].default_value = 0.22
    me.materials.append(mat)
    if shadow_catcher:
        floor.is_shadow_catcher = True
        sc.render.film_transparent = True

    def area(name, loc, target, size, energy, color="#FFF6EA"):
        ld = bpy.data.lights.new(name, "AREA")
        ld.shape = "DISK"
        ld.size = size
        ld.energy = energy
        ld.color = k.lin(color)[:3]
        ob = bpy.data.objects.new(name, ld)
        sc.collection.objects.link(ob)
        ob.location = loc
        d = Vector(target) - Vector(loc)
        ob.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
        return ob

    area("Den_Chinh", (-2.4, -2.8, 3.3), (0, 0, 0.5), 2.6, 430)
    area("Den_Phu", (3.0, -1.8, 1.7), (0, 0, 0.5), 3.2, 120, "#FFEBD8")
    area("Den_Vien", (1.6, 3.2, 3.0), (0, 0, 0.6), 1.8, 420, "#FFF2DF")
    area("Den_Tren", (0.0, 0.0, 4.5), (0, 0, 0), 3.0, 70)
    return floor


def bounds(root):
    dg = bpy.context.evaluated_depsgraph_get()
    pts = []
    for o in [root] + list(root.children_recursive):
        if o.type != "MESH" or o.name.endswith("_Vien"):
            continue
        ev = o.evaluated_get(dg)
        mw = ev.matrix_world
        for c in ev.bound_box:
            pts.append(mw @ Vector(c))
    a = np.array([tuple(p) for p in pts])
    return Vector(a.min(0)), Vector(a.max(0))


def camera(name, lens=50.0, ortho=None):
    cd = bpy.data.cameras.new(name)
    cd.lens = lens
    cd.sensor_width = 36
    if ortho:
        cd.type = "ORTHO"
        cd.ortho_scale = ortho
    cam = bpy.data.objects.new(name, cd)
    bpy.context.scene.collection.objects.link(cam)
    bpy.context.scene.camera = cam
    return cam


def aim(cam, target, direction, distance):
    d = Vector(direction).normalized()
    cam.location = Vector(target) + d * distance
    cam.rotation_euler = (-d).to_track_quat("-Z", "Y").to_euler()


def frame(cam, lo, hi, direction, aspect=1.0, margin=0.92):
    center = (lo + hi) / 2
    radius = (hi - lo).length / 2
    fov = 2 * math.atan(cam.data.sensor_width / 2 / cam.data.lens)
    if aspect < 1:
        fov = 2 * math.atan(math.tan(fov / 2) * aspect)
    dist = radius * margin / math.sin(fov / 2)
    aim(cam, center, direction, dist)
    return center


def render(path, w, h):
    sc = bpy.context.scene
    sc.render.resolution_x = w
    sc.render.resolution_y = h
    sc.render.resolution_percentage = 100
    sc.render.filepath = path
    os.makedirs(os.path.dirname(path), exist_ok=True)
    bpy.ops.render.render(write_still=True)
    print("RENDERED", path)


def clear_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def single(a, which, views, w, h, samples, transparent=False, tag=""):
    clear_scene()
    setup_cycles(samples)
    root = append_character(a["out_root"], which)
    add_outlines(root)
    studio(shadow_catcher=transparent)
    cam = camera("Cam", lens=55)
    lo, hi = bounds(root)
    for vname, direction in views:
        frame(cam, lo, hi, direction, aspect=w / h)
        render(os.path.join(a["dest"], "%s%s-%s.png" % (FILES[which], tag, vname)), w, h)


def sheet(a, which, samples):
    clear_scene()
    setup_cycles(samples)
    k.STATE["coll"] = bpy.context.scene.collection
    k.STATE["font"] = a["font"]
    root = append_character(a["out_root"], which)
    add_outlines(root)
    studio()
    lo, hi = bounds(root)
    size = hi - lo
    extent = max(size.x, size.y, size.z) * 1.22
    cam = camera("CamSheet", ortho=extent)
    center = (lo + hi) / 2
    center.z = lo.z + extent / 2 - 0.06 * extent
    names = [("truoc", 0), ("ba-phan-tu", 40), ("ben", 90), ("sau", 180)]
    paths = []
    for vname, yaw in names:
        root.rotation_euler = (0, 0, math.radians(yaw))
        bpy.context.view_layer.update()
        aim(cam, center, (0, -1, 0.16), 8.0)
        p = os.path.join(a["dest"], "_sheet_%s_%s.png" % (which, vname))
        render(p, 1000, 1100)
        paths.append(p)
    imgs = []
    for p in paths:
        im = bpy.data.images.load(p)
        arr = np.empty(im.size[0] * im.size[1] * 4, np.float32)
        im.pixels.foreach_get(arr)
        imgs.append(arr.reshape(im.size[1], im.size[0], 4))
    strip = np.concatenate(imgs, axis=1)
    hgt, wid = strip.shape[:2]
    out = bpy.data.images.new("sheet_" + which, wid, hgt, alpha=True)
    out.pixels.foreach_set(strip.ravel())
    dest = os.path.join(a["dest"], "%s-model-sheet.png" % FILES[which])
    out.filepath_raw = dest
    out.file_format = "PNG"
    out.save()
    for p in paths:
        os.remove(p)
    print("RENDERED", dest)


def group(a, samples, w=2400, h=1350):
    clear_scene()
    setup_cycles(samples)
    sofa = append_character(a["out_root"], "sofa")
    nga = append_character(a["out_root"], "nga")
    boss = append_character(a["out_root"], "boss")
    ngo = append_character(a["out_root"], "ngo")
    sofa.location = (-0.95, 0.45, 0)
    sofa.rotation_euler = (0, 0, math.radians(6))
    nga.location = (-0.98, 0.30, float(sofa.get("seat_height", 0.5)))
    nga.rotation_euler = (0, 0, math.radians(6))
    nga.scale = (0.9, 0.9, 0.9)
    boss.location = (1.45, 0.35, 0)
    boss.rotation_euler = (0, 0, math.radians(-32))
    ngo.location = (0.0, -0.95, 0)
    ngo.rotation_euler = (0, 0, math.radians(-12))
    bpy.context.view_layer.update()
    for r in (sofa, nga, boss, ngo):
        add_outlines(r, scale=1.35)
    studio()
    cam = camera("CamGroup", lens=42)
    los, his = zip(*[bounds(r) for r in (sofa, nga, boss, ngo)])
    lo = Vector(np.min(np.array([tuple(v) for v in los]), 0))
    hi = Vector(np.max(np.array([tuple(v) for v in his]), 0))
    frame(cam, lo, hi, (-0.35, -1.0, 0.42), aspect=w / h, margin=0.82)
    render(os.path.join(a["dest"], "Xoem-Linh-vat-3D-nhom.png"), w, h)


def main():
    a = args()
    which = ["boss", "nga", "ngo"] if a["which"] == "all" else [a["which"]]
    if a["mode"] == "preview":
        for c in which:
            single(a, c, [("34", (-0.75, -1.0, 0.45)), ("sau", (0.6, 1.0, 0.5))], 900, 900, 24)
    elif a["mode"] == "hero":
        for c in which:
            single(a, c, [("hero", (-0.72, -1.0, 0.42))], 1600, 1600, 160)
    elif a["mode"] == "cutout":
        for c in which:
            single(a, c, [("trong-suot", (-0.72, -1.0, 0.42))], 1600, 1600, 128, transparent=True)
    elif a["mode"] == "sheet":
        for c in which:
            sheet(a, c, 96)
    elif a["mode"] == "group":
        group(a, 160)


main()
