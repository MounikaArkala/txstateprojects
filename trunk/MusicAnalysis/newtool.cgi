#!/usr/local/bin/python
# -*- coding: cp1252 -*-
#!"C:/python26/python.exe"
import os, cgi
from libs import structure
from musiclib import all_notes
from libs import prime_forms

# Debug code, shouldn't be included unless testing.
import cgitb
cgitb.enable()
    
    
    
debug = False

#TODO: 
#!---------------------------
#!---------------------------

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
    if debug:
        print "<hr />"
        print "Calculating Rahn..."
        print "<br />"
    if index == None:
        index = 0 # initial index.
    if len(candidates[0]) == 12: #TODO: fix stopping case in a less clunky way (12 notes should end just as gracefully as 11 notes...)
        return candidates[0]
        
        
    old_candidates = candidates[:]
    if index < 0:
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
        
        if debug:
            print "Multiple items have the same minimum outside interval..."
            print "<br />"
            print "Candidates:", old_candidates
            print "<br />"
            print "candidate_lengths: ", candidate_lengths
            print "<br />"
            print "min_candidate: ", min_candidate
            print "<br />"
            print "min_candidates: ", min_candidate
            print "<br />"
        
        if len(min_candidates) == 1:
            return old_candidates[candidate_lengths.index(min_candidate)]
        
        else:
            #multiple items have the same (minimum) outside interval.
            if debug:
                print "Multiple items still have the same minimum outside interval."
            temp = []
            #build a list of all the ones that have the same outside interval.
            for i in range(len(candidate_lengths)):
                if candidate_lengths[i] == min_candidate:
                    temp.append(old_candidates[i])
            if debug:
                print "<br /> The items are: ", temp, "<br />"
                print "recursing..."
            
            if len(candidates[0]) <= 2:
                return candidates[0]#todo make this better?
            
            return calc_rahn(temp, index-1)
        return chosen
        
        
    
def calc_forte(candidates):
    if debug:
        print "<hr />"
        print "Calculating Forte..."
        print "<br />"
    old_candidates = candidates
    
    if len(candidates[0]) == 12: #TODO: fix stopping case in a less clunky way (12 notes should end just as gracefully as 11 notes...)
        return candidates[0]
        
    candidate_lengths = [sum(intervals(candidate)) for candidate in candidates]
    min_candidate = min(candidate_lengths)
    # check how many items meet candidate_lengths
    min_candidates = [candidate for candidate in candidates if sum(intervals(candidate)) == min_candidate]
        
    if len(min_candidates) == 1:
        return old_candidates[candidate_lengths.index(min_candidate)]
    
    else:
        if debug:
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
    
    

def getPrime(candidate):  # get the prime form of an input.
    prime1 = [0]
    for item in candidate[1:]:
        prime1.append((item - candidate[0]) % 12)
    
    temp = [i for i in prime1] # copy it
    temp.reverse()
    prime2 = [0]
    for item in temp[1:]:
        prime2.append((temp[0] - item) % 12)
        
    if debug:
        print "prime candidate 1: ", prime1, "<br />"
        print "Prime candidate 2: ", prime2, "<br />"
    
    prime = prime1#compare pairwise and choose whichever one is packed more to the left.
    for i, item in enumerate(prime1):
        if prime2[i] < item:
            prime = prime2
            break
        elif prime2[i] > item:
            break
    return prime
    
    
     
def printPrime(orig, prime, encoding, header): #output a prime's information.
    temp = None
    try:
        temp = prime_forms.forms[tuple(prime)]
    except:
        print "<h2> header </h2>"
        print "Normal Form: ", pretty(orig, encoding), "<br />"
        print tuple(prime), "is the prime form. <br /> "
        print "this prime form was not found in the prime forms list.<br />"
        
    if temp != None:
    
        print "<table class='primes'>"
        print "<tr class='primes'><th class='primes' colspan=2>%s</th> </tr>" % header
        print "<tr class='primes'><td class='primes'>Normal Form</td><td class='primes2'>", pretty(orig, encoding), "</td></tr>"
        print "<tr class='primes'><td class='primes'>Prime Form</td><td class='primes2'>%s</td></tr>" % " ".join([str(i) for i in prime])
        print "<tr class='primes'><td class='primes'>Forte Name</td><td class='primes2'>%s</td></tr>" % temp[0]
        print "<tr class='primes'><td class='primes'>Distinct Forms</td><td class='primes2'>%s</td></tr>" % temp[1]
        iv = []
        for i in vector(prime):
            if i >= 10:
                i -= 10
                try:
                    iv.append('ABCDEFGHIJKLMNOPQRSTUVWXYZ'[i])
                except:
                    iv.append(' ' + str(i+10) + ' ')
            else:
                iv.append(str(i))
        print "<tr class='primes'><td class='primes'>Interval Vector</td><td class='primes2'>%s</td></tr>" % "".join(iv)
        print "</table>"
    #if debug:
    #    print "<hr />"
    #else:
    #    print "<br />"
    
    
    
    
    
    
#!---------------------------
#!---------------------------
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
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
    global notes, wraparound
    if len(notes) == 0:
        return
    encoding = {}
    temp = []
    for note in notes:
        i = note.strip()
        i = i[0].upper() + i[1:].lower()
        try:
            encoding[(all_notes[i]-3) % 12] = i
            temp.append((all_notes[i]-3) % 12)
            """
            
            encoding[all_notes[i]] = i
            temp.append(all_notes[i])
            """
            
        except KeyError:
            print '<h2 class="error">You entered an invalid note: %s</h2>' % i
            return
    notes = temp
    if len(set(notes)) < 12:
        print '<h2 class="error">Not enough notes for calculation!  Enter 12 unique notes.</h2>'
        return
        
    # print '<div id="symmdiv">'
    print "original row: ", pretty(notes, encoding)
    print "wraparound: ", wraparound
    


    #notes = map(str, notes)
    notes.extend(notes)
    print "<br />", notes, "<br />"
    print '<table class="primes">'
    print '<tr class="primes">'
    print '<td class="primes">Forte Code</td><td class="primes">Prime form</td><td class="primes">Inversion form</td><td class="primes">Interval Vector</td><td  class="primes" colspan=12>pitches</td>'
    print '</tr>'
    for length in range(2,13):
        ranges = range(13-length)
        totalvecs = [0,0,0,0,0,0]
        if wraparound:
            ranges = range(12)
            if length == 12:
                ranges = range(1)
        for i in ranges:
            print '<tr class="primes">'
            line = []
            selected_notes = notes[i:i+length]
            #TODO: clean this up.
            if i+length > 12:
                line.extend([encoding[j] for j in notes[12:i+length]])
                line.extend([""]*(12-len(line) - (12-i)))
                line.extend([encoding[j] for j in notes[i:12]])
            else:
                line.extend([""]*i)
                line.extend([encoding[j] for j in notes[i:i+length]])
                line.extend([""]*(12-i-length))
                
            temp = list(set(selected_notes))
            temp.sort()
            candidates = [temp[j:len(temp)] + temp[0:j] for j in range(len(temp))]
            
            rahn = calc_forte(candidates)
            rprime = getPrime(rahn)
            victor = vector(rprime)
            try:
                forte = prime_forms.forms[tuple(rprime)][0]
            except:
                forte = "N/A"
            for x,v in enumerate(victor):
                totalvecs[x] += v
                
            
            iv = []
            for j in vector(rprime):
                if j >= 10:
                    j -= 10
                    try:
                        iv.append('ABCDEFGHIJKLMNOPQRSTUVWXYZ'[j])
                    except:
                        iv.append(' ' + str(j+10) + ' ')
                else:
                    iv.append(str(j))
                    
            print '<td class="primes">%s</td>' % str(forte) # forte code
            print '<td class="primes">%s</td>' % repr(tuple(rprime)) # prime form
            print '<td class="primes">%s</td>' % "N/A" # inversion form
            print '<td class="primes">%s</td>' % "".join(iv) # interval vector
            print '<td class="primes">%s</td>'*12 % tuple(line)
            print "</tr>"
        print '<tr class="primes"><td class="primes" colspan=3>Interval Vector Total:</td><td class="primes" colspan=13>%s</td></tr>' % repr(totalvecs)
        print "<tr><td colspan=16></td></tr>"
    print '</table>'
        
    # print '</div> <!-- ~symmdiv -->'
    
    
structure.print_header(title="New Tool by Nico Schuler and Luke Paireepinart",
                       scripts=["main.js"], css=["main.css", 'newtool.css'])

                       
                  

                       
try:
    # Get data from fields
    notes = form.getvalue('notes').strip().lower().split()
    try:
        wraparound = (form.getvalue('wraparound').strip().lower() == "on")
    except:
        wraparound = False

    
except:
    notes = []
    #main page.
    from scales.filters import filters
    structure.print_body("newtool/main.html")
       

printPage()
structure.print_footer()