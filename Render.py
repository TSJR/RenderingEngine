from Triangle import Triangle
import pygame
import math
import sys
from RotationUtils import *
from Perspective import *
from Vector import *

pygame.init()
screen = pygame.display.set_mode([750, 750])
screen_size = 750
screen.fill((255, 255, 255))
f = open(sys.argv[1] if len(sys.argv) > 1 else "tinker.obj", "r")

camera = [0, 0, -150]

points = {}
raw_triangles = []
triangles = []
counter = 1


for point in f.readlines():
    if point[0] == "v" :
        points[str(counter)] = [int(float(i) * 15) for i in point.replace("\n", "").replace("\t", "")[2:].split()]
        counter += 1
    elif point[0] == "f":
        raw_triangles.append(point.replace("\n", "").replace("\t", "")[2:].split(" "))


x_center = round(sum([x for x, y, z in points.values()]) / len(points))
y_center = round(sum([y for x, y, z in points.values()]) / len(points))
z_center = round(sum([z for x, y, z in points.values()]) / len(points))

#center = (center_x, center_y, center_z)

x_offset = round(750/2) - x_center
y_offset = round(750/2) - y_center
z_offset = round(750/2) - z_center

new_points = {}

for i in points:
    x, y, z = points[i][0], points[i][1], points[i][2]
    new_points[i] = (x + x_offset, y + y_offset, z + z_offset)

points = new_points 

def make_2d(point):
    return (point[0], point[1])

def get_line(vert1, vert2):
    point_a = (vert1[0], vert1[1])

    point_b = (vert2[0], vert2[1])
    

    if point_a[0] == point_b[0] and point_a[1] == point_b[1]:
        return
    
    slope = 0
    intercept = point_a[1] - slope * point_a[0]
    if point_b[0] == point_a[0]:

        for i in range(min(point_a[1], point_b[1]), max(point_a[1], point_b[1])):
            screen.set_at((point_b[0], i), (0, 255, 255))
        return
    elif point_b[1] == point_a[1]:

        for i in range(min(point_a[0], point_b[0]), max(point_a[0], point_b[0]) + 1):
            screen.set_at((i, point_b[1]), (0, 255, 255))
        return
        
    else:
        slope = (point_b[1] - point_a[1]) / (point_b[0] - point_a[0])
    intercept = int(point_a[1] - slope * point_a[0])
 
    if abs(slope) < 1:
        for i in range(min(point_a[0], point_b[0]), max(point_a[0], point_b[0]) + 1):
            screen.set_at((i, int(i * slope) + intercept), (0, 255, 255))
    else:
        for i in range(min(point_a[1], point_b[1]), max(point_a[1], point_b[1])):
            screen.set_at((int((i - intercept) / slope), i), (0, 255, 255))    

for triangle in raw_triangles:
    cur_tri = []
    for ref_point in triangle:
        cur_tri.append(points[ref_point])
    triangles.append(Triangle(cur_tri, (0, 0, 0), triangle))


def draw_triangle(triangle):
    points = triangle.points
    points = points + [points[0]]

    for i in range(3):
        get_line(points[i], points[i + 1])

def render(triangles, to_render="other"):
    proj_tris = []
    triangles = sorted(triangles, key=lambda tri: min(tri.points[0][2], tri.points[1][2], tri.points[2][2]), reverse=True)
    for triangle in triangles:
        triangle.points[0] = (triangle.points[0][0] - 375, triangle.points[0][1] - 375, triangle.points[0][2])
        triangle.points[1] = (triangle.points[1][0] - 375, triangle.points[1][1] - 375, triangle.points[1][2])
        triangle.points[2] = (triangle.points[2][0] - 375, triangle.points[2][1] - 375, triangle.points[2][2])
  
        
        line1 = [0, 0, 0]
        line2 = [0, 0, 0]
        normal = [0, 0, 0]

        line1 = Vector(
            triangle.points[1][0] - triangle.points[0][0],
            triangle.points[1][1] - triangle.points[0][1],
            triangle.points[1][2] - triangle.points[0][2]
        )

        line2 = Vector(
            triangle.points[2][0] - triangle.points[0][0],
            triangle.points[2][1] - triangle.points[0][1],
            triangle.points[2][2] - triangle.points[0][2]
        )

        normal = Vector(
            line1.y * line2.z - line1.z * line2.y,
            line1.z * line2.x - line1.x * line2.z,
            line1.x * line2.y - line1.y * line2.x
        )

        
        l = math.sqrt(normal.x ** 2 + normal.y ** 2 + normal.z ** 2)
        if l != 0:
            normal.x /= l
            normal.y /= l
            normal.z /= l
        
        if normal.x * (triangle.points[0][0] - camera[0]) + normal.y * (triangle.points[0][1] - camera[1]) + normal.z * (triangle.points[0][2] - camera[2]) < 0:
            
            light_dir = Vector(0, 0, -1)
            l = (light_dir.x ** 2 + light_dir.y ** 2 + light_dir.z ** 2)
            if l != 0:
                light_dir.x /= l
                light_dir.y /= l
                light_dir.z /= l

            color = 255 * (normal.x * light_dir.x + normal.y * light_dir.y + normal.z * light_dir.z) - 5
            print("color", color)
            if color < 255 and color > 0:
                triangle.color = (color, color, color)
            
            new_points = []
            for point in triangle.points:
                
                temp_point = (point[0], point[1], point[2] - camera[2])
                temp_point = mult_mat_vector(temp_point)
                new_point = [round(point) for point in temp_point]
                
                new_points.append(new_point)

            new_tri = Triangle(new_points, triangle.color, triangle.name)
                
            triangle.points = new_points
            if to_render == "wire":
                draw_triangle(new_tri)
            elif to_render == "obj":
                pygame.draw.polygon(screen, triangle.color, (make_2d(new_points[0]), make_2d(new_points[1]), make_2d(new_points[2])))
            else:
                pygame.draw.polygon(screen, triangle.color, (make_2d(new_points[0]), make_2d(new_points[1]), make_2d(new_points[2])))
                #draw_triangle(triangle)
        

done = False
import time

projected = rotate_x(270, triangles)
i = 0
while not done:
    
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill((255, 255, 255))
    
    tris = rotate_y(i, projected)
    tris = rotate_x(i / 2, tris) 
    render(tris, sys.argv[2] if len(sys.argv) > 2 else "both")
    pygame.display.flip()
    
    
    time.sleep(0.05)
    i += 5
    
pygame.quit()
