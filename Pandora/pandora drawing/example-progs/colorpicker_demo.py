
import pygame
from pygame.locals import *

screen = pygame.display.set_mode((800,480))

screen.fill((0,244,0), (0,0,800,480))
from colorpicker import colorpick

exit = False
drawing = False


prevpos = (0,0)
width = 800
height = 480
gradient, colors = colorpick(width, height)

#print colors
clicked = False
while not exit:
    
    screen.blit(gradient, (800-width,480-height))
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                exit = True
                continue
                
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                clicked = True
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                clicked = False
                
    if clicked:
        color = colors[pygame.mouse.get_pos()[0]][pygame.mouse.get_pos()[1]]
        screen.fill(color, (0,0,40,40))
    
    if exit:
        continue
    
 
    pygame.display.update()