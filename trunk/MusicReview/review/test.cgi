#!/usr/local/bin/python
# -*- coding: cp1252 -*-
#!"C:/python26/python.exe"


import os, cgi
import Cookie

# Debug code, shouldn't be included unless testing.
import cgitb
cgitb.enable()
    
from libs import structure


thiscookie = Cookie.SimpleCookie()

print "Content-Type: text/html"
username = None

try:
    thiscookie.load(os.environ['HTTP_COOKIE'])
    username = thiscookie['username'].value
    print
    
except:
    thiscookie['username'] = 'rabidpoobear'
    thiscookie['username']['max-age'] = 60*30 #30 mins
    thiscookie['username']['path'] = ''
    thiscookie['session'] = '23fwe90erjgbe0f'
    thiscookie['session']['max-age'] = 60*30 #30 mins
    thiscookie['session']['path'] = ''
    print thiscookie
    print

print "<html><head><title>cookie example</title></head><body>"
if not username:
    print "Sent cookie!"
else:
    print "username: ", username, "<br />"
print "</body></html>"