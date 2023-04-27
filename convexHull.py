from math import atan2, sqrt
from stack import Stack
from vector import Vector


class ConvexHull():
    def __init__(self, dots):
        self.dots = list(dots)
        polar = self.sort_polar(self.dots)
        self.hull = self.search_hull(polar)


    def sort_polar(self, dots):
        self.lower_dot = min(self.dots, key=lambda x: (x[1], x[0]))
        lower_x = self.lower_dot[0]
        lower_y = self.lower_dot[1]
        polar = dots[:]
        polar.remove(self.lower_dot)
        # пересчет всех точек в систему координат нижней
        for i in range(len(polar)):
            polar[i] = [polar[i][0]-lower_x, polar[i][1]-lower_y, sqrt((polar[i][0]-lower_x)**2 + (polar[i][1]-lower_y)**2)]

        polar.sort(key=lambda x: (atan2(x[1], x[0]), x[2]), reverse=True)
        polar_st = Stack()
        for i in range(len(polar)):
            polar[i].pop(-1)
            polar_st.add(polar[i])
        return polar_st

    def search_hull(self, polar):
        stack = Stack()
        stack.add([0, 0])
        two_el = polar.get()
        stack.add(two_el)

        while len(polar) > 0:
            dot2 = stack.get()
            dot1 = stack.get()
            dot3 = polar.get()
            vector1 = Vector(dot1, dot2)
            vector2 = Vector(dot1, dot3)
            cross_product = vector1.crossProduct(vector2)
            if cross_product >= 0:
                stack.add(dot1)
                stack.add(dot2)
                stack.add(dot3)
            else:
                if len(stack) > 0:
                    stack.add(dot1)
                    polar.add(dot3)
        lst = stack.getList()
        for i in range(len(lst)):
            lst[i][0] += self.lower_dot[0]
            lst[i][1] += self.lower_dot[1]
        return lst
