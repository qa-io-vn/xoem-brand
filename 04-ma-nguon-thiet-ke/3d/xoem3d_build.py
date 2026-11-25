import importlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import bpy
import xoem3d_core as k

CHARACTERS = {
    "boss": ("Boss", "Boss"),
    "nga": ("Em_Nga", "Em-Nga"),
    "ngo": ("Em_Ngo", "Em-Ngo"),
    "sofa": ("Sofa_Em_Nga", "Sofa-Em-Nga"),
}


def args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    out_root = os.path.abspath(argv[0])
    which = argv[1]
    font = os.path.abspath(argv[2]) if len(argv) > 2 else None
    return out_root, which, font


def main():
    out_root, which, font = args()
    coll_name, file_name = CHARACTERS[which]
    k.reset_scene()
    k.begin(coll_name, os.path.join(out_root, "texture"), font)
    k.define_standard_materials()
    module = importlib.import_module("xoem3d_" + which)
    root = module.build()
    root_obj = root.obj if hasattr(root, "obj") else root
    objs = k.hierarchy(root_obj)
    for o in objs:
        if "vparam" in o:
            del o["vparam"]
    glb_dir = os.path.join(out_root, "glb")
    blend_dir = os.path.join(out_root, "blend")
    os.makedirs(glb_dir, exist_ok=True)
    os.makedirs(blend_dir, exist_ok=True)
    k.export_glb(os.path.join(glb_dir, file_name + ".glb"), objs)
    k.export_glb(os.path.join(glb_dir, file_name + "-lite.glb"), objs, lite=True)
    tris = 0
    dg = bpy.context.evaluated_depsgraph_get()
    for o in objs:
        if o.type == "MESH":
            me = o.evaluated_get(dg).to_mesh()
            me.calc_loop_triangles()
            tris += len(me.loop_triangles)
            o.evaluated_get(dg).to_mesh_clear()
    actions = [a.name for a in bpy.data.actions]
    print("BUILD_OK", which, "objects", len(objs), "tris", tris, "actions", actions)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(blend_dir, file_name + ".blend"), compress=True)


main()
