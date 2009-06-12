# use a scale rooted at A for best effect.

#!/usr/local/bin/python

import sys, copy
from musiclib import *
from scaleslib import *


def pretty(notes, encoding):
    """ notes is int array, encoding is a dict such as {"A":0, "A#":1 ... "G#":11}"""
    temp = "    <td class=\"primesdata\">%s</td>\n" * len(notes)
    return temp % tuple([encoding[i] for i in notes])




all_notes = {}
current_note = 0
for note in [("A",2),("B",1),("C",2),("D",2),("E",1),("F",2),("G",2)]:
    all_notes["%sbb" % note[0]] = (12 + current_note - 2) % 12
    all_notes["%sb"  % note[0]] = (12 + current_note - 1) % 12
    all_notes["%s"   % note[0]] = current_note
    all_notes["%s#"  % note[0]] = (current_note + 1) % 12
    all_notes["%sx" % note[0]] = (current_note + 2) % 12
    current_note += note[1]


def find_interval(notes):
    a = []
    for i in range(len(notes) - 1):
        #if next note is smaller, we add 12 to it to make it larger.
        if (notes[i+1] < notes[i]):
            val = (notes[i+1] + 12) - notes[i]
        else:
            val = notes[i+1] - notes[i]
        a.append(val)
    return a


while 1:
    scale = raw_input("enter scale (or exit): ")
    if scale.strip() == "exit":
        break
    notes = [all_notes[i] for i in scale.split()]
    print find_interval(notes)

    
"""
def fix(note):
    note = note[0].upper() + note[1:].lower()
    return note


state = 'name'
for line in open("scales.txt"):
    if line.strip() == "":
        continue

    if state == 'name':
        name = line.strip()
        state = 'scale'
    elif state == 'scale':
        scale = line.strip()
        notes = [all_notes[fix(i)] for i in scale.split()]
        interval = find_interval(notes)
        print "            '%s Scale'" % name + " " * (max(22 - len(name), 0)) + ": %s," % repr(interval)
        state = 'name'

"""
