#!/usr/local/bin/python
# -*- coding: cp1252 -*-
#!"C:/python26/python.exe"
""" Index.cgi
------------------------------
Author:    Luke Paireepinart
Copyright: Nico Schüler

Texas State University
Summer 2009
------------------------------
Brief Summary:
This is the index page that is loaded when the user visits the site initially.
It contains information on the site as well as navigation links to other areas of the site.
"""
import os, cgi
from libs import structure

structure.print_header(title = "Music Analysis: Web-Based Analytical Tools by Nico Schuler and Luke Paireepinart",
                       css = ["main.css"],
                       scripts = ["main.js"])

structure.print_body("main/main.html")
structure.print_footer()