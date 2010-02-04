#!/usr/local/bin/python
# -*- coding: cp1252 -*-
#!"C:/python26/python.exe"


#TODO: use md5 or SHA or something for passwords.

import os, cgi
from libs import structure

# Debug code, shouldn't be included unless testing.
import cgitb
cgitb.enable()
    
# Create instance of FieldStorage 
form = cgi.FieldStorage()

    
structure.print_header(title="Performances List by Nico Schuler and Luke Paireepinart",
                       scripts=["main.js", "audio-player.js"], css=["main.css", "performances.css"])

               

#user = structure.get_username()



def printPage(query):
    import MySQLdb
    from dbsupport.sqlobject import table, db
    d = db(host = "rabidpoobear.db", user="rabidpoobear", passwd="ice1288!!zZ", db="musicanalysis")
    t = d.table('performance')
    qitems = [i.strip().lower() for i in query.split()]
    print "Matching Records: "
    print "<hr />"
    matches = 0
    for result in t:
        s = d.table('submission')
        s.search('performance_id="%s"' % result[0])
        u = d.table('user')
        u.search('user_id="%i"' % int(s['user_id'][0][0]))
        
        if result[7] == 0:
            live = "No"
        else:
            live = "Yes"
            
        p = d.table('period')
        p.search('period_id="%s"' % result[8])
        period = p[0][1]
        
        files = d.table('performance_files')
        files.search('performance_id="%s"' % result[0])
        
        match = False
        
        for item in qitems:
            for candidate in [u[0][4], u[0][5], result[1], result[2], result[3], result[4], str(result[5]), str(result[6]), live, period, result[9]]:
                if item in candidate.lower():#substring
                    match = True
                    
        if match:             
            #check to see if the performance passed review or not.  must be unanimous and not marked inadmissible by anyone, and
            #must have been reviewed by all users marked as reviewers.
            ##### DO THIS NOW
            performance_id = result[0]
            #find out how many people are assigned to review it.
            assignment = d.table("reviewer_assignment")
            assignment.search('performance_id="%s"' % performance_id)
            reviewers = len(assignment)
            
            if reviewers <= 0:
                print "<table border=1 class='Performance'>"
                print "<tr class='Performance'><td class='Performance'>Submitter</td><td class='Performance'>",u[0][4], u[0][5],"</td></tr>"
                print "<tr class='Performance'><td class='Performance'>Performers</td><td class='Performance'>",result[1],"</td></tr>"
                print "<tr class='Performance'><td class='Performance'>Composer</td><td class='Performance'>",result[2],"</td></tr>"
                print "<tr class='Performance'><td class='Performance'>Title</td><td class='Performance'>",result[3],"</td></tr>"
                print "<tr class='Performance'><td class='Performance' colspan=2>This submission has not been assigned reviewers yet.</td></tr>"
                print "</table>"
            
            review = d.table("review")
            review.search('performance_id="%s"' % performance_id)
            inadmissible = 0
            passed = 0
            for item in review:
                passed += item[3]
                inadmissible += item[2]
            print_it = False
            if inadmissible:
                print "<table border=1 class='Performance'>"
                print "<tr class='Performance'><td class='Performance'>Submitter</td><td class='Performance'>",u[0][4], u[0][5],"</td></tr>"
                print "<tr class='Performance'><td class='Performance'>Performers</td><td class='Performance'>",result[1],"</td></tr>"
                print "<tr class='Performance'><td class='Performance'>Composer</td><td class='Performance'>",result[2],"</td></tr>"
                print "<tr class='Performance'><td class='Performance'>Title</td><td class='Performance'>",result[3],"</td></tr>"
                print "<tr class='Performance'><td class='Performance' colspan=2>This submission has been marked inadmissible by one or more reviewers.</td></tr>"
                print "</table>"
                
            elif len(review) == reviewers: # every reviewer reviewed.  TODO: make sure there aren't duplicate reviews.
                if passed >= reviewers/2: # at least half of the reviewers liked it...
                    print_it = True
                #if the reviewers didn't like it let's just leave it out of the search results.
                
                
            else:
                print "<table border=1 class='Performance'>"
                print "<tr class='Performance'><td class='Performance'>Submitter</td><td class='Performance'>",u[0][4], u[0][5],"</td></tr>"
                print "<tr class='Performance'><td class='Performance'>Performers</td><td class='Performance'>",result[1],"</td></tr>"
                print "<tr class='Performance'><td class='Performance'>Composer</td><td class='Performance'>",result[2],"</td></tr>"
                print "<tr class='Performance'><td class='Performance'>Title</td><td class='Performance'>",result[3],"</td></tr>"
                print "<tr class='Performance'><td class='Performance' colspan=2>This submission is still under review.</td></tr>"
                print "</table>"
                
                
            if print_it:
                print "<table border=1 class='Performance'>"
                print "<tr class='Performance'><td class='Performance'>Submitter</td><td class='Performance'>",u[0][4], u[0][5],"</td></tr>"
                print "<tr class='Performance'><td class='Performance'>Performers</td><td class='Performance'>",result[1],"</td></tr>"
                print "<tr class='Performance'><td class='Performance'>Composer</td><td class='Performance'>",result[2],"</td></tr>"
                print "<tr class='Performance'><td class='Performance'>Title</td><td class='Performance'>",result[3],"</td></tr>"
                print "<tr class='Performance'><td class='Performance'>Instruments</td><td class='Performance'>",result[4],"</td></tr>"
                print "<tr class='Performance'><td class='Performance'>Composition Year</td><td class='Performance'>",result[5],"</td></tr>"
                print "<tr class='Performance'><td class='Performance'>Performance Year</td><td class='Performance'>",result[6],"</td></tr>"
                print "<tr class='Performance'><td class='Performance'>Live Performance</td><td class='Performance'>",live,"</td></tr>"
                print "<tr class='Performance'><td class='Performance'>Period</td><td class='Performance'>",period,"</td></tr>"
                print "<tr class='Performance'><td class='Performance'>Composition Century</td><td class='Performance'>",result[9],"</td></tr>"
                #print '<script language="JavaScript" src="scripts/audio-player.js"></script>'
                for i,fileinfo in enumerate(files):
                    print "<tr class='Performance'><td class='Performance'>File %i</td>" % (i+1)
                    
                    print "<td class='Performance'>"
                    print """<object type="application/x-shockwave-flash" data="audio/player.swf" id="audioplayer%i" height="24" width="290">
                    <param name="movie" value="audio/player.swf">
                    <param name="FlashVars" value="playerID=audioplayer%i&soundFile=%s">
                    <param name="quality" value="high">
                    <param name="menu" value="false">
                    <param name="wmode" value="transparent">
                    </object>""" % (i+1, i+1, fileinfo[2])
                    print "</td></tr>"
                    
                print "</table>"
                print "<br /><br />"
            matches += 1
            
    if matches == 0:
        print "No matches found for query ", query
       

    print "Click <a href='performances.cgi'>here</a> to return to search page.</a>"

                     
try:
    query = form.getvalue('query').strip().lower()
    printPage(query)       

except:
    #main page.
    structure.print_body("performances/main.html")
    
    

structure.print_footer()