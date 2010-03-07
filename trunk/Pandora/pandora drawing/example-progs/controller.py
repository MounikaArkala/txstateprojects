import pygame
from pygame.locals import *

screen = pygame.display.set_mode((640, 480))

pygame.joystick.init()
x = pygame.joystick.Joystick(0)
x.init()
while 1:
    
    #print x
    for event in pygame.event.get():
        print event
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.quit()
            continue

    pygame.display.update()