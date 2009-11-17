#!/usr/local/bin/python
# -*- coding: cp1252 -*-
#!"C:/python26/python.exe"
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


    
def intervals(notes):
    ints = []
    for i in range(len(notes)-1):
        ints.append((notes[i+1]-notes[i]) % 12)
    return ints
    
def vector(notes):
    vectors = [0]*6
    for i in range(len(notes)-1):
        for j in range(i+1, len(notes)):
            vectors[(((notes[j]-notes[i]) % 12) -1) % 6] += 1
    return vectors
     
def printPage():
    global notes, order
    if len(notes) == 0:
        return
        
    encoding = {0:"C", 1:"C#", 2:"D", 3:"D#", 4:"E", 5:"F", 6:"F#", 7:"G", 8:"G#", 9:"A", 10:"A#", 11:"B"}
    temp = []
    for note in notes:
        i = note.strip()
        i = i[0].upper() + i[1:].lower()
        try:
            #  our all_notes refers to notes from base A but we refer to them as base C.
            encoding[(all_notes[i]-3) % 12] = i
            temp.append((all_notes[i]-3) % 12)
        except KeyError:
            print '<h2 class="error">You entered an invalid note: %s</h2>' % i
            return
    notes = temp
    if len(notes) < 2:
        print '<h2 class="error">Not enough notes for calculating normal form!  Enter at least 2 notes.</h2>'
        return
      
    print "Input: "
    print pretty(notes, encoding)
    print '<hr />'
    if not order:
        print "Order was not preserved, so we reorder notes.<br />"
        notes.sort()
        print "Notes are now: ", pretty(notes, encoding), "<br />"
    else:
        print "Order was preserved, so we leave the notes alone."
    print '<hr />'
    candidates = [notes[i:len(notes)] + notes[0:i] for i in range(len(notes))]
    print "Possible ascending orderings<hr />"
    
    
    original_candidates = candidates
    chosen = None
    #loop until we run out of items, or find the minimum result. we do 'til -1 because an interval is only defined if 2 notes are present.
    for i in range(len(notes)-1):
        
        for candidate in candidates:
            print pretty(candidate, encoding), ": "
            print "intervals ", intervals(candidate)
            print ", vector ", "".join([str(i) for i in vector(candidate)])
            print ", outside interval ", sum(intervals(candidate))
            print "<br />"
           
    
        candidate_lengths = [sum(intervals(candidate)) for candidate in candidates]
        min_candidate = min(candidate_lengths)
        # check how many items meet candidate_lengths
        if len([i for i in candidate_lengths if i == min_candidate]) == 1:
            chosen = original_candidates[candidate_lengths.index(min_candidate)]
            break
        print "multiple items have the same (minumum) outside interval! reducing length and recalculating...<hr />"
        #there were too many matches so let's pop one off the end of all our candidates.
        temp = []
        for candidate in candidates:
            temp.append(candidate[:-1])
        candidates = temp
        
    if not chosen:
        print 'choosing the interval vector with the least first pc integer...'
        # first get a list of all the colliding ones
        candidate_lengths = [sum(intervals(candidate)) for candidate in original_candidates]
        min_candidate = min(candidate_lengths)
        colliding = [i for i in original_candidates if sum(intervals(i)) == min_candidate]
        chosen = colliding[0]
        for c in colliding[1:]:
            if c[0] < chosen[0]:
                chosen = c
        print "Chose", pretty(chosen, encoding)
    print '<hr />'
    print pretty(chosen, encoding), "is the normal form."
    print '<hr />'
    
    #if chosen is still None by this point we weren't able to find a candidate.
    
    
    #print notes
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
    """
    
    
structure.print_header(title="normal",
                       scripts=["main.js","normal.js"], css=["main.css", "normal.css"])

                       
                  

print "<font color='red'> This tool is currently under testing!<br /></font>"
                       
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
    structure.print_body("normal/main.html")
       

printPage()
structure.print_footer()