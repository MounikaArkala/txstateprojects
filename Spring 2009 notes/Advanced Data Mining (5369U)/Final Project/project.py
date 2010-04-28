import sys, urllib, re
prefix = 'storemap://'
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
print storename
print params


#first we try to coerce the name to a standardized name from our DB.  If we can't do this, we'll throw up an error message.
valid_names = [('Walmart', 'wal-?mart')]
newname = None
for name in valid_names:
    if re.match(name[1], storename, re.IGNORECASE):
        newname = name[0]
if not newname:
    raw_input("Unfortunately the name \"%s\" does not have any store maps associated with it.  Please check back later." % storename)
    raise SystemExit

storename = newname

print newname
    
raw_input("")