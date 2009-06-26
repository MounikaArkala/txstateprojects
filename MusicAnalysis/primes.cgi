#!/usr/local/bin/python

import sys
from musiclib import *

import cgi, cgitb
cgitb.enable()

print "Content-type: text/html"
print

def pretty(notes, encoding):
    #notes is int array, encoding is a dict such as {"A":0, "A#":1 ... "G#":11}
    temp = "    <td class=\"primesdata\">%s</td>\n" * len(notes)
    return temp % tuple([encoding[i] for i in notes])

    
    
def printPage():
    # Create instance of FieldStorage 
    form = cgi.FieldStorage() 
    try:
        # Get data from fields
        page = form.getvalue('page').strip().lower()
        row = form.getvalue('notes').strip()
    
    except:
        print "Unable to process input parameters."
        return

    #set up encoding.
    encoding = {}
    for note in row.split():
        try:
            encoding[all_notes[note]] = note
        except KeyError:
            print "You entered an invalid note: %s" % note
            return

    temp = row.split()
    if len(temp) != 12:
        print "You must enter exactly 12 notes."
        return
        
    rownumerals = []
    for i in temp:
        i = i.strip()
        if len(i) == 2:
            i = i[0].upper() + i[1].lower()
        elif len(i) > 2:
            print "You entered an invalid note: %s" % i
            return
        try:
            rownumerals.append(all_notes[i])
        except KeyError:
            print "You entered an invalid note: %s" % i
            return

    if len(set(rownumerals)) != 12:
        #TODO: figure out which notes they entered that were duplicates.
        print "You must enter exactly 12 UNIQUE notes."
        return
    # store all primes by starting note
    allprimes = []
    for x in range(12):
        allprimes.append(prime(rownumerals, x))


        
            
    if page == "main":

        print "<br />12-Tone Table<br />"
        
        # primes table
        print "<table class=\"primes\">"
        print "  <tr class=\"primesrow\">"
        #pretty-print columns in correct order.
        print "    <td />"
        print "".join([("    <th class=\"primesheader\">I%s</th>\n" % i)for i in rownumerals])
        print "  </tr>"
        for y in inversion(rownumerals, 0):
            print "  <tr class=\"primesrow\">"
            sys.stdout.write(("    <th class=\"primesheader\">P%s</th>\n" % y))
            print pretty(allprimes[y], encoding)
            sys.stdout.write(("    <th class=\"primesheader\">R%s</th>\n" % y))
            print "  </tr>"
            
            
        print "    <td />"
        print "".join([("    <th class=\"primesheader\">RI%s</th>\n" % i)for i in rownumerals])
        print "  </tr>"
        print "</table>"


        print '<br />'
        print 'Search for an order-dependent series<br />'
        print '<input type="text" name="odseries" id="odseries" class="TextInput" onkeypress="handleEnter(event, loadOD);"/>'
        print '<button type="button" onClick="loadOD();" class="SubmitButton">Submit</button>'
        print '<br />'
        print 'Search for an order-independent series<br />'
        print '<input type="text" name="oidseries" id="oidseries" class="TextInput" onkeypress="handleEnter(event, loadOID);"/>'
        print '<button type="button" onClick="loadOID();" class="SubmitButton">Submit</button>'
        print '<br />Enable wraparound <input type="checkbox" checked id="wraparound"><br />'
        print '<div id="primesdiv">'
    
    if page == "od" or page == "oid":
        try:
            # Get data from fields
            series = form.getvalue('series').strip()
            wrap = form.getvalue('wrap').strip()

        except:
            print '<div id="occurrence">Unable to process input parameters.</div>'
            return
            
        if wrap == "true":
            wrap = True
        else:
            wrap = False
        
        series = series.split()
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
            

    if page == "main":
        print '</div>'
        

printPage()