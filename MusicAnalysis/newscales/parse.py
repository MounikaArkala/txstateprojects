pat = "<option value=\"(.*?)\">(.*?)(: \w*)?(\(.* .*\))?(</option>)"
import re
def tointervals(values):
    #only works for ascending scales.
    intervals = []
    prev = values[0]
    for i in values[1:]:
        if i < prev:
            i += 12
            
        intervals.append( i - prev)
        prev = i
    return intervals
x = 0
y = 0
names = []
import sys
sys.stdout = open("out.txt", 'w')
for line in open('src.txt'):
    temp, name = re.match(pat, line).groups()[:2]
    name = name.strip()
    if name in names:
        continue #eliminate repeated names.
    names.append(name)
    #print re.match(pat, line).groups()
    translator = {'Ab': 11,
                  'An': 0,
                  'As': 1,
                  'Bf': 0, #Bbb
                  'Bb': 1,
                  'Bn': 2,
                  'Cb': 2,
                  'Cn': 3,
                  'Cs': 4,
                  'Db': 4,
                  'Dn': 5,
                  'Ds': 6,
                  'Eb': 6,
                  'En': 7,
                  'Es': 8,
                  'Fb': 7,
                  'Fn': 8,
                  'Fs': 9,
                  'Gb': 9,
                  'Gn': 10,
                  'Gs': 11}
    direction = temp[3]
    temp = temp[5:]
    if direction.lower() != "u":
        continue
    vals = [translator[temp[i:i+2]] for i in range(0, len(temp), 2)]
    
    tags = ["Exotic"]
    if "raga " in name.lower():
        tags.append("Raga")
    if "maqam " in name.lower():
        tags.append("Maqam")
    if "mela " in name.lower():
        tags.append("Mela")
    if "blues" in name.lower():
        tags.append("Blues")
    if "'" in name:
        name = name.replace("'", "")
    if len(name) > x:
        x = len(name)
    if len(repr(tointervals(vals))) > y:
           y = len(repr(tointervals(vals)))

    print "            %s: (%s %s)," % ("'" + name + "'" + " "*(45-len(name)), repr(tointervals(vals))+","+" " * (36-len(repr(tointervals(vals)))), repr(tags))

sys.stdout.close()
