
items = []
for line in open('chars.txt'):
    if line.strip().startswith('0x'):
        items.append(int(line[2:],16))
print items