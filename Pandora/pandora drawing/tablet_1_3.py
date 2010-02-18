"""
http://www.akeric.com/python/tablet/tablet.py
Eric Pavey - warpcat@sbcglobal.net - 2009-10-17
http://www.akeric.com/blog
Permission to use and modify given by author, as long as author is given credit.

Allows for pressure sensitivity detection of tablets for use in PyGame.
http://www.pygame.org

*Windows only*, due to usage of the "Python Computer Graphics Kit" and it's hooks
into wintab:
http://cgkit.sourceforge.net
http://cgkit.sourceforge.net/doc2/wintab.html

Tested on WinXP, using Wacom Bamboo.
See http://www.akeric.com/python/tablet/pressureTest_0_3.py for simple PyGame example usage.

Updates:
    * v1.3 : Simplified:  Realized that Pygame can already track position
        and button press information.  All this system now returns is
        tablet pressure.  Easily modifiable to do more, but that's what it
        does by default.
"""
__version__ = '1.3'

import sys

from cgkit import wintab
from cgkit.wintab.constants import *

import pygame

class Tablet(object):
    """
    Tablet object for use in PyGame, for capturing tablet pressure.
    Position and button press can be captured via mouse calls in Pygame.
    """

    def __init__(self):
        """
        Build our Tablet object, which is Pygames interface into the world
        of tablet pressure sensiviity.
        """
        if "win" not in sys.platform:
            raise Exception("Tablet is only spported in Windows OS")

        # This is the 'window id' for the current Pygame window
        self.hwnd = pygame.display.get_wm_info()["window"]

        self.context = wintab.Context()
        # Define the type of data we want the Packets to return.  In this
        # case, it's just the pressure, since buttons and position can be
        # captured from Pygame directly.
        #self.context.pktdata = (PK_X | PK_Y | PK_BUTTONS | PK_NORMAL_PRESSURE)
        self.context.pktdata = (PK_NORMAL_PRESSURE)

        # If this isn't set, it will map the whole tablet into the extents
        # of the pygame display, which may not be desirable.
        self.context.options = CXO_SYSTEM
        self.context.open(self.hwnd, True)

        self.prevPressure = 0


    def getPressure(self):
        """
        Can be called to every Pygame loop to capture the tablet pressure info.

        return : int : Pressure is mapped from 0->1023
        """
        packetExtents = self.context.queuePacketsEx()
        if packetExtents[1] is not None:
            # This is a sub-list of Packet objects:
            packets = self.context.packetsGet(packetExtents[1])
            # Get the last Packet object:
            packet = packets[-1]

            # Capture pressure data:
            pressure = packet.normalpressure

            # Fill our "previous" values in case the user takes the pen away
            # from the PyGame screen:
            self.prevPressure = pressure
            return pressure
        else:
            return self.prevPressure