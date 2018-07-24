from numpy import ones,vstack
from numpy.linalg import lstsq
import math

def close_to(a, b):
    if abs(a - b) < 0.0000001:
        return True
    return False

def ge(a, b):
    if (a - b) > -0.0000001:
        return True
    return False

def le(a, b):
    if (b - a) > -0.0000001:
        return True
    return False

class Node:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class Box:
    def __init__(self, nodes):
        if len(nodes) != 8:
            raise ValueError('Box needs exactly 8 nodes')
        self.nodes = nodes

    def intersect_with(self, box):
        h1, h2 = self.height_intersection_with(box)
        rectangle_nodes = self.rectangle_intersection_with(box)
        intersection = []
        for node in rectangle_nodes:
            intersection.append((node[0], node[1], h1))
        for node in rectangle_nodes:
            intersection.append((node[0], node[1], h2))
        return intersection

    def height_intersection_with(self, box):
        a1 = self.nodes[0].z
        a2 = self.nodes[4].z
        b1 = box.nodes[0].z
        b2 = box.nodes[4].z

        if a2 > a1 or b2 > b1:
            raise ValueError('Invalid box heights')

        difference = max(0, min(a1, b1) - max(a2, b2))
        if difference == 0:
            return None, None
        if difference == (a1 - a2):
            return a1, a2
        if difference == (b1 - b2):
            return b1, b2

        if a1 >= b1:
            return b1, a2
        else:
            return a1, b2

    def rectangle_intersection_with(self, box):
        lines1 = []
        for idx in range(3):
            lines1.append((self.nodes[idx].x, self.nodes[idx].y, self.nodes[idx+1].x, self.nodes[idx+1].y))
        lines1.append((self.nodes[3].x, self.nodes[3].y, self.nodes[0].x, self.nodes[0].y))
        lines2 = []
        for idx in range(3):
            lines2.append((box.nodes[idx].x, box.nodes[idx].y, box.nodes[idx+1].x, box.nodes[idx+1].y))
        lines2.append((box.nodes[3].x, box.nodes[3].y, box.nodes[0].x, box.nodes[0].y))

        def intersecting_point(line1, line2):
            points = [(line1[0], line1[1]), (line1[2], line1[3])]
            x_coords, y_coords = zip(*points)
            A = vstack([x_coords,ones(len(x_coords))]).T
            m1, c1 = lstsq(A, y_coords)[0]

            points = [(line2[0], line2[1]), (line2[2], line2[3])]
            x_coords, y_coords = zip(*points)
            A = vstack([x_coords,ones(len(x_coords))]).T
            m2, c2 = lstsq(A, y_coords)[0]

            x1 = None
            if close_to(line1[0], line1[2]):
                x1 = line1[0]
            x2 = None
            if close_to(line2[0], line2[2]):
                x2 = line2[0]

            x = None
            y = None
            if x1 is not None and x2 is not None:
                if close_to(x1, x2):
                    a1 = max(line1[1], line1[3])
                    a2 = min(line1[1], line1[3])
                    b1 = max(line2[1], line2[3])
                    b2 = min(line2[1], line2[3])
                    difference = max(0, min(a1, b1) - max(a2, b2))
                    if difference == 0:
                        return (None, None, None, None)
                    if difference == (a1 - a2):
                        return (x1, a1, x2, a2)
                    if difference == (b1 - b2):
                        return (x1, b1, x2, b2)

                    if a1 >= b1:
                        return (x1, b1, x2, a2)
                    else:
                        return (x1, a1, x2, b2)
                else:
                    return (None, None, None, None)
            elif x1 is not None:
                y = m2 * x1 + c2
                x = x1
            elif x2 is not None:
                y = m1 * x2 + c1
                x = x2
            else:
                if close_to(m1, m2):
                    if close_to(c1, c2):
                        a1, a2, b1, b2, a1y, a2y, b1y, b2y = (None,) * 8
                        if line1[0] > line1[2]:
                            a1 = line1[0]
                            a1y = line1[1]
                            a2 = line1[2]
                            a2y = line1[3]
                        else:
                            a1 = line1[2]
                            a1y = line1[3]
                            a2 = line1[0]
                            a2y = line1[1]
                        if line2[0] > line2[2]:
                            b1 = line2[0]
                            b1y = line2[1]
                            b2 = line2[2]
                            b2y = line2[3]
                        else:
                            b1 = line2[2]
                            b1y = line2[3]
                            b2 = line2[0]
                            b2y = line2[1]
                        difference = max(0, min(a1, b1) - max(a2, b2))
                        if difference == 0:
                            return (None, None, None, None)
                        if difference == (a1 - a2):
                            return (a1, a1y, a2, a2y)
                        if difference == (b1 - b2):
                            return (b1, b1y, b2, b2y)

                        if a1 >= b1:
                            return (b1, b1y, a2, a2y)
                        else:
                            return (a1, a1y, b2, b2y)
                    else:
                        return (None, None, None, None)

                x = (c2 - c1) / (m1 - m2)
                y = m1 * x + c1

            if ((ge(x, line1[0]) and le(x, line1[2])) or (le(x, line1[0]) and ge(x, line1[2]))) and \
                ((ge(x, line2[0]) and le(x, line2[2])) or (le(x, line2[0]) and ge(x, line2[2]))) and \
                ((ge(y, line1[1]) and le(y, line1[3])) or (le(y, line1[1]) and ge(y, line1[3]))) and \
                ((ge(y, line2[1]) and le(y, line2[3])) or (le(y, line2[1]) and ge(y, line2[3]))):
                return (x, y, None, None)
            return (None, None, None, None)

        intersecting_points = []
        for line in lines1:
            for other_line in lines2:
                (x, y, x2, y2) = intersecting_point(line, other_line)
                if x is not None and y is not None and x2 is not None and y2 is not None:
                    intersecting_points.append((x, y))
                    intersecting_points.append((x2, y2))
                if x is not None and y is not None:
                    intersecting_points.append((x, y))

        points1 = []
        for idx in range(4):
            points1.append((self.nodes[idx].x, self.nodes[idx].y))
        points2 = []
        for idx in range(4):
            points2.append((box.nodes[idx].x, box.nodes[idx].y))

        def distance(p1, p2):
            return math.hypot(p1[0]-p2[0], p1[1]-p2[1])

        def triangle_area(a, b, c):
            side_a = distance(a, b)
            side_b = distance(b, c)
            side_c = distance(c, a)
            s = 0.5 * (side_a + side_b + side_c)
            area = math.sqrt(s * (s - side_a) * (s - side_b) * (s - side_c))
            return area

        def point_in_rectangle(point, rectangle_points):
            area1 = triangle_area(point, rectangle_points[0], rectangle_points[1])
            area2 = triangle_area(point, rectangle_points[1], rectangle_points[2])
            area3 = triangle_area(point, rectangle_points[2], rectangle_points[3])
            area4 = triangle_area(point, rectangle_points[3], rectangle_points[0])
            len1 = distance(rectangle_points[0], rectangle_points[1])
            len2 = distance(rectangle_points[1], rectangle_points[2])
            rectangle_area = len1 * len2
            return close_to(rectangle_area, area1 + area2 + area3 + area4)

        crossover_points = []
        for point in points1:
            if point_in_rectangle(point, points2):
                crossover_points.append(point)
        for point in points2:
            if point_in_rectangle(point, points1):
                crossover_points.append(point)

        total_points = intersecting_points + crossover_points
        new_total_points = []
        for point in total_points:
            duplicate = False
            for point2 in new_total_points:
                if close_to(point[0], point2[0]) and close_to(point[1], point2[1]):
                    duplicate = True
                    break
            if not duplicate:
                new_total_points.append(point)
        return new_total_points

def main():
    test()


def test():
    nodes = []
    nodes.append(Node(0, 0, 5))
    nodes.append(Node(0, 5, 5))
    nodes.append(Node(5, 5, 5))
    nodes.append(Node(5, 0, 5))
    nodes.append(Node(0, 0, 0))
    nodes.append(Node(0, 5, 0))
    nodes.append(Node(5, 5, 0))
    nodes.append(Node(5, 0, 0))

    nodes2 = []
    nodes2.append(Node(0, 0, 6))
    nodes2.append(Node(0, 4, 6))
    nodes2.append(Node(6, 4, 6))
    nodes2.append(Node(6, 0, 6))
    nodes2.append(Node(0, 0, 1))
    nodes2.append(Node(0, 4, 1))
    nodes2.append(Node(4, 6, 1))
    nodes2.append(Node(6, 0, 1))

    nodes3 = []
    nodes3.append(Node(1, 3.5, 6))
    nodes3.append(Node(3.5, 6, 6))
    nodes3.append(Node(6, 3.5, 6))
    nodes3.append(Node(3.5, 1, 6))
    nodes3.append(Node(1, 3.5, 1))
    nodes3.append(Node(3.5, 6, 1))
    nodes3.append(Node(6, 3.5, 1))
    nodes3.append(Node(3.5, 1, 1))

    nodes4 = []
    nodes4.append(Node(4, 5, 6))
    nodes4.append(Node(5, 6, 6))
    nodes4.append(Node(6, 5, 6))
    nodes4.append(Node(5, 4, 6))
    nodes4.append(Node(4, 5, 1))
    nodes4.append(Node(5, 6, 1))
    nodes4.append(Node(6, 5, 1))
    nodes4.append(Node(5, 4, 1))

    box = Box(nodes)
    box2 = Box(nodes2)
    print box.rectangle_intersection_with(box2)
    print box.height_intersection_with(box2)
    print box.intersect_with(box2)


if __name__ == '__main__':
    main()
