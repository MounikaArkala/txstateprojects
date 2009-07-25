#!/usr/local/bin/python
#!"C:/python26/python.exe"

""" Scales.cgi
----------------------------
Author:    Luke Paireepinart
Copyright: Nico Schuler

Texas State University
Summer 2009
----------------------------
Brief Summary:  This program finds all of the scales in its database that match with
the user's chosen notes.  Can also enforce order of notes as well as whether they
must be consecutive or not.
"""

import sys, copy
from musiclib import *
from scaleslib import *
import cgi

# Debug code, shouldn't be included unless testing.
#import cgitb
#cgitb.enable()

print "Content-type: text/html"
print

#it just uses this encoding because it doesn't know how to refer to items in a scale
#(eg. is an item a Eb or a D#?  It depends on the scale.
#but this information is not encoded in the scale database, so it uses defaults.
default_encoding = {0:"A", 1:"A#", 2:"B", 3:"C", 4:"C#", 5:"D", 6:"D#", 7:"E", 8:"F", 9:"F#", 10:"G", 11:"G#"}

def pretty(notes, encoding):
    ' notes is int array, encoding is a dict such as {0:"A", 1:"A#" ... 11:"G#"}'
    return " ".join([encoding[i] for i in notes])

def get_scale(note, intervals):
    """ pass it a note and a set of intervals and it will generate the scale.
    eg. note 5 and scale 2,2,3,1,2 would generate
    5,7,9,0,1,3."""
    scale = [note]
    val = note
    for i in intervals:
        val = (val + i) % 12
        scale.append(val)
    return scale
    
def get_scales(intervals):
    """ a helper function to generate all 12 transpositions of a scale at once."""
    scales = []
    for i in range(12):
        scales.append(get_scale(i, intervals))
    return scales
    
# Create instance of FieldStorage 
form = cgi.FieldStorage() 

def printPage():
    #this is a function so it can be "return'd" from.
    #it's a bit of an exploitation of a function for a control flow advantage but
    #I feel it greatly simplifies the code in this case.
    try:
        # Get data from fields
        page = form.getvalue('page').strip().lower()
        temp = form.getvalue('notes').strip()
        order = (form.getvalue('order').strip().lower() == "true")
        consecutive = (form.getvalue('consecutive').strip().lower() == "true")
    except:
        print "Unable to process input parameters."
        return
    
    #convert notes from strings to their correct corresponding note (integer).
    notes = []
    for i in temp.split():
        i = i.strip()
        i = i[0].upper() + i[1:].lower()
        
        try:
            if not all_notes[i] in notes:
                notes.append(all_notes[i])
        except KeyError:
            print "You entered an invalid note: %s" % i
            return

    groups = []
    for scale in scales:
        for group in scales[scale][1]:
            groups.append(group)
    groups = list(set(groups))
    groups.sort()

    if page.strip().lower() == "main":# print out the filter list, but don't do any filtering.
    
        print "using notes: %s <br /><br />" % pretty(notes, default_encoding)
        
        #filter list.
        print '<table class="filters">'
        print '<tr class="filters"><th class="filters" colspan=50>Music Filter</td></tr>'
        print '<tr class="filters">'
        for i, group in enumerate(groups):
            print '<td class="filters"><input type="checkbox" class="filterbox" \
            checked id="filter%i" onClick="updateScales();">%s</input></td>' % (i, group)
        print '</tr></table>'
        print '<input type="hidden" id="grps" value="%s" />' % len(groups)
        
        print '<div id="scalesdiv">'

        #scale filter
        scalenames = scales.keys()
        
    elif page == "filtered": #just print out the (filtered) scales table.
        
        valid_groups = []
        for i, group in enumerate(groups):
            try:
                temp = form.getvalue("filter%i" % i).strip()
                if temp == "true":
                    valid_groups.append(group)
            except:
                print "Error processing music filters."
                return
                
        valid_groups = frozenset(valid_groups)
                
        scalenames = []
        for scale in scales:
            if valid_groups.intersection(set(scales[scale][1])):
                scalenames.append(scale)


    else:
        #they specified an invalid page name.
        print "404 - Page %s could not be found!" % page
        
    #scales result table.
    print '<table class="scales">'
    print '<tr class="scales">'
    print '<th scope="col" class="scales">Scale Name</th>'
    print '<th scope="col" class="scales">Music</th>'
    print '<th scope="col" class="scales">Matching Scales</th></tr>'

    scalenames.sort()
    for scale in scalenames:
        matched = []
        for s in get_scales(scales[scale][0]):
            tempscale = []
            found = []
                
            current = 0
            
            for note in s:
                if consecutive and current > 0:
                    if current < len(notes) and note != notes[current]:
                        # if we're still looking for notes, and
                        #the current note doesn't match...
                        found = []
                        break
                        
                if order:
                # monitor the current note and only allow the note to be added if the notes are
                #in the correct order.
                    if note == notes[min(len(notes) - 1, current)]:
                        tempscale.append((note, 1))
                        # tempscale contains a tuple which lets the program know if
                        #it should highlight that note or not.
                        found.append(note)
                        current += 1
                        
                    else:
                        if note in notes:
                            tempscale.append((note, 1))
                        else:
                            tempscale.append((note, 0))
                            
                else:
                    if note in notes:
                        tempscale.append((note, 1))
                        found.append(note)
                        current += 1
                        
                    else:
                        tempscale.append((note, 0))
                        
            if len(set(found)) == len(notes): #use a set so it supports scales that repeat notes as well as those that don't.
                #it was a match, so add the scale to our list.
                matched.append(tempscale)
                
        if len(matched) > 0: # there were valid matches so print them out.
            print '<tr class="scales">'
            print '<td class="scales">%s</td><td class="scales">%s</td>' % (scale, ", ".join(scales[scale][1]))
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
    
    
printPage()