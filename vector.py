from math import atan2, pi


class Vector():
    def __init__(self, dot1, dot2):
        self.x = dot2[0] - dot1[0]
        self.y = dot2[1] - dot1[1]
        self.vector = (self.x, self.y)

    def crossProduct(self, vector2):
        return self.x * vector2.y - self.y * vector2.x

    def angle(self, vector2):
        return abs(self.polar() - vector2.polar())

    def polar(self):
        return atan2(self.y, self.x)

    def angularCoefficient(self):
        return self.y / self.x

    def __str__(self):
        return f"{self.x}, {self.y}"
