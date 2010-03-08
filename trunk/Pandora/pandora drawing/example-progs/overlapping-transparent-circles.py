#License: GPL v3 @ Luke Paireepinart

#replay mechanism: basically have a "Draw Event" that stores every "Draw Action" which is just mousepos and timestamp anytime the mousepos changes.
#Draw Action timestamps are relative to Draw Event, that is, they start at 0 as the draw event occurs.
# draw event timestamp is relative to when the drawing was started.

#that way the replay can be either of 3 ways, it can be based on draw events,  so it's exactly how they drew it originally,
# or it can draw the draw actions at a steady pace, or it can draw the events at a steady pace (so if the person drew in a whole cloud with one draw event then it'd appear at once.)
# and you can adjust the speed of either way, accordingly.

#the replay mechanism can just playback exactly how the drawing works, just disable their mouse input.



#useful features (after version 1.0):
# - have the brush rotate to follow cursor (align to slope).

#TODO: Clear Screen event should be logged.
#TODO: if they leave mouse in same spot but push harder then will it get updated?

import pygame, math, time
from pygame.locals import *

import pygame.gfxdraw #SUPPOSEDLY this is experimental and will break.

from mathfuncs import lerp

pygame.init()
width, height = 800, 480

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pandora Drawing Application Prototype")
canvas = pygame.Surface((width,height))
canvas.fill((255,255,255), (0,0,width,height))
screen.blit(canvas, (0,0))


exit = False
while not exit:
    for event in pygame.event.get():
        #TODO: make a State class and move all this state bull-crap out of here.
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.exit()
                
                
    canvas.fill((255,255,255), (0,0,width,height))
    prevpos = (100,100)
    currentpos = (150, 240)
    drawlocs = lerp(prevpos, currentpos, 1, 5)
    #print drawlocs
    drawlocs = [((100,100),1), ((150,100),1)]
    for pos in drawlocs:
        
        radius = 30
        trans = 100
            
        temp = (128,128,33, 200)
        #tempsurf = pygame.Surface((radius*2, radius*2), flags=SRCALPHA|BLEND_RGBA_MULT)
        tempsurf = pygame.Surface((radius*2, radius*2))
        tempsurf.fill((0,0,0,0))
        #tempsurf.fill((0,255,0))
        #tempsurf.set_colorkey((0,255,0))
        #tempsurf.set_alpha(100)
        tempsurf.convert_alpha()
        #pygame.draw.circle(tempsurf, temp, (radius, radius), radius)
        pygame.gfxdraw.filled_circle(tempsurf, radius, radius, radius, temp)
        pygame.gfxdraw.aacircle(tempsurf, radius, radius, radius-1, temp)
        #canvas.blit(tempsurf, (pos[0][0], pos[0][1]), special_flags=BLEND_RGB_MULT)
        canvas.blit(tempsurf, (pos[0][0], pos[0][1]))
                
  
    screen.blit(canvas, (0,0))
    
    pygame.display.update()