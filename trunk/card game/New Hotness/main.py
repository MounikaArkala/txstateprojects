

from cards import cards
cwidth = 72
cheight = 72
separator = 1
width = 800
height = 480

import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((width,height))
cardimgs = pygame.image.load("img/fullset.bmp")
geezard = cardimgs.subsurface(0,0,width,height)
font = pygame.font.Font(None, 24)
current = 0
while 1:
    screen.fill((0,0,0), (0,0,width,height))
    cardloc = ((width-cwidth) / 2, (height-cheight) / 2)
    screen.blit(cardimgs.subsurface(0,(cheight+separator)*current, cwidth, cheight), cardloc)
    
    # place card name above card.
    x = font.render(cards[0][current][0], 0, (255,255,255))
    textloc = ((width - x.get_width()) / 2, cardloc[1] - 20 - x.get_height())
    
    screen.blit(x, textloc)
    
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                current = max(0, current-1)
            elif event.key == K_RIGHT:
                current = min(10, current+1)