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
pygame.display.set_caption("Particle/Shadow Demo with PAdLib - Ian Mallett - 2008")
#make the window
Surface = pygame.display.set_mode(Screen)

#input function
def get_input():
    key = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == QUIT or key[K_ESCAPE]:
            pygame.quit(); sys.exit()

#Make the particle system object
position = (0,0)
colors = [(255,0,0),(255,255,0),(0,255,0),(0,255,255),(0,0,255),(0,0,0)]
speeds = [1,2]
disperse = 360
direction = 0
density = 2
framestolast = 200
p1 = particle_system(position,colors,speeds,disperse,direction,density,framestolast)

#Main Loop
while True:
    #Get input
    get_input()
    #Get the mouse position
    mpos = pygame.mouse.get_pos()
    #Re-make the shadow object each frame, leaving out the particles
    #at the mouse point.  (Remember, those cause artifacts).
    Occluders = []
    for p in p1.particles:
        pos = (p[0][0],p[0][1])
        if abs(pos[0]-mpos[0]) >= 2 and abs(pos[1]-mpos[1]) >= 2:
            Occluders.append(pygame.Rect(pos,(1,1)))
    s1 = Shadow(min([Screen[0]/2,Screen[1]/2]),[Screen[0]/2,Screen[1]/2],Occluders,(180,180,180),200)
    #Change the light and particle system position to the mouse position
    p1.change_position(mpos)
    #Update all of the particles.
    p1.update()
    #Clear the Screen
    Surface.fill((0,0,0))
    #Draw the Particles and Shadows
    p1.draw(Surface)
    s1.draw(Surface)
    #Draw a Small Circle at the Light's Position.
    pygame.draw.circle(Surface,(255,255,255),(Screen[0]/2,Screen[1]/2),2)
    #Flip to the Screen
    pygame.display.flip()
