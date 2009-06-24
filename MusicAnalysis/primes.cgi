#!/usr/local/bin/python

import sys
from musiclib import *

import cgi, cgitb
cgitb.enable()

print "Content-type: text/html"
print

# Create instance of FieldStorage 
form = cgi.FieldStorage() 

page = form.getvalue('page').strip().lower()

# Get data from fields
row = form.getvalue('notes')


encoding = {}
for note in row.split():
    encoding[all_notes[note]] = note

    
rownumerals = [all_notes[i.strip()] for i in row.split()]


# store all primes by starting note
allprimes = []
for x in range(12):
    allprimes.append(prime(rownumerals, x))


def pretty(notes, encoding):
    #notes is int array, encoding is a dict such as {"A":0, "A#":1 ... "G#":11}
    temp = "    <td class=\"primesdata\">%s</td>\n" * len(notes)
    return temp % tuple([encoding[i] for i in notes])

    
        
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
    
elif page == "od":
    series = form.getvalue('series')
    wrap = form.getvalue('wrap')
    if wrap == "true":
        wrap = True
    else:
        wrap = False
    temp = [all_notes[i] for i in series.split()]
    print '<div id="occurrence">Occurrences of <table class="primesresult">' + pretty(temp, encoding) + "</table><br />"
    result = detect(rownumerals, temp, wrap)
    if len(result) == 0:
        print "No occurrences were found!<br />"
    for item in detect(rownumerals, temp, wrap):
        markupstr = '<table class="primesresult"><tr>%s</tr></table>'
        datastr = ""
        wraparound = 0
        if item[2] + len(series.split()) > 12:
            wraparound = (item[2] + len(series.split())) % 12
        for i in range(12):
            if (i >= item[2] and i < (item[2] + len(series.split()))) or i < wraparound:
                datastr += '<td class="primesresulty">' + encoding[item[3][i]] + '</td>'
            else:
                datastr += '<td class="primesresultn">' + encoding[item[3][i]] + '</td>'
        print "%s %i <div>%s</div> <br />" % (item[0], item[1], markupstr % datastr)

    print "</div>"

elif page == "oid":
    series = form.getvalue('series')
    wrap = form.getvalue('wrap')
    if wrap == "true":
        wrap = True
    else:
        wrap = False
    notes = [all_notes[i] for i in series.split()]
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
                if item[2] + len(series.split()) > 12:
                    wraparound = (item[2] + len(series.split())) % 12
                for i in range(12):
                    if (i >= item[2] and i < (item[2] + len(series.split()))) or i < wraparound:
                        datastr += '<td class="primesresulty">' + encoding[item[3][i]] + '</td>'
                    else:
                        datastr += '<td class="primesresultn">' + encoding[item[3][i]] + '</td>'
                print "%s %i <div>%s</div> <br />" % (item[0], item[1], markupstr % datastr)
            print "</div>"

    if not someresult:
        print "<br />That sequence did not occur in any order!<br />"
        
        
else:
    print "404 - Page %s could not be found!" % page

if page == "main":
    print '</div>'