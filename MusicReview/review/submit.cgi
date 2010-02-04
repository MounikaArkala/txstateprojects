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
    
    
structure.print_header(title="Submission Site by Nico Schuler and Luke Paireepinart",
                       scripts=["main.js", "register.js"], css=["main.css", "register.css"])
                       
# Create instance of FieldStorage 
form = cgi.FieldStorage()         
            
if structure.get_username():
        
    try:
        # Get data from fields
        performers = form.getvalue('performers').strip().lower()
        composer = form.getvalue('composer').strip().lower()
        title = form.getvalue('title').strip().lower()
        instruments = form.getvalue('instruments').strip().lower()
        composition_year = form.getvalue('composition_year').strip().lower()
        performance_year = form.getvalue('performance_year').strip().lower()
        files = form.getvalue('fileurl').strip().lower()
        
        try:
            live_performance = (form.getvalue('live_performance').strip().lower() == "on")
        except:
            live_performance = False
            
        
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
        cursor.execute ("""
           INSERT INTO performance (performers, composer, title, instruments, composition_year, performance_year, live_performance, period_id, century)
           VALUES
             ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')
        """ % (performers, composer, title, instruments, composition_year, performance_year, live_performance, 1, "17th")
        )
        #TODO: get the performance ID of the item we just entered.
        
        
        from dbsupport.sqlobject import table, db
        d = db(host = "rabidpoobear.db", user="rabidpoobear", passwd="ice1288!!zZ", db="musicanalysis")
        performance = d.table('performance')
        performance.search('performers="%s" AND composer="%s" AND title="%s"' % (performers, composer, title))
        performance_id = performance[0][0]
        
        user = d.table('user')
        user.search('username="%s"' % structure.get_username())
        user = user[0] #grab just the first result.
        uid = user[0]
        
        cursor.execute ("""
           INSERT INTO submission (user_id, performance_id, submission_date)
           VALUES
             ('%s', '%s', CURDATE())
        """ % (uid, performance_id)
        )
        
        cursor.execute ("""
           INSERT INTO performance_files (performance_id, url)
           VALUES
             ('%s', '%s')
        """ % (performance_id, files)
        )
        #print "Number of rows inserted: %d" % cursor.rowcount

        print "Thank you for your submission, your information has been added to the database and will be reviewed as soon as possible."
        #print them out a nice display page.
        

    except Exception, e:
        #main page.
        structure.print_body("submit/main.html")
           
        
        
    
    
else:
    structure.print_body("main/notloggedin.html")
    

structure.print_footer()