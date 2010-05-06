

import pygame, time
from pygame.locals import *
from hillclimbing import tsp
import db, urllib, time, re

#this should be moved to a map-specific file.
mapping = {'Entrance/Exit': (36, 78), 'Electronics': (40, 5),
           'Grocery': (9,7), 'Lawn & Garden': (67, 7),
           'Home & Office': (9, 23), 'Fashion': (67, 23),
           'Restaurant': (28, 29), 'Health & Pharmacy': (47, 30),
           'Auto': (68, 36), 'Jewelry': (9, 38),
           'Books & Magazines': (37, 42),
           'Cards & Party': (9, 52),
           'Shoes': (67, 52),
           'Toys': (39, 59),
           'Checkout': (49, 59)}
           
#globals!
enterstr = "" # the query string they're typing in.
state = 'fullmap' # the current state we're in.
removeitem = False #whether we wanna remove the last item.

if __name__ == "__main__":
    main()
        
class fakeClass(object):
    def __init__(self): pass
    def play(self): pass

def handleKeypress(event):
    global enterstr
    global state
    global removeitem
        
    #set up keymap so we can more easily display keys without having to deal with a bunch of pygame.local vars.
    keymap = {}
    for i in range(97, 123):
        keymap[i] = chr(i)
    for i in range(48, 58):
        keymap[i] = str(i-48)
    keymap[32] = ' '
    
    try:
        keyascii = keymap[event.key]
    except:
        keyascii = None
        
    if keyascii:
        enterstr += keyascii
        
    elif event.key == K_BACKSPACE or event.key == K_DELETE:
        enterstr = enterstr[:-1]
        
    elif event.key == K_F1:
        state = 'text'
        enterstr = ''
        
    elif event.key == K_F2:
        state = 'fullmap'
    elif event.key == K_F3:
        
        if state == 'removeLastItem' or state == 'suspend' or state == 'confirmRemoveLastItem':
            removeitem = True
        else:
            removeitem = False
            state = 'removeLastItem'
        
    else:
        print "unknown key: ", event.key
        

def centerBlit(surf1, surf2):
    # blit surf2 centered in surf1.
    xval = surf1.get_width() / 2
    xval -= surf2.get_width() / 2
    yval = surf1.get_height() / 2
    yval -= surf2.get_height() / 2
    surf1.blit(surf2, (xval, yval))

def autoscale(text, fonts):
    for font in fonts:
        temp = font.render(text, True, (255,255,255), (0,0,0))
        if temp.get_width() <= 1280:
            break
    return temp
    
    
def main(mapfile = 'maps/walmart.png', storename='Walmart'):
    global state, querystr
    pygame.init()
    pygame.mixer.init()
    pygame.key.set_repeat(400,50)
    screen = pygame.display.set_mode((1280, 800))
    pygame.font.init()
    suspendlength = 2
    nextState = 'fullmap'
    updateItemSidebar = False
    route = pygame.Surface((1280,800), flags=SRCALPHA)
    route.fill((0,0,0,0), (0,0,1280,800))
    
    font = pygame.font.Font(None, 128)
    smallfont = pygame.font.Font(None, 32)
    medfont = pygame.font.Font(None, 64)
    medlargefont = pygame.font.Font(None, 96)
    
    fonts = [font, medlargefont, medfont, smallfont]
    itemlist = []
    previtemlistlen = -1

    #todo - get map name from other code.
    mapfile = 'maps/walmart.png'
    mapsurf = pygame.image.load(mapfile)
    
    #get our map data.
    passability = []
    unique_colors = []
    locations = []
    mapsurf.lock()
    for y in range(mapsurf.get_height()):
        passabilityrow = []
        for x in range(mapsurf.get_width()):
            color = mapsurf.get_at((x,y))[:3]
                
            if color == (0,0,0): #black is impassable.
                passabilityrow.append(-1)
            else:
                passabilityrow.append(1)
                if color not in unique_colors and color != (255,255,255):
                    unique_colors.append(color)
                    locations.append((unique_colors.index(color), x,y))
                        
        passability.append(passabilityrow)
    print locations
    mapsurf.unlock()
    mapsurf = mapsurf.convert()
    mapsurf = pygame.transform.scale(mapsurf, (800,800))
    itemsidebar = pygame.Surface((480, 800))
    #print unique_colors
    sidebarsurf = pygame.Surface((480, 800))
    sidebarsurf.fill((255,255,255), (0,0,480,800))

    #mapsidebar contains the detailed info about the location points.
    mapsidebar = pygame.Surface((480, 800))
    for i in range(20): #display at MOST 20 points.
        if i == 0:
            color = (0,0,0)
        elif i == 1:
            color = (127, 127, 127)
        elif i == 2:
            color = (255, 255, 255)
        else:
            try:
                color = unique_colors[i-3]
            except:
                break
        try:
            title = db.categories[storename][i]
        except:
            break
        mapsidebar.fill(color, (1, i*40+2, 38, 38))
        tempsurf = smallfont.render(title, True, (255,255,255), (0,0,0))
        mapsidebar.blit(tempsurf, (41, i*40+2+20 - (tempsurf.get_height()/2)))
        
    
    coinsound = fakeClass()
    try:
        coinsound = pygame.mixer.Sound('smw_coin.wav')
    except:
        print "Failed to load coin sound :("    
      

       
    #mainloop crap.
    exit = False
    cycle = time.time() #blinking cursor
    addPipe = False
    
    while not exit:
        #clear the screen.
        screen.fill((0,0,0), (0,0,1280,800))
        screen.blit(mapsurf, (480, 0))
        screen.blit(sidebarsurf, (0,0))
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exit = True
                    break
                elif event.key == K_RETURN:
                    if state == 'text':
                        coinsound.play()
                        state = 'query'
                else:
                    handleKeypress(event)      
        if exit:
            pygame.quit()
            continue
            
        if state == 'text':
            if addPipe: tempstr = "query: " + enterstr + "|"
            else:       tempstr = "query: " + enterstr + " "
            tempsurf = autoscale(tempstr, fonts)
            overlay = lambda: centerBlit(screen, tempsurf)
        
        elif state == 'query':
            #here is where the magic happens :)
            overlay = None
            queryitem = None
            for item in db.items:
                if enterstr == item[1] or enterstr.lower() in item[0].lower() or enterstr.lower() in item[1].lower():
                    queryitem = item
                    break
                
            if not queryitem:
                tempsurf = autoscale(enterstr + " not found in DB.", fonts)
            else:
                if queryitem[0] == 'Book':
                    tempsurf = autoscale("Looking up book with ISBN %s." % queryitem[1], fonts)
                    
                    centerBlit(screen, tempsurf)
                    pygame.display.update()
                    time.sleep(0.4)
                    
                    try:     
                        text =  urllib.urlopen('http://isbndb.com/api/books.xml?access_key=Z69YMGT9&index1=isbn&value1=%s' % queryitem[2]).read()
                        print text
                        title, author = re.findall('<Title>(.*?)</Title>.*<AuthorsText>(.*?)</AuthorsText>', text, re.DOTALL)[0]
                        author = author.split(';')[0]
                        tempsurf = autoscale("Found %s by %s." % (title, author), fonts)
                    except:
                        print "Retrieve failed."
                else:
                    tempsurf = autoscale("Found %s." % queryitem[0], fonts)
                    
                # add to our items list.
                itemlist.append(queryitem)
            state = 'suspend'
            suspendlength = 2
            nextState = 'displayList'
                    
            overlay = lambda: centerBlit(screen, tempsurf)
                
            #TODO : levenshtien if it is a miss.
            
            print "Query!"
            
        elif state == 'fullmap':
            #draw the labels.
            screen.blit(mapsidebar, (0,0))
            overlay = None
            
        elif state == 'suspend':
            time.sleep(suspendlength)
            state = nextState
            
            
            
            
        elif state == 'displayList':
            # Draw our item list and our route and whatnot.
            screen.blit(itemsidebar, (0,0))
            screen.blit(mapsurf, (480, 0))
            screen.blit(route, (0,0))
            overlay = None
            
            
            
            
        elif state == 'removeLastItem':
            tempsurf = autoscale("Press F3 again to remove the last-entered item.", fonts)
            overlay = lambda: centerBlit(screen, tempsurf)
            state = 'suspend'
            suspendlength = 1
            nextState = 'confirmRemoveLastItem'
            
        elif state == 'confirmRemoveLastItem':
            if removeitem:
                print "last item removed."
                itemlist = itemlist[:-1]
                tempsurf = autoscale("last item removed.", fonts)
            else:
                print "last item not removed."
                tempsurf = autoscale("last item not removed.", fonts)
                
            overlay = lambda: centerBlit(screen, tempsurf)
            state = 'suspend'
            suspendlength = 1
            nextState = 'displayList'
            
        if time.time() - cycle > 0.4:
            addPipe = not addPipe
            cycle = time.time()
            
        if overlay:
            overlay()
        if previtemlistlen != len(itemlist):
            previtemlistlen = len(itemlist)
            #update item sidebar.
            itemsidebar.fill((0,0,0), (0,0,480,800))
            locations = []
            
            templist = [('Entrance','','','Entrance/Exit','product_images/door.jpg')]
            templist.extend(itemlist)
            templist.append(('Checkout','','','Checkout','product_images/checkout.jpg'))
            for item in itemlist:
                try:
                    #this is sort of a hack. shouldn't assume the order of the categories.
                    location = mapping[item[3]]
                    locations.append(location)
                except:
                    pass
            
            neworder = tsp.customTSPSolve(locations)[2]
            newlist = []
            for i in neworder:
                newlist.append(itemlist[i])
                
            itemlist = newlist
            
            
            
            
            
            templist = [('Entrance','','','Entrance/Exit','product_images/door.jpg')]
            templist.extend(itemlist)
            templist.append(('Checkout','','','Checkout','product_images/checkout.jpg'))
            templist.append(('Exit','','','Entrance/Exit','product_images/door.jpg'))
            for i, item in enumerate(templist):
                try:
                    print "loading: ", item[4]
                    img = pygame.image.load(item[4])
                    img = img.convert()
                    img = pygame.transform.scale(img, (38,38))
                except:
                    img = pygame.Surface((40,40))
                    
                itemsidebar.blit(img, (1, i*40+2))
                tempsurf = smallfont.render(item[0], True, (255,255,255), (0,0,0))
                itemsidebar.blit(tempsurf, (41, i*40+2+20 - (tempsurf.get_height()/2)))
                
                
            #update route.
            print templist
            route.fill((0,0,0,0), (0,0,1280,800))
            locations = []
            for item in templist:
                try:
                    #this is sort of a hack. shouldn't assume the order of the categories.
                    location = mapping[item[3]]
                    print "found", item, 'at: ', location
                    locations.append(location)
                except:
                    print "failure for a location.", item
                    pass
                    
            
            for loc in locations:
                route.fill((0,255,0), (loc[0]*10+2+480, loc[1]*10+2, 5,5))
            from AStar import AStar
            mapdata = []
            for i in range(80):
                mapdata.extend(passability[i])
            for i in range(len(locations)-1):
                astar = AStar.AStar(AStar.SQ_MapHandler(mapdata,80,80))
                start = AStar.SQ_Location(locations[i][0], locations[i][1])
                end = AStar.SQ_Location(locations[i+1][0], locations[i+1][1])
                p = astar.findPath(start,end)
                path = [locations[i]]
                for n in p.nodes:
                    path.append((n.location.x,n.location.y))
                path.append((end.x,end.y))
                for i in range(len(path)-1):
                    pygame.draw.line(route, (0,255,0), (path[i][0]*10+2+480, path[i][1]*10+2), (path[i+1][0]*10+2+480, path[i+1][1]*10+2), 1)
                
        pygame.display.update()
        
    