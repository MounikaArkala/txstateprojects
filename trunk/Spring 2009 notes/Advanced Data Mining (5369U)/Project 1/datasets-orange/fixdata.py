import sys
if len(sys.argv) < 3:
    print "Must pass filename and destination."
    raise SystemExit
lines = open(sys.argv[1]).readlines()
num_attributes = len(lines[0].split(','))
print "There are ", num_attributes, " attributes."
print "type the attributes in order, space-separated, on the next line."
attribute_names = raw_input(": ").split()
if len(attribute_names) != num_attributes:
    print "You didn't enter the correct number of attributes!"
    raise SystemExit
    
print "Which attribute is a class?"
class_name = raw_input(": ").strip()
if class_name not in attribute_names:
    print "Your class wasn't in the attributes list you entered. Exiting."
    raise SystemExit
    
    
output = open(sys.argv[2], 'w')
output.write("\t".join(attribute_names))
output.write("\n")
output.write("\t".join(['discrete'] * len(attribute_names)))
output.write("\n")
strings = []
for attribute in attribute_names:
    if attribute != class_name:
        strings.append("")
    else:
        strings.append("class")
output.write("\t".join(strings))
output.write("\n")
for line in lines:
    output.write("\t".join(line.split(',')))
    output.write("\n")
output.close()