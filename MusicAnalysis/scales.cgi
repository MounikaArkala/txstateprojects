#!/usr/local/bin/python

import sys, copy
from musiclib import *
from scaleslib import *


import cgi, cgitb
cgitb.enable()

print "Content-type: text/html"
print



def pretty(notes, encoding):
    """ notes is int array, encoding is a dict such as {0:"A", 1:"A#" ... 11:"G#"}"""
    return " ".join([encoding[i] for i in notes])


# Create instance of FieldStorage 
form = cgi.FieldStorage() 

page = form.getvalue('page').strip().lower()

# Get data from fields
notes = form.getvalue('notes')


all_notes = {}
current_note = 0
for note in [("A",2),("B",1),("C",2),("D",2),("E",1),("F",2),("G",2)]:
    all_notes["%sbb" % note[0]] = (12 + current_note - 2) % 12
    all_notes["%sb"  % note[0]] = (12 + current_note - 1) % 12
    all_notes["%s"   % note[0]] = current_note
    all_notes["%s#"  % note[0]] = (current_note + 1) % 12
    all_notes["%sx" % note[0]] = (current_note + 2) % 12
    current_note += note[1]



notes = [all_notes[i.strip()] for i in notes.split()]




def get_scale(note, intervals):
	scale = [note]
	val = note
	for i in intervals:
		val = (val + i) % 12
		scale.append(val)
	return scale
	
def get_scales(intervals):
	scales = []
	for i in range(12):
		scales.append(get_scale(i, intervals))
	return scales
	
	

default_encoding = {0:"A", 1:"A#", 2:"B", 3:"C", 4:"C#", 5:"D", 6:"D#", 7:"E", 8:"F", 9:"F#", 10:"G", 11:"G#"}


if page.strip().lower() == "main":# print out the filter list, don't do any filtering.


	print "using notes: %s <br />" % pretty(notes, default_encoding)
	
	#filter list.
	print '<table class="filters">'
	print '<tr class="filters">'
	groups = []
	for scale in scales.keys():
		groups.append(scales[scale][1])
	groups = list(set(groups))
	groups.sort()
	for i, group in enumerate(groups):
		print '<td class="filters"><input type="checkbox" class="filters" checked id="check%i" onClick="updateScales();">%s</input></td>' % (i, group)
	print '</tr></table>'
	print '<input type="hidden" id="grps" value="%s" />' % len(groups)
	
	print '<div id="scalesdiv">'

	#scale filter
	scalenames = scales.keys()
	
elif page == "filtered": #just print out the scales table.
	groups = []
	for scale in scales.keys():
		groups.append(scales[scale][1])
	groups = list(set(groups))
	groups.sort()
	valid_groups = []
	for i in range(len(groups)):
		temp = form.getvalue("check%i" % i)
		if temp == "true":
			valid_groups.append(i)
	valid_groups = [groups[i] for i in valid_groups]
	scalenames = []
	for scale in scales.keys():
		if scales[scale][1] in valid_groups:
			scalenames.append(scale)


else:
    print "404 - Page %s could not be found!" % page
	
print '<table class="scales">'
print '<tr class="scales">'
print '<th scope="col" class="scales">Scale Name</th>'
print '<th scope="col" class="scales">Genres</th>'
print '<th scope="col" class="scales">Matching Scales</th></tr>'

scalenames.sort()
for scale in scalenames:
	matched = []
	for s in get_scales(scales[scale][0]):
		tempscale = []
		found = []
		for note in s:
			if note in notes:
				tempscale.append((note, 1))
				found.append(note)
			else:
				tempscale.append((note, 0))
		if len(set(found)) == len(notes): #support scales that repeat notes as well as those that don't.
			matched.append(tempscale)
			
	if len(matched) > 0:
		print '<tr class="scales">'
		print '<td class="scales">%s</td><td class="scales">%s</td>' % (scale, scales[scale][1])
		print '<td class="scales">'
		for item in matched:
			print '<table class="scale"><tr class="scale">'
			for note, match in item:
				if match:
					print '<td class="scaley">%s</td>' % default_encoding[note]
				else:
					print '<td class="scalen">%s</td>' % default_encoding[note]
			print '</tr></table>\n'
		print '</td></tr>'
		
print '</table>'

if page == "main":
	print "</div>"