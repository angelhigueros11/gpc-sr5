# Graficas por computador
# Angel Higueros - 20460
# SR5

from vector import *

light = V3(0, 0, 1)

def cross(v1, v2):
    return V3(
        v1.y * v2.z - v1.z * v2.y,
        v1.z * v2.x - v1.x * v2.z,
        v1.x * v2.y - v1.y * v2.x,
    )


def load_triangle_3(face, transform_vertex, obj, scale_factor, translate_factor, texture, triangle):
    f1 = face[0][0] - 1
    f2 = face[1][0] - 1
    f3 = face[2][0] - 1

    v1 = transform_vertex(obj.vertex[f1], scale_factor, translate_factor)
    v2 = transform_vertex(obj.vertex[f2], scale_factor, translate_factor)
    v3 = transform_vertex(obj.vertex[f3], scale_factor, translate_factor)

    bright = (normalize(cross((v2 - v1), (v3 - v1))) @ light)

    if texture:

        fa = face[0][1] - 1
        fb = face[1][1] - 1
        fc = face[2][1] - 1

        t1 = V3(*obj.tvertex[fa])
        t2 = V3(*obj.tvertex[fb])
        t3 = V3(*obj.tvertex[fc])

        triangle(
            v2, v1, v3,
            cords=(t1, t3, t2),
            light=bright
        )

    elif bright >= 0:
        triangle(
            v1, v2, v3,
            bytes([bright, bright, bright])
        )


def load_triangle_4(face, transform_vertex, obj, scale_factor, translate_factor, texture, triangle):
    f1 = face[0][0] - 1
    f2 = face[1][0] - 1
    f3 = face[2][0] - 1
    f4 = face[3][0] - 1

    v1 = transform_vertex(obj.vertex[f1], scale_factor, translate_factor)
    v2 = transform_vertex(obj.vertex[f2], scale_factor, translate_factor)
    v3 = transform_vertex(obj.vertex[f3], scale_factor, translate_factor)
    v4 = transform_vertex(obj.vertex[f4], scale_factor, translate_factor)

    bright = (normalize(cross((v1 - v2), (v2 - v3))) @ light)

    if texture:
        fa = face[0][1] - 1
        fb = face[1][1] - 1
        fc = face[2][1] - 1
        f42 = face[3][1] - 1

        t1 = V3(*obj.tvertex[fa])
        t2 = V3(*obj.tvertex[fb])
        t3 = V3(*obj.tvertex[fc])
        t4 = V3(*obj.tvertex[f42])

        triangle(
            v1, v3, v2,
            cords=(t1, t3, t2),
            light=bright
        )
        triangle(
            v1, v4, v3,
            cords=(t1, t4, t3),
            light=bright
        )

    else:
        triangle(
            v1, v3, v2,
            bytes([bright, bright, bright])
        )
        triangle(
            v1, v4, v3,
            bytes([bright, bright, bright])
        )
