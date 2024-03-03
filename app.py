
import time
import pygame
from rendering.Render import Object

pygame.init()
screen = pygame.display.set_mode([750, 750])
screen_size = 750
screen.fill((255, 255, 255))
i = 0

object = Object("obj/tinker.obj", screen)
object.draw()

object.rotate_x(270)

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill((255, 255, 255))
    
    object.rotate_y(i)
    object.rotate_x(i / 2) 
    object.render("both")
    pygame.display.flip()
    
    time.sleep(0.05)
    i += 5
    
pygame.quit()
