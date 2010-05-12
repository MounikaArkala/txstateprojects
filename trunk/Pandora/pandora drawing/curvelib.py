#!/usr/bin/env python2.3
#
#  curvelib.py
#  
#
#  Created by Matthew Mitchell on 20/09/2009.
#  Copyright (c) 2009 Matthew Mitchell. All rights reserved.
#
import math,numpy,pygame
from pygame.locals import *
def basic_arc_gen(r): #For basic aliased circles
	arc = []
	radius_sq = float(r) ** float(2)
	for y in xrange(r):
		x = (radius_sq - float(y) ** float(2)) ** 0.5
		arc.append((x,y))
	for x in xrange(r):
		y = (radius_sq - float(x) ** float(2)) ** 0.5
		if not (x,y) in arc:
			arc.append((x,y))
	return arc
def arc_gen(r):
	arc = []
	for d in xrange(0,46):
		rad = math.radians(d)
		arc.append([math.cos(rad) * r,math.sin(rad) * r])
	for co in reversed(arc):
		arc.append([co[1],co[0]])
	return arc
def aacircle(s,x,y,r,colour):
	r -= 2
	x += 1
	y += 1
	circle = []
	arc = arc_gen(r)
	for c in arc:
		circle.append([c[0] + r + x,c[1] + r + y])
	arc.reverse()
	for c in arc:
		c[0] = r - c[0]
		circle.append([c[0] + x,c[1] + r + y])
	arc.reverse()
	for c in arc:
		c[1] = r - c[1]
		circle.append([c[0] +x,c[1] +y])
	arc.reverse()
	for c in arc:
		c[0] = r - c[0]
		circle.append([c[0] + r + x,c[1] + y])
	pxb = 0
	for px in circle:
		if pxb != 0:
			pygame.draw.aaline(s, colour, px, pxb)
		pxb = px
def rounded_corners(s,r):
	t = pygame.Surface((r,r))
	r -= 2
	arc = arc_gen(r)
	pxb = 0
	for px in arc:
		if pxb != 0:
			pygame.draw.aaline(t, (255,255,255), px, pxb)
		pxb = px
	pa = pygame.PixelArray(t)
	ab = pygame.surfarray.pixels_alpha(s)
	xlen = len(pa[0])
	ablen = [len(ab)-1,len(ab[1])-2]
	for y in xrange(len(pa)):
		a = 0
		for x in xrange(xlen):
			if pa[y][x] < a:
				alpha = 0
				ab[(ablen[0] - r) + y][(ablen[1] - r) + x] = alpha
				ab[(ablen[0] - r) + y][r - x] = alpha
				ab[r - y][(ablen[1] - r) + x] = alpha
				ab[r - y][ r - x] = alpha
			else:
				if pa[y][x] != 0:
					alpha = int(float(255) - float(pa[y][x]) ** (float(1)/float(3)))
					ab[(ablen[0] - r) + y][(ablen[1] - r) + x] = alpha
					ab[(ablen[0] - r) + y][r - x] = alpha
					ab[r - y][(ablen[1] - r) + x] = alpha
					ab[r - y][r - x] = alpha
				a = pa[y][x]
	for y in xrange(ablen[0]):
		ab[y][0] = 0
		ab[y][1] = 0
		ab[y][ablen[1]] = 0
		ab[y][ablen[1] + 1] = 0
	for x in xrange(ablen[1]):
		ab[0][x] = 0
		ab[ablen[0]][x] = 0
	del ab
	del pa
if __name__ == '__main__':	
	import sys
	pygame.init()
	window = pygame.display.set_mode((500,500))
	screen = pygame.Surface((400,400),SRCALPHA)
	screen.fill((200,120,250))
	rounded_corners(screen,60)
	aacircle(screen,100,100,100,(10,60,200))
	aacircle(screen,30,20,80,(180,150,60))
	window.blit(screen,(50,50))
	pygame.display.flip()
	while 1:
		events = pygame.event.get()
		for event in events:
			if event.type == QUIT:
				sys.exit()