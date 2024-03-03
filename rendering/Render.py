from maths.Triangle import Triangle
import pygame
import math
import sys
from rendering.RotationUtils import *
from rendering.Perspective import *
from maths.Vector import *

class Object:
    def __init__(self, obj_path, screen, rgb):
        self.camera = [0, 0, -150]
        self.points = {}
        self.raw_triangles = []
        self.triangles = []
        self.counter = 1
        self.projected_triangles = []
        self.rgb = rgb

        self.rotation_x = 0
        self.rotation_y = 0

        self.file_data = open(obj_path, "r")
        self.screen = screen

        for point in self.file_data.readlines():
            if point[0] == "v" :
                self.points[str(self.counter)] = [int(float(i) * 15) for i in point.replace("\n", "").replace("\t", "")[2:].split()]
                self.counter += 1
            elif point[0] == "f":
                self.raw_triangles.append(point.replace("\n", "").replace("\t", "")[2:].split(" "))

        x_center = round(sum([x for x, y, z in self.points.values()]) / len(self.points))
        y_center = round(sum([y for x, y, z in self.points.values()]) / len(self.points))
        z_center = round(sum([z for x, y, z in self.points.values()]) / len(self.points))

        x_offset = round(750/2) - x_center
        y_offset = round(750/2) - y_center
        z_offset = round(750/2) - z_center

        new_points = {}

        for i in self.points:
            x, y, z = self.points[i][0], self.points[i][1], self.points[i][2]
            new_points[i] = (x + x_offset, y + y_offset, z + z_offset)

        self.points = new_points 

        for triangle in self.raw_triangles:
            cur_tri = []
            for ref_point in triangle:
                cur_tri.append(self.points[ref_point])
            self.triangles.append(Triangle(cur_tri, rgb, triangle))

    def make_2d(self, point):
        return (point[0], point[1])
    def get_line(self, vert1, vert2):
        point_a = (vert1[0], vert1[1])

        point_b = (vert2[0], vert2[1])
        
        if point_a[0] == point_b[0] and point_a[1] == point_b[1]:
            return
        
        slope = 0
        intercept = point_a[1] - slope * point_a[0]
        if point_b[0] == point_a[0]:

            for i in range(min(point_a[1], point_b[1]), max(point_a[1], point_b[1])):
                self.screen.set_at((point_b[0], i), (0, 255, 255))
            return
        elif point_b[1] == point_a[1]:

            for i in range(min(point_a[0], point_b[0]), max(point_a[0], point_b[0]) + 1):
                self.screen.set_at((i, point_b[1]), (0, 255, 255))
            return
            
        else:
            slope = (point_b[1] - point_a[1]) / (point_b[0] - point_a[0])
        intercept = int(point_a[1] - slope * point_a[0])
    
        if abs(slope) < 1:
            for i in range(min(point_a[0], point_b[0]), max(point_a[0], point_b[0]) + 1):
                self.screen.set_at((i, int(i * slope) + intercept), (0, 255, 255))
        else:
            for i in range(min(point_a[1], point_b[1]), max(point_a[1], point_b[1])):
                self.screen.set_at((int((i - intercept) / slope), i), (0, 255, 255))    
    def draw_triangle(self, triangle):
        points = triangle.points
        points = points + [points[0]]

        for i in range(3):
            self.get_line(points[i], points[i + 1])

    def render(self, to_render="other"):
        proj_tris = []
        rotated_tris = rotate_x(self.rotation_x, self.triangles)
        rotated_tris = rotate_y(self.rotation_y, rotated_tris)

        triangles = sorted(rotated_tris, key=lambda tri: min(tri.points[0][2], tri.points[1][2], tri.points[2][2]), reverse=True)
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
            
            if normal.x * (triangle.points[0][0] - self.camera[0]) + normal.y * (triangle.points[0][1] - self.camera[1]) + normal.z * (triangle.points[0][2] - self.camera[2]) < 0:
                light_dir = Vector(0, 0, -1)
                l = (light_dir.x ** 2 + light_dir.y ** 2 + light_dir.z ** 2)
                if l != 0:
                    light_dir.x /= l
                    light_dir.y /= l
                    light_dir.z /= l

                color = [0, 0, 0]
                color[0] = max(0, min(255, self.rgb[0] * (normal.x * light_dir.x + normal.y * light_dir.y + normal.z * light_dir.z)))
                color[1] = max(0, min(255, self.rgb[1] * (normal.x * light_dir.x + normal.y * light_dir.y + normal.z * light_dir.z)))
                color[2] = max(0, min(255, self.rgb[2] * (normal.x * light_dir.x + normal.y * light_dir.y + normal.z * light_dir.z)))
       
                triangle.color = color
                
                new_points = []
                for point in triangle.points:
                    temp_point = (point[0], point[1], point[2] - self.camera[2])
                    temp_point = mult_mat_vector(temp_point)
                    new_point = [round(point) for point in temp_point]
                    
                    new_points.append(new_point)

                new_tri = Triangle(new_points, triangle.color, triangle.name)
                    
                triangle.points = new_points
                if to_render == "wire":
                    self.draw_triangle(new_tri)
                elif to_render == "obj":
                    pygame.draw.polygon(self.screen, triangle.color, (self.make_2d(new_points[0]), self.make_2d(new_points[1]), self.make_2d(new_points[2])))
                else:
                    pygame.draw.polygon(self.screen, triangle.color, (self.make_2d(new_points[0]), self.make_2d(new_points[1]), self.make_2d(new_points[2])))
                    #draw_triangle(triangle)

    def rotate_x(self, a):
        self.rotation_x = a
        
    def rotate_y(self, a):
        self.rotation_y = a
        
            
