# -*- coding: utf-8 -*-

# *** THIS CLASS IS PUBLIC DOMAIN ***
# Made by John Eriksson in 2009
# http://arainyday.se

import pygame
from pygame.locals import *
from lib.loader import Loader

from lib.PaintBrush import PaintBrush
                       
class SimpleDemo(object):
    
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600),1)
        pygame.display.set_caption("PaintBrush simple demo v1.0 - Press space to clear paper")
        
        loader = Loader()
                        
        self.brush = PaintBrush(self.screen)
        self.brush.set_brush(loader.load_image("brush_6.png", True))
        self.brush.set_follow_angle(True)
        self.brush.set_color(pygame.Color("Blue"))
        self.brush.set_alpha(0.2)

        self.screen.fill((255,255,255))
                        
    def main_loop(self):                    
        next_update = pygame.time.get_ticks()
        while 1:            
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return                    
                    elif event.key == K_SPACE:
                        self.screen.fill((255,255,255))
                            
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.brush.paint_from(event.pos)
                elif event.type == MOUSEMOTION:
                    if event.buttons[0]:
                        self.brush.paint_to(event.pos)                        
                                                          
            if pygame.time.get_ticks() >= next_update:
                next_update+=33                
                pygame.display.flip()            

def main():
    try:
        import psyco
        psyco.full()
    except ImportError:
        pass

    pygame.init()

    g = SimpleDemo()
    g.main_loop()
 
if __name__ == '__main__': 
    main()


