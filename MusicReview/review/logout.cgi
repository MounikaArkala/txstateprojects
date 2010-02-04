#!/usr/local/bin/python
# -*- coding: cp1252 -*-
#!"C:/python26/python.exe"


#TODO: actually remove their session ID from the server instead of just breaking the cookie var.


import os, cgi, Cookie
from libs import structure

# Debug code, shouldn't be included unless testing.
import cgitb
cgitb.enable()


thiscookie = Cookie.SimpleCookie()
thiscookie['username'] = ""
thiscookie['username']['max-age'] = 60*30 #30 mins
thiscookie['username']['path'] = '/'
thiscookie['session'] = ""
thiscookie['session']['max-age'] = 60*30 #30 mins
thiscookie['session']['path'] = '/'
structure.print_header(title="Logout of Music Review Site by Nico Schuler and Luke Paireepinart",
               scripts=["main.js", "login.js"], css=["main.css"], cookie=thiscookie)
structure.print_body("logout/main.html")
 

structure.print_footer()