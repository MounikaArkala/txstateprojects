Homework 1 by Virpobe Luke Paireepinart
for CS 5334, Spring 2010, Texas State University




============================================================
Problem 1
============================================================


Comments are interspersed in the log, denoted by ##.
Comments follow (not precede) what they explain.
So basically

- perform some action
-- comment on why it behaved that way
- another action
-- comment for second action
etc.

########################################
Trying to get acquainted with the syntax (problem 1)
########################################

[vp1021@zeus ~]$ telnet www.cs.txstate.edu
Trying 147.26.100.174...

telnet: connect to address 147.26.100.174: Connection refused
telnet: Unable to connect to remote host: Connection refused

## didn't work because i forgot to specify port.

[vp1021@zeus ~]$ telnet www.cs.txstate.edu 80
Trying 147.26.100.174...

Connected to www.cs.txstate.edu (147.26.100.174).

Escape character is '^]'.

asdf
Connection closed by foreign host.

## if you don't type something it understands it will hangup without any information.

[vp1021@zeus ~]$ telnet www.cs.txstate.edu 80
Trying 147.26.100.174...

Connected to www.cs.txstate.edu (147.26.100.174).

Escape character is '^]'.

OPTION * http/1.1

HTTP/1.1 400 Bad Request
Date: Thu, 18 Mar 2010 04:52:32 GMT
Server: Apache
Content-Length: 226
Connection: close
Content-Type: text/html; charset=iso-8859-1

<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>400 Bad Request</title>
</head><body>
<h1>Bad Request</h1>
<p>Your browser sent a request that this server could not understand.<br />
</p>
</body></html>
Connection closed by foreign host.

##if you say something it sort of understands but not quite, it will give you some HTML back and close the connection.

[vp1021@zeus ~]$ telnet www.cs.txstate.edu 80
Trying 147.26.100.174...

Connected to www.cs.txstate.edu (147.26.100.174).

Escape character is '^]'.

GET /index.html http/1.1
Connection closed by foreign host.

##I tried to GET something I wasn't supposed to GET, apparently, and it just hung up on me immediately.

[vp1021@zeus ~]$ telnet www.cs.txstate.edu 80
Trying 147.26.100.174...

Connected to www.cs.txstate.edu (147.26.100.174).

Escape character is '^]'.

GET /prospective_students http/1.1
Host: www.cs.txstate.edu

HTTP/1.1 301 Moved Permanently
Date: Thu, 18 Mar 2010 04:53:29 GMT
Server: Apache
Location: http://www.cs.txstate.edu/prospective_students/
Content-Length: 255
Content-Type: text/html; charset=iso-8859-1

<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>301 Moved Permanently</title>
</head><body>
<h1>Moved Permanently</h1>
<p>The document has moved <a href="http://www.cs.txstate.edu/prospective_students/">here</a>.</p>
</body></html>


##I got something I was allowed to get, so it worked fine.





########################################
Trying to send post request (problem 2)
-- I used the w3 schools server for converting celsius to fahrenheit,
because the form is very simple so it's easy to hand-write the POST request.
########################################


[vp1021@zeus ~]$ telnet www.w3schools.com 80
Trying 216.128.29.26...

Connected to www.w3schools.com (216.128.29.26).

Escape character is '^]'.

POST /webservices/tempconvert.asmx/CelsiusToFahrenheit HTTP/1.1
Host: www.w3schools.com
Content-Type: application/x-www-form-urlencoded
Content-Length: 10
Celsius=34
HTTP/1.1 400 Bad Request
Content-Type: text/html
Date: Thu, 18 Mar 2010 04:50:00 GMT
Connection: close
Content-Length: 42

<h1>Bad Request (Invalid Header Name)</h1>Connection closed by foreign host.

## I forgot to put a blank line after the headers so the Celcius=34 tried to be
## interpreted by the browser as part of the header, so it threw a bad request error.


[vp1021@zeus ~]$ telnet www.w3schools.com 80
Trying 216.128.29.26...

Connected to www.w3schools.com (216.128.29.26).

Escape character is '^]'.

POST /webservices/tempconvert.asmx/CelsiusToFahrenheit HTTP/1.1
Host: www.w3schools.com
Content-Type: application/x-www-form-urlencoded
Content-Length: 10

Celsius=34
HTTP/1.1 200 OK
Date: Thu, 18 Mar 2010 04:51:11 GMT
Server: Microsoft-IIS/6.0
MicrosoftOfficeWebServer: 5.0_Pub
X-Powered-By: ASP.NET
X-AspNet-Version: 2.0.50727
Cache-Control: private, max-age=0
Content-Type: text/xml; charset=utf-8
Content-Length: 89

<?xml version="1.0" encoding="utf-8"?>
<string xmlns="http://tempuri.org/">93.2</string>



Connection closed by foreign host.

## This time I did it right, and the server converted my 35 celsius and returned a page with the answer (93.2) as the text.







########################################
Trying to send get request (problem 3)
-- I used wikipedia to see if I could GET a big document.
########################################

[vp1021@zeus ~]$ telnet en.wikipedia.org 80
Trying 208.80.152.2...

Connected to en.wikipedia.org (208.80.152.2).

Escape character is '^]'.

GET /wiki/Main_Page http/1.1
Host: en.wikipedia.org


## must include Host with a GET request.


HTTP/1.0 200 OK
Date: Thu, 18 Mar 2010 04:42:59 GMT
Server: Apache
Cache-Control: private, s-maxage=0, max-age=0, must-revalidate
Content-Language: en
Vary: Accept-Encoding,Cookie
Last-Modified: Thu, 18 Mar 2010 04:27:09 GMT
Content-Length: 55111
Content-Type: text/html; charset=UTF-8
X-Cache: MISS from sq75.wikimedia.org
X-Cache-Lookup: HIT from sq75.wikimedia.org:3128
Age: 81
X-Cache: HIT from sq32.wikimedia.org
X-Cache-Lookup: HIT from sq32.wikimedia.org:80
Connection: close

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en" dir="ltr">
<head>
<title>Wikipedia, the free encyclopedia</title>

[i removed many pages of output here... body of wikipedia homepage.]

<script type="text/javascript">if (window.runOnloadHook) runOnloadHook();</script>
<!-- Served by srv248 in 0.034 secs. --></body></html>
Connection closed by foreign host.

##Server replied and gave me the whole frontpage of wikipedia (I removed most of the text because it was many pages long.)







============================================================
Problem 2
============================================================

Files can also be found online at: http://www.cs.txstate.edu/~vp1021/iip/

The first page I wrote is called page1.html.  It just is a plain HTML page.  NO frills really.  Used a header and a horizontal rule.

The second page I wrote is called page2.html.  It has a lot of syntax errors, but I noticed that most syntax errors are ignored!
There are a few syntax errors that will cause problems, for example
<br   sometext <br>
will make 'sometext' not show up.
But some tags you don't need to close properly.  It's very forgiving.


The third page I wrote is called page3.html.  It's got 2 frames in it, which are html pages "linkframe.html" and "tableframe.html".
Linkframe is a couple links to websites, and tableframe contains a table (an XOR truth one.)



============================================================
Problem 3
============================================================

Files can also be found online at: http://www.cs.txstate.edu/~vp1021/iip/

This program can be run on the linux servers by typing
./problem3.pl
in the current directory.

If your interpreter is in a different directory you must change the first #! line to be your interpreter.
If you get an exection / permission error please
chmod 755 problem3.pl
to make it executable.
It can also be run as a cgi file by placing it in the cgi-bin folder.


This program works fine, it assumes 'input.txt' is defined and it will read in the file and count the words for you.


============================================================
Problem 4
============================================================

Files can also be found online at: http://www.cs.txstate.edu/~vp1021/iip/

This program can be run on the linux servers by typing
./problem4.pl
in the current directory.

If your interpreter is in a different directory you must change the first #! line to be your interpreter.
If you get an exection / permission error please
chmod 755 problem3.pl
to make it executable.
It can also be run as a cgi file by placing it in the cgi-bin folder.

This program works fine, it has the test string built in as a variable.  Change this to whatever you want. 
Uses the 'split' method to divide on &'s then splits the '=' and removes whitespace.