import random
import numpy as np
import warnings
from multiprocessing import Pool, cpu_count


class CircumferenceAndArea(object):
    """用于计算三角形周长和面积"""

    def __init__(self, a=0, b=0, c=0, bottom=0, high=0, pax=0, pbx=0, pcx=0, pay=0, pby=0, pcy=0, paz=0, pbz=0, pcz=0,
                 getparms=0, dimensionality=0,decimal=0):
        self.SidesA = a
        self.SidesB = b
        self.SidesC = c
        self.bottom = bottom
        self.high = high
        self.CoordinatePointAX = pax
        self.CoordinatePointBX = pbx
        self.CoordinatePointCX = pcx
        self.CoordinatePointAY = pay
        self.CoordinatePointBY = pby
        self.CoordinatePointCY = pcy
        self.CoordinatePointAZ = paz
        self.CoordinatePointBZ = pbz
        self.CoordinatePointCZ = pcz
        self.Getparms = getparms
        self.Dimensionality = dimensionality
        self.decimal = decimal

    def circumference(self):
        return np.round(self.SidesA + self.SidesB + self.SidesC, self.decimal)

    def distance_2d(self, x1, y1, x2, y2):
        return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    def distance_3d(self, x1, y1, z1, x2, y2, z2):
        return np.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)

    def circumference_points(self):
        if self.Dimensionality == 2:
            side_ab = self.distance_2d(self.CoordinatePointAX, self.CoordinatePointAY,
                            self.CoordinatePointBX, self.CoordinatePointBY)
            side_bc = self.distance_2d(self.CoordinatePointBX, self.CoordinatePointBY,
                            self.CoordinatePointCX, self.CoordinatePointCY)
            side_ca = self.distance_2d(self.CoordinatePointCX, self.CoordinatePointCY,
                            self.CoordinatePointAX, self.CoordinatePointAY)
            return np.round(side_ab + side_bc + side_ca, self.decimal)
        elif self.Dimensionality == 3:
            side_ab = self.distance_3d(self.CoordinatePointAX, self.CoordinatePointAY, self.CoordinatePointAZ,
                                self.CoordinatePointBX, self.CoordinatePointBY, self.CoordinatePointBZ)
            side_bc = self.distance_3d(self.CoordinatePointBX, self.CoordinatePointBY, self.CoordinatePointBZ,
                                self.CoordinatePointCX, self.CoordinatePointCY, self.CoordinatePointCZ)
            side_ca = self.distance_3d(self.CoordinatePointCX, self.CoordinatePointCY, self.CoordinatePointCZ,
                                self.CoordinatePointAX, self.CoordinatePointAY, self.CoordinatePointAZ)
            return np.round(side_ab + side_bc + side_ca, self.decimal)
        else:
            warnings.warn("Please enter whether it is 2D or 3D", SyntaxWarning)

    def area_is_bottom_high(self):
        return np.round(self.bottom * self.high * 0.5, self.decimal)

    def area_is_sides(self):
        p = (self.SidesA + self.SidesB + self.SidesC) * 0.5
        area = np.sqrt(p * (p - self.SidesA) * (p - self.SidesB) * (p - self.SidesC))
        return np.round(area, self.decimal)

    def area_is_planar_vector(self):
        vector_ab = np.array([self.CoordinatePointAX - self.CoordinatePointBX,
                              self.CoordinatePointAY - self.CoordinatePointBY])
        vector_ac = np.array([self.CoordinatePointAX - self.CoordinatePointCX,
                              self.CoordinatePointAY - self.CoordinatePointCY])
        area = 0.5 * np.abs(np.cross(vector_ab, vector_ac))
        return np.round(area, self.decimal)

    def area_is_spatial_vectors(self):
        vector_ab = np.array([self.CoordinatePointBX - self.CoordinatePointAX,
                              self.CoordinatePointBY - self.CoordinatePointAY,
                              self.CoordinatePointBZ - self.CoordinatePointAZ])
        vector_ac = np.array([self.CoordinatePointCX - self.CoordinatePointAX,
                              self.CoordinatePointCY - self.CoordinatePointAY,
                              self.CoordinatePointCZ - self.CoordinatePointAZ])
        area = 0.5 * np.linalg.norm(np.cross(vector_ab, vector_ac))
        return np.round(area, self.decimal)

class TriangleCentres(CircumferenceAndArea):
    """用于求三角形四心-平面-空间"""

    def centroid(self):
        points = np.array([
            [self.CoordinatePointAX, self.CoordinatePointAY, self.CoordinatePointAZ if self.Dimensionality == 3 else 0],
            [self.CoordinatePointBX, self.CoordinatePointBY, self.CoordinatePointBZ if self.Dimensionality == 3 else 0],
            [self.CoordinatePointCX, self.CoordinatePointCY, self.CoordinatePointCZ if self.Dimensionality == 3 else 0]
        ])

        if self.Dimensionality not in [2, 3]:
            warnings.warn("Please enter whether it is 2D or 3D", SyntaxWarning)
            return None

        centroid = np.mean(points[:, :self.Dimensionality], axis=0)

        return np.round(centroid, self.decimal)

    def incentre(self):
        if self.Dimensionality == 2:
            A = np.array([self.CoordinatePointAX, self.CoordinatePointAY])
            B = np.array([self.CoordinatePointBX, self.CoordinatePointBY])
            C = np.array([self.CoordinatePointCX, self.CoordinatePointCY])

            a = np.linalg.norm(B - C)
            b = np.linalg.norm(C - A)
            c = np.linalg.norm(A - B)

            planar_incentre = (a * A + b * B + c * C) / (a + b + c)
            return np.round(planar_incentre, self.decimal)

        elif self.Dimensionality == 3:
            A = np.array([self.CoordinatePointAX, self.CoordinatePointAY, self.CoordinatePointAZ])
            B = np.array([self.CoordinatePointBX, self.CoordinatePointBY, self.CoordinatePointBZ])
            C = np.array([self.CoordinatePointCX, self.CoordinatePointCY, self.CoordinatePointCZ])

            a = np.linalg.norm(B - C)
            b = np.linalg.norm(C - A)
            c = np.linalg.norm(A - B)

            spatial_incentre = (a * A + b * B + c * C) / (a + b + c)
            return np.round(spatial_incentre, self.decimal)

        else:
            warnings.warn("Please enter whether it is 2D or 3D", SyntaxWarning)

    def orthocentre(self):
        if self.Dimensionality == 2:
            A = np.array([self.CoordinatePointAX, self.CoordinatePointAY])
            B = np.array([self.CoordinatePointBX, self.CoordinatePointBY])
            C = np.array([self.CoordinatePointCX, self.CoordinatePointCY])

            AB = B - A
            AC = C - A
            BC = C - B

            a = np.dot(AB, AC)
            b = np.dot(-AB, -BC)
            c = np.dot(AC, -BC)
            d = np.dot(-AC, B - C)
            e = np.linalg.det([AB, BC, AC])

            if e == 0:
                warnings.warn("The points are collinear, cannot compute orthocentre.", RuntimeWarning)
                return None

            planar_orthocentre_x = (b + c) / e
            planar_orthocentre_y = (a + d) / e
            planar_orthocentre_xy = (planar_orthocentre_x, planar_orthocentre_y)
            return np.round(planar_orthocentre_xy, self.decimal)

        elif self.Dimensionality == 3:
            A = np.array([self.CoordinatePointAX, self.CoordinatePointAY, self.CoordinatePointAZ])
            B = np.array([self.CoordinatePointBX, self.CoordinatePointBY, self.CoordinatePointBZ])
            C = np.array([self.CoordinatePointCX, self.CoordinatePointCY, self.CoordinatePointCZ])

            AB = B - A
            AC = C - A
            BC = C - B

            a = np.dot(AB, AC)
            b = np.dot(-AB, -BC)
            c = np.dot(AC, -BC)
            denominator = b * c + a * c + a * b

            if denominator == 0:
                warnings.warn("The points are coplanar or not distinct, cannot compute orthocentre.", RuntimeWarning)
                return None

            spatial_orthocentre_x = (b * c * A[0] + a * c * B[0] + a * b * C[0]) / denominator
            spatial_orthocentre_y = (b * c * A[1] + a * c * B[1] + a * b * C[1]) / denominator
            spatial_orthocentre_z = (b * c * A[2] + a * c * B[2] + a * b * C[2]) / denominator
            spatial_orthocentre_xyz = (spatial_orthocentre_x, spatial_orthocentre_y, spatial_orthocentre_z)
            return np.round(spatial_orthocentre_xyz, self.decimal)

        else:
            warnings.warn("Please enter whether it is 2D or 3D", SyntaxWarning)

    def circumcentre(self):
        if self.Dimensionality == 2:
            A = np.array([self.CoordinatePointAX, self.CoordinatePointAY])
            B = np.array([self.CoordinatePointBX, self.CoordinatePointBY])
            C = np.array([self.CoordinatePointCX, self.CoordinatePointCY])

            AB = B - A
            AC = C - A
            BC = C - B

            a = np.dot(B, B) - np.dot(A, A)
            b = np.dot(C, C) - np.dot(B, B)

            fm = 2 * (AC[1] * AB[0] - AB[1] * AC[0])
            planar_circumcentre_x = (AC[1] * a - AB[1] * b) / fm
            planar_circumcentre_y = (AB[0] * b - AC[0] * a) / fm

            planar_circumcentre_xy = (planar_circumcentre_x, planar_circumcentre_y)

            return np.round(planar_circumcentre_xy, self.decimal)

        elif self.Dimensionality == 3:
            A = np.array([self.CoordinatePointAX, self.CoordinatePointAY, self.CoordinatePointAZ])
            B = np.array([self.CoordinatePointBX, self.CoordinatePointBY, self.CoordinatePointBZ])
            C = np.array([self.CoordinatePointCX, self.CoordinatePointCY, self.CoordinatePointCZ])

            AB = B - A
            AC = C - A
            BC = C - B

            a = np.dot(B, B) - np.dot(A, A)
            b = np.dot(C, C) - np.dot(B, B)
            c = np.dot(A, A) - np.dot(C, C)

            normal = np.cross(AB, AC)
            d = np.dot(normal, normal)

            if d != 0:
                planar_circumcentre_x = (np.dot(normal, np.cross(AC, [a, b, c])) / d)
                planar_circumcentre_y = (np.dot(normal, np.cross(BC, [a, b, c])) / d)
                planar_circumcentre_z = (np.dot(normal, np.cross(AB, [a, b, c])) / d)
                planar_circumcentre_xyz = (planar_circumcentre_x, planar_circumcentre_y, planar_circumcentre_z)
            else:
                planar_circumcentre_xyz = (float('nan'), float('nan'), float('nan'))

            return np.round(planar_circumcentre_xyz, self.decimal)
        
'''
费马点退火算法
'''

def distance(p1, p2):
    return np.linalg.norm(p1 - p2)


def total_distance(p, A, B, C):
    return distance(p, A) + distance(p, B) + distance(p, C)


def neighbor(point, scale=0.1):
    return point + np.random.uniform(-scale, scale, size=point.shape)


def acceptance_probability(old_cost, new_cost, temperature):
    return 1.0 if new_cost < old_cost else np.exp((old_cost - new_cost) / temperature)


def simulated_annealing(A, B, C, initial_point):
    current_point = initial_point
    current_cost = total_distance(current_point, A, B, C)

    T = 1.0
    T_min = 1e-9
    alpha = 0.999

    while T > T_min:
        new_point = neighbor(current_point)
        new_cost = total_distance(new_point, A, B, C)
        if acceptance_probability(current_cost, new_cost, T) > random.random():
            current_point = new_point
            current_cost = new_cost
        T *= alpha

    return current_point


class FermatProblem(CircumferenceAndArea):

    @staticmethod
    def run_simulated_annealing(args):
        A, B, C, initial_point = args
        return simulated_annealing(A, B, C, initial_point)

    def fermat_problem(self):

        if self.Dimensionality == 2:
            A = np.array([self.CoordinatePointAX, self.CoordinatePointAY])
            B = np.array([self.CoordinatePointBX, self.CoordinatePointBY])
            C = np.array([self.CoordinatePointCX, self.CoordinatePointCY])
        elif self.Dimensionality == 3:
            A = np.array([self.CoordinatePointAX, self.CoordinatePointAY, self.CoordinatePointAZ])
            B = np.array([self.CoordinatePointBX, self.CoordinatePointBY, self.CoordinatePointBZ])
            C = np.array([self.CoordinatePointCX, self.CoordinatePointCY, self.CoordinatePointCZ])
        else:
            warnings.warn("Please enter whether it is 2D or 3D", SyntaxWarning)

        num_processes = cpu_count()
        initial_points = [(A + B + C) / 3 for _ in range(num_processes)]
        args = [(A, B, C, initial_point) for initial_point in initial_points]

        with Pool(processes=num_processes) as pool:
            results = pool.map(FermatProblem.run_simulated_annealing, args)

        best_result = min(results, key=lambda p: total_distance(p, A, B, C))

        return np.round(best_result, self.decimal)


class NapoleonicTriangle(CircumferenceAndArea):
    def napoleonic_triangle(self):
        if self.Dimensionality == 2:
            p1 = np.array([self.CoordinatePointAX, self.CoordinatePointAY])
            p2 = np.array([self.CoordinatePointBX, self.CoordinatePointBY])
            p3 = np.array([self.CoordinatePointCX, self.CoordinatePointCY])

            def midpoint(p, q):
                return (p + q) / 2

            def perpendicular(p, q):
                direction = q - p
                return np.array([-direction[1], direction[0]])

            def line_intersection(a1, b1, a2, b2):
                A1 = b1[1] - a1[1]
                B1 = a1[0] - b1[0]
                C1 = A1 * a1[0] + B1 * a1[1]

                A2 = b2[1] - a2[1]
                B2 = a2[0] - b2[0]
                C2 = A2 * a2[0] + B2 * a2[1]

                determinant = A1 * B2 - A2 * B1
                if determinant == 0:
                    raise ValueError("Lines do not intersect")

                x = (B2 * C1 - B1 * C2) / determinant
                y = (A1 * C2 - A2 * C1) / determinant
                return np.array([x, y])

            m1 = midpoint(p1, p2)
            m2 = midpoint(p2, p3)
            m3 = midpoint(p3, p1)

            n1 = perpendicular(p1, p2)
            n2 = perpendicular(p2, p3)
            n3 = perpendicular(p3, p1)

            napoleon1 = line_intersection(m1, m1 + n1, m2, m2 + n2)
            napoleon2 = line_intersection(m2, m2 + n2, m3, m3 + n3)
            napoleon3 = line_intersection(m3, m3 + n3, m1, m1 + n1)

            napoleon_point = (napoleon1 + napoleon2 + napoleon3) / 3
        
        elif self.Dimensionality == 3:
            p1 = np.array([self.CoordinatePointAX, self.CoordinatePointAY, self.CoordinatePointAZ])
            p2 = np.array([self.CoordinatePointBX, self.CoordinatePointBY, self.CoordinatePointBZ])
            p3 = np.array([self.CoordinatePointCX, self.CoordinatePointCY, self.CoordinatePointCZ])
            def triangle_normal(p1, p2, p3):
                u = p2 - p1
                v = p3 - p1
                return np.cross(u, v)

            def plane_from_points(p1, p2, p3):
                normal = triangle_normal(p1, p2, p3)
                d = -np.dot(normal, p1)
                return normal, d

            def line_intersection(p1, d1, p2, d2):
                A1 = np.array([[d1[0], -d2[0]], [d1[1], -d2[1]], [d1[2], -d2[2]]])
                b = p2 - p1
                t = np.linalg.lstsq(A1, b, rcond=None)[0]
                return p1 + t[0] * d1

            mid1 = (p1 + p2) / 2
            mid2 = (p2 + p3) / 2
            mid3 = (p3 + p1) / 2

            normal1 = triangle_normal(p1, p2, p3)
            normal2 = triangle_normal(mid1, p1, p2)
            normal3 = triangle_normal(mid2, p2, p3)

            normal1 /= np.linalg.norm(normal1)
            normal2 /= np.linalg.norm(normal2)
            normal3 /= np.linalg.norm(normal3)

            plane1_normal, plane1_d = plane_from_points(mid1, p1, p2)
            plane2_normal, plane2_d = plane_from_points(mid2, p2, p3)
            plane3_normal, plane3_d = plane_from_points(mid3, p3, p1)

            intersection1 = line_intersection(mid1, plane1_normal, mid2, plane2_normal)
            intersection2 = line_intersection(mid2, plane2_normal, mid3, plane3_normal)
            intersection3 = line_intersection(mid3, plane3_normal, mid1, plane1_normal)

            napoleon_point = (intersection1 + intersection2 + intersection3) / 3

        return np.round(napoleon_point, self.decimal)
