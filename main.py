# Graficas por computador
# Angel Higueros - 20460
# SR5

import struct
from cube import Obj
from vector import *
from textures import *

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
    return (
        v1.y * v2.z - v1.z * v2.y,
        v1.z * v2.x - v1.x * v2.z,
        v1.x * v2.y - v1.y * v2.x,
    )


def bounding_box(A, B, C):
    coords = [(A.x, A.y), (B.x, B.y), (C.x, C.y)]

    xmin = 999999
    xmax = -999999
    ymin = 999999
    ymax = -999999

    for (x, y) in coords:
        if x < xmin:
            xmin = x
        if x > xmax:
            xmax = x
        if y < ymin:
            ymin = y
        if y > ymax:
            ymax = y

    return V3(xmin, ymin),  V3(xmax, ymax)


def barycenter(a, b, c, p):
    cx, cy, cz = cross(
        V3(b.x - a.x, c.x - a.x, a.x - p.x), 
        V3(b.y - a.y, c.y - a.y, a.y - p.y)
    )


    if abs(cz) < 1:
        return -1, -1, -1 

    u = cx / cz
    v = cy / cz
    w = 1 - (cx + cy) / cz

    return (w, v, u)



class Render(object):

    def glInit(self, filename = 'sr3.bmp'):
        self.filename = filename 
        self.width = 100 
        self.height = 100
        self.current_color = color(255, 255, 255) # por defecto blanco
        self.framebuffer = []
        self.texture = None
        self.glClear()

    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height

    def glClear(self):
        self.framebuffer = [
            [color(0, 0, 0) for x in range(self.width)]
            for y in range(self.height)
        ]

        self.zBuffer= [
            [-9999 for x in range(self.width)]
            for y in range(self.height)
        ]

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
            x0, y0 =  y0, x0
            x1, y1 =  y1, x1

        if x0 > x1:
            x0, x1 = x1, x0 
            y0, y1 = y1, y0 

        dy = abs(y1 - y0)
        dx = x1 - x0

        offset = 0
        threshold = dx
        y =  y0

        for x in range(x0, x1 + 1):           
            if steep:
                self.point(x, y)
            else:
                self.point(y, x)

            # offset += (dy/dx) * dx * 2
            offset += dy * 2

            if offset >= threshold:
                y += 1 if y0 < y1 else  -1
                # threshold += 1 * dx * 2
                threshold += dx * 2


    def transform_vertex(self, vertex, scale, translate):
        return V3(
            (vertex[0] * scale[0]) + translate[0],
            (vertex[1] * scale[1]) + translate[1],
            (vertex[2] * scale[2]) + translate[2],
        )

    def load_model(self, filename, scale_factor = (1, 1, 1), translate_factor = (0, 0, 0)):
        obj = Obj(filename)
        for face in obj.faces:
            if len(face) == 3:
                f1 = face[0][0] - 1
                f2 = face[1][0] - 1
                f3 = face[2][0] - 1

  
                v1 =  self.transform_vertex(obj.vertices[f1], scale_factor, translate_factor)
                v2 =  self.transform_vertex(obj.vertices[f2], scale_factor, translate_factor)
                v3 =  self.transform_vertex(obj.vertices[f3], scale_factor, translate_factor)

                if self.texture:
                    ft1 = face[0][1] - 1
                    ft2 = face[1][1] - 1
                    ft3 = face[2][1] - 1
                    
                    vt1 = V3(
                        obj.tvertices[ft1][0],
                        obj.tvertices[ft1][1],
                        )
                    vt2 = V3(
                        obj.tvertices[ft2][0],
                        obj.tvertices[ft2][1],
                        )
                    vt3 = V3(
                        obj.tvertices[ft3][0],
                        obj.tvertices[ft3][1],
                        )
                    
                    self.triangle(
                        (v1, v2, v3),
                        (vt1, vt2, vt3)
                    )
                    
                else:
                    self.triangle((v1, v2, v3))

            if len(face) == 4:
                f1 = face[0][0] - 1
                f2 = face[1][0] - 1
                f3 = face[2][0] - 1
                f4 = face[3][0] - 1

                v1 =  self.transform_vertex(obj.vertices[f1], scale_factor, translate_factor)
                v2 =  self.transform_vertex(obj.vertices[f2], scale_factor, translate_factor)
                v3 =  self.transform_vertex(obj.vertices[f3], scale_factor, translate_factor)
                v4 =  self.transform_vertex(obj.vertices[f4], scale_factor, translate_factor)

                self.line(v1[0], v1[1], v2[0], v2[1])
                self.line(v2[0], v2[1], v3[0], v3[1])
                self.line(v3[0], v3[1], v1[0], v1[1])
                self.line(v4[0], v4[1], v1[0], v1[1]) 

    def triangle(self, vertices, tvertices = ()):
        a, b, c = vertices

        if self.texture:
            ta, tb, tc = tvertices


        luz = V3(0, 0, 1)
        n = (b - a) * (c - a)
        i = n.norm() @ luz.norm()

        if i < 0:
            return

        grey = round(255 * i)
        self.glColor(grey,  grey, grey)
  

        box_min, box_max = bounding_box(a, b, c)
        box_min.round()
        box_max.round()
        for x in range(box_min.x, box_max.x + 1):
            for y in range(box_min.y, box_max.y + 1):
                w, v, u = barycenter(a, b, c, V3(x, y))

                if (w < 0 or v < 0 or u < 0):
                    continue
                

                z = a.z * w + b.z * v + c.z * u

                if (self.zBuffer[x][y] < z):
                    self.zBuffer[x][y] = z

                    if self.texture:
                        tx = ta.x * w + tb.x + u + tc.x * v
                        ty = ta.y * w + tb.y + u + tc.y * v

                        self.current_color = self.texture.get_color_with_intensity(tx, ty, i)

                        self.get_
                    self.point(y, x)


       
        

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
        f.write(dword(40)) # tamaño header
        f.write(dword(self.width)) # ancho
        f.write(dword(self.height)) # alto
        f.write(word(1)) # numero de planos (siempre 1)
        f.write(word(24)) # bits por pixel (24 - rgb)
        f.write(dword(0)) # compresion
        f.write(dword(self.width * self.height * 3)) # tamaño imagen sin header
        f.write(dword(0)) # resolucion
        f.write(dword(0)) # resolucion
        f.write(dword(0)) # resolucion
        f.write(dword(0)) # resolucion


        for y in range(self.height):
            for x in range(self.width):
                f.write(self.framebuffer[y][x])


# IMPLEMENTACION
r = Render()
r.glInit('sr5-textures.bmp')
r.glCreateWindow(1050, 1000)
r.glColor(0, 250, 250)

scale_factor = (400, 400, 500)
translate_factor = (512, 512, 0)
r.texture = Texture('./model.bmp')
r.load_model('object.obj', scale_factor, translate_factor)

# r.triangle(V3(10, 70), V3(50, 160), V3(70, 80))
# r.triangle(V3(180, 50), V3(150, 1), V3(70, 180))
# r.triangle(V3(180, 150), V3(120, 160), V3(130, 180))


r.glFinish()
