#!"C:/python26/python.exe"
# -*- coding: cp1252 -*-
#!/usr/local/bin/python
import os, cgi
from libs import structure
from musiclib import all_notes

# Debug code, shouldn't be included unless testing.
import cgitb
cgitb.enable()
    
    
def pretty(notes, encoding):
    ' notes is int array, encoding is a dict such as {0:"A", 1:"A#" ... 11:"G#"}'
    return " ".join([encoding[i] for i in notes])


# Create instance of FieldStorage 
form = cgi.FieldStorage()
def rotations(notes):
    results = [notes[:]]
    for i in range(len(notes) - 1):
        temp = [results[-1][1]]
        temp.extend(results[-1][2:])
        temp.append(results[-1][0])
        results.append(temp)
    return results
    
def printPage():
    global notes, order
    if len(notes) == 0:
        return
    encoding = {0:"A", 1:"A#", 2:"B", 3:"C", 4:"C#", 5:"D", 6:"D#", 7:"E", 8:"F", 9:"F#", 10:"G", 11:"G#"}
    temp = []
    for note in notes:
        i = note.strip()
        i = i[0].upper() + i[1:].lower()
        try:
            encoding[all_notes[i]] = i
            temp.append(all_notes[i])
        except KeyError:
            print '<h2 class="error">You entered an invalid note: %s</h2>' % i
            return
    notes = temp
    if len(notes) < 3:
        print '<h2 class="error">Not enough notes for checking symmetry!  Enter at least 3 notes.</h2>'
        return
    symmetrical = []
    if order:
        
        rots = rotations(notes)
        for rotation in rots:
            #print rotation
            intervals = []
            prev = rotation[0]
            for note in rotation[1:]:
                if note < prev:
                    prev -= 12
                intervals.append(note-prev)
                prev = note
            
            matched = True
            for i in range(len(intervals) / 2):
                #print "comparing %s to %s.<br />" % (intervals[i], intervals[-i-1])
                if intervals[i] != intervals[-i-1]:
                    #print "no match!"
                    matched = False
                    break
            if matched:
                symmetrical.append(rotation)
        
        

    else:
        notes = list(set(notes))
        notes.sort()
        #Debug print pretty(notes, encoding)
        rots = rotations(notes)
        #Debug print rots
        
        #check symmetry of each.
        if len(notes) < 3:
            print '<h2 class="error">Not enough notes for checking symmetry!  Enter at least 3 unique notes.</h2>'
            return
        iterations = len(notes) / 2
        if len(notes) % 2 == 0:
            iterations -= 1
                
        for rotation in rots:
            matched = True
            for i in range(iterations):
                #Debug print "<br /><hr />"
                first = rotation[i]
                next = rotation[i+1]
                if next < first:
                    next += 12
                interval = next - first
                #Debug print "%i interval for " % i, pretty(rotation, encoding), " is", interval
                first = rotation[-i-2]
                next = rotation[-i-1]
                if next < first:
                    next += 12
                interval2 = next - first
                #Debug print "%i interval for " % (-i-1), pretty(rotation, encoding), " is", interval2
            
                if interval != interval2:
                    matched = False
                    break
            if matched:
                symmetrical.append(rotation)
                

                
    """debug        
    for s in symmetrical:
        print "<br /><hr />"
        print pretty(s, encoding)
    print "<br /><hr />"
    """
    
    if len(symmetrical) < 1:
        print '<h2 class="error">None of the rotations of %s are symmetrical!</h2>' % pretty(notes, encoding)
        return
    
    print '<div id="symmdiv">'
    if order:
        print "Symmetrical rotations - with preserved input order - of "
    else:
        print "Symmetrical rotations of "
    print '<table class="symm">'
    print '<tr class="symm">'
    for note in notes:
        print '<td class="symm">%s</td>' % encoding[note]
    print '</tr></table>'
    
    print "<hr /><br />"
    for rotation in symmetrical:
        if len(rotation) % 2 == 0:
            first = rotation[len(rotation) / 2 - 1]
            second = rotation[len(rotation) / 2]
            if second < first:
                second += 12
            axis = second - first
            axis /= 2.
            axis += first
            if axis != int(axis): # has a .5 left over
                axis1 = int(axis)
                axis2 = axis1 + 1
            else:
                axis1 = axis2 = axis
            
            axis1 %= 12
            axis2 %= 12
                
        print '<table class="symm">'
        print '<tr class="symm">'
        for i in range(len(rotation)):
            #even-length items must be handled differently.
            if len(rotation) % 2 == 0:
                if i == (len(rotation) / 2 - 1):
                    print '<td class="symm">%s</td>' % encoding[rotation[i]]
                    print '<td class="exaxis">%s/%s</td>' % (encoding[axis1] , encoding[axis2])
                else:
                    print '<td class="symm">%s</td>' % encoding[rotation[i]]
            else:
                if i == len(rotation) / 2:
                    print '<td class="inaxis">%s</td>' % (encoding[rotation[i]])
                else:
                    print '<td class="symm">%s</td>' % encoding[rotation[i]]
        print '</tr></table>'
        
    print '</div> <!-- ~symmdiv -->'
    
    
structure.print_header(title="Analysis of Symmetry in Music: Web-Based Analytical Tool for the Calculation of the Axis of Symmetry by Nico Schuler and Luke Paireepinart",
                       scripts=["main.js","symmetry.js"], css=["main.css", "symmetry.css"])

                       
                  

                       
try:
    # Get data from fields
    notes = form.getvalue('notes').strip().lower().split()
    try:
        order = (form.getvalue('order').strip().lower() == "on")
    except:
        order = False

    
except:
    notes = []
    #main page.
    from scales.filters import filters
    structure.print_body("symmetry/main.html")
       

printPage()
structure.print_footer()