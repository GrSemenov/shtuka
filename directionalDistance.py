from vector import Vector
from math import atan2, sqrt, pi, tan


class DirectionalDistance():
    def distance(self, line, dot):
        return -(dot[0] * tan(line.polar())+ - dot[1]) / sqrt(tan(line.polar())**2 + line.y ** 2)
'''
        angle = line.polar()
        if angle < 0:
            angle = pi + angle
        at2 = atan2(dot[1], dot[0])

        if at2 > 0:
            if at2 > angle:
                return abs(line.x * dot[0] - line.y * dot[1]) / sqrt(line.x ** 2 + line.y ** 2)
            return -abs(line.x * dot[0] - line.y * dot[1]) / sqrt(line.x ** 2 + line.y ** 2)
        else:
            if at2 > angle - pi:
                return -abs(line.x * dot[0] - line.y * dot[1]) / sqrt(line.x ** 2 + line.y ** 2)
            return abs(line.x * dot[0] - line.y * dot[1]) / sqrt(line.x ** 2 + line.y ** 2)
'''
#      if (atan2(dot[1], dot[0]) > angle) and (atan2(dot[1], dot[0]) < angle + 180):
#         return -abs(line.x * dot[0] - line.y * dot[1]) / sqrt(line.x ** 2 + line.y ** 2)
#    return abs(line.x * dot[0] - line.y * dot[1]) / sqrt(line.x ** 2 + line.y ** 2)
