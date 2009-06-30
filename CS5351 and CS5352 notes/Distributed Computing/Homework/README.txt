UDPClient and UDPServer directions
by Virpobe Paireepinart
for CS5352, Texas State University
Summer 2009


Prerequisites:
- must have javac and java on path (located in java/bin directory)
- must be in same directory as UDPClient and UDPServer

Notes:
- client issuing command "quit" will cause server to exit as well as client!
- client should enter ctrl-d ("^d" or ASCII 0x04) as last line to prevent
  server from exiting as well.
  
==================
   Compilation
==================
	
--- UDPClient ---
	
$> javac UDPClient.java

$>

--- UDPServer ---

$> javac UDPServer.java

$>

=================
    Execution
=================

--- Starting the Server ---

$> java UDPServer
Waiting for client request...

--- Starting the Client ---

$> java UDPClient
Server Hostname: 127.0.0.1
Filename (or "ls" or "quit"):


=================
  Example Run
=================

--- Server Output ---
C:\temp>java UDPServer
Waiting for client request...
Listing directories...
Waiting for client request...
Client requested file: foo.bar
Attempting to open file...
File opened successfully!
File Contents:
Foo: $1.23
Bar: $4.56
Baz: $7.89


Waiting for client request...
Client requested file: test.txt
Attempting to open file...
File opened successfully!
File Contents:
Some file
with some random
lines of text



Waiting for client request...
Client requested file: asdflkj
Attempting to open file...
Could not find file on server.


Waiting for client request...
Client requested file: .
Attempting to open file...
Could not find file on server.


Waiting for client request...
Client requested file: ..
Attempting to open file...
Could not find file on server.


Waiting for client request...
Listing directories...
Waiting for client request...

C:\temp>


--- Client Output ---

C:\temp>java UDPClient
Server Hostname: localhost
Filename (or "ls" or "quit"): ls
5352 Assignment 1.pdf
5352 Assignment 2.pdf
Distributed Computing Homework 1.txt
Distributed Computing Homework 2.txt
foo.bar
README.txt
test.txt
UDPClient.class
UDPClient.java
UDPServer.class
UDPServer.java
End of Listing
Filename (or "ls" or "quit"): foo.bar
Foo: $1.23
Bar: $4.56
Baz: $7.89

Filename (or "ls" or "quit"): test.txt
Some file
with some random
lines of text


Filename (or "ls" or "quit"): asdflkj
Could not find file on server.
Filename (or "ls" or "quit"): .
Could not find file on server.
Filename (or "ls" or "quit"): ..
Could not find file on server.
Filename (or "ls" or "quit"): ls
5352 Assignment 1.pdf
5352 Assignment 2.pdf
Distributed Computing Homework 1.txt
Distributed Computing Homework 2.txt
foo.bar
README.txt
test.txt
UDPClient.class
UDPClient.java
UDPServer.class
UDPServer.java
End of Listing
Filename (or "ls" or "quit"): quit

C:\temp>