

import pygame
from pygame.locals import *
import random, scaleslib
#import Numeric
from math import *

WIDTH = 800    #width of screen
HEIGHT = 480    #height of screen

import sc
import time, os



    
def main():
    pygame.display.init()
    
    screen = pygame.display.set_mode((WIDTH,HEIGHT),DOUBLEBUF,32)

        
    # we need to tell python where the scserver application lives, this
    # changes between platforms and systems. You might need to edit it.
    # exedir = 'usr/local' # where does scsynth live?
    # sc.start(exedir, verbose=1, spew=1 )

    sc.start()

    player = sc.Synth( "StereoPlayer" )

    player.bufnum = sc.loadSnd( "numeros.wav", wait=True )

    print "loading bufnum with ID", player.bufnum

    time.sleep(5) # wait while sound plays

    sc.unloadSnd( player.bufnum )
    player.free()
    sc.quit()

    print 'quiting'


        
    pygame.display.update()
    done = False
    while not done:
        for e in pygame.event.get():
            if e.type == KEYDOWN:
                done = True
        
if __name__ == "__main__":
    main()
