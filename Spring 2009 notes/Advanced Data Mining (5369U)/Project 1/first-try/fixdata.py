import sys
if len(sys.argv) < 3:
    print "Must pass filename and destination."
    raise SystemExit
lines = open(sys.argv[1]).readlines()
num_attributes = len(lines[0].split(','))
print "There are ", num_attributes, " attributes."
print "type the attributes in order, space-separated, on the next line."
attribute_names = [i.strip() for i in raw_input(": ").split()]
if len(attribute_names) != num_attributes:
    print "You didn't enter the correct number of attributes!"
    raise SystemExit
    
print "Which attribute is a class?"
class_name = raw_input(": ").strip()
if class_name not in attribute_names:
    print "Your class wasn't in the attributes list you entered. Exiting."
    raise SystemExit
else:
    target = attribute_names.index(class_name)

swap = False
if target != len(attribute_names) - 1:
    # we'll have to do a swap.
    swap = True
    
output = open(sys.argv[2], 'w')
if swap: #reorder the attributes so the class is the last one.
    temp = attribute_names[:target]
    temp.extend(attribute_names[target+1:])
    temp.append(class_name)
    attribute_names =  temp

output.write(", ".join(attribute_names))
output.write("\n")
for line in lines:
    out_lines = [i.strip() for i in line.split(',')]
    if swap:
        temp = out_lines[:target]
        temp.extend(out_lines[target+1:])
        temp.append(out_lines[target])
        out_lines =  temp
    output.write(", ".join(out_lines))
    output.write("\n")
output.close()






