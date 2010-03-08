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
pygame.display.set_caption("Shadows Demo with PAdLib - Ian Mallett - 2008")
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

#Add the occluders.  Occluders are objects which block light
#This code adds an occluder for each black pixel
Occluders = []
for y in xrange(bg.get_height()):
    for x in xrange(bg.get_height()):
        color = bg.get_at((x,y))
        if color == (0,0,0,255):
            Occluders.append(pygame.Rect(x*16,y*16,16,16))

#Scale the background to the screensize, and convert it for speed
bg = pygame.transform.scale(bg,Screen)
bg.convert()

#Make the shadow object
s1 = Shadow(100,[1,1],Occluders,(180,180,180),200)
# - 100 is the radius of the light.
# - [1,1] is the light's position.  This is updated by change_position, below, but if
#   you won't update the position, set this to your light's position.
# - Occluders is a list of pygame.Rects representing the objects that can block light.
# - (180,180,180) is the light's color.
# - 200 is the opacity of the light.  255 = opaque.  0 = transparent.

#Main Loop
while True:
    #Get input
    get_input()
    #Get the mouse position
    mpos = pygame.mouse.get_pos()
    #Change the light's position to the mouse position
    s1.change_position(mpos)
    #Draw the background
    Surface.blit(bg,(0,0))
    #If the light is inside an occluder, it will cause artifacts.
    #So, test it, and don't draw it if it is inside an object.
    WillDrawShadow = True
    for o in Occluders:
        if o.collidepoint(mpos):
            WillDrawShadow = False
            break
    if WillDrawShadow:
        s1.draw(Surface)
    #Flip to the Screen
    pygame.display.flip()
