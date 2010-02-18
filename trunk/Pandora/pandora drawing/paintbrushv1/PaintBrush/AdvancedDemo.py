# -*- coding: utf-8 -*-

# *** THIS CLASS IS PUBLIC DOMAIN ***
# Made by John Eriksson in 2009
# http://arainyday.se

import pygame
from pygame.locals import *
from lib.loader import Loader

from lib.PaintBrush import PaintBrush
                       
class AdvancedDemo(object):
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600),1)
        pygame.display.set_caption("PaintBrush advanced demo v1.1")
        
        self.loader = Loader()
        
        self.simple_pal = self.loader.load_image("simple.png",False)
        self.advanced_pal = self.loader.load_image("advanced.png",False)
        self.simple = True
        
        self.knob = self.loader.load_image("knob.png",True)
        self.knob_rect = self.knob.get_rect()
        self.knob_rect.topleft = (14,215)
        
        self.back = self.loader.load_image("back.png", False)

        self.help = self.loader.load_image("help.png", True)
                        
        self.b1 = self.loader.load_image("brush_1.png", True) 
        self.b2 = self.loader.load_image("brush_2.png", True) 
        self.b3 = self.loader.load_image("brush_3.png", True) 
        self.b4 = self.loader.load_image("brush_4.png", True) 
        self.b5 = self.loader.load_image("brush_5.png", True) 
        self.b6 = self.loader.load_image("brush_6.png", True) 
        self.b7 = self.loader.load_image("brush_7.png", True)
        self.b8 = self.loader.load_image("brush_8.png", True)
        self.b9 = self.loader.load_image("brush_9.png", True)
        self.cur_color = pygame.Color(0,0,0)
        
        self.paper_rect = pygame.Rect(127,12,659,574)
        self.paper = (pygame.Surface(self.paper_rect.size,1)).convert()
        self.paper.fill((255,255,255))
        self.painting = False
        self.undo_cache = []
        
        self.pal_rect = pygame.Rect(12,12,101,200)
        
        self.brush_rect = pygame.Rect(12,231,101,355)
        self.brush_rects = [] 
        self.brush_rects.append(pygame.Rect(12,231,101,200))
        self.brush_rects.append(pygame.Rect(12,332,50,50))
        self.brush_rects.append(pygame.Rect(63,332,50,50))
        self.brush_rects.append(pygame.Rect(12,332+51*1,50,50))
        self.brush_rects.append(pygame.Rect(63,332+51*1,50,50))
        self.brush_rects.append(pygame.Rect(12,332+51*2,50,50))
        self.brush_rects.append(pygame.Rect(63,332+51*2,50,50))
        self.brush_rects.append(pygame.Rect(12,332+51*3,50,50))
        self.brush_rects.append(pygame.Rect(63,332+51*3,50,50))
        self.brush_rects.append(pygame.Rect(12,332+51*4,50,50))
        self.brush_rects.append(pygame.Rect(63,332+51*4,50,50))
        
        self.brush = PaintBrush(self.paper)
        
        self.set_brush(2)

    def save_paper(self):
        self.undo_cache.append(self.paper.copy())
        self.undo_cache = self.undo_cache[-30:]

    def undo_paper(self):
        if len(self.undo_cache):
            p = self.undo_cache.pop()
            self.paper.blit(p,(0,0))

    def set_color(self,c):
        self.cur_color = c
        self.brush.set_color(c)
        
    def set_alpha(self,a):
        if a <= 0.0:
            a = 0.005
            x = 14
        elif a >= 1.0:
            a = 1.0
            x = 97
        else:
            x = int(round(14.0+83.0*a))
        self.brush.set_alpha(a)
        self.knob_rect.left = x

    def set_brush(self,idx):
        if idx == 0:
            self.brush.set_brush(self.b1)
            self.brush.set_space(5.0)
            self.brush.set_color(self.cur_color)
            self.set_alpha(1.0)
        elif idx == 1:
            self.brush.set_brush(self.b2)
            self.brush.set_space(2.0)
            self.brush.set_color(self.cur_color)
            self.set_alpha(1.0)
        elif idx == 2:
            self.brush.set_brush(self.b3)
            self.brush.set_space(1.0)
            self.brush.set_color(self.cur_color)
            self.set_alpha(1.0)
        elif idx == 3:
            self.brush.set_brush(self.b4)
            self.brush.set_space(1.0)
            self.brush.set_color(self.cur_color)
            self.set_alpha(1.0)
        elif idx == 4:
            self.brush.set_brush(self.b5)
            self.brush.set_space(1.0)
            self.brush.set_color(self.cur_color)
            self.set_alpha(0.06)
        elif idx == 5:
            self.brush.set_brush(self.b6)
            self.brush.set_space(1.0)
            self.brush.set_color(self.cur_color)
            self.set_alpha(0.2)
        elif idx == 6:
            self.brush.set_brush(self.b6)
            self.brush.set_space(1.0)
            self.brush.set_color(self.cur_color)
            self.brush.set_follow_angle(True)
            self.set_alpha(0.2)
        elif idx == 7:
            self.brush.set_brush(self.b7)
            self.brush.set_space(1.0)
            self.brush.set_color(self.cur_color)
            self.set_alpha(0.15)
        elif idx == 8:
            self.brush.set_brush(self.b3)
            self.brush.set_space(1.0)
            self.brush.set_color(self.cur_color)
            self.brush.set_pattern([30,20,8,20])
            self.set_alpha(1.0)
        elif idx == 9:
            self.brush.set_brush(self.b8,True)
            self.brush.set_space(65.0)
            self.set_alpha(1.0)
        elif idx == 10:            
            self.brush.set_brush(self.b9,True)
            self.brush.set_space(20.0)
            self.brush.set_follow_angle(True)
            self.set_alpha(1.0)
        
    def paint_start(self):
        self.painting = True
        self.save_paper()
        
    def paint_stop(self):
        self.painting = False
    
    def swap_palette(self):
        self.simple = not self.simple
        if self.simple:
            self.back.blit(self.simple_pal,(12,12))
        else:
            self.back.blit(self.advanced_pal,(12,12))
                
    def main_loop(self):            
        clock = pygame.time.Clock()
        
        line_from = None
        line_to = None

        cur_color = pygame.Color(0,0,0)

        next_update = pygame.time.get_ticks()
        drag_knob = False
        
        view_help = True
        
        while 1:            
            for event in pygame.event.get():
                
                if view_help:
                    if event.type == QUIT:
                        return
                    elif event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            return                    
                        else:
                            view_help = False
                    elif event.type == MOUSEBUTTONDOWN:
                        view_help=False
                else:
                    if event.type == QUIT:
                        return
                    elif event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            return                    
                        elif event.key == K_SPACE:
                            self.paint_start()
                            self.paper.fill((255,255,255))
                            self.paint_stop()    
                        elif event.key == K_F1:
                            view_help = True
                        elif event.key == K_F2:
                            self.swap_palette()
                        elif event.key == 122 and event.mod == 64:
                            self.undo_paper()
                    
                    elif event.type == MOUSEBUTTONDOWN:
                        if event.button == 1:
                            if self.pal_rect.collidepoint(event.pos):
                                c = self.back.get_at(event.pos)
                                self.set_color(c)
                            elif self.brush_rect.collidepoint(event.pos):
                                i = 0
                                for r in self.brush_rects:
                                    if r.collidepoint(event.pos):
                                        self.set_brush(i)
                                    i+=1
                            elif self.knob_rect.collidepoint(event.pos):
                                drag_knob = True
                            elif self.paper_rect.collidepoint(event.pos):
                                self.paint_start()
                                x = event.pos[0]-self.paper_rect.x
                                y = event.pos[1]-self.paper_rect.y
                                self.brush.paint_from((x,y))
                        elif event.button == 3:
                            if self.paper_rect.collidepoint(event.pos):
                                line_from = event.pos
                            elif self.pal_rect.collidepoint(event.pos):
                                self.swap_palette()
                    elif event.type == MOUSEMOTION:
                        if event.buttons[0]:
                            if drag_knob:
                                self.knob_rect.left+=event.rel[0]
                                if self.knob_rect.left < 14:
                                    self.knob_rect.left = 14
                                if self.knob_rect.left > 97:
                                    self.knob_rect.left = 97
                            elif self.paper_rect.collidepoint(event.pos):
                                if self.painting:
                                    x = event.pos[0]-self.paper_rect.x
                                    y = event.pos[1]-self.paper_rect.y
                                    self.brush.paint_to((x,y))                            
                        elif event.buttons[2]:
                            if self.paper_rect.collidepoint(event.pos):
                                line_to = event.pos
                                painting = False                            
                    elif event.type == MOUSEBUTTONUP:
                        if drag_knob:
                            drag_knob = False
                            a = float(self.knob_rect.left-14)/83.0
                            self.set_alpha(a)
                        if event.button == 1 and self.painting:
                            self.paint_stop()
                        if event.button == 3:
                            if line_from:
                                self.paint_start()
                                fx = line_from[0]-self.paper_rect.x
                                fy = line_from[1]-self.paper_rect.y
                                tx = event.pos[0]-self.paper_rect.x
                                ty = event.pos[1]-self.paper_rect.y
                                self.brush.paint_line((fx,fy),(tx,ty))
                                self.paint_stop()
                                line_from = None
                                line_to = None
                                                          
            if pygame.time.get_ticks() >= next_update:
                next_update+=33
                self.screen.blit(self.back,(0,0))
                self.screen.blit(self.paper,self.paper_rect.topleft)
                if not view_help:
                    if line_from and line_to:
                        pygame.draw.line(self.screen, (0,0,0), line_from, line_to)
                self.screen.blit(self.knob,self.knob_rect.topleft)
                
                if view_help:
                    self.screen.blit(self.help,(0,0))
                
                pygame.display.flip()            

def main():
    try:
        import psyco
        psyco.full()
    except ImportError:
        pass

    pygame.init()

    g = AdvancedDemo()
    g.main_loop()
 
if __name__ == '__main__': 
    main()


