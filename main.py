# Graficas por computador
# Angel Higueros - 20460
# SR5

import struct

from cube import *
from texture import *
from vector import *
from utils import *


# Métodos de escritura
def char(c):
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    return struct.pack('=h', w)

def dword(d):
    return struct.pack('=l', d)

def color(r, g, b):
    return bytes([b, g, r])

def cross(v1, v2):
    return V3(
        v1.y * v2.z - v1.z * v2.y,
        v1.z * v2.x - v1.x * v2.z,
        v1.x * v2.y - v1.y * v2.x,
    )

def bounding_box(v1, v2, v3):
    x = [v1.x, v2.x, v3.x]
    y = [v1.y, v2.y, v3.y]
    
    x.sort()
    y.sort()

    return V3(x[0], y[0], 0), V3(x[-1], y[-1], 0)


def barycentric(v1, v2, v3, v4):
    c = cross(
        V3(v2.x - v1.x, v3.x - v1.x, v1.x - v4.x),
        V3(v2.y - v1.y, v3.y - v1.y, v1.y - v4.y)
    )

    if c.z == 0:
        return -1, -1, -1

    return (
        c.x / c.z, c.y / c.z, 
        1 - ((c.x + c.y) / c.z)
    )


# def barycenter(a, b, c, p):
#     cx, cy, cz = cross(
#         V3(b.x - a.x, c.x - a.x, a.x - p.x), 
#         V3(b.y - a.y, c.y - a.y, a.y - p.y)
#     )


#     if abs(cz) < 1:
#         return -1, -1, -1 

#     u = cx / cz
#     v = cy / cz
#     w = 1 - (cx + cy) / cz

#     return (w, v, u)


class Render(object):
    def __init__(self, filename):
        self.filename = filename
        self.width = 100
        self.height = 100
        self.width_vertex = 100
        self.height_vertex = 100
        self.current_color = color(255, 255, 255)  # por defecto blanco
        self.framebuffer = []
        self.background_color = color(0, 0, 0)  # por defecto negro
        self.x_vertex = None
        self.y_vertex = None
        self.Texture = None
        self.glClear()

    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height

    def glClear(self):
        self.framebuffer = [[self.background_color for _ in range(
            self.width)] for _ in range(self.height)]
        self.zbuffer = [
            [-99999 for _ in range(self.width)] for _ in range(self.height)]

    def glVertex(self, cords):
        
        vertex_x = (self.width_vertex / 2) + (cords[0] * self.width_vertex / 2)
        vertex_y = (self.height_vertex / 2) + (-cords[1] * self.height_vertex / 2)
        x = self.x_vertex + vertex_x
        y = self.y_vertex + vertex_y
        
        self.framebuffer[
            int(x)][int(y)
            ] = self.current_color
    
    def point(self, x, y):
        if 0 < x < self.width and 0 < y < self.height:
            self.framebuffer[x][y] = self.current_color

    def line(self, v1, v2):
        x0 = round(v1.x)
        y0 = round(v1.y)
        x1 = round(v2.x)
        y1 = round(v2.y)

        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        steep = dy > dx

        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dy = abs(y1 - y0)
        dx = x1 - x0

        offset = 0
        threshold = dx
        y = y0

        for x in range(x0, x1 + 1):
            if steep:
                self.point(x, y)
            else:
                self.point(y, x)

            offset += dy * 2

            if offset >= threshold:
                y += 1 if y0 < y1 else -1
                # threshold += 1 * dx * 2
                threshold += dx * 2


    def glViewPort(self, cords, width, height):
        self.width_vertex, self.height_vertex = width - 1, height - 1
        self.x_vertex, self.y_vertex = cords

    def glColor(self, r, g, b):
        self.current_color = color(r, g, b)

    def glFinish(self):
        f = open(self.filename, 'bw')
        # Pixel header
        f.write(char('B'))
        f.write(char('M'))
        # tamaño archivo = 14 header + 40  info header + resolucion
        f.write(dword(14 + 40 + self.width * self.height * 3))
        f.write(word(0))
        f.write(word(0))
        f.write(dword(14 + 40))

        # Info header
        f.write(dword(40))  # tamaño header
        f.write(dword(self.width))  # ancho
        f.write(dword(self.height))  # alto
        f.write(word(1))  # numero de planos (siempre 1)
        f.write(word(24))  # bits por pixel (24 - rgb)
        f.write(dword(0))  # compresion
        # tamaño imagen sin header
        f.write(dword(self.width * self.height * 3))
        f.write(dword(0))  # resolucion
        f.write(dword(0))  # resolucion
        f.write(dword(0))  # resolucion
        f.write(dword(0))  # resolucion

        for y in range(self.height-1, -1, -1):
          for x in range(self.width):
              f.write(self.framebuffer[x][y])


    def triangle(self, v1, v2, v3, cords, light):

        m, n = bounding_box(v1, v2, v3)

        # a, b, c = vertices

        # if self.texture:
        #     ta, tb, tc = tvertices


        # luz = V3(0, 0, 1)
        # n = (b - a) * (c - a)
        # i = n.norm() @ luz.norm()

        # if i < 0:
        #     return

        # grey = round(255 * i)
        # self.glColor(grey,  grey, grey)

        for x in range(m.x , n.x):
            for y in range(m.y, n.y):
                w, v, u = barycentric(v1, v2, v3, V3(x, y))

                if w < 0 or v < 0 or u < 0:
                    continue

                if self.Texture:
                    tx = (cords[0].x * w) + (cords[1].x * v) + (cords[2].x * u)
                    ty = (cords[0].y * w) + (cords[1].y * v) + (cords[2].y * u)

                    self.current_color = self.Texture.get_color_with_intensity(
                        tx, ty, light
                    )

                z = (v1.z * w) + (v2.z * v) + (v3.z * u)

                # if (self.zBuffer[x][y] < z):
                #     self.zBuffer[x][y] = z

                #     if self.texture:
                #         tx = ta.x * w + tb.x + u + tc.x * v
                #         ty = ta.y * w + tb.y + u + tc.y * v

                #         self.current_color = self.texture.get_color_with_intensity(tx, ty, i)

                #         self.get_
                #     self.point(y, x)
                if z > self.zbuffer[
                        int(
                        self.x_vertex +
                        (self.width_vertex/2) +
                        (x / self.width * self.width_vertex / 2))
                    ][
                        int(self.y_vertex + (self.height_vertex / 2) +
                        (-y / self.height * self.height_vertex / 2))
                    ]:
                    self.zbuffer[
                        int(
                        self.x_vertex +
                        (self.width_vertex/2) +
                        (x / self.width * self.width_vertex/2))
                    ][
                        int(self.y_vertex +
                        (self.height_vertex/2) +
                        (-y / self.height * self.height_vertex/2))
                    ] = z
                    self.glVertex((x / self.width, y / self.height))


    def transform_vertex(self, vertex, scale, translate):
        return V3(
            round((vertex[0] + translate[0]) * scale[0]),
            round((vertex[1] + translate[1]) * scale[1]),
            round((vertex[2] + translate[2]) * scale[2]),
        )

    def load_model(self, filename, scale_factor, translate_factor):
        obj = Obj(filename)
        for face in obj.faces:
            if len(face) == 3:
                load_triangle_3(face, self.transform_vertex, obj, scale_factor, translate_factor, self.Texture, self.triangle)
            if len(face) == 4:
                load_triangle_4(face, self.transform_vertex, obj, scale_factor, translate_factor, self.Texture, self.triangle)
                

# IMPLEMENTACION
r = Render('sr5.bmp')

r.glCreateWindow(600, 600)
r.glViewPort((0, 0), 600, 600)
r.glClear()

scale_factor = (600, 600, 600)
translate_factor = (0, 0, 0)
r.Texture = Texture('./model.bmp')
r.load_model('./model.obj', scale_factor, translate_factor)

# r.triangle(V3(10, 70), V3(50, 160), V3(70, 80))
# r.triangle(V3(180, 50), V3(150, 1), V3(70, 180))
# r.triangle(V3(180, 150), V3(120, 160), V3(130, 180))


r.glFinish()
