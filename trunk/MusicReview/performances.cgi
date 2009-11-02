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
                       scripts=["main.js"], css=["main.css"])

            
structure.print_body("performances/main.html")           
                  

import MySQLdb
from sqlobject import table, db
d = db(host = "rabidpoobear.db", user="rabidpoobear", passwd="ice1288!!zZ", db="musicanalysis")

t = d.table('performance')
print "<p>"
for result in t:
    s = d.table('submission')
    s.search('performance_id="%s"' % result[0])
    u = d.table('user')
    u.search('user_id="%i"' % int(s['user_id'][0][0]))
    print "<table border=1>"
    print "<tr><td>Submitter</td><td>",u[0][4], u[0][5],"</td></tr>"
    print "<tr><td>Performers</td><td>",result[1],"</td></tr>"
    print "<tr><td>Composer</td><td>",result[2],"</td></tr>"
    print "<tr><td>Title</td><td>",result[3],"</td></tr>"
    print "<tr><td>Instruments</td><td>",result[4],"</td></tr>"
    print "<tr><td>Composition Year</td><td>",result[5],"</td></tr>"
    print "<tr><td>Performance Year</td><td>",result[6],"</td></tr>"
    if result[7] == 0:
        live = "No"
    else:
        live = "Yes"
    print "<tr><td>Live Performance</td><td>",live,"</td></tr>"
    p = d.table('period')
    p.search('period_id="%s"' % result[8])
    print "<tr><td>Period</td><td>",p[0][1],"</td></tr>"
    print "<tr><td>Composition Century</td><td>",result[9],"</td></tr>"
    print "</table>"
    print "<br />"
        
print "</p>"
       

structure.print_footer()