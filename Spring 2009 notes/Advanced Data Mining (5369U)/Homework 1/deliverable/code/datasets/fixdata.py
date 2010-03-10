import sys
if len(sys.argv) < 3:
    print "Must pass filename and destination."
    raise SystemExit
lines = open(sys.argv[1]).readlines()
num_attributes = len(lines[0].split(','))
print "There are ", num_attributes, " attributes."
print "type the attributes in order, comma-separated, on the next line."
attribute_names = [i.strip() for i in raw_input(": ").split(',')]
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
if target != 0:
    # we'll have to do a swap.
    swap = True
    
if swap: #reorder the attributes so the class is the last one.
    temp = [class_name]
    temp.extend(attribute_names[:target])
    temp.extend(attribute_names[target+1:])
    attribute_names =  temp

output = open(sys.argv[2], 'w')
output.write("\t".join(attribute_names))
output.write("\n")
output.write("\t".join(["discrete" for i in attribute_names]))
output.write("\n")
output.write("class")
output.write("\t".join(["" for i in range(len(attribute_names) - 1)]))
output.write("\n")
for line in lines:
    if len(line.strip()) == 0:
        continue
    out_lines = [i.strip() for i in line.split(',')]
    if swap:    
        temp = [out_lines[target]]
        temp.extend(out_lines[:target])
        temp.extend(out_lines[target+1:])
        out_lines =  temp
    output.write("\t".join(out_lines))
    output.write("\n")
output.close()






