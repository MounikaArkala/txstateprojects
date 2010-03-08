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
pygame.display.set_caption("Anti-Aliased Circle Demo with PAdLib - Ian Mallett - 2008")
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
    
    #Draw the Circle - This function is still rather slow.
    aacircle(Surface,(0,0,255),(Screen[0]/2,Screen[1]/2),100,4,0)
    #Surface - Draw to this surface
    #(0,0,255) - The circle is blue
    #(Screen[0]/2,Screen[1]/2) - Draw to the center of the screen
    #100 - Circle's Radius
    #2 - antialias level: more take longer
    #0 - width (0 = filled)
    
    #Flip to the Screen
    pygame.display.flip()
