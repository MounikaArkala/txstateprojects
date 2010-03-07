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


from brushes import Brush



import colorpicker, config


from mathfuncs import lerp
from events import Register, DrawEvent, DrawAction

pygame.init()
width, height = config.width, config.height
if config.fullscreen:
    screen = pygame.display.set_mode((width,height), FULLSCREEN)
else:
    screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pandora Drawing Application Prototype")
canvas = pygame.Surface((width,height))
canvas.fill((255,255,255), (0,0,width,height))
screen.blit(canvas, (0,0))




if config.pressure:
    #set up our pressure support
    from tablet_1_3 import Tablet
    tablet = Tablet()

brushsize = config.default_brush_size
transparency = config.default_transparency

exit = False
mousedown = False
prevpos = (0,0)
prevpressure = 0

 
gradient, colors = colorpicker.colorpick(width,height)
state = 'drawing'
active = canvas

color = (0,0,0)
colorloc = (width/2, height)
colorloc_temp = colorloc

tool = "brush"
prevtool = "brush"

#we need to subclass Register so we can tell it how to draw our events on our canvas.


events = Register()


drawevent = None
end_event = False
starttime = time.time()
replaycanvas = None

if config.gamepad:
    pygame.joystick.init()
    x = pygame.joystick.Joystick(0)
    x.init()

exit = False
while not exit:
    for event in pygame.event.get():
        #TODO: make a State class and move all this state bull-crap out of here.
        if event.type == config.buttondown:
            if config.gamepad:
                val = event.button
            else:
                val = event.key
           
            if val == config.keys['colorpicker']:
                end_event = True
                if state != 'colorpicker':
                    state = 'colorpicker'
                else:
                    state = 'drawing' #they can press the button again to back out of the page.
                        
            elif val == config.keys['replay']:
                end_event = True
                if state != "replay":
                    state = "replay"
                else:
                    state = "drawing"
                    
            elif val == config.keys['eyedropper']:
                    end_event = True
                    
                    if state == "drawing":
                        if tool != "eyedropper":
                            prevtool = tool
                            tool = "eyedropper"
                        else:
                            tool = prevtool
                            #clear out the temporary canvas
                            eyedropcanvas = None
                    
            elif val == config.keys['exit']:
                pygame.quit()
                exit = True
                continue
                
            elif val == config.keys['cls']:
                #TODO: make this an event
                print "Cleared Screen."
                canvas.fill((255,255,255), (0,0,width,height))
            
            elif val == config.keys['size+']:
                brushsize = min(255, brushsize+1)
            elif val == config.keys['size-']:
                brushsize = max(1, brushsize-1)
            elif val == config.keys['trans+']:
                transparency = min(255, transparency+1)
            elif val == config.keys['trans-']:
                transparency = max(0, transparency-1)
            
            
                    
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                mousedown = True
                prevpos = (-1, -1)
                prevpressure = -1
                if state == "drawing":
                    drawevent = DrawEvent(time.time()-starttime, Brush(color, brushsize, 255))
                    end_event = False
                
                    
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                end_event = True
                mousedown = False
                
                if state == "colorpicker":
                    #switch back from colorpicker.
                    state = 'drawing'
                    #save state info when transitioning state.
                    colorloc = colorloc_temp
                
                
                
    if end_event and drawevent:
        events.add(drawevent)
        drawevent = None
        
        
    if state == 'drawing':
        active = canvas
        if mousedown:
            if tool == "eyedropper":
                eyedropcanvas = canvas.copy()
                color = eyedropcanvas.get_at(pygame.mouse.get_pos())
                x,y = pygame.mouse.get_pos()
                if y > 100:
                    y -= 50
                else:
                    y += 50
                if x > 100:
                    x -= 50
                else:
                    x += 50
                
                squareloc = (x, y, 100,100)
                pygame.draw.circle(eyedropcanvas, color, (x,y), 50)#gradient2.fill(color, squareloc)
                active = eyedropcanvas
                    
            else:
                currentpos = pygame.mouse.get_pos()
                if currentpos == prevpos:
                    continue
                if prevpos == (-1, -1):
                
                    try:
                        pressure = prevpressure = tablet.getPressure()
                    except:
                        pressure = prevpressure = config.default_pressure
                    
                    drawlocs = [(currentpos, pressure)]
                else:
                    #interpolate every point between prevpos and currentpos and draw at every point.
                    #interpolate the pressure too.
                    
                    try:
                        pressure = tablet.getPressure()
                    except:
                        pressure = config.default_pressure
                        
                    drawlocs = lerp(prevpos, currentpos, prevpressure, pressure)
                    prevpressure = pressure
                
                #print "startpos: ", prevpos, "endpos: ", currentpos
                
                #add in a draw action for each draw location in addition to drawing it.
                for pos in drawlocs:
                    if pos[1] < 60:
                        continue # small pressure values on my pad suck.
                    
                    if config.pressure_size:
                        radius = int(pos[1] * config.pressure_multiplier * brushsize)
                    else:
                        radius = brushsize
                        
                    if config.pressure_trans:
                        trans = min(pos[1] * config.pressure_multiplier * 10, 255)
                    else:
                        trans = transparency
                        
                    temp = (color[0], color[1], color[2], trans)
                        
                    pygame.gfxdraw.filled_circle(canvas, pos[0][0], pos[0][1], radius, temp)
                    pygame.gfxdraw.aacircle(canvas, pos[0][0], pos[0][1], radius, temp)
                    
                    #pygame.draw.circle(canvas, color, pos[0], radius)
                    drawevent.add(DrawAction(time.time()-drawevent.starttime , pos[0], pos[1]))
                
                prevpos = currentpos
        
    elif state == 'colorpicker':
        gradient2 = gradient.copy()
        active = gradient2
        pygame.draw.circle(gradient2, (255,255,255), colorloc, 8)
        pygame.draw.circle(gradient2, (255,0,0), colorloc, 6)
        if mousedown:
            color = gradient.get_at(pygame.mouse.get_pos()) #colors[pygame.mouse.get_pos()[0]][pygame.mouse.get_pos()[1]]
            colorloc_temp = pygame.mouse.get_pos()
            x,y = pygame.mouse.get_pos()
            if y > 100:
                y -= 50
            else:
                y += 50
            if x > 100:
                x -= 50
            else:
                x += 50
            
            squareloc = (x, y, 100,100)
            pygame.draw.circle(gradient2, color, (x,y), 50)#gradient2.fill(color, squareloc)
        
    elif state == 'brushes':
        brushsurf = pygame.Surface((0,0))
        if mousedown:
            print "clicked in brush mode!"
    
    elif state == 'replay':
        if not replaycanvas:
            replaycanvas = pygame.Surface((800, 480))
            replaycanvas.fill((255,255,255), (0,0,800,480))
            active = replaycanvas
        print "PLAYBACK:::"
        events.playone(active)
        time.sleep(.2)
        
        if events.done():
            events.reset()
            state = 'drawing'
            replaycanvas = None
    """
    elif state == 'replay2':
        replaycanvas = pygame.Surface((800, 480))
        replaycanvas.fill((255,255,255), (0,0,800,480))
        active = replaycanvas
        print "PLAYBACK:::FULL"
        events.playback(replaycanvas, screen)
        state = 'drawing'
    """
    
    if exit:
        continue
    screen.blit(active, (0,0))
    
    pygame.display.update()