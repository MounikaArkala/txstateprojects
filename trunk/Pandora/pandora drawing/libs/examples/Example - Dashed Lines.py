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
pygame.display.set_caption("Dotted/Dashed Line Demo with PAdLib - Ian Mallett - 2008")
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
    #Get the mouse position
    mpos = pygame.mouse.get_pos()

    #Clear the Surface.
    Surface.fill((0,0,0))
    #Draw the Dotted Line
    DashedLine(Surface,(255,255,255),(0,0,255),mpos,(Screen[0]/2,Screen[1]/2),4)
    #Surface - Draw to this surface
    #(255,255,255) - one of the colors
    #(0,0,255) - the other color
    #mpos, (Screen[0]/2,Screen[1]/2) - Draw a dotted line from the mouse to the center of the screen
    #4 - this is the length of each dash.  (1 makes dots)

    #Draw some more dotted lines (Un-comment to see)
##    xdiff = (Screen[0]/2) - mpos[0]
##    ydiff = (Screen[1]/2) - mpos[1]
##    DottedLine(Surface,(255,255,255),(0,0,255),(Screen[0]/2+xdiff,mpos[1]),(Screen[0]/2,Screen[1]/2),4)
##    DottedLine(Surface,(255,255,255),(0,0,255),(Screen[0]/2+xdiff,Screen[1]/2+ydiff),(Screen[0]/2,Screen[1]/2),4)
##    DottedLine(Surface,(255,255,255),(0,0,255),(Screen[0]/2-xdiff,Screen[1]/2+ydiff),(Screen[0]/2,Screen[1]/2),4)
##
##    DottedLine(Surface,(255,255,255),(0,0,255),(Screen[0]/2-xdiff,Screen[1]/2),(Screen[0]/2,Screen[1]/2),4)
##    DottedLine(Surface,(255,255,255),(0,0,255),(Screen[0]/2+xdiff,Screen[1]/2),(Screen[0]/2,Screen[1]/2),4)
##    DottedLine(Surface,(255,255,255),(0,0,255),(Screen[0]/2,Screen[1]/2+ydiff),(Screen[0]/2,Screen[1]/2),4)
##    DottedLine(Surface,(255,255,255),(0,0,255),(Screen[0]/2,Screen[1]/2-ydiff),(Screen[0]/2,Screen[1]/2),4)
    
    #Flip to the Screen
    pygame.display.flip()
