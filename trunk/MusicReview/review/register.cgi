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
    
    
structure.print_header(title="Registration Site by Nico Schuler and Luke Paireepinart",
                       scripts=["main.js", "register.js"], css=["main.css", "register.css"])
                       
# Create instance of FieldStorage 
form = cgi.FieldStorage()
def printPage(**kwargs):
    print "Thanks for registering, %s %s!<br />" % (kwargs['fname'], kwargs['lname'])
    print "Please go to the <a href='login.cgi'>login</a> page to log in.<br />"
    """
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
        print thiscookie
        print structure.get_username()
    else:
        structure.print_header(title="Login Site by Nico Schuler and Luke Paireepinart",
                       scripts=["main.js", "login.js"], css=["main.css"])
        print "That username or password does not exist."
        structure.print_body("login/main.html")
 

                       
    """ 
                  
            
                       
try:
    
    # Get data from fields
    username = form.getvalue('username').strip().lower()
    password = form.getvalue('password').strip().lower()
    fname = form.getvalue('fname').strip().lower()
    fname = fname[0].upper() + fname[1:]
    lname = form.getvalue('lname').strip().lower()
    lname = lname[0].upper() + lname[1:]
    email = form.getvalue('email').strip().lower()
    credentials = form.getvalue('credentials').strip().lower()
    #TODO: verify their input.
    
    
    # add their information to the database...
    import MySQLdb, hashlib
    try:
        conn = MySQLdb.connect (host = "rabidpoobear.db",
                                user = "rabidpoobear",
                                passwd = "ice1288!!zZ",
                                db = "musicanalysis")
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit (1)

     
    cursor = conn.cursor()
    
    #default authid 0, admin can change later.
    
    #TODO: make sure their username doesn't exist already or anything like that.
    #TODO: look up submitter authentication ID so we don't rely on the automatically-assigned value.
    cursor.execute ("""
       INSERT INTO user (authorization_id, username, password, first_name, last_name, email, credentials)
       VALUES
         ('%s', '%s', '%s', '%s', '%s', '%s', '%s')
    """ % (3, username, hashlib.sha1(password).hexdigest(), fname, lname, email, credentials)
    )
    #print "Number of rows inserted: %d" % cursor.rowcount

     
    #print them out a nice display page.
    printPage(fname=fname, lname=lname)
    

except:
    #main page.
    structure.print_body("register/main.html")
       

structure.print_footer()