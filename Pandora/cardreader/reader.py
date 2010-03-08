import  pygame
from pygame.locals import *


screen = pygame.display.set_mode((640,480))


while 1:
    for event in pygame.event.get():
        print event
        

    pygame.display.update()