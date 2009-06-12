#!/usr/local/bin/python

import sys
from musiclib import *
from scaleslib import *


import cgi, cgitb
cgitb.enable()

print "Content-type: text/html"
print

print "<br />Matching Scales<br />"


def pretty(notes, encoding):
    """ notes is int array, encoding is a dict such as {"A":0, "A#":1 ... "G#":11}"""
    temp = "    <td class=\"primesdata\">%s</td>\n" * len(notes)
    return temp % tuple([encoding[i] for i in notes])


# Create instance of FieldStorage 
form = cgi.FieldStorage() 

#page = form.getvalue('page')

# Get data from fields
row = form.getvalue('notes')


row = "A B C"


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
        a.append(abs(notes[i+1] - notes[i]))
    return a
        
notes = [all_notes[i.strip()] for i in row.split()]
notes.sort()
intervals = find_interval(notes)
print intervals
print "located at: ", find_in_list(scales['Major Scale'], intervals, wraparound=False)
