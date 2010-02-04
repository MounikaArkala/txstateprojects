#!/usr/local/bin/python
# -*- coding: cp1252 -*-
#!"C:/python26/python.exe"
import os, cgi
from libs import structure
from musiclib import all_notes
from normal import prime_forms
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
    #calculates the interval vector of an input set of notes.
    vectors = [0]*6
    for i in range(len(notes)-1):
        for j in range(i+1, len(notes)):
            offset = ((notes[j]-notes[i]) % 12)
            if offset == 0:
                continue
            offset -= 1
            if offset > 5:
                offset = 10 - offset
            vectors[offset] += 1
    return vectors
     
def calc_rahn(candidates, index=None):
    print "<hr />"
    print "Calculating Rahn..."
    print "<br />"
    if index == None:
        index = -1 # initial index.
        
        
    old_candidates = candidates
    candidates = [candidate[:index] for candidate in candidates]
    if len(candidates[0]) == 1:
        #return the candidate with least-most first item.
        min_item = 0
        for x, candidate in old_candidates:
            if candidate[0] < old_candidates[min_item][0]:
                min_item = x
        return old_candidates[x]
        
    else:
                   
        candidate_lengths = [sum(intervals(candidate)) for candidate in candidates]
        min_candidate = min(candidate_lengths)
        # check how many items meet candidate_lengths
        min_candidates = [candidate for candidate in candidates if sum(intervals(candidate)) == min_candidate]
        
        if len(min_candidates) == 1:
            return old_candidates[candidate_lengths.index(min_candidate)]
        
        else:
            #multiple items have the same (minimum) outside interval.
            print "Multiple items have the same minimum outside interval."
            temp = []
            #build a list of all the ones that have the same outside interval.
            for i in range(len(candidate_lengths)):
                if candidate_lengths[i] == min_candidate:
                    temp.append(old_candidates[i])
            print "<br /> The items are: ", temp, "<br />"
            print "recursing..."
            return calc_rahn(temp, index-1)
        return chosen
    
def calc_forte(candidates):
    print "<hr />"
    print "Calculating Forte..."
    print "<br />"
    old_candidates = candidates
    
    candidate_lengths = [sum(intervals(candidate)) for candidate in candidates]
    min_candidate = min(candidate_lengths)
    # check how many items meet candidate_lengths
    min_candidates = [candidate for candidate in candidates if sum(intervals(candidate)) == min_candidate]
        
    if len(min_candidates) == 1:
        return old_candidates[candidate_lengths.index(min_candidate)]
    
    else:
        
        #multiple items have the same (minimum) outside interval.
        print "Multiple items have the same minimum outside interval."
        temp = []
        #build a list of all the ones that have the same outside interval.
        for i in range(len(candidate_lengths)):
            if candidate_lengths[i] == min_candidate:
                temp.append(old_candidates[i])
        old_candidates = temp
        
        for i in range(1, len(candidates) - 1):
            candidates = [candidate[:i+1] for candidate in old_candidates]
            
            candidate_lengths = [sum(intervals(candidate)) for candidate in candidates]
            min_candidate = min(candidate_lengths)
            # check how many items meet candidate_lengths
            min_candidates = [candidate for candidate in candidates if sum(intervals(candidate)) == min_candidate]
                
            if len(min_candidates) == 1:
                return old_candidates[candidate_lengths.index(min_candidate)]
            
            else:
                temp = []
                #build a list of all the ones that have the same outside interval.
                for i in range(len(candidate_lengths)):
                    if candidate_lengths[i] == min_candidate:
                        temp.append(old_candidates[i])
                                
        return old_candidates[0]
    #hopefully we never get here.
     
def printPage(notes):
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
    #reorder notes
    notes.sort()
    print "Sorted Notes: ", pretty(notes, encoding), "<br />"
    print '<hr />'
    
    
    
    candidates = [notes[i:len(notes)] + notes[0:i] for i in range(len(notes))]
    print "Candidates:<br />"
    for candidate in candidates:
        print pretty(candidate, encoding), ": "
        print "intervals ", intervals(candidate)
        print ", vector ", "".join([str(i) for i in vector(candidate)])
        print ", outside interval ", sum(intervals(candidate))
        print "<br />"
    print "<hr />"
    
    rahn = calc_rahn(candidates)
    forte = calc_forte(candidates)
    
    
    
    
        
        
    print '<hr />'
    print "<h2>Rahn</h2>"
    print "Normal Form : ", pretty(rahn, encoding), "<br />"
    
    prime1 = [0]
    for item in rahn[1:]:
        prime1.append((item - rahn[0]) % 12)
    
    temp = [i for i in prime1] # copy it
    temp.reverse()
    prime2 = [0]
    for item in temp[1:]:
        prime2.append((temp[0] - item) % 12)
    print "prime candidate 1: ", prime1, "<br />"
    print "Prime candidate 2: ", prime2, "<br />"
    
    prime = prime1
    for i, item in enumerate(prime1):
        if prime2[i] < item:
            prime = prime2
            break
        elif prime2[i] > item:
            break
            
        
    try:
        temp = prime_forms.forms[tuple(prime)]
        print "<br />Prime Form: %s" % " ".join([str(i) for i in prime])
        print "<br />Forte Name: %s" % temp[0]
        print "<br />Distinct Forms: %s" % temp[1]
        print "<br />Interval Vector: %s" % "".join([str(i) for i in vector(prime)])
        
    except:
        print tuple(prime), "is the prime form.  "
        print "this prime form was not found in the prime forms list."
    
    
    print "<hr />"
    print "<h2>Forte</h2>"   
    print "Normal Order: ", pretty(forte, encoding), "<br />"
    
    prime1 = []
    for item in forte:
        prime1.append((item - forte[0]) % 12)
    
    temp = [i for i in prime1] # copy it
    temp.reverse()
    prime2 = [0]
    for item in temp[1:]:
        prime2.append((temp[0] - item) % 12)
    print "prime candidate 1: ", prime1, "<br />"
    print "Prime candidate 2: ", prime2, "<br />"
        
    prime = prime1
    for i, item in enumerate(prime1):
        if prime2[i] < item:
            prime = prime2
            break
        elif prime2[i] > item:
            break
    
    
    
    try:
        temp = prime_forms.forms[tuple(prime)]
        print "<br />Prime Form: %s" % " ".join([str(i) for i in prime])
        print "<br />Forte Name: %s" % temp[0]
        print "<br />Distinct Forms: %s" % temp[1]
        print "<br />Interval Vector: %s" % "".join([str(i) for i in vector(prime)])
        
    except:
        print tuple(prime), "is the prime form.  "
        print "this prime form was not found in the prime forms list."
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
    
    
structure.print_header(title="Analysis of Normal Form, Normal Order, and Prime Form of Sets: Web-Based Analytical Tool for Set Theory by Nico Schuler and Luke Paireepinart",
                       scripts=["main.js","normal.js"], css=["main.css", "normal.css"])

                       
                  

print "<font color='red'> This tool is currently under testing!<br /></font>"
                       
try:
    # Get data from fields
    notes = form.getvalue('notes').strip().lower().split()
    
except:
    notes = []
    #main page.
    structure.print_body("normal/main.html")
       

printPage(notes)
structure.print_footer()