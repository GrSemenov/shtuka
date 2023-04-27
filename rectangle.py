from math import tan, sqrt
from vector import Vector
from directionalDistance import DirectionalDistance as dis


class Rectangle():
    def UnitUI(self, dots_hull):
        self.dots_hull = list(dots_hull)
        self.ln_hull = len(dots_hull)
        square = 10e9
        self.dots_rect = list()
        for i in range(self.ln_hull):
            a1, a2, a3, a4, a5 = self.searchFirstRect(self.dots_hull[i - 1], self.dots_hull[i])
            square1 = abs(a5[1] * (a4[1] - a3[1]))
            #print(square1)
            if square1 < square:
                #print(1)
                square = square1
                self.dots_rect = [a1, a2, a4[0], a5[0], a3[0]]

        # self.searchMinSquare(a1, [a2, 1], a3, a4, a5)
        return self.vertices(self.dots_rect)
        # return self.dots_rect

    def vertices(self, dots_rect):
        #print(dots_rect, '-------------')
        """if len(dots_rect) < 5:
            return self.dots_rect"""
        line = Vector(dots_rect[0], dots_rect[1])
        k_line = tan(line.polar())
        b_line = dots_rect[0][1] - k_line * dots_rect[0][0]
        normal = Vector([0, 0], [-line.y, line.x])
        k_normal = tan(normal.polar())
        b_normal = dots_rect[2][1] - k_normal * dots_rect[2][0]
        x1 = (b_line - b_normal) / (k_normal - k_line)
        y1 = x1 * k_line + b_line

        b_line = dots_rect[3][1] - k_line * dots_rect[3][0]
        x2 = (b_line - b_normal) / (k_normal - k_line)
        y2 = x2 * k_line + b_line

        b_normal = dots_rect[4][1] - k_normal * dots_rect[4][0]
        x3 = (b_line - b_normal) / (k_normal - k_line)
        y3 = x3 * k_line + b_line

        b_line = dots_rect[0][1] - k_line * dots_rect[0][0]
        x4 = (b_line - b_normal) / (k_normal - k_line)
        y4 = x4 * k_line + b_line

        square = sqrt((x1-x2)**2 + (y1-y2)**2) * sqrt((x3-x4)**2 + (y3-y4)**2)
        return [[round(x1), round(y1)], [round(x2), round(y2)], [round(x3), round(y3)], [round(x4), round(y4)]], square

    def searchFirstRect(self, dot1, dot2):
        line = Vector(dot1, dot2)
        #print(dot1, dot2, self.dots_hull)
        normal = Vector([0, 0], [-line.y, line.x])
        #print(line)
        #print(normal)
        min_right = min([[dot1, dis().distance(normal, dot1)], [dot2, dis().distance(normal, dot2)]],
                        key=lambda x: x[1])
        max_right = max([[dot1, dis().distance(normal, dot1)], [dot2, dis().distance(normal, dot2)]],
                        key=lambda x: x[1])
        max_up = [dot1, dis().distance(line, dot1)]
        #print(max_right, min_right, max_up)
        for i in range(self.ln_hull - 2):
            dist = (dis().distance(normal, self.dots_hull[i + 2]))
            #print(self.dots_hull[i + 2], 'точка')
            if dist < min_right[1]:
                min_right = [self.dots_hull[i + 2], dist, i + 2]
            elif dist > max_right[1]:
                max_right = [self.dots_hull[i + 2], dist, i + 2]
            dist2 = (dis().distance(line, self.dots_hull[i + 2]))
            #print(dist, min_right, max_right)
            #print(dist2, max_up)
            if dist2 > max_up[1]:
                #print('-')
                max_up = [self.dots_hull[i + 2], dist2, i + 2]
        #print(min_right, max_right, max_up)
        return dot1, dot2, min_right, max_right, max_up


'''
    def searchMinSquare(self, a1, a2, a3, a4, a5):
        square = abs(a5[1] * (a4[1]-a3[1]))
        dots_min = [a1, a2, a3, a4, a5]
        print(dots_min)
        dots = dots_min[:]
        for cnt in range(len(self.dots_hull)):
            print(a1, a2[0])
            line1 = Vector(dots[0], dots[1][0])
            normal1 = Vector([0, 0], [-line1.y, line1.x])
            print(line1, normal1)
            vec1 = Vector(dots[1][0], self.dots_hull[dots[1][1]+1])
            print('-----------')
            print(dots[1][0], self.dots_hull[dots[1][1]+1])
            vec2 = Vector(dots[2][0], self.dots_hull[dots[2][2]+1])
            print(dots[2][0], self.dots_hull[dots[2][2]+1])
            vec3 = Vector(dots[3][0], self.dots_hull[dots[3][2]+1])
            vec4 = Vector(dots[4][0], self.dots_hull[dots[4][2]+1])
            angle1 = vec1.angle(line1)
            angle2 = vec2.angle(normal1)
            angle3 = vec3.angle(line1)
            angle4 = vec4.angle(normal1)
            print(f'{line1}| {normal1}| {vec1}| {angle1}| {vec2}| {angle2}| {vec3}| {angle3}| {vec4}| {angle4}')
'''
