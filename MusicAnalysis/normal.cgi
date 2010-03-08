#!/usr/local/bin/python
# -*- coding: cp1252 -*-
#!"C:/python26/python.exe"
import os, cgi
from libs import structure
from musiclib import all_notes
from normal import prime_forms
# Debug code, shouldn't be included unless testing.
debug = False

if debug:
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
     
     
"""
 def printPrime(orig, prime, encoding):
    print "<table class='primestable'>"
    print "<tr><td>Normal Form</td><td>", pretty(orig, encoding), "</td></tr>"
    try:
        temp = prime_forms.forms[tuple(prime)]
        print "Prime Form: %s<br />" % " ".join([str(i) for i in prime])
        print "Forte Name: %s<br />" % temp[0]
        print "Distinct Forms: %s<br />" % temp[1]
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
        print "Interval Vector: %s<br />" % "".join(iv)
        
    except:
        print tuple(prime), "is the prime form.  "
        print "this prime form was not found in the prime forms list."
    
    if debug:
        print "<hr />"
    else:
        print "<br />"
"""
     
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
    if len(set(notes)) < 2:
        print '<h2 class="error">Not enough notes for calculating normal form!  Enter at least 2 unique notes.</h2>'
        return
      
    if debug:
        print "Input: "
        print pretty(notes, encoding)
    noteslen = len(notes)
    notes = list(set(temp))
    if len(notes) < noteslen:
        print "<br />You entered some duplicate notes, discarding duplicates...<br />"
    #reorder notes
    notes.sort()
    if debug:
        print '<hr />'
        print "Sorted Notes: ", pretty(notes, encoding), "<br />"
        print '<hr />'
    
    else:
        print "<br /><br /><br />"
    
    candidates = [notes[i:len(notes)] + notes[0:i] for i in range(len(notes))]
    if debug:
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
    
    
    
    
    if debug:
        print "<hr />"
        print "rahn func returned", rahn
        print "<br />"
        print "forte func returned", forte
        print '<hr />'
        
        
    #if rahn and forte are different, display both, otherwise just display 1.
    rprime = getPrime(rahn)
    fprime = getPrime(forte)
    
    if rprime == fprime: #they're combined!
        printPrime(rahn, rprime, encoding, "Rahn/Forte")
    else:
        printPrime(rahn, rprime, encoding, "Rahn")
        print "<br />"
        printPrime(forte, fprime, encoding, "Forte")
        
    
    
    
structure.print_header(title="Analysis of Normal Form, Normal Order, and Prime Form of Sets: Web-Based Analytical Tool for Set Theory by Nico Schuler and Luke Paireepinart",
                       scripts=["main.js","normal.js"], css=["main.css", "normal.css"])

                       
                  
if debug:
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