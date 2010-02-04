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

    
structure.print_header(title="My Account Page",
                       scripts=["main.js"], css=["main.css", "account.css"])

               

#user = structure.get_username()



def printPage(username):
    import MySQLdb
    from dbsupport.sqlobject import table, db
    d = db(host = "rabidpoobear.db", user="rabidpoobear", passwd="ice1288!!zZ", db="musicanalysis")
    user = d.table('user')
    user.search('username="%s"' % username)
    user = user[0] #grab just the first result.
    uid = user[0]
    #check if they're administrator. TODO: make this more robust (use auth table).
    if user[1] == 1:
        admin = True
    else:
        admin = False
        
    print "Hello, %s %s.<br /><br /> <br />" % (user[4], user[5])
    
    #TODO: let them reset their e-mail address, password, etc.
    
    submission = d.table('submission')
    submission.search('user_id="%s"' % uid)
    print "Submitted performances: "
    print "<div id='submissions'>"
    if len(submission) == 0:
        print "No submissions.<br />"
        
    for item in submission:
        performance = d.table('performance')
        performance.search('performance_id="%s"' % item[1])
        review = d.table('review')
        review.search('performance_id="%s"' % item[1])
        reviews = len(review)
        print "<br />You submitted performance %s by %s on %s.<br />  This item has been reviewed %i time(s).<br />" % (performance[0][3], performance[0][2], item[2], reviews)
        if reviews > 0:
            print 'Reviews for this item can be found <a href="view_review.cgi?performance_id=%s">here</a>.<br />' % (item[1])
    
    print "</div>"
    
    print "<br /><br />Items you have reviewed:"
    outputted = 0
    print "<div id='reviewed'>"
    reviewer_assignment = d.table('reviewer_assignment')
    reviewer_assignment.search('user_id="%s"' % uid)
    for assignment in reviewer_assignment:
        review = d.table('review')
        review.search('user_id="%s" AND performance_id="%s"' % (uid, item[1]))
        if len(review) != 0:
            performance = d.table('performance')
            performance.search('performance_id="%s"' % item[1])
            print "<br />You reviewed performance %s by %s on %s.<br />" % (performance[0][3], performance[0][2], review[0][5])
            print "<br />"
            outputted += 1
    if not outputted:
        print "<br />You have not reviewed any items yet.<br />"
    
    print "</div>"
    
    print "<br /><br />Items you need to review:"
    outputted = 0
    print "<div id='to_review'>"
    reviewer_assignment = d.table('reviewer_assignment')
    reviewer_assignment.search('user_id="%s"' % uid)
    for assignment in reviewer_assignment:
        review = d.table('review')
        review.search('user_id="%s" AND performance_id="%s"' % (uid, item[1]))
        if len(review) == 0:
            
            performance = d.table('performance')
            performance.search('performance_id="%s"' % item[1])
            print "<br />You are assigned to review performance %s by %s.<br />" % (performance[0][3], performance[0][2])
            print 'You can go <a href="review.cgi?performance_id=%s">here</a> to review this item.<br />' % (item[1])
            outputted += 1
            
    
    if not outputted:
        print "<br />Currently there are no items scheduled to be reviewed for you.  Please check back later.<br />"
    
    print "</div>"
username = structure.get_username()
if username:
    printPage(username)    
    
else:
    structure.print_body("main/notloggedin.html")
    
    

structure.print_footer()