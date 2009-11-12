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
def printPage(success, name=None):
    if success:
        print "Thank you, you have successfully logged in!<br />"
        u = d.table('user')
        print "Welcome back, %s." % name
    else:
        print "That username or password does not exist."
        structure.print_body("login/main.html")
    
structure.print_header(title="Login Site by Nico Schuler and Luke Paireepinart",
                       scripts=["main.js", "login.js"], css=["main.css"])

                       
                  

                       
try:
    # Get data from fields
    username = form.getvalue('username').strip().lower()
    password = form.getvalue('password').strip().lower()
    import MySQLdb, hashlib
    from sqlobject import table, db
    d = db(host = "rabidpoobear.db", user="rabidpoobear", passwd="ice1288!!zZ", db="musicanalysis")
    
    t = d.table('user')
    t.debug = False
    t.search('username="%s" AND password="%s"' % (username, hashlib.sha1(password).hexdigest()))
    if len(t) > 0:
        printPage(True, t[0][4]+" "+t[0][5])
    else:
        printPage(False)
    #try:
    #    order = (form.getvalue('order').strip().lower() == "on")
    #except:
    #    order = False

except:
    #main page.
    
    structure.print_body("login/main.html")
       

structure.print_footer()