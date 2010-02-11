#!/usr/local/bin/python
# -*- coding: cp1252 -*-
#!"C:/python26/python.exe"
""" Primes.cgi
----------------------------
Author:    Luke Paireepinart
Copyright: Nico Schuler

Texas State University
Summer 2009
----------------------------
Brief Summary:  This program generates 12-tone matrices, and allows the user
to search through them for different specific primes/retrogrades or inversions of those.
Expects a website as output and frontend.
"""
import sys, urllib
from libs import structure
from musiclib import *
import cgi

# Debug code, shouldn't be included unless testing.
import cgitb
cgitb.enable()


def pretty(notes, encoding):
    #notes is int array, encoding is a dict such as {"A":0, "A#":1 ... "G#":11}
    temp = "    <td class=\"primesdata\">%s</td>\n" * len(notes)
    return temp % tuple([encoding[i] for i in notes])
    
def printPage():
    global row, normal, absolute, wrap
    #this is a function so it can be "return'd" from.
    #it's a bit of an exploitation of a function for a control flow advantage but
    #I feel it greatly simplifies the code in this case.

    #set up encoding.
    encoding = {}
    for note in row.split():
        i = note.strip()
        i = i[0].upper() + i[1:].lower()
        try:
            encoding[all_notes[i]] = i
        except KeyError:
            print "You entered an invalid note: %s" % i
            return

    temp = row.split()
    if len(temp) != 12: # tone rows must be exactly 12 notes long.
        print "You must enter exactly 12 notes."
        return
    
    
    rownumerals = []
    for i in temp:
        i = i.strip()
        i = i[0].upper() + i[1:].lower()
        try:
            rownumerals.append(all_notes[i])
        except KeyError:
            print "You entered an invalid note: %s" % i
            return

    #print "Rownumerals: ", rownumerals, "<br />"
   # print "inversion: ", inversion(rownumerals, 0),"<br />"
    
    if len(set(rownumerals)) != 12:
        #TODO: figure out which notes they entered that were duplicates.
        print "You must enter exactly 12 UNIQUE notes."
        return
        
    # store all primes by starting note
    allprimes = []
    
    #realign rownumerals...
    labels = rownumerals[:]
    shiftamt = rownumerals[0]
    labels = [(i-shiftamt) % 12 for i in labels] 
    
    for x in range(12):
        allprimes.append(prime(labels, x))
    

    #display the primes table and the search fields.
    
    #TODO: fix these links so they preserve queries.
    if absolute:
        print '<br />12-Tone Table (Absolute)'
    else:
        print '<br />12-Tone Table<br />'
    # primes table
    print "<table class=\"primes\">"
    print "  <tr class=\"primesrow\">"
    #pretty-print columns in correct order.
    print "    <td />"
    # add headers to row so it looks nice.
    
        
    inv = inversion(rownumerals, 0)
    invlabels = inversion(labels, 0)
    
    
    #if absolute we just assume that the first row of the table has the labels we want.
    if absolute:
        print "".join([("    <th class=\"primesheader\">I<sub>%s</sub></th>\n" % ((i - 3) % 12))for i in rownumerals]) # we normally assume A = 0 but in this case C = 0 so shift by 3.
    else:
        print "".join([("    <th class=\"primesheader\">I%s</th>\n" % i) for i in labels])
    
    print "  </tr>"
    
    
    for item in range(12):
        print "  <tr class=\"primesrow\">"
        # add headers to first and last column so it looks nice.
        if absolute:            
            print "    <th class=\"primesheader\">P<sub>%s</sub></th>\n" % ((allprimes[inv[item]][0] - 3) % 12)
        else:
            print "    <th class=\"primesheader\">P%s</th>\n" % invlabels[item]
            
        print pretty(allprimes[inv[item]], encoding)
        if absolute:
            print "    <th class=\"primesheader\">R<sub>%s</sub></th>\n" % ((allprimes[inv[item]][0] - 3) % 12)
        else:
            print "    <th class=\"primesheader\">R%s</th>\n" % invlabels[item]
        print "  </tr>"
        
        
    print "    <td />"
    if absolute:
        print "".join([("    <th class=\"primesheader\">RI<sub>%s</sub></th>\n" % ((i - 3) % 12))for i in rownumerals]) # we normally assume A = 0 but in this case C = 0 so shift by 3.
    
    else:
        print "".join([("    <th class=\"primesheader\">RI%s</th>\n" % i)for i in labels])
    print "  </tr>"
    print "</table>"
    
    if absolute:
        print '<a href="./12tone.cgi?notes=%s&normal=on">Switch to %s is P0</a><br />' % (urllib.quote_plus(row), encoding[rownumerals[0]])
    else:
        print '<a href="./12tone.cgi?notes=%s&absolute=on">Switch to C is P0</a><br />' % urllib.quote_plus(row)
    
    
    
    
    
    
    print '<br />'
    print '<div id="searchborder">'
    print '<div id="searchheader">'
    print 'Search table for a series of notes'
    print '<form name="search" id="search" action="12tone.cgi" method="get">'
    print '<input class="TextInput" type="text" name="series" id="series" size="40" onkeypress="handleEnter(event, document.search.submit);" value="%s" />' % " ".join(series)
    print '<input class="SubmitButton" type="submit" value="Submit" />'
    print '</div> <!-- ~searchheader -->'
    print '<div id="searchcheck">'
    if order:
        print 'Match Input Order <input type="checkbox" checked name="order" id="order"><br />'
    else:
        print 'Match Input Order <input type="checkbox" name="order" id="order"><br />'
    if wrap:
        print 'Allow Rotations (Wrap-Around) <input type="checkbox" checked name="wrap" id="wrap"><br />'
    else:
        print 'Allow Rotations (Wrap-Around) <input type="checkbox" name="wrap" id="wrap"><br />'
    print '</div> <!-- ~searchcheck -->'
    print '<input type="hidden" name="notes" id="notes" value="%s" />' % row
    if absolute:
        print '<input type="hidden" name="absolute" id="absolute" value="on" />'
    if normal:
        print '<input type="hidden" name="normal" id="normal" value="on" />'
		
    print '</form>'
    print '</div> <!-- ~searchborder -->'
    print '<div id="primesdiv">'
    
    #process input parameters
    if page == "od" or page == "oid": 
        notes = []
        for i in series:
            i = i.strip()
            if len(i) == 2:
                i = i[0].upper() + i[1].lower()
            elif len(i) > 2:
                print '<div id="occurrence">You entered an invalid note: %s</div>' % i
                return
            try:
                notes.append(all_notes[i])
            except KeyError:
                print '<div id="occurrence">You entered an invalid note: %s</div>' % i
                return
    
    #display ordered search results.
    if page == "od":
        print '<div id="occurrence">Occurrences of <table class="primesresult">' + pretty(notes, encoding) + "</table><br />"
        result = detect(rownumerals, notes, wrap)
        if len(result) == 0:
            print "No occurrences were found!<br />"
        for item in detect(rownumerals, notes, wrap):
            markupstr = '<table class="primesresult"><tr>%s</tr></table>'
            datastr = ""
            wraparound = 0
            if item[2] + len(series) > 12:
                wraparound = (item[2] + len(series)) % 12
            for i in range(12):
                if (i >= item[2] and i < (item[2] + len(series))) or i < wraparound:
                    datastr += '<td class="primesresulty">' + encoding[item[3][i]] + '</td>'
                else:
                    datastr += '<td class="primesresultn">' + encoding[item[3][i]] + '</td>'
            print "%s %i <div>%s</div> <br />" % (item[0], item[1], markupstr % datastr)

        print "</div>"
        

    #display unordered search results.
    if page == "oid":
    
        someresult = False
        for perm in all_perms(notes):
            result = detect(rownumerals, perm, wrap)
            if len(result) > 0:
                someresult = True
                print '<div id="occurrence">Occurrences of <table class="primesresult">' + pretty(perm, encoding) + "</table><br />"
                for item in result:
                    markupstr = '<table class="primesresult"><tr>%s</tr></table>'
                    datastr = ""
                    wraparound = 0
                    if item[2] + len(series) > 12:
                        wraparound = (item[2] + len(series)) % 12
                    for i in range(12):
                        if (i >= item[2] and i < (item[2] + len(series))) or i < wraparound:
                            datastr += '<td class="primesresulty">' + encoding[item[3][i]] + '</td>'
                        else:
                            datastr += '<td class="primesresultn">' + encoding[item[3][i]] + '</td>'
                    print "%s %i <div>%s</div> <br />" % (item[0], item[1], markupstr % datastr)
                print "</div>"

        if not someresult:
            print '<div id="occurrence">That sequence did not occur in any order!<br /></div>'
            
    print '</div>'
   

    

form = cgi.FieldStorage() 
    
structure.print_header(title="Twelve-Tone Music Analysis: Web-Based Analytical Tool for 12-Tone Music by Nico Schuler and Luke Paireepinart",
                       scripts=["main.js", "12tone.js"], css=["main.css", "12tone.css"])


#default values.    
wrap = False
order = False
absolute = False
normal = False
series = [""]
try:       
    #The following items are not set unless the user has searched for something.
        
    series = form.getvalue('series').strip()       
    series = series.split()    
    try:
        wrap = (form.getvalue('wrap').strip().lower() == "on")
    except:
        #it won't submit "wrap"'s value if it's not checked, so default it to False.
        wrap = False        
    try:
        order = (form.getvalue('order').strip().lower() == "on")
    except:
        order = False
        
    if order:
        page = "od"
    else:
        page = "oid"
except:
    page = "result"



try:
    # Grab all input and get it ready for print function.
    row = form.getvalue('notes').strip().lower()
    try:
        absolute = (form.getvalue('absolute').strip().lower() == "on")
    except:
        absolute = False
    try:
        normal = (form.getvalue('normal').strip().lower() == "on")
    except:
        normal = False
    
    
except:
    structure.print_body("12tone/main.html")
    page = "main"

    
#output all the page data.
if page != "main":
    printPage()
structure.print_footer()   
