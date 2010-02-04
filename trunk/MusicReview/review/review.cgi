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
    
    
structure.print_header(title="Review Site by Nico Schuler and Luke Paireepinart",
                       scripts=["main.js"], css=["main.css", "review.css", "performances.css"])
                       
# Create instance of FieldStorage 
form = cgi.FieldStorage()


                  
            
                   
if structure.get_username():
    # Get data from fields   
    try:
        performanceid = form.getvalue('performance_id').strip().lower()
        from dbsupport.sqlobject import table, db
        d = db(host = "rabidpoobear.db", user="rabidpoobear", passwd="ice1288!!zZ", db="musicanalysis")
        try:
            t = d.table('user')
            t.search('username="%s"' % structure.get_username())
            
            uid = t[0][0]
            comments = form.getvalue('comments').strip().lower()
            try:
                passed = (form.getvalue('passed').strip().lower() == "on")
            except:
                passed = False
            try:
                inadmissible = (form.getvalue('inadmissible').strip().lower() == "on")
            except:
                inadmissible = False
                
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
               INSERT INTO review (user_id, performance_id, inadmissible, passed_review, comments, review_date)
               VALUES
                 ('%s', '%s', '%s', '%s', '%s', CURDATE())
            """ % (uid, performanceid, inadmissible, passed, comments)
            )
            print "Thank you for your review!"
            
        except Exception, e:
            #print e
            # print out the form page.
            t = d.table('performance')
            t.search('performance_id="%s"' % performanceid)
            result = t[0]
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
            
            
            out = ["<table border=1 class='Performance'>",
                "<tr class='Performance'><td class='Performance'>Submitter</td><td class='Performance'>",u[0][4], u[0][5],"</td></tr>\n",
               "<tr class='Performance'><td class='Performance'>Performers</td><td class='Performance'>",result[1],"</td></tr>\n",
                "<tr class='Performance'><td class='Performance'>Composer</td><td class='Performance'>",result[2],"</td></tr>\n",
                "<tr class='Performance'><td class='Performance'>Title</td><td class='Performance'>",result[3],"</td></tr>\n",
                "<tr class='Performance'><td class='Performance'>Instruments</td><td class='Performance'>",result[4],"</td></tr>\n",
                "<tr class='Performance'><td class='Performance'>Composition Year</td><td class='Performance'>",str(result[5]),"</td></tr>\n",
                "<tr class='Performance'><td class='Performance'>Performance Year</td><td class='Performance'>",str(result[6]),"</td></tr>\n",
                "<tr class='Performance'><td class='Performance'>Live Performance</td><td class='Performance'>",live,"</td></tr>\n",
                "<tr class='Performance'><td class='Performance'>Period</td><td class='Performance'>",period,"</td></tr>\n",
                "<tr class='Performance'><td class='Performance'>Composition Century</td><td class='Performance'>",result[9],"</td></tr>\n"]
            out = " ".join(out)
            
            #print '<script language="JavaScript" src="scripts/audio-player.js"></script>'
            for i,fileinfo in enumerate(files):
                out += "<tr class='Performance'><td class='Performance'>File %i</td>" % (i+1)
                
                out += "<td class='Performance'>"
                out += """<object type="application/x-shockwave-flash" data="audio/player.swf" id="audioplayer%i" height="24" width="290">
                <param name="movie" value="audio/player.swf">
                <param name="FlashVars" value="playerID=audioplayer%i&soundFile=%s">
                <param name="quality" value="high">
                <param name="menu" value="false">
                <param name="wmode" value="transparent">
                </object>""" % (i+1, i+1, fileinfo[2])
                out += "</td></tr>"
                
            out += "</table>"
            out += "<br /><br />"
            structure.print_body("review/main.html", {'infotable': out, 'performance_id':performanceid})
    except:
        print "Somethin' went wrong :("
else:
    #main page.
    structure.print_body("main/notloggedin.html")
       

structure.print_footer()