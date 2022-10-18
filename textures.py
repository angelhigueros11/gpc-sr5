import struct
from main import color

class Texture(object):
    def __init__(self, path):
        self.path = path
        self.read()
        
    def read(self):
        with open(self.path, "rb") as image:
            image.seek(2 + 4 + 2 + 2)
            header_size = struct.unpack('=l', image.read(4))
            image.seek(2 + 4 + 2 + 2 + 4 + 4)
            self.width = struct.unpack('=l', image.read(4))
            self.height = struct.unpack('=l', image.read(4))

            image.seek(header_size)
        
            self.pixels = []
            for y in range(self.height + 1):
                self.pixels.append([])

                for x in range(self.width + 2):
                    b = ord(image.read(1))
                    g = ord(image.read(1))
                    r = ord(image.read(1))

                    self.pixels[y].append(
                        color(r, g, b)
                    )


