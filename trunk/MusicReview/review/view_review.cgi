#!/usr/local/bin/python
# -*- coding: cp1252 -*-
#!"C:/python26/python.exe"


import os, cgi
from libs import structure

# Debug code, shouldn't be included unless testing.
import cgitb
cgitb.enable()
    
# Create instance of FieldStorage 
form = cgi.FieldStorage()

    
structure.print_header(title="Reviews List by Nico Schuler and Luke Paireepinart",
                       scripts=["main.js"], css=["main.css", "view_review.css"])

               

#user = structure.get_username()



def printPage(performanceid):
    import MySQLdb
    from dbsupport.sqlobject import table, db
    d = db(host = "rabidpoobear.db", user="rabidpoobear", passwd="ice1288!!zZ", db="musicanalysis")
    t = d.table('review')
    t.search('performance_id="%s"' % performanceid)
    
    print "Matching Reviews: "
    print "<hr />"
    for result in t:
            print "<table border=1 class='Review'>"
            passed = "No"
            if result[1]:
                passed = "Yes"
            inadmissible = "No"
            if result[2]:
                inadmissible = "Yes"
            print "<tr class='Review'><td class='Review'>Comments</td><td class='Review'>",result[4],"</td></tr>"
            if inadmissible == "Yes":
                print "<tr class='Review'><td class='Review'>Inadmissible</td><td class='Review'>",inadmissible,"</td></tr>"
            else:
                print "<tr class='Review'><td class='Review'>Passed Review</td><td class='Review'>", passed, "</td></tr>"
                print "<tr class='Review'><td class='Review'>Inadmissible</td><td class='Review'>",inadmissible,"</td></tr>"
                
            print "<tr class='Review'><td class='Review'>Review Date</td><td class='Review'>",result[5],"</td></tr>"
            print "</table>"
    print '<hr />Click <a href="account.cgi">here</a> to return to your account information.'
       


                     
try:
    performanceid = form.getvalue('performance_id').strip().lower()
    printPage(performanceid)       

except:
    #main page.
    #structure.print_body("performances/main.html")
    pass
    
    

structure.print_footer()