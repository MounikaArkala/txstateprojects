#IAN MALLETT'S PADLIB - PyGame Advance Graphics Library - v.4.0.0 - April 2008
#---IMPORTS---
import pygame
from pygame.locals import *
import random, sys
from math import *
try:
    import psyco
    psyco.full()
except:
    pass
#---INITIALISATIONS---
pygame.init()
#---ANTI-ALIASED CIRCLE---
def aacircle(Surface,color,pos,radius,antialiaslevel,width=0):
    surfacesize = (radius*2)+(2*antialiaslevel)
    circlesurface = pygame.Surface((surfacesize,surfacesize))
    circlesurface.set_colorkey((0,0,0))
    pygame.draw.circle(circlesurface,color,(radius+antialiaslevel,radius+antialiaslevel),radius,width)
    circlesurface = antialias(circlesurface,antialiaslevel)
    Surface.blit(circlesurface,(pos[0]-radius-antialiaslevel,pos[1]-radius-antialiaslevel))
#---ANTI-ALIASING---
decayfactor = 0.05
def antialias(surface,antialiaslevel):
    width = surface.get_width()
    height = surface.get_height()
    for x in xrange(antialiaslevel):
        Colors = []
        for y in xrange(height):
            xarray = []
            for x in xrange(width):
                Color = surface.get_at((x,y))
                xarray.append(Color)
            Colors.append(xarray)
        surface2 = pygame.Surface(surface.get_size())
        y = 0
        for xline in Colors:
            x = 0
            for color in xline:
                red = color[0]
                green = color[1]
                blue = color[2]
                reddifference   = 0
                greendifference = 0
                bluedifference  = 0
                index = [[x-1,y-1],[x,y-1],[x+1,y-1],
                           [x-1,y],          [x+1,y],
                         [x-1,y+1],[x,y+1],[x+1,y+1]]
                for i in index:
                    if i[1] > 0:
                        try:
                            colorpixel = Colors[i[1]]
                            color2 = colorpixel[i[0]]
                            red2   = color2[0]
                            green2 = color2[1]
                            blue2  = color2[2]
                            reddifference   -= red - red2
                            greendifference -= green - green2
                            bluedifference  -= blue - blue2
                        except:
                            pass
                redadd   = int(red+(decayfactor*reddifference))
                greenadd = int(green+(decayfactor*greendifference))
                blueadd  = int(blue+(decayfactor*bluedifference))
                if redadd > 255: redadd = 255
                if greenadd > 255: greenadd = 255
                if blueadd > 255: blueadd = 255
                if redadd < 0: redadd = 0
                if greenadd < 0: greenadd = 0
                if blueadd < 0: blueadd = 0
                Color = (redadd,greenadd,blueadd)
                surface2.set_at((x,y),Color)
                x += 1
            y += 1
        surface = surface2
    return surface2
#---PARTICLE SYSTEM---
class particle_system:
    def __init__(self,position,colorarray,speedrange,disperse,direction,density,frames):
        self.pos = position
        self.colorarray = colorarray
        self.speedrange = speedrange
        self.disperse = disperse
        self.direction = direction
        self.density = density
        self.frames = frames
        self.particles = []
        self.occluders = []
        self.entropy = None
        self.bouncerandomness = 0.0
        self.gravity = None
    def set_occluders(self,occluders):       self.occluders = occluders
    def set_bounce(self,entropy,randomness): self.entropy = entropy; self.bouncerandomness = randomness
    def set_gravity(self,gravity):           self.gravity = gravity
    def change_position(self,NewPos):           self.pos        = NewPos
    def change_speed(self,NewSpeedRange):       self.speedrange = NewSpeedRange
    def change_disperse(self,NewDisperse):      self.disperse   = NewDisperse
    def change_direction(self,NewDirection):    self.direction  = NewDirection
    def change_density(self,NewDensity):        self.density    = NewDensity
    def update(self):
        for x in xrange(self.density):
            PosBx = self.pos[0]
            PosBy = self.pos[1]
            angle = radians(  self.direction+((random.random()-0.5)*self.disperse)  )
            speed = (random.uniform(self.speedrange[0],self.speedrange[1]))/4.0
            Speed = [speed*cos(angle),speed*sin(angle)]
            self.particles.append([[PosBx,PosBy],Speed,0])
        for p in self.particles:
            p[0][0] += p[1][0]
            p[0][1] += p[1][1]
            p[2] += 1
            if p[2] == self.frames:
                self.particles.remove(p);continue
        if len(self.occluders) > 0:
            for o in self.occluders:
                for p in self.particles:
                    if o.collidepoint(p[0]):
                        if self.entropy == None:
                            self.particles.remove(p)
                        else:
                            XDiff1 = abs(p[0][0]-o.left)
                            XDiff2 = abs(p[0][0]-o.right)
                            YDiff1 = abs(p[0][1]-o.top)
                            YDiff2 = abs(p[0][1]-o.bottom)
                            if XDiff1 > XDiff2: XSide = "Right"; XDiff3 = XDiff2
                            else: XSide = "Left"; XDiff3 = XDiff1
                            if YDiff1 > YDiff2: YSide = "Bottom"; YDiff3 = YDiff2
                            else: YSide = "Top"; YDiff3 = YDiff1
                            if XDiff3 > YDiff3: #Top or Bottom Collision
                                p[1][1] *= -1
                                if YSide == "Top": p[0][1] -= 1
                                else: p[0][1] += 1
                            else: #Side Collision
                                p[1][0] *= -1
                                if XSide == "Left": p[0][0] -= 1
                                else: p[0][0] += 1
                            BounceFactor = self.entropy + (random.random()*self.bouncerandomness)
                            p[1][0] *= BounceFactor
                            p[1][1] *= BounceFactor
        if self.gravity != None:
            for p in self.particles:
                p[1][0] += self.gravity[0]
                p[1][1] += self.gravity[1]
    def get_color(self,frame):
        part_done = float(frame)/float(self.frames)
        index = part_done*len(self.colorarray)
        int_index = int(index)
        start_color = self.colorarray[int_index]
        try:end_color = self.colorarray[int_index+1]
        except:end_color = self.colorarray[int_index]
        part_through = index - int_index
        red = start_color[0]
        green = start_color[1]
        blue = start_color[2]
        red_difference = end_color[0] - red
        green_difference = end_color[1] - green
        blue_difference = end_color[2] - blue
        red += red_difference * part_through
        green += green_difference * part_through
        blue += blue_difference * part_through
        between_color = (int(red),int(green),int(blue))
        return between_color
    def draw(self,Surface):
        for p in self.particles:
            Surface.set_at((int(p[0][0]),int(p[0][1])),self.get_color(p[2]))
#---SHADOWS---
class Shadow:
    def __init__(self,size,Pos,occluder,color,lightopacity):
        global mapd, LIGHT_SIZE, lightPos, lightRect, lightBody, mask, lightcolor
        LIGHT_SIZE = size
        lightPos = Pos
        mapd = occluder
        lightRect = None
        mask = pygame.Surface((LIGHT_SIZE*2,LIGHT_SIZE*2))
        mask.set_colorkey((0,0,0))
        mask.set_alpha(lightopacity)
        lightRect = mask.get_rect()
        lightRect.center = lightPos
        lightcolor = color
    def tracePoint(self,x1,y1,x2,y2,l):
        theta = atan2((y2-y1),(x2-x1));    
        if theta<0:
            d= (180*(theta+(pi*2))/pi)
        else:
            d= (180*(theta)/pi)
        dx = cos(radians(d))
        dy = sin(radians(d))
        return (x2+dx*l,y2+dy*l)
    def getPolygon(self,x,y,box):
        r = box.right
        l = box.left
        t = box.top
        b = box.bottom
        L = LIGHT_SIZE+10
        box = pygame.Rect(l,t,box.width-1,box.height-1)
        lightPos = (LIGHT_SIZE,LIGHT_SIZE)
        if x >= l and x <= r:
            if y >= b: # directly under
                #print "UNDER"
                tp1 = self.tracePoint(x,y,l,b,L)
                tp2 = self.tracePoint(x,y,r,b,L)
                return ((box.bottomleft,tp1,[lightPos[0]-L,lightPos[1]-L],[lightPos[0]+L,lightPos[1]-L],tp2,box.bottomright))
            else:   # directly above             
                #print "ABOVE"
                tp1 = self.tracePoint(x,y,l,t,L)
                tp2 = self.tracePoint(x,y,r,t,L)
                return ((box.topleft,tp1,[lightPos[0]-L,lightPos[1]+L],[lightPos[0]+L,lightPos[1]+L],tp2,box.topright))
        elif y >= t and y <= b:
            if x <= l: # directly to the left
                #print "LEFT"
                tp1 = self.tracePoint(x,y,l,b,L)
                tp2 = self.tracePoint(x,y,l,t,L)
                return ((box.bottomleft,tp1,[lightPos[0]+L,lightPos[1]+L],[lightPos[0]+L,lightPos[1]-L],tp2,box.topleft))
            else:   # directly to the right
                #print "RIGHT"
                tp1 = self.tracePoint(x,y,r,b,L)
                tp2 = self.tracePoint(x,y,r,t,L)
                return ((box.bottomright,tp1,[lightPos[0]-L,lightPos[1]+L],[lightPos[0]-L,lightPos[1]-L],tp2,box.topright))
        if y <= t:
            if x <= l: # upper left
                #print "UPPER LEFT"
                tp1 = self.tracePoint(x,y,r,t,L)
                tp2 = self.tracePoint(x,y,l,b,L)
                return ((box.topleft,box.topright,tp1,tp2,box.bottomleft))
            else:     # upper right
                #print "UPPER RIGHT"
                tp1 = self.tracePoint(x,y,l,t,L)
                tp2 = self.tracePoint(x,y,r,b,L)
                return ((box.topright,box.topleft,tp1,tp2,box.bottomright))
        elif y >= b:
            if x <= l: # lower left
                #print "LOWER LEFT"
                tp1 = self.tracePoint(x,y,r,b,L)
                tp2 = self.tracePoint(x,y,l,t,L)
                return ((box.bottomleft,box.bottomright,tp1,tp2,box.topleft))
            else:     # lower right
                #print "LOWER RIGHT"
                tp1 = self.tracePoint(x,y,l,b,L)
                tp2 = self.tracePoint(x,y,r,t,L)
                return ((box.bottomright,box.bottomleft,tp1,tp2,box.topright))
        return None
    def change_position(self,pos):
        lightPos[0] = pos[0]
        lightPos[1] = pos[1]
        lightRect.center = lightPos
    def DrawMask(self,img):
        nrects = []
        for r in mapd:
            if lightRect.colliderect(r):
                nr = r.clip(lightRect)
                nr.top = nr.top - lightRect.top
                nr.left = nr.left - lightRect.left
                nrects.append(nr)
        img.fill((0,0,0))
        pygame.draw.circle(img, lightcolor, (LIGHT_SIZE,LIGHT_SIZE), LIGHT_SIZE,0)
        for r in nrects:
            p = self.getPolygon(LIGHT_SIZE,LIGHT_SIZE,r)
            if p:
                pygame.draw.polygon(img, (0,0,0), p, 0)
    def draw(self,screen):
        self.DrawMask(mask)
        screen.blit(mask, lightRect.topleft)
        pygame.display.flip()
#---ROUNDED RECTANGLE---
def Rect(s,rect,roundedsize,color,width=0):
    pygame.draw.circle(s,color,(roundedsize+width,roundedsize+width),roundedsize)
    pygame.draw.circle(s,color,(rect[2]-roundedsize-width,roundedsize+width),roundedsize)
    pygame.draw.circle(s,color,(roundedsize+width,rect[3]-roundedsize-width),roundedsize)
    pygame.draw.circle(s,color,(rect[2]-roundedsize-width,rect[3]-roundedsize-width),roundedsize)
    pygame.draw.rect(s,color,(roundedsize+width, width, rect[2]-(2*roundedsize)-(2*width), rect[3]-(2*width)))
    pygame.draw.rect(s,color,(width, roundedsize+width, rect[2]-(2*width), rect[3]-(2*roundedsize)-(2*width)))
def RoundedRect(surface,color,rect,roundedsize,width=0):
    s = pygame.Surface((rect[2],rect[3]))
    colorkey = (255-color[0],255-color[1],255-color[2])
    s.fill(colorkey)
    s.set_colorkey(colorkey)
    Rect(s,rect,roundedsize,color)
    if width != 0:
        Rect(s,(rect[0],rect[1],rect[2],rect[3]),roundedsize-width,colorkey,width)
    surface.blit(s,(rect[0],rect[1]))
#---DOTTED LINE---
def DashedLine(surface,color1,color2,pos1,pos2,increment):
    YDiff = float(pos2[1]-pos1[1])
    XDiff = float(pos2[0]-pos1[0])
    Length = sqrt((XDiff**2)+(YDiff**2))
    colornumber = 0
    Color = color1
    for pos in xrange(int(round(Length))):
        Position = (  int(round(((pos/Length)*XDiff)+pos1[0])),  int(round(((pos/Length)*YDiff)+pos1[1]))  )
        surface.set_at(Position,Color)
        colornumber += 1
        if colornumber == increment:
            colornumber = 0
            if Color == color1:
                Color = color2
            else:
                Color = color1
#---BEZIER CURVES---
def BezierCurve(Surface,PointList,Thickness,Resolution,color):
    KochanekBartels(Surface, PointList, 1.0/float(Resolution), False, color, Thickness)
def aaBezierCurve(Surface,PointList,Resolution,color):
    KochanekBartels(Surface, PointList, 1.0/float(Resolution), True, color)
    
t=b=c=0
def KochanekBartels(Surface,ControlPoints,step,aa,color,Thickness=1):
    global t,b,c
    tans = []
    tand = []
    for x in xrange(len(ControlPoints)-2):
        tans.append([])
        tand.append([])
    cona = (1-t)*(1+b)*(1-c)*0.5
    conb = (1-t)*(1-b)*(1+c)*0.5
    conc = (1-t)*(1+b)*(1+c)*0.5
    cond = (1-t)*(1-b)*(1-c)*0.5
    i = 1
    while i < len(ControlPoints)-1:
        pa = ControlPoints[i-1]
        pb = ControlPoints[i]
        pc = ControlPoints[i+1]
        x1 = pb[0] - pa[0]
        y1 = pb[1] - pa[1]
        x2 = pc[0] - pb[0]
        y2 = pc[1] - pb[1]
        tans[i-1] = (cona*x1+conb*x2, cona*y1+conb*y2)
        tand[i-1] = (conc*x1+cond*x2, conc*y1+cond*y2)
        i += 1
    t_inc = step
    i = 1
    while i < len(ControlPoints)-2:
        p0 = ControlPoints[i]
        p1 = ControlPoints[i+1]
        m0 = tand[i-1]
        m1 = tans[i]
        #draw curve from p0 to p1
        Lines = [(p0[0],p0[1])]
        t_iter = t_inc
        while t_iter < 1.0:
            h00 = ( 2*(t_iter**3)) - ( 3*(t_iter**2)) + 1
            h10 = ( 1*(t_iter**3)) - ( 2*(t_iter**2)) + t_iter
            h01 = (-2*(t_iter**3)) + ( 3*(t_iter**2))
            h11 = ( 1*(t_iter**3)) - ( 1*(t_iter**2))
            px = h00*p0[0] + h10*m0[0] + h01*p1[0] + h11*m1[0]
            py = h00*p0[1] + h10*m0[1] + h01*p1[1] + h11*m1[1]
            Lines.append((px,py))
            t_iter += t_inc
        Lines.append((p1[0],p1[1]))
        Lines2 = []
        for p in Lines:
            Lines2.append((int(round(p[0])),int(round(p[1]))))
        if aa:
            pygame.draw.aalines(Surface,color,False,Lines2)
        else:
            pygame.draw.lines(Surface,color,False,Lines2,Thickness)
        i += 1
