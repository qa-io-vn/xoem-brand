import math
import bpy
from mathutils import Vector
import xoem3d_core as k

NAME = "Sofa_Em_Nga"
SEAT_TOP = 0.556


def seams(box, faces, radius, mat, name):
    return [k.tube("%s_Vien%s" % (name, f.replace("+", "P").replace("-", "M")), None, radius, mat, ring=10,
                   closed=True, caps=False, outline=k.OUTLINE_NONE, dense=box.seam(f, offset=0.002)) for f in faces]


def build():
    root = bpy.data.objects.new(NAME, None)
    root.empty_display_type = "PLAIN_AXES"
    k.link(root)
    root["seat_height"] = SEAT_TOP
    parts = []
    base = k.RBox("Sofa_De", (0, 0, 0.27), (2.0, 0.88, 0.28), 0.07, "Vai_DatNung", cuts=12, bulge={"-y": 0.012})
    parts += [base.obj] + seams(base, ("+z", "-z"), 0.0085, "Vai_DatNungDam", "Sofa_De")
    back = k.RBox("Sofa_Lung", (0, 0.31, 0.64), (1.52, 0.26, 0.62), 0.11, "Vai_DatNung", rot_deg=(-6, 0, 0), cuts=12,
                  bulge={"-y": 0.03, "+z": 0.015})
    parts += [back.obj] + seams(back, ("-y", "+y"), 0.0085, "Vai_DatNungDam", "Sofa_Lung")
    lines = []
    for x in (-0.25, 0.25):
        lines.append([back.face_point("-y", x, -0.2 + 0.44 * s / 10, offset=0.001)[0] for s in range(11)])
    parts.append(k.multi_tube("Sofa_Lung_DuongChia", lines, 0.009, "Vai_DatNungDam", ring=10))
    for side in (-1, 1):
        tag = "R" if side < 0 else "L"
        arm = k.RBox("Sofa_TayVin_" + tag, (0.88 * side, 0, 0.47), (0.26, 0.88, 0.58), 0.12, "Vai_DatNung", cuts=10,
                     bulge={("+x" if side > 0 else "-x"): 0.012, "+z": 0.01})
        parts += [arm.obj] + seams(arm, ("-y",), 0.0085, "Vai_DatNungDam", "Sofa_TayVin_" + tag)
        p, n = arm.face_point("-y", 0.0, 0.06)
        parts.append(k.ellipsoid("Sofa_TayVin_%s_Nut" % tag, p + n * 0.006, (0.024, 0.024, 0.014), "Vai_DatNungDam",
                                 R=k.frame_z(n), seg=16, rings=8, subsurf=1, outline=k.OUTLINE_NONE))
        cushion = k.RBox("Sofa_Dem_" + tag, (0.375 * side, -0.09, 0.47), (0.74, 0.66, 0.13), 0.05, "Vai_DatNung",
                         cuts=10, bulge={"+z": 0.026, "-y": 0.01})
        parts += [cushion.obj] + seams(cushion, ("+z", "-z"), 0.0075, "Vai_DatNungDam", "Sofa_Dem_" + tag)
    leg = [(0.0, 0.0), (0.024, 0.0), (0.03, 0.01), (0.038, 0.12), (0.044, 0.135), (0.0, 0.135)]
    for i, (x, y) in enumerate(((-0.86, -0.34), (0.86, -0.34), (-0.86, 0.34), (0.86, 0.34))):
        parts.append(k.lathe("Sofa_Chan_%d" % i, leg, "Go_OcCho", seg=24, matrix=k.to4(k.rot(), (x, y, 0.0)),
                             subsurf=1))
    pillow = k.RBox("Sofa_GoiOm", (0.6, 0.13, 0.7), (0.38, 0.13, 0.36), 0.06, "Vai_Kem", rot_deg=(-16, 0, -14),
                    cuts=10, bulge={"-y": 0.035, "+y": 0.03})
    parts += [pillow.obj] + seams(pillow, ("-y", "+y"), 0.0065, "Vai_DatNung", "Sofa_GoiOm")
    p, n = pillow.face_point("-y", 0.0, 0.0)
    F = k.frame_z(n) @ k.rot(0, 0, 30)
    parts.append(k.ellipsoid("Sofa_GoiOm_HatCaPhe", p + n * 0.002, (0.04, 0.058, 0.01), "Vai_DatNung", R=F, seg=24,
                             rings=12, subsurf=1, outline=k.OUTLINE_NONE))
    groove = [p + n * 0.011 + F @ Vector((0.009 * math.sin(math.pi * s / 3), -0.045 + 0.015 * s, 0)) for s in range(7)]
    parts.append(k.tube("Sofa_GoiOm_RanhHat", None, 0.0035, "Vai_DatNungDam", ring=6, outline=k.OUTLINE_NONE,
                        dense=groove))
    for o in parts:
        o.parent = root
    return root
