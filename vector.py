# Graficas por computador
# Angel Higueros - 20460
# SR5

class V3(object):
    def __init__(self, x, y, z = 0):
            self.x = x
            self.y = y
            self.z = z

    def round(self):
        self.x = round(self.x)
        self.y = round(self.y)
        self.z = round(self.z)

    def __add__(self, other):
        return V3(
                self.x + other.x,
                self.y + other.y,
                self.z + other.z,
            )
    
    def __sub__(self, other):
        return V3(
                self.x - other.x,
                self.y - other.y,
                self.z - other.z,
            )
    
    def __mul__(self, other):
        if type(other) in [int, float]:
            return V3(
                    self.x * other, 
                    self.y * other,
                    self.z * other,
                )

        return V3(
            self.y * other.z - self.z * self.y,
            self.z * other.x - self.x * self.z,
            self.x * other.y - self.y * self.x,
        )

    def length(self):
        return (self.x**2 + self.y**2 + self.z**2)**0.5
    
    def __matmul__(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def norm(self):
        return self * (1 / self.length())

    def __repr__(self):
        return f"V3({self.x}, {self.y}, {self.z})"


def normalize(vector):
    l = vector.length()
    return V3(vector.x / l, vector.y / l, vector.z / l) if l else V3(0, 0, 0)
