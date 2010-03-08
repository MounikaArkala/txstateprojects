import pygame


def colorpick(width, height):
    """ returns a surface with a color picker, and an array
    so you can convert screen coordinates to a color. """
    gradient = pygame.Surface((width, height))
    gradient.lock()
    red = 255.0
    green = 0.0
    blue = 0.0
    swidth = (width / 6) - 5
    colors = []
    for x in range(width):
        column1 = []
        column2 = []
        for y in range(height+1):
            #y is a multiplier for color. in the center it's 100% the color,
            # above the center it's the distance % mixed with white
            # and below the center it's the distance % mixed with black
            if y <= height / 2: # mix with black.
                mul = (1.0/(height / 2)) * y
               #gradient.set_at((x,height-y), (min(red* mul, 255), min(green*mul, 255), min(blue*mul, 255))).
                mul = (1.0/(height / 2)) * y
                color = (int(red*mul), int(green*mul), int(blue*mul))  # This line is not getting the correct color value.
                gradient.set_at((x,height-y), color)
                column2.append(color)
                
            elif y >= height / 2: # mix with white.
                y -= (height / 2) + 1
                mul = (1.0/(height / 2)) * y
                color = (int(red*mul + 255*(1-mul)), int(green*mul + 255*(1-mul)), int(blue*mul + 255*(1-mul)))  # This line is not getting the correct color value.
                #print color
                gradient.set_at((x,y), color)
                column1.append(color)
            
        column2.reverse()
        column1.extend(column2)
        colors.append(column1)

            
        if x < swidth:#green goes to 100%
            green += (255.0 / swidth)
        elif swidth <= x < swidth*2:#red goes to 0%
            #print "red goes to 0"
            red -= (255.0 / swidth)
        elif swidth*2 <= x < swidth*3:#blue goes to 100%
            #print "blue goes to 100%"
            blue += (255.0 / swidth)
        elif swidth*3 <= x < swidth*4:#green goes to 0%
            green -= (255.0 / swidth)
        elif swidth*4 <= x < swidth*5:#red goes to 100%
            red += (255.0 / swidth)
        elif swidth*5 <= x < swidth*6:#blue goes to 0%
            blue -= (255.0 / swidth)
        elif swidth * 6 == x:
            red = 255
            green = 255
            blue = 255

    gradient.unlock()
    return (gradient, colors)
#pygame.surfarray.blit_array(screen, [[(244,0,0) * 480]*800]) - should be faster, try to change to this!