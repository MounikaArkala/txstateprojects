#!/usr/bin/python
import pygame
import os
import glob
import zlib
import random
import math
#import psyco
#psyco.full()

def efekt(start, end, step):
 n=pygame.surface.Surface(s.get_size())
 n0=pygame.surface.Surface(s.get_size())
 n0.blit(s,(0,0))
 for i in range(start,end,step):
  n.blit(n0,(0,0))
  for x in range(0,319,i):
   for y in range(0,239,i):
       pygame.draw.rect(n,n.get_at([x,y]),(x,y,i,i))
  s.blit(n,(0,0))
  pygame.display.flip()

def bgdraw():
 bgoffx=offx
 while bgoffx<0:
  bgoffx+=256
 while bgoffx>768:
  bgoffx-=1024
 bgoffy=offy
 while bgoffy<0:
  bgoffy+=256
 while bgoffy>768:
  bgoffy-=1024
 s.blit(bg,((-bgoffx/4),h*4-(bgoffy/4)))
 s.blit(bg,((-bgoffx/4+256),h*4-(bgoffy/4)))
 s.blit(bg,((-bgoffx/4-257),h*4-(bgoffy/4)))

def worlddraw():
 y=0
 sy=(offy/16)
 while y<=256:
  x=0
  sx=(offx/16)
  while x<=320:
   if sx<w and sy<h and sx>=0 and sy>=0:
    s.blit(tls,(x-offx%16,y-offy%16),tiles[map[int(sy)][int(sx)]])
   x+=16
   sx+=1
  y+=16
  sy+=1

def collision(px, py, pvx, pvy, speed, standing):
 if bt.count(map[int((py)/16)][int(px/16)]):
  if not bt2.count(map[int((py)/16)][int(px/16)]): 
   py=int(py/16)*16
   standing=1
   pvy=0
  elif bt2.count(map[int((py)/16)][int(px/16)]) and pvy>0:
   py=int(py/16)*16
   standing=1
   pvy=0   
 if bt.count(map[int((py)/16)-1][int(px/16)]):
  if not bt2.count(map[int((py)/16)-1][int(px/16)]):
   py=int(py/16+1)*16
   pvy=0
 if bt.count(map[int((py-1)/16)][int((px+6)/16)]):
  if not bt2.count(map[int((py-1)/16)][int((px+6)/16)]):
   speed=0.5
   px=int((px-1)/16)*16+10
   pvx/=2
 elif bt.count(map[int((py-1)/16)][int((px-6)/16)]):
  if not bt2.count(map[int((py-1)/16)][int((px-6)/16)]):
   speed=0.5
   px=int((px+1)/16)*16+6
   pvx/=2
 if px<8: px=8
 if px>w*16-17: px=w*16-17
 if py>h*16-8: die()
 return px,py,pvx,pvy,speed,standing

def playerdraw():
 if standing:
  if running and speed>0.9:
   s.blit(player, (px-offx-8,py-offy-15), pr[lor][4+int(step)%2])
  else:
   s.blit(player, (px-offx-8,py-offy-15), pr[lor][int(step)%2])
 else:
  if speed<0.9:
   s.blit(player, (px-offx-8,py-offy-15), pr[lor][2])	
  else:
   s.blit(player, (px-offx-8,py-offy-15), pr[lor][3])

def die():
 vy=-5
 y=py-offy-16
 while y<250:
  bgdraw()
  worlddraw()
  for i in range(len(monsters)):
   monsters[i].draw()
  s.blit(tls,(px-offx-8,y),tiles[239])
  y+=vy
  vy+=1
  pygame.display.flip()
  pygame.time.delay(fpsdelay)
 efekt(1,20,1)
 raise SystemExit

class sprt:
 def __init__(self, type, (x,y)):
  self.x,self.y=(x,y)
  self.type=type
  self.lor=random.choice((-1,1))
  self.vx=self.lor
  self.vy=0
  self.standing=0
  self.alive=1
  self.id=len(monsters)
 def draw(self):
  if self.alive:
   if self.type==1:
    s.blit(tls,(self.x-offx-8,self.y-offy-16), tiles[254+(frame/5)%2])
 def commit(self,pvy):
  if self.alive:
   if self.type==1:
    if self.standing: self.x+=self.vx
    self.y+=self.vy
    if self.x>w*16 or self.x<-9 or self.y>h*16-4 or self.y<0: self.alive=0
    if math.hypot(px-self.x,py-self.y)<16:
     if py+4<self.y: 
      self.alive=0
      s.blit(tls,(self.x-offx-8,self.y-offy-16), tiles[253])
      pygame.display.flip()
      return -pvy
     else: die()    
    if bt.count(map[int((self.y)/16)][int(self.x/16)]):
     self.y=int(self.y/16)*16
     self.standing=1
     self.vy=0
    if bt.count(map[int((self.y-1)/16)][int((self.x+self.vx*8)/16)]):
     self.vx=-self.vx
    for i in range(len(monsters)):
     if i!=self.id and math.hypot(self.x-monsters[i].x,self.y-monsters[i].y)<16 and monsters[i].alive:
      self.vx=-self.vx
    self.draw()
    self.vy+=0.5
  return pvy
   
pygame.init()
pygame.mouse.set_visible(0)
s=pygame.display.set_mode((320,240),pygame.FULLSCREEN)

monsters=[]
bt=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 31, 32, 33, 35, 38, 39, 40, 41, 42, 43, 43, 44, 45, 46, 47, 59, 61, 60, 63, 64, 65, 66, 67]
bt2=[9, 10, 11, 32, 33, 35, 64, 65, 66, 67]
tiles=[]
tls=pygame.image.load("data/tileset.png")
tls.set_colorkey((255,0,255,0))
for i in range(256):
 tiles.append(((i%16)*16,int(i/16)*16,16,16))
player=pygame.image.load('data/player.png')
bg=pygame.image.load('data/bg1.png')
player.set_colorkey((255,0,255,0))
pr=[[],[]]
for i in range(0,96,16):
 pr[0].append((i,0,16,16))
 pr[1].append((i,16,16,16))
p=zlib.decompress(open("mapa","rb").read())
open("_temp",'wb').write(p)
p=open("_temp","rb")
map=[]
y=0
while 1:
 x=0
 map.append([])
 while 1:
  c=p.read(1)
  if c=='\n' or c=='^':
   break
  c+=p.read(2)
  if c=="255":
   monsters.append(sprt(1,(x*16,y*16)))
   c=0
  map[y].append(int(c))
  x+=1
 y+=1
 if c=="^":
  break
p.close()
os.unlink("_temp")
w=len(map[0])
h=len(map)

run=1
px=py=17.0
pvx=pvy=pax=pay=0.0
speed=0.5
offx=offy=standing=lor=step=alreadyjumped=running=0
fpsdelay=20
clock = pygame.time.Clock()
frame=0


while run:
 clock.tick()
 frame+=1
 if frame>20:
  if clock.get_fps()>30:
   fpsdelay+=1
  else:
   fpsdelay-=1
  frame=0
 pygame.draw.rect(s,(152,144,248),(0,0,320,240))

 bgdraw()

 pax=pay=0

 pygame.event.peek()
 keys=pygame.key.get_pressed() 
 if keys[pygame.K_ESCAPE]:
  run=0
 if keys[pygame.K_LEFT]:
  if pax>0:
   speed=0.5
  pax-=speed
  if running and speed<1.2:
   speed+=0.01
  lor=1
 if keys[pygame.K_RIGHT]:
  if pax<0:
   speed=0.5
  pax+=speed
  if running and speed<1.2:
   speed+=0.01
  lor=0
 if not keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
  if speed>0.5:
   speed-=0.1
 if keys[pygame.K_LALT] and standing and not alreadyjumped:
  py-=1
  pvy-=5+speed*10
  standing=0
  alreadyjumped=1
  if(speed>0.5): 
   speed-=0.25
 if not keys[pygame.K_LALT]:
  alreadyjumped=0
 if keys[pygame.K_LSHIFT]:
  running=1
 else:
  running=0
  speed=0.5

 pax-=pvx*0.1
 pay-=pvy*0.04
 pvx+=pax
 pvy+=pay
 if(pvx>6.1):pvx=6.1    
 if(pvx<-6):pvx=-6
 if(pvy>12):pvy=12
 if(pvy<-12):pvy=-12

 if abs(pvx)<0.01:
  step=0
 step+=pvx/15

 px+=pvx
 py+=pvy
 pvy+=1


 px, py, pvx, pvy, speed, standing=collision(px, py, pvx, pvy, speed, standing)

 if px-offx<160:
  offx-=abs(px-offx-160)/5
 if px-offx>160:
  offx+=abs(px-offx-160)/5
 if py-offy<120:
  offy-=abs(py-offy-120)/5
 if py-offy>120:
  offy+=abs(py-offy-120)/5
 if offx<0:
  offx=0
 if offy<0:
  offy=0
 if offx>w*16-320:
  offx=w*16-320
 if offy>h*16-240:
  offy=h*16-240

 worlddraw()
 for i in range(len(monsters)):
  pvy=monsters[i].commit(pvy)

 playerdraw()
 pygame.display.flip()
 pygame.time.delay(fpsdelay)
raise SystemExit

