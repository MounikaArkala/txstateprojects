#imports
import pygame
from pygame.locals import *
from padlib import *
import sys, os
import random

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
pygame.display.set_caption("Particles Demo with PAdLib - Ian Mallett - 2008")
#make the window
Surface = pygame.display.set_mode(Screen)

#input function
def get_input():
    key = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == QUIT or key[K_ESCAPE]:
            pygame.quit(); sys.exit()

#Define some parameters - see below
position = (0,0)
colors = [(255,0,0),(255,255,0),(0,255,0),(0,255,255),(0,0,255),(0,0,0)]
speeds = [1,4]
disperse = 360
direction = 0
density = 8
framestolast = 200
#Make the particle system object
p1 = particle_system(position,colors,speeds,disperse,direction,density,framestolast)
# - colors is a list of colors each particle will become.  In this case,
#   beginning with (255,0,0) and ending with (0,0,0).  The particle will
#   spend its lifetime as a color derived by its passage through this list.
#   If you wanted to have is stay a certain color, say, blue, longer than
#   green, you would call it twice so it would spend twice the time blue:
#   colors = [(0,0,255),(0,0,255),(0,255,0)]
# - speeds is the range of speeds each particle can have.  Each speed
#   component moves the particle 1/4 its integer value.  For example:
#   speeds = [1,4] so the pixels move (  1*(1/4), 4*(1/4)  ) = (1/4,1)
# - disperse is the angle, in degrees, through which the particle's
#   trajectory can deviate from the given direction.  In this case, it
#   is 360 degrees, meaning that the particles travel in all directions.
# - direction is the direction where the stream of particles is directed.
#   Here, the disperse is 360 degrees, so direction's effects are not
#   noticed.  direction = 0 makes the particles stream go right.
# - density is the measure of particles.  Naturally, higher means the
#   program will run more slowly.  density = 8 means that 8 new particles
#   are added to the particle system, and 8 old ones are thrown away each
#   frame.
# - framestolast is the number of frames each particle will exist.

#Define some more parameters for effects - again, see below
occluders = []
for number in xrange(4):
    x = random.randint(0,Screen[0]-64)
    y = random.randint(0,Screen[1]-64)
    occluders.append(pygame.Rect(x,y,64,64))
entropy = 0.5
gravity = (0.0,0.1)
randomness = 0.1
#Add effects
p1.set_occluders(occluders)
p1.set_bounce(entropy,randomness)
p1.set_gravity(gravity)
# - occluders is a list of rects each particle can bounce against.  One
#   can pass [] for there to be no collision detection again.  
# - entropy is the bounce factor.  None kills particles on collision.
# - randomness is a measure of how much the particles' bounce varies.
#   (Change this to 0.0 and you'll see why this might be desireable).
#   This number is the maximum deviation from the bounce entropy.  For
#   example, if randomness is 0.1 and entropy is 0.5, (as is the default
#   here), then the particles rebound factor will be in the range
#   [0.4, 0.6].  This only really does something if entropy != None.
# - gravity is a list or tuple of two numbers representing a gravity
#   vector.  (0,1) is straight down with a magnitude of 1.  (1,0) is
#   right with a magnitude of 1.  (1,1) is down and right with a
#   magnitude of 1.414.  None means no gravity.  A magnitude of 1 will
#   accelerate a particle 1 pixel/frame.  Generally speaking, such
#   accelerations are too strong for a game.  This example, for instance,
#   uses (0.0,0.1), one 1/10th as strong.  Pass None to deactivate.

#Main Loop
while True:
    #Get input
    get_input()

    #Get the mouse position
    mpos = pygame.mouse.get_pos()
    #Change the Particle System origin to the mouse position*
    p1.change_position(mpos)
    #Update all of the particles.
    p1.update()

    #Clear the Surface.
    Surface.fill((0,0,0))
    #Draw the Occluders as filled blue rects with grey borders.
    for o in occluders:
        pygame.draw.rect(Surface,(0,0,200),o,0)
        pygame.draw.rect(Surface,(200,200,200),o,1)
    #Draw the Particles
    p1.draw(Surface)
    #Flip to the Screen
    pygame.display.flip()
#*Note: There are other functions you can update, which are not used here.
#Here are all of the Particle System Functions:
#change_position (NewPosition)
#change_speed    (NewSpeedRange)
#change_disperse (NewDisperse)
#change_direction(NewDirection)
#change_density  (NewDensity)
#NewPosition   is a tuple or list of length 2.
#NewSpeedRange is a tuple or list of length 2.
#NewDisperse   is a float or integer.
#NewDirection  is a float or integer.
#NewDensity    is an integer.
