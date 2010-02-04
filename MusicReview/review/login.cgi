#!/usr/local/bin/python
# -*- coding: cp1252 -*-
#!"C:/python26/python.exe"


#TODO: use md5 or SHA or something for passwords.


import os, cgi, Cookie
from libs import structure

# Debug code, shouldn't be included unless testing.
import cgitb
cgitb.enable()
    
username = ""
    
    
# Create instance of FieldStorage 
form = cgi.FieldStorage()
def printPage(success, name=None):
    global username
    if success:
        # set cookie
        thiscookie = Cookie.SimpleCookie()
        thiscookie['username'] = username
        thiscookie['username']['max-age'] = 60*30 #30 mins
        thiscookie['username']['path'] = '/'
        thiscookie['session'] = '23fwe90erjgbe0f'
        thiscookie['session']['max-age'] = 60*30 #30 mins
        thiscookie['session']['path'] = '/'
        structure.print_header(title="Login Site by Nico Schuler and Luke Paireepinart",
                       scripts=["main.js", "login.js"], css=["main.css"], cookie=thiscookie)
                       
        print "Thank you, you have successfully logged in!<br />"
        
        print "Welcome back, %s." % name
    else:
        structure.print_header(title="Login Site by Nico Schuler and Luke Paireepinart",
                       scripts=["main.js", "login.js"], css=["main.css"])
        print "That username or password does not exist."
        structure.print_body("login/main.html")
 

                       
                  
                  
                  
                       
try:
    if structure.get_username():
        structure.print_header(title="Login Site by Nico Schuler and Luke Paireepinart",
                       scripts=["main.js", "login.js"], css=["main.css"])
        structure.print_body("login/loggedin.html", {"username":structure.get_username()})
        
    else:
        # Get data from fields
        username = form.getvalue('username').strip().lower()
        password = form.getvalue('password').strip().lower()
        import MySQLdb, hashlib
        from dbsupport.sqlobject import table, db
        d = db(host = "rabidpoobear.db", user="rabidpoobear", passwd="ice1288!!zZ", db="musicanalysis")
        
        t = d.table('user')
        t.debug = False
        t.search('username="%s" AND password="%s"' % (username, hashlib.sha1(password).hexdigest()))
        if len(t) > 0:
            printPage(True, t[0][4]+" "+t[0][5])
        else:
            printPage(False)
        

except:
    #main page.
    
    structure.print_header(title="Login Site by Nico Schuler and Luke Paireepinart",
                   scripts=["main.js", "login.js"], css=["main.css"])
    structure.print_body("login/main.html")
       

structure.print_footer()