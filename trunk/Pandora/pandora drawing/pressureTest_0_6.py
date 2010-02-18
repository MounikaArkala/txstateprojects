"""
http://www.akeric.com/python/tablet/pressureTest_0_6.py
Eric Pavey - warpcat@sbcglobal.net - 2009-11-03
http://www.akeric.com/blog
Permission to use and modify given by author, as long as author is given credit.

Simple example of usage of the tablet_1_3.py module, for detecting tablet pressure
in pygame.  See tablet_1_3.py for more details.
Button 0 (LMB) draws white
Button 3 (RMB) draws black
"""
__version__ = "0.6"

import pygame
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
from tablet_1_3 import Tablet
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

pygame.init()

# CONSTANTS -----------------------------------------
# Used to change size of pressure based values (from 0->1023)
PRESSURMULT = .025

# Global vars: --------------------------------------
# Default window size:
width = 512
height = 512

def makeBackground(width, height):
    """
    Make our backround surface
    """
    background = pygame.surface.Surface((width, height))
    background.fill(pygame.Color("Black"))
    background = background.convert()
    return background

def main():
    """
    Simple Pygame to show off tablet pressure sensitivity.
    """
    # Pull in globals, since they can be modified due to screen resize
    global width
    global height

    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    pygame.display.set_caption("Pressure Test v%s"%__version__)
    background = makeBackground(width, height)
    screen.blit(background, (0,0))

    overlay = pygame.surface.Surface(screen.get_size(), flags=pygame.SRCALPHA, depth=32)
    overlay.convert_alpha()
    overlay.fill((0,0,0,0))

    #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
    # Make our Tablet object:
    tablet = Tablet()
    #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

    #---------------------------------------------------------------------------
    # Main loop:
    looping = True
    while looping:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                # allow for exit:
                looping = False
            # If the window is resized, update the Pygame screen, and update
            # the area of our tablet:
            if event.type == pygame.VIDEORESIZE:
                width, height = event.size
                screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                # Copy our old background, to apply that image to the new one:
                oldBg = background.copy()
                background = makeBackground(width, height)
                background.blit(oldBg, (0,0))

        overlay.fill((0,0,0,0))

        #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
        # Get our tablet data, and draw:
        pressure = tablet.getPressure()
        #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

        xPos, yPos = pygame.mouse.get_pos()
        #Turn our pressure into a reasonabliy sized radius value:
        radius = int(pressure * PRESSURMULT)

        # If user is pressing the button 0, or button 3, (LMB, RMB) draw:
        mouseButtons = pygame.mouse.get_pressed()
        if mouseButtons[0]:
            pygame.draw.circle(background, pygame.Color("white"), (xPos,yPos), radius)
        if mouseButtons[2]:
            pygame.draw.circle(background, pygame.Color("black"), (xPos,yPos), radius)

        # Draw our mouse pointer representation:
        pygame.draw.circle(overlay, pygame.Color("orange"), (xPos,yPos), radius)

        screen.blit(background, (0,0))
        screen.blit(overlay, (0,0))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
