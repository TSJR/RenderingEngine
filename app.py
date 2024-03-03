
import time
import pygame
from rendering.Render import Object

pygame.init()
screen = pygame.display.set_mode([750, 750])
screen_size = 750
screen.fill((255, 255, 255))
i = 0

object = Object("obj/house.obj", screen, (0, 255, 255))
dragging = False
origin = (0,0)
rot_x = 270
rot_y = 180

add_x = 0
add_y = 0

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not dragging:
                add_x = rot_x
                add_y = rot_y
                origin = pygame.mouse.get_pos()
            dragging = True
        if event.type == pygame.MOUSEBUTTONUP:
            dragging = False
        if event.type == pygame.MOUSEWHEEL:
            object.camera[2] += event.y * 7
       

    screen.fill((255, 255, 255))

    if dragging:
        rot_x = -(origin[1] - pygame.mouse.get_pos()[1]) / 5 + add_x
        rot_y = -(origin[0] - pygame.mouse.get_pos()[0]) / 5 + add_y
        
    object.rotate_x(rot_x)
    object.rotate_y(rot_y)

    object.render("both")
    pygame.display.flip()
    
    time.sleep(0.05)
    i += 5
    
pygame.quit()
