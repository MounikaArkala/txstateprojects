#!/usr/local/bin/python

import sys, copy
from musiclib import *
from scaleslib import *


import cgi, cgitb
cgitb.enable()

print "Content-type: text/html"
print

print "<br />Matching Scales<br />"


def pretty(notes, encoding):
    """ notes is int array, encoding is a dict such as {0:"A", 1:"A#" ... 11:"G#"}"""
    return " ".join([encoding[i] for i in notes])


# Create instance of FieldStorage 
form = cgi.FieldStorage() 

#page = form.getvalue('page')

# Get data from fields
row = form.getvalue('notes')


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
    
def reverse_interval(interval):
    a = [0]
    for i in interval:
        a.append((a[-1] + i) % 12)
    return a
        
def shift_notes(notes):
    temp = copy.copy(notes)
    a = [temp]
    for i in range(len(notes) - 1):
        temp = copy.copy(temp)
        temp.append(temp.pop(0))
        a.append(temp)
    return a

                
notes = [all_notes[i.strip()] for i in row.split()]
notes.sort()
intervals = [find_interval(i) for i in shift_notes(notes)]

default_encoding = {0:"C", 1:"C#", 2:"D", 3:"D#", 4:"E", 5:"F", 6:"F#", 7:"G", 8:"G#", 9:"A", 10:"A#", 11:"B"}
print '<table class="scales">'
print '<tr class="scales">'
print '<th scope="col" class="scales">Scale Name</th>'
print '<th scope="col" class="scales">Commonly Used In</th>'
print '<th scope="col" class="scales">Example of Scale</th></tr>'
for scale in scales:
    for interval in intervals:
        index = find_in_list(scales[scale][0], interval, wraparound=True)
        if index > -1:
            example = pretty(reverse_interval(scales[scale][0]), default_encoding)
            print '<tr class="scales">'
            print '<td class="scales">%s</td><td class="scales">%s</td><td class="scales">%s</td></tr>' % (scale, scales[scale][1], example)
            break
print '</table>'