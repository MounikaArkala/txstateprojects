#!"C:/python26/python.exe"
# -*- coding: cp1252 -*-
#!/usr/local/bin/python
import os, cgi
from libs import structure
from musiclib import all_notes
from chordslib import chords

# Debug code, shouldn't be included unless testing.
import cgitb
cgitb.enable()
    
    
    
def get_chord(note, intervals):
    """ pass it a note and a set of intervals and it will generate the chord.
    eg. note 5 and chord 2,2,3,1,2 would generate
    5,7,9,0,1,3."""
    result = [note]
    for i in intervals:
        result.append((result[-1] + i) % 12)
    return result
    
#it just uses this encoding because it doesn't know how to refer to items in a chord
#(eg. is an item a Eb or a D#?  It depends on the chord.
#but this information is not encoded in the chord database, so it uses defaults.

default_encoding = {0:"A", 1:"A#/Bb", 2:"B/Cb", 3:"B#/C", 4:"C#/Db",
                    5:"D", 6:"D#/Eb", 7:"E/Fb", 8:"E#/F", 9:"F#/Gb", 10:"G", 11:"G#/Ab"}
"""
default_encoding = {0:"A", 1:"A#", 2:"B", 3:"C", 4:"C#",
                    5:"D", 6:"D#", 7:"E", 8:"F", 9:"F#", 10:"G", 11:"G#"}"""
def pretty(notes, encoding):
    ' notes is int array, encoding is a dict such as {0:"A", 1:"A#" ... 11:"G#"}'
    return " ".join([encoding[i] for i in notes])
    
    
    

# Create instance of FieldStorage 
form = cgi.FieldStorage() 

def printPage(page):
    page = page.lower()
    global notes, complete, order, consecutive, default_encoding
    filters = []
    for chord in chords:
        filters.extend(chords[chord][-1])
    filters = list(set(filters))
    searchfields = {"notes": "", "complete": "", "consec": "", "order": ""}
    
    active_filters = []
    
    #must build filtertable dynamically
    filtertable = []
    filtertable.append('<table class="filters" id="filtertable">')
    filtertable.append('<tr class="filters"><th class="filters" colspan=50>Chord Filter</td></tr>')
    filtertable.append('<tr class="filters">')

    #just set them all to checked by default
    if page == "main":
        for filter in filters:
            filtertable.append('<td class="filters"><input type="checkbox" class="filterbox" \
            checked name="%s" id="%s">%s</input></td>' % (filter, filter, filter))
    
    #get the filter information from the query string, and set the check boxes correctly.
    elif page == "result":
        for filter in filters:
            try:
                filter_checked = (form.getvalue(filter).strip().lower() == "on")
            except:
                filter_checked = False
            if filter_checked:
                filtertable.append('<td class="filters"><input type="checkbox" class="filterbox" \
                checked name="%s" id="%s">%s</input></td>' % (filter, filter, filter))
                active_filters.append(filter)
            else:
                filtertable.append('<td class="filters"><input type="checkbox" class="filterbox" \
                name="%s" id="%s">%s</input></td>' % (filter, filter, filter))
        
        temp = []
        for i in notes.split():
            i = i.strip()
            i = i[0].upper() + i[1:].lower()
            temp.append(i)
        searchfields["notes"] = " ".join(temp)
            
        if complete:
            searchfields["complete"] = "checked"
        if consecutive:
            searchfields["consec"] = "checked"
        if order:
            searchfields["order"] = "checked"
  
    
    filtertable.append('</tr></table>')
    filtertable.append('<button class="SubmitButton" type="button" onClick="selectAll();">Select All</button>')
    filtertable.append('<button class="SubmitButton" type="button" onClick="selectNone();">Select None</button>')
    filtertable = "\n".join(filtertable)
    searchfields["filtertable"] = filtertable
    
    structure.print_body("chords/main.html", subdict=searchfields)
    
    if page == "main":
        structure.print_body("chords/directions.html")
        return
    
 
    #-- start of results generation.
    
    temp = []
    for i in notes.split():
        i = i.strip()
        i = i[0].upper() + i[1:].lower()
        try:
            if not all_notes[i] in temp:
                temp.append(all_notes[i])
        except KeyError:
            print '<h2 class="chords">You entered an invalid note: %s</h2>' % i
            return
    notes = temp
    chord_groups = []
    for chord_name in chords:
        matched_chords = []
        temp = False
        for filter in chords[chord_name][1]:
            if filter not in active_filters:
                temp = True
        if temp:
            continue
        intervals = chords[chord_name][0]
        for startnote in range(12):
            chord = get_chord(startnote, intervals)
            #print pretty(chord, default_encoding)
            matches = []
            prev = None
            for note in notes:
                try:
                    loc = chord.index(note)
                    if order:
                        #print pretty(chord, default_encoding), "<br />"
                        #print chord_name, "<br />"
                        #print note, "<br />"
                        if prev != None:
                            #print "prev is ", prev
                            #print "loc is ", loc, "<br />"
                            #print "len(chord) - 1 = ", len(chord) - 1, "<br />"
                            #print (prev == len(chord) - 1)
                            #print (loc != 0)
                            if loc > prev or (prev == len(chord) - 1 and loc == 0): #wraparound
                                prev = loc
                            else:
                                #print "loc <= min_loc"
                                matches = []
                                break
                        else:
                            #print "loc is ", loc
                            prev = loc
                    matches.append(loc)
                except:
                    matches = []
                    break
            if len(matches) == 0:
                continue
            
            if complete:
                if len(chord) != len(notes):
                    continue
                        
            if consecutive:
                # accounts for wrap-around
                transitions = 0
                status = chord[0] in notes
                for note in chord[1:]:
                    if note in notes:
                        if not status: #transition
                            status = True
                            transitions += 1
                    else:
                        if status: #transition
                            status = False
                            transitions += 1
                if transitions > 2:
                    continue
            
            matched_chords.append(chord)
            
        if len(matched_chords) > 0:
            chord_groups.append((chord_name, matched_chords))
       
       
        
    if len(chord_groups) == 0:
        print '<h2 class="chords">No chords matched that search!</h2>'
        return
        
    print '<div id="chordsdiv">'
    print '<table class="chords">'
    print '<tr class="chords">'
    print '<th class="chords" scope="col">Chord Name</th>'
    print '<th class="chords" scope="col">Type</th>'
    print '<th class="chords" scope="col">Chord</th>'
    print '</tr class="chords">'
    for matched_chords in chord_groups:
        print '<tr class="chords">'
        print '<td class="chords">%s</td><td class="chords">%s</td>' % (matched_chords[0], ", ".join(chords[matched_chords[0]][1]))
        print '<td class="chords">'
        for chord in matched_chords[1]:
            print '<table class="chordsresult"><tr class="chordsresult">'
            for note in chord:
                    if note in notes:
                        print '<td class="chordsy">%s</td>' % default_encoding[note]
                    else:
                        print '<td class="chordsn">%s</td>' % default_encoding[note]
            print '</tr></table>'
        print '</td></tr>'
            
    print '</table>'

    print '</div> <!-- ~chordsdiv -->'
    
    
    
structure.print_header(title="Chord Identification in Music Analysis: Web-Based Analytical Tool for the Matching of Vertical Pitch Collections by Nico Schuler and Luke Paireepinart",
                       scripts=["main.js", "chords.js"], css=["main.css", "chords.css"])
  
try:
    # Get data from fields
    notes = form.getvalue('notes').strip().lower()
    try:
        start = form.getvalue('start').strip()
        if start.lower() == pitchclass_txt.lower():
            start = None
    except:
        start = None
    try:
        complete = (form.getvalue('complete').strip().lower() == "on")
    except:
        complete = False
        
    try:
        order = (form.getvalue('order').strip().lower() == "on")
    except:
        order = False
    try:
        consecutive = (form.getvalue('consec').strip().lower() == "on")
    except:
        consecutive = False
    page = "result"
    
except:
    page = "main"

printPage(page)
       

structure.print_footer()