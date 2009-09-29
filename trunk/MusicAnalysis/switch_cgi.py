# swaps line 1 and 3 of target files.

import os
x = [i for i in os.listdir(".") if os.path.splitext(i)[-1].lower() == ".cgi"]
for filename in x:
    print "processing file: ", filename
    handle = open(filename)
    lines = handle.readlines()
    temp = lines[0]
    lines[0] = lines[2]
    lines[2] = temp
    handle.close()
    handle = open(filename, "w")
    for line in lines:
        handle.write(line)
    handle.close()