import sys, urllib, re, db, gis, hashlib, os
threshold = 0.5
prefix = 'storemap://'
directory = r'C:\Projects\Spring 2009 notes\Advanced Data Mining (5369U)\Final Project'
os.chdir(directory)



if len(sys.argv) < 2 or not sys.argv[1].startswith(prefix):
    raw_input("Must start with storemap:// url as first parameter.")
    raise SystemExit

data = urllib.unquote(sys.argv[1][len(prefix):])
storename, params = data.split('?')
storename = storename.strip()
params = params.split('&')
temp = {}
for param in params:
    key, val = param.split('=')
    temp[key.strip()] = val.strip()
    
params = temp
print
print "Original Store Name:", storename
print "Passed parameters:  ", params
print
print "Using regular expressions to normalize the store name..."
print
#first we try to coerce the name to a standardized name from our DB.  If we can't do this, we'll throw up an error message.
valid_names = db.valid
newname = None
for name in valid_names:
    if re.match(name[1], storename, re.IGNORECASE):
        newname = name[0]
if not newname:
    raw_input("Unfortunately the name \"%s\" does not have any store maps associated with it.  Please check back later." % storename)
    raise SystemExit

storename = newname
print "Normalized store name:", storename
print
print "Using Haversine distance to determine if the selected %s" % storename
print " is within %s kilometers of any of our known %s stores" % (threshold, storename)
print " (to account for inaccuracies in map data.)"
print 
def hash(tuple):
    return hashlib.md5(''.join(tuple)).hexdigest()
    
storelocation = [params['lat'], params['lng']]
foundstore = None
for i,location in enumerate(db.storelocs[storename]):
    l1 = (float(location[0]), float(location[1]))
    l2 = (float(storelocation[0]), float(storelocation[1]))
    dist = gis.getDistanceByHaversine(l1, l2)
    print 'Store %i is %0.4f kilometers from our store.' % (i+1, dist)
    if gis.isWithinDistance(l1, l2, threshold):
        print '  Store %i is within %s kilometers from our store.' % (i+1, threshold)
        storehash = hash(location)
        if foundstore:
            if foundstore[1] > dist:
                foundstore = (storehash, dist, i+1)
        else:
            foundstore = (storehash, dist, i+1)
    else:
        print '  Store %i is not within %s kilometers from our store.' % (i+1, threshold)
    print
print 
generic = False
store = None
if not foundstore:
    print "!! Didn't find a store within our threshold !!"
    print "!!     Using the store's generic layout     !!"
    generic = True
else:
    try:        
        store = db.storemaps[foundstore[0]]
        print "Selected Store %s, with hash %s, which is the closest at %0.4f kilometers." % (foundstore[2], foundstore[0], foundstore[1])  
    except:
        print "!!   There is no data for that store.   !!"
        print "!!   Using the store's generic layout   !!"
        generic = True
        
print

if generic:
    store = db.genmaps[storename]
    
print
raw_input("hit enter to run the UI.")
import ui
ui.main(store, storename)