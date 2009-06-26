#!/usr/local/bin/python

import sys, copy
from musiclib import *
from scaleslib import *


import cgi, cgitb
cgitb.enable()

print "Content-type: text/html"
print



default_encoding = {0:"A", 1:"A#", 2:"B", 3:"C", 4:"C#", 5:"D", 6:"D#", 7:"E", 8:"F", 9:"F#", 10:"G", 11:"G#"}

def pretty(notes, encoding):
    ' notes is int array, encoding is a dict such as {0:"A", 1:"A#" ... 11:"G#"}'
    return " ".join([encoding[i] for i in notes])

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
    
    

# Create instance of FieldStorage 
form = cgi.FieldStorage() 



def printPage():

    try:
        # Get data from fields
        page = form.getvalue('page').strip().lower()
        temp = form.getvalue('notes').strip()
    
    except:
        print "Unable to process input parameters."
        return
    
    
    notes = []
    for i in temp.split():
        i = i.strip()
        if len(i) == 2:
            i = i[0].upper() + i[1].lower()
        elif len(i) == 3:
            i = i[0].upper() + i[1].lower() + i[2].lower()
        elif len(i) > 3:
            print "You entered an invalid note: %s" % i
            return
        try:
            if not all_notes[i] in notes:
                notes.append(all_notes[i])
        except KeyError:
            print "You entered an invalid note: %s" % i
            return

    groups = []
    for scale in scales:
        for group in scales[scale][1]:
            groups.append(group) #bogus value, just exploiting uniqueness of dict keys.
    groups = list(set(groups))
    groups.sort()

    if page.strip().lower() == "main":# print out the filter list, don't do any filtering.
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
        print "404 - Page %s could not be found!" % page
        
        
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