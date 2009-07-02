#!/usr/bin/python
import pygame
import sys
import os
import zlib

def worlddraw():
 y=0
 sy=(offy/16)
 while y<=256:
  x=0
  sx=(offx/16)
  while x<=320:
   if sx<width and sy<height and sx>=0 and sy>=0:
    pygame.draw.rect(s,(0,0,0),(x-offx%16,y-offy%16,16,16),1)
    s.blit(tls,(x-offx%16,y-offy%16),tiles[map[int(sy)][int(sx)]])
   x+=16
   sx+=1
  y+=16
  sy+=1

if len(sys.argv)!=4: 
 print "Using: %s name width height"%sys.argv[0]
 raise SystemExit

name=sys.argv[1]
width=int(sys.argv[2])
height=int(sys.argv[3])

pygame.init()
s=pygame.display.set_mode((320,240),pygame.FULLSCREEN)

tiles=[]
tls=pygame.image.load("data/tileset.png")
tls.set_colorkey((255,0,255,0))
for i in range(256):
 tiles.append(((i%16)*16,int(i/16)*16,16,16))

try:
 p=zlib.decompress(open(sys.argv[1],"rb").read())
 print "Loading map"
 open("_temp",'wb').write(p)
 p=open("_temp","rb")
 map=[]
 y=0
 while 1:
  map.append([])
  while 1:
   c=p.read(1)
   if c=='\n' or c=='^':
    break
   c+=p.read(2)
   map[y].append(int(c))
  y+=1
  if c=="^":
   break
 p.close()
 width=len(map[0])
 height=len(map)
 os.unlink("_temp")
except:
 print "Creating new map"
 y=0
 map=[]
 while y<height:
  x=0
  map.append([])
  while x<width:
   map[y].append(0)
   x+=1
  y+=1

run=1
offx=offy=0
ctile=1
font = pygame.font.SysFont("Monospace",14)

iii=""
while run:
 pygame.draw.rect(s,(152,144,248),(0,0,320,240))
 pygame.event.peek()
 keys=pygame.key.get_pressed() 
 if keys[pygame.K_ESCAPE]:
  run=0
 if keys[pygame.K_LEFT]:
  ctile-=1
  if ctile<0:ctile=len(tiles)-1
  pygame.time.delay(50)
 if keys[pygame.K_RIGHT]:
  ctile+=1
  if ctile==len(tiles):ctile=0
  pygame.time.delay(50)
 if keys[pygame.K_SPACE]:
  iii+="%i, "%ctile
  pygame.time.delay(100)
 mx,my=pygame.mouse.get_pos()
 if pygame.mouse.get_pressed()==(1,0,0):
  map[int((my+offy)/16)][int((mx+offx)/16)]=ctile
 if pygame.mouse.get_pressed()==(0,0,1):
  map[int((my+offy)/16)][int((mx+offx)/16)]=0
 if mx<20:
  offx-=5
 if mx>300:
  offx+=5
 if my<20:
  offy-=5
 if my>220:
  offy+=5
 if offx<0:
  offx=0
 if offy<0:
  offy=0
 if offx>width*16-320:
  offx=width*16-320
 if offy>height*16-240:
  offy=height*16-240
 worlddraw()
 s.blit(font.render("tile no: %d"%ctile,1,(255,255,255)),(1,1))
 s.blit(tls,(mx+10 ,my +8),tiles[ctile])
 pygame.display.flip()
 pygame.time.delay(20)

out=""
for y in range(len(map)):
 for x in range(len(map[0])):
  out+="%03d"%map[y][x]
 out+="\n"
out=out[:-1]
out+="^"
out=zlib.compress(out)
open(sys.argv[1],"wb").write(out)
print iii
raise SystemExit