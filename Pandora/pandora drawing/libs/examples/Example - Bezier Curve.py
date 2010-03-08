#imports
import pygame
from pygame.locals import *
from padlib import *
import sys, os, random

#Center the screen
if sys.platform == 'win32' or sys.platform == 'win64':
    os.environ['SDL_VIDEO_CENTERED'] = '1'

#Initialise PyGame
pygame.init()

#Screen size
Screen = (512,512)

#Set the display icon
icon = pygame.Surface((1,1)); icon.set_alpha(0); pygame.display.set_icon(icon)
#Set the display caption
pygame.display.set_caption("Bezier Curve Demo with PAdLib - Ian Mallett - 2008")
#make the window
Surface = pygame.display.set_mode(Screen)

#input function
def get_input():
    key = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == QUIT or key[K_ESCAPE]:
            pygame.quit(); sys.exit()

#Make a whole buch of control points at random positions.
A = [random.randint(10,502),random.randint(10,502)]
B = [random.randint(10,502),random.randint(10,502)]
C = [random.randint(10,502),random.randint(10,502)]
D = [random.randint(10,502),random.randint(10,502)]
E = [random.randint(10,502),random.randint(10,502)]
F = [random.randint(10,502),random.randint(10,502)]
G = [random.randint(10,502),random.randint(10,502)]
H = [random.randint(10,502),random.randint(10,502)]
I = [random.randint(10,502),random.randint(10,502)]
J = [random.randint(10,502),random.randint(10,502)]
K = [random.randint(10,502),random.randint(10,502)]
L = [random.randint(10,502),random.randint(10,502)]
M = [random.randint(10,502),random.randint(10,502)]
N = [random.randint(10,502),random.randint(10,502)]
O = [random.randint(10,502),random.randint(10,502)]
P = [random.randint(10,502),random.randint(10,502)]
Q = [random.randint(10,502),random.randint(10,502)]
R = [random.randint(10,502),random.randint(10,502)]
S = [random.randint(10,502),random.randint(10,502)]
T = [random.randint(10,502),random.randint(10,502)]
U = [random.randint(10,502),random.randint(10,502)]
V = [random.randint(10,502),random.randint(10,502)]
W = [random.randint(10,502),random.randint(10,502)]
X = [random.randint(10,502),random.randint(10,502)]
Y = [random.randint(10,502),random.randint(10,502)]
Z = [random.randint(10,502),random.randint(10,502)]

Dragging = None

#Main Loop
while True:
    #Get input
    get_input()
    #Get the mouse position and pressed
    mpos = pygame.mouse.get_pos()

    #Move the Control Points
    if Dragging == "A": A = [mpos[0],mpos[1]]
    if Dragging == "B": B = [mpos[0],mpos[1]]
    if Dragging == "C": C = [mpos[0],mpos[1]]
    if Dragging == "D": D = [mpos[0],mpos[1]]
    if Dragging == "E": E = [mpos[0],mpos[1]]
    if Dragging == "F": F = [mpos[0],mpos[1]]
    if Dragging == "G": G = [mpos[0],mpos[1]]
    if Dragging == "H": H = [mpos[0],mpos[1]]
    if Dragging == "I": I = [mpos[0],mpos[1]]
    if Dragging == "J": J = [mpos[0],mpos[1]]
    if Dragging == "K": K = [mpos[0],mpos[1]]
    if Dragging == "L": L = [mpos[0],mpos[1]]
    if Dragging == "M": M = [mpos[0],mpos[1]]
    if Dragging == "N": N = [mpos[0],mpos[1]]
    if Dragging == "O": O = [mpos[0],mpos[1]]
    if Dragging == "P": P = [mpos[0],mpos[1]]
    if Dragging == "Q": Q = [mpos[0],mpos[1]]
    if Dragging == "R": R = [mpos[0],mpos[1]]
    if Dragging == "S": S = [mpos[0],mpos[1]]
    if Dragging == "T": T = [mpos[0],mpos[1]]
    if Dragging == "U": U = [mpos[0],mpos[1]]
    if Dragging == "V": V = [mpos[0],mpos[1]]
    if Dragging == "W": W = [mpos[0],mpos[1]]
    if Dragging == "X": X = [mpos[0],mpos[1]]
    if Dragging == "Y": Y = [mpos[0],mpos[1]]
    if Dragging == "Z": Z = [mpos[0],mpos[1]]
    mpress = pygame.mouse.get_pressed()
    #If clicked on point, drag it.
    if mpress[0]:
        rect = pygame.Rect(mpos[0]-3,mpos[1]-3,6,6)
        if   rect.collidepoint(A): Dragging = "A"
        elif rect.collidepoint(B): Dragging = "B"
        elif rect.collidepoint(C): Dragging = "C"
        elif rect.collidepoint(D): Dragging = "D"
        elif rect.collidepoint(E): Dragging = "E"
        elif rect.collidepoint(F): Dragging = "F"
        elif rect.collidepoint(G): Dragging = "G"
        elif rect.collidepoint(H): Dragging = "H"
        elif rect.collidepoint(I): Dragging = "I"
        elif rect.collidepoint(J): Dragging = "J"
        elif rect.collidepoint(K): Dragging = "K"
        elif rect.collidepoint(L): Dragging = "L"
        elif rect.collidepoint(M): Dragging = "M"
        elif rect.collidepoint(N): Dragging = "N"
        elif rect.collidepoint(O): Dragging = "O"
        elif rect.collidepoint(P): Dragging = "P"
        elif rect.collidepoint(Q): Dragging = "Q"
        elif rect.collidepoint(R): Dragging = "R"
        elif rect.collidepoint(S): Dragging = "S"
        elif rect.collidepoint(T): Dragging = "T"
        elif rect.collidepoint(U): Dragging = "U"
        elif rect.collidepoint(V): Dragging = "V"
        elif rect.collidepoint(W): Dragging = "W"
        elif rect.collidepoint(X): Dragging = "X"
        elif rect.collidepoint(Y): Dragging = "Y"
        elif rect.collidepoint(Z): Dragging = "Z"
    else:
        Dragging = None

    #Clear the Surface.
    Surface.fill((0,0,0))

    #Draw the Bezier Curve
    BezierCurve(Surface,(A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z),3,100,(255,0,0))
    #Surface - draw bezier onto this surface.
    #(A,B,C,D,E,F) - the Control Points
    #3 - the thickness of the line.
    #100 - the resolution.
    #(255,0,0) - the color, red

    #Anti-aliased Version (Thickness always is 1)
##    aaBezierCurve(Surface,(A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z),100,(0,0,255))
    #Surface - draw bezier onto this surface.
    #(A,B,C,D,E,F) - the Control Points
    #100 - the resolution.
    #(0,0,255) - the color, blue

    #Draw the Control Points
    pygame.draw.circle(Surface,(0,0,255),A,3)
    pygame.draw.circle(Surface,(0,0,255),B,3)
    pygame.draw.circle(Surface,(0,0,255),C,3)
    pygame.draw.circle(Surface,(0,0,255),D,3)
    pygame.draw.circle(Surface,(0,0,255),E,3)
    pygame.draw.circle(Surface,(0,0,255),F,3)
    pygame.draw.circle(Surface,(0,0,255),G,3)
    pygame.draw.circle(Surface,(0,0,255),H,3)
    pygame.draw.circle(Surface,(0,0,255),I,3)
    pygame.draw.circle(Surface,(0,0,255),J,3)
    pygame.draw.circle(Surface,(0,0,255),K,3)
    pygame.draw.circle(Surface,(0,0,255),L,3)
    pygame.draw.circle(Surface,(0,0,255),M,3)
    pygame.draw.circle(Surface,(0,0,255),N,3)
    pygame.draw.circle(Surface,(0,0,255),O,3)
    pygame.draw.circle(Surface,(0,0,255),P,3)
    pygame.draw.circle(Surface,(0,0,255),Q,3)
    pygame.draw.circle(Surface,(0,0,255),R,3)
    pygame.draw.circle(Surface,(0,0,255),S,3)
    pygame.draw.circle(Surface,(0,0,255),T,3)
    pygame.draw.circle(Surface,(0,0,255),U,3)
    pygame.draw.circle(Surface,(0,0,255),V,3)
    pygame.draw.circle(Surface,(0,0,255),W,3)
    pygame.draw.circle(Surface,(0,0,255),X,3)
    pygame.draw.circle(Surface,(0,0,255),Y,3)
    pygame.draw.circle(Surface,(0,0,255),Z,3)

    #Some Info. Lines
    DashedLine(Surface,(0,0,255),(0,255,0),B,A,4)
    DashedLine(Surface,(0,0,255),(0,255,0),Y,Z,4)
    
    #Flip to the Screen
    pygame.display.flip()
