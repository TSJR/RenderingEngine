import math
from maths.Vector import Vector

mat_proj = []
for i in range(4):
    row = []
    for j in range(4):
        row.append(0)
    mat_proj.append(row)

def mult_mat_vector(temp):
    vector = Vector(temp[0], temp[1], temp[2])
    
    near = 0.1
    far = 1000
    fov = 90.0
    aspect_ratio = 1.0
    fov_rad = math.tan(math.radians(fov * 0.5))

    mat_proj[0][0] = aspect_ratio * fov_rad
    mat_proj[1][1] = fov_rad
    mat_proj[2][2] = far / (far - near)
    mat_proj[3][2] = (-far * near) / (far - near)
    mat_proj[2][3] = 1.0
    mat_proj[3][3] = 0.0


    matrix = mat_proj
    new_vector = [0, 0, 0]
    if vector.z < 0 or vector.x < 0 or vector.y < 0:

        pass#print(vector.x, vector.y, vector.z)
    
    new_vector[0] = vector.x * matrix[0][0] + -vector.y * matrix[1][0] + vector.z * matrix[2][0] + matrix[3][0]
    new_vector[1] = vector.x * matrix[0][1] + -vector.y * matrix[1][1] + vector.z * matrix[2][1] + matrix[3][1]
    new_vector[2] = vector.x * matrix[0][2] + -vector.y * matrix[1][2] + vector.z * matrix[2][2] + matrix[3][2]

    
    w = vector.x * matrix[0][3] + vector.y * matrix[1][3] + vector.z * matrix[2][3] + matrix[3][3]
    if w != 0:
        new_vector[0] /= w
        new_vector[1] /= w
        new_vector[2] /= w
    new_vector[0] += 1
    new_vector[1] += 1
    new_vector[0] *= 375
    new_vector[1] *= 375
    #new_vector[2] *= 100


    return new_vector
    

