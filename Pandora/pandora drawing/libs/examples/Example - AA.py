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
pygame.display.set_caption("Anti-Aliasing Demo with PAdLib - Ian Mallett - 2008")
#make the window
Surface = pygame.display.set_mode(Screen)

#input function
def get_input():
    key = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == QUIT or key[K_ESCAPE]:
            pygame.quit(); sys.exit()

#load the background
bg = pygame.image.load("bg.png")
bg = pygame.transform.scale(bg,Screen)
bg.convert()

#Anti-Alias - can sometimes take a while.
bg = antialias(bg,2)
#You pass the surface to antialias(), and it
#returns the antialiased surface.  2 is the anti-alias level.
#Higher is more anti-aliasing.

#Main Loop
while True:
    #Get input
    get_input()
    #Draw the background
    Surface.blit(bg,(0,0))
    #Flip to the Screen
    pygame.display.flip()
