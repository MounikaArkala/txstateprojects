

import pygame
from pygame.locals import *
import random, scaleslib
#import Numeric
from math import *

WIDTH = 800    #width of screen
HEIGHT = 480    #height of screen

import sc
import time, os
import scaleslib


def get_scale(note, intervals):
	scale = [note]
	val = note
	for i in intervals:
		val = (val + i) % 12
		scale.append(val)
	return scale

    
def main():
    pygame.display.init()
    
    screen = pygame.display.set_mode((WIDTH,HEIGHT),DOUBLEBUF,32)

        
    # we need to tell python where the scserver application lives, this
    # changes between platforms and systems. You might need to edit it.
    # exedir = 'usr/local' # where does scsynth live?
    # sc.start(exedir, verbose=1, spew=1 )

    sc.start()



    """
    player = sc.Synth( "StereoPlayer" )
    player.bufnum = sc.loadSnd( "numeros.wav", wait=True )

    print "loading bufnum with ID", player.bufnum

    time.sleep(5) # wait while sound plays
    sc.unloadSnd( player.bufnum )
    player.free()
    """

    #TODO: keep track of previous frequency/amplitude so we don't update it unnecessarily.
    pygame.display.update()
    done = False
    sine = sc.Synth( "sine" )
    intervals = scaleslib.scales["Blues Scale"][0]
    scale = get_scale(0, intervals)
    base_note = 440 #frequency of note referred to as "0", in this case, A.
    max_amp = 0.5
    sine.freq = 440
    octave_range = 3
    first_octave = - 1
    update = False
    oct_span = WIDTH / octave_range
    print "using scale:", scale
    
    """ create an image for background that colors out our scale."""
    surf = pygame.Surface((WIDTH, HEIGHT))
    for x in range(octave_range):
        print "x: ", x
        color = 1
        for i in range(12):
            print "i: ", i
            if i in scale:
                color += 1
                
            if color % 2 == 0:
                surf.fill((180,0,0),(x * oct_span + (i*oct_span / 12),0,oct_span/12,HEIGHT))
            else:
                surf.fill((0,180,0),(x * oct_span + (i*oct_span / 12),0,oct_span/12,HEIGHT))
                
    screen.blit(surf, (0,0))
    
    while not done:
        if update:
            x,y = pygame.mouse.get_pos()
            
            #we want our scale to span n octaves.
            octave = x / oct_span + first_octave
            
            #now we need to find out which note it is.
            #first get the absolute area
            note = x % oct_span
            #now get where the note is positioned in that area...
            notespacing = oct_span / 12.0
            actual_note = int(note / notespacing)
                        
            #some simple rounding, more sophisticated can be added later.
            #HACK!!! DO NOT LEAVE THIS IN HERE!
            target = 0
            for i in range(12):
                if i not in scale:
                    continue
                if i > actual_note:
                    break
                target = i
            
            print "Actual note: ", target
            print "octave: ", octave
            frequency = (2 ** ((target + (octave * 12)) / 12.0)) * base_note
            print frequency
            #set the frequency
            sine.freq = frequency
            
            #set volume to be based on Y coordinate.
            #first get vol on a scale of 0-1.
            vol = float(y) / HEIGHT
            # flip it so volume increases with height.
            vol = 1 - vol
            #now we possibly need to change y to a logarithmic scale for vol to sound right, not sure.
            
            #now use vol to modify max_amp to correct volume.
            sine.amp = max_amp * vol
        else:
            sine.amp = 0
        for e in pygame.event.get():
            if e.type == KEYDOWN:
                done = True
            elif e.type == MOUSEBUTTONDOWN:
                if e.button == 1:
                    update = True
                print e
            elif e.type == MOUSEBUTTONUP:
                if e.button == 1:
                    update = False
                        
        pygame.display.update()
        
    
    sine.free()
    sc.quit()
                
        
if __name__ == "__main__":
    main()
