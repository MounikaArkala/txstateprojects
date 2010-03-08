#imports
import pygame
from pygame.locals import *
from padlib import *
import sys, os

#Center the screen
if sys.platform == 'win32' or sys.platform == 'win64':
    os.environ['SDL_VIDEO_CENTERED'] = '1'

#Initialise PyGame
pygame.init()

#Screen size
Screen = (512,512)

#Set the display icon
icon = pygame.Surface((1,1)); icon.set_alpha(0); pygame.display.set_icon(icon)
#Set the display caption
pygame.display.set_caption("Rounded Rectangles Demo with PAdLib - Ian Mallett - 2008")
#make the window
Surface = pygame.display.set_mode(Screen)

#input function
def get_input():
    key = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == QUIT or key[K_ESCAPE]:
            pygame.quit(); sys.exit()

#Main Loop
while True:
    #Get input
    get_input()

    #Draw some Rounded Rectangles
    #surface, color, rect, rounded_edge_size, width_of_edge=0
    RoundedRect(Surface,(0,255,0),(10,10,200,200),31)
    RoundedRect(Surface,(255,0,255),(230,80,250,300),18,2)
    RoundedRect(Surface,(0,0,255),(20,220,200,200),11,4)
    RoundedRect(Surface,(255,0,0),(40,430,350,64),18,3)

    #Flip to the Screen
    pygame.display.flip()
