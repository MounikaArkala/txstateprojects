#!/usr/bin/env python

"""Python sample code to play sound.Taken from the pygame examples"""

import os.path
import pygame.mixer, pygame.time
mixer = pygame.mixer
time = pygame.time

#choose a desired audio format
mixer.init(11025) #raises exception on fail


#load the sound    
file = os.path.join('data', 'first.ogg')
sound = mixer.Sound(file)


#start playing
print 'Playing Sound...'
channel = sound.play()


#poll until finished
while channel.get_busy(): #still playing
    print '  ...still going...'
    time.wait(1000)
print '...Finished'



