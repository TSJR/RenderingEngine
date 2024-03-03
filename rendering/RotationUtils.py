import math
from maths.Triangle import Triangle

def rotate_y(a, tris):
    while a >= 360:
        a -= 360
    angle = math.radians(a)
    new_triangles = []
    for triangle in tris:
        new_points = []
        for point in triangle.points:
            x = point[0]
            z = point[2]
            new_x = (x - 375) * math.cos(angle) - (z - 375) * math.sin(angle) + 375
            new_z = (x - 375) * math.sin(angle) + (z - 375) * math.cos(angle) + 375
            new_points.append((round(new_x), point[1], round(new_z)))
        new_triangle = Triangle(new_points, triangle.color, triangle.name)
        new_triangles.append(new_triangle)
    return new_triangles

def rotate_x(a, tris):
    while a >= 360:
        a -= 360
    angle = math.radians(a)
    new_triangles = []
    for triangle in tris:
        new_points = []
        for point in triangle.points:
            y = point[1]
            z = point[2]
            new_y = (y - 375) * math.cos(angle) - (z - 375) * math.sin(angle) + 375
            new_z = (y - 375) * math.sin(angle) + (z - 375) * math.cos(angle) + 375
            new_points.append((point[0], round(new_y), round(new_z)))
        new_triangle = Triangle(new_points, triangle.color, triangle.name)
        new_triangles.append(new_triangle)
    return new_triangles
 
