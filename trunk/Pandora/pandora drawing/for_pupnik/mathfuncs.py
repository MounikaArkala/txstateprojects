 
 


def valueRangeMap(val, origMin, origMax, newMin, newMax):
    """
    Will remap val from the original range into the new range.
    
    val : The value you are mapping.
    origMin : The original minimum value that val should be greater than.
    origMax : The original maximum value that val should be less than.
    newMin : The new minimum value that val will be mapped into.
    newMax : the new maximum value that val will be mapped into.
    
    return : float : The newly mapped value.
    """
    # Find the percentage val is between origMin and origMax:
    percetVal = float(val - origMin) / float(origMax - origMin)
    # Map into the new range:
    mappedVal = (newMin+newMax)*percetVal
    
    return mappedVal


 
 
def lerp(start, end, startpressure, endpressure):
    datapoints = [(start, startpressure)]
    # 4 situations, moving up and left, up and right, down and left, or down and right.
   
    startx, starty = start
    endx,endy = end
    
    ydist = endy - starty
    xdist = endx - startx
    x, y = startx, starty
    if ydist < 0:# y is decreasing
        yadd = -1
    else:
        yadd = 1
    if xdist < 0:
        xadd = -1
    else:
        xadd = 1
    if startpressure < endpressure:
        padd = 1
    else:
        padd = -1
    pressure = startpressure
    if abs(xdist) > abs(ydist): # we're gonna be lerp'ing the y's.
        try:
            yinc = abs(ydist/float(xdist))
        except:
            yinc = 0
        try:
            pinc = abs((endpressure-startpressure)/float(xdist))
        except:
            pinc = 0
        
        for q in range(abs(xdist)):
            x += xadd
            y += yadd * yinc
            pressure += padd * pinc
            datapoints.append(((int(x),int(y)), int(pressure)))
            
    else: #we're gonna be lerp'ing on the x's.
        try:
            xinc = abs(xdist/float(ydist))
        except:
            xinc = 0
        try:
            pinc = abs((endpressure-startpressure)/float(ydist))
        except:
            pinc = 0
            
        for q in range(abs(ydist)):
            x += xadd * xinc
            y += yadd
            pressure += padd * pinc
            datapoints.append(((int(x),int(y)), int(pressure)))
    return datapoints
    
    
if __name__ == "__main__":
    print "Test a quadrant 1 lerp."
    print lerp((0,0), (10,10)) # quadrant 1
    print "test a quadrant 2 lerp."
    print lerp((0,10), (10, 0))
    print "test a quadrant 3 lerp."
    print lerp((10, 10), (0,0))
    print "test a quadrant 4 lerp."
    print lerp((10, 0), (0, 10))
    print lerp((223,232), (211,240))