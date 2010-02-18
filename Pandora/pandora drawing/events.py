#import brushes
import pygame
import config, time
from mathfuncs import lerp
#TODO: do lerp'ing of the opacity and the brush size too.

class Register(object):#TODO: inherit from List so you don't have to have an 'add' method, you can just use 'append'.
    
    def __init__(self):
        self.events = []
        self.index = 0
        
    def add(self, event):
        self.events.append(event)
    
    def done(self):
        if self.index == len(self.events):
            return True
        return False
    def reset(self):
        self.index = 0
        
    def playback(self, targetsurf, screen):
        print "Playing back all events in real time (original time)."
        playbacktime = time.time()
        self.index = 0
        while 1:
            if self.done():
                break
            #wait until the appropriate time and then issue the item to run.
            if time.time() - playbacktime >= self.events[self.index].starttime:
                self.events[self.index].run(targetsurf)
                self.index += 1
            else:
                time.sleep(.02)
                
            screen.blit(targetsurf, (0,0))
            pygame.display.update()
            #then it will run and when it's done then we're ready for the next event.
            #remember events are completely linear (none can occur simultaneously with other events)
            # so this is fine.
    
    def playone(self, targetsurf):
        #play an event onto a surface.
        try:
            self.events[self.index].run(targetsurf)
        except:
            self.index = 0 # TODO: decide what to do here.
        self.index += 1

class Event(object):
    """ an event is a series of actions that starts at absolute time starttime (absolute to the beginning of the program.)
        each action is an event that occurs at a time relative to the event time and the end of an event is when it exhausts all actions.
        an event should have a Brush object associated with it."""
    def __init__(self, type, starttime, brush):
        self.actions = []
        self.type = type
        self.starttime = starttime
        self.brush = brush
        
    def add(self, action):
        self.actions.append(action)
        
    def run(self):
        pass
        
class DrawEvent(Event):
    def __init__(self, starttime, brush):
        super(DrawEvent, self).__init__('draw', starttime, brush)
        
    def run(self, targetsurf):
        if len(self.actions) <= 0:
            print "Empty Event!"
            return
        prevpos = self.actions[0].location
        prevpressure = self.actions[0].pressure
        #for every DrawAction in our self.actions we need to draw it to our parent surface.
        for action in self.actions[1:]:
            currentpos = action.location                
            #interpolate every point between prevpos and currentpos and draw at every point.
            #interpolate the pressure too.
            pressure = action.pressure
            drawlocs = lerp(prevpos, currentpos, prevpressure, pressure)
            prevpressure = pressure
            
            for pos in drawlocs:
                radius = self.brush.radius * pos[1] * config.pressure_multiplier
                pygame.draw.circle(targetsurf, self.brush.color, pos[0], radius)
                prevpos = currentpos
            #just ignore starttime for now and just draw at the location.


class ClearEvent(Event):
    def __init__(self, starttime, brush):
        super(DrawEvent, self).__init__('draw', starttime, brush)
        
    def run(self, targetsurf):
        targetsurf.fill(self.brush.color, (0,0,targetsurf.get_width(), targetsurf.get_height()))
        
class DrawAction(object):
    def __init__(self, starttime, location, pressure):
        self.starttime = starttime #relative to start of event.
        self.location = location   #currently in absolute screen coords, eventually will be in canvas coords.
        self.pressure = pressure