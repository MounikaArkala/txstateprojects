UDPClient and UDPServer directions
by Virpobe Paireepinart
for CS5352 Assignment 4
Texas State University
Summer 2009

This is a set of 2 programs, a client and a server.
The server just waits until it gets messages from the clients.
It has 4 files called "packetlossx.txt" where x is an integer from 1 to 4.
When the client starts, it sends multiple messages to the server to figure out the RTT.
Once the client has calculated a reasonable timeout, by calculating the average
RTT, it will allow the user to enter a message into the client
that the client will then send to the server.
The server will accept a message from the client and reply to the client
with a message containing only the ID of the message it received from client.
Because this is run on a LAN, there isn't any actual RTT (or it's negligible) so the server
simulates it by doing random sleeps before replying to every client request.
The client will assume that a message has been lost after waiting for its
estimated timeout (2 * average RTT is formula I used).

Tips on analyzing the sample run:
look at the server output - it will have a bunch of RTT requests whenever a client was started,
and it illustrates that multiple clients can easily interact with the server at the same time
(there are interleaved requests from all clients.)

You can also examine the client output to see the actual messages sent and such but it's
not as important.

The example run was run with the total supported number of 4 clients all started one after the other
with a few messages sent by each before starting another.  At the end, they were all running simultaneously,
and I attempted to send a few messages at exactly the same time, and the server handled them fine.

Make sure the server is started before the clients or they will just timeout and exit.

I realized the Console class I used in Assignment 2 is not in JDK 5, which is what the school's linux servers have.
I replaced it with a BufferedReader for user input, and Assignment 3 now compiles with no errors
on older versions of Java as well as with JDK 6.

I tested the clients running on my local computer with the server running on zeus, and
that worked fine as well.


Prerequisites:
- must have javac and java on path (located in java/bin directory)
- must be in same directory as UDPClient and UDPServer
- probably need at least JDK 5.

Notes for Running:
- Client _must_ be given the following cmdline args:
- arg 0 is the client ID (0-3)
- arg 1 is server address (eg. localhost)


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
Attempting to open packetloss files...
Successfully input all packetloss data.
Waiting for client messages...

--- Starting the Client ---

$> java UDPClient 0 localhost
Measuring server RTT....
Average RTT for 10 measurements: 6ms.
Setting RTT to twice measured average (12 ms).
Message (or "quit"):


=================
  Example Run
=================

--- Server Output ---
C:\temp>java UDPServer
Attempting to open packetloss files...
Successfully input all packetloss data.
Waiting for client messages...
Client 0 measured RTT.
Client 0 measured RTT.
Client 0 measured RTT.
Client 0 measured RTT.
Client 0 measured RTT.
Client 0 measured RTT.
Client 0 measured RTT.
Client 0 measured RTT.
Client 0 measured RTT.
Client 0 measured RTT.
Ignoring message 0 from client 0.  Have dropped 1 of 1 messages.
Enough packets have been dropped for message 0, replying to client 0.
Ignoring message 1 from client 0.  Have dropped 1 of 2 messages.
Ignoring message 1 from client 0.  Have dropped 2 of 2 messages.
Enough packets have been dropped for message 1, replying to client 0.
Enough packets have been dropped for message 2, replying to client 0.
Ignoring message 3 from client 0.  Have dropped 1 of 3 messages.
Ignoring message 3 from client 0.  Have dropped 2 of 3 messages.
Ignoring message 3 from client 0.  Have dropped 3 of 3 messages.
Enough packets have been dropped for message 3, replying to client 0.
Ignoring message 4 from client 0.  Have dropped 1 of 4 messages.
Ignoring message 4 from client 0.  Have dropped 2 of 4 messages.
Ignoring message 4 from client 0.  Have dropped 3 of 4 messages.
Ignoring message 4 from client 0.  Have dropped 4 of 4 messages.
Enough packets have been dropped for message 4, replying to client 0.
Ignoring message 5 from client 0.  Have dropped 1 of 5 messages.
Ignoring message 5 from client 0.  Have dropped 2 of 5 messages.
Ignoring message 5 from client 0.  Have dropped 3 of 5 messages.
Ignoring message 5 from client 0.  Have dropped 4 of 5 messages.
Ignoring message 5 from client 0.  Have dropped 5 of 5 messages.
Enough packets have been dropped for message 5, replying to client 0.
Ignoring message 6 from client 0.  Have dropped 1 of 1 messages.
Enough packets have been dropped for message 6, replying to client 0.
Client 1 measured RTT.
Client 1 measured RTT.
Client 1 measured RTT.
Client 1 measured RTT.
Client 1 measured RTT.
Client 1 measured RTT.
Client 1 measured RTT.
Client 1 measured RTT.
Client 1 measured RTT.
Client 1 measured RTT.
Ignoring message 0 from client 1.  Have dropped 1 of 7 messages.
Ignoring message 0 from client 1.  Have dropped 2 of 7 messages.
Ignoring message 0 from client 1.  Have dropped 3 of 7 messages.
Ignoring message 0 from client 1.  Have dropped 4 of 7 messages.
Ignoring message 0 from client 1.  Have dropped 5 of 7 messages.
Ignoring message 0 from client 1.  Have dropped 6 of 7 messages.
Ignoring message 0 from client 1.  Have dropped 7 of 7 messages.
Enough packets have been dropped for message 0, replying to client 1.
Ignoring message 1 from client 1.  Have dropped 1 of 2 messages.
Ignoring message 1 from client 1.  Have dropped 2 of 2 messages.
Enough packets have been dropped for message 1, replying to client 1.
Ignoring message 2 from client 1.  Have dropped 1 of 2 messages.
Ignoring message 2 from client 1.  Have dropped 2 of 2 messages.
Enough packets have been dropped for message 2, replying to client 1.
Ignoring message 3 from client 1.  Have dropped 1 of 4 messages.
Ignoring message 3 from client 1.  Have dropped 2 of 4 messages.
Ignoring message 3 from client 1.  Have dropped 3 of 4 messages.
Ignoring message 3 from client 1.  Have dropped 4 of 4 messages.
Enough packets have been dropped for message 3, replying to client 1.
Ignoring message 4 from client 1.  Have dropped 1 of 2 messages.
Ignoring message 4 from client 1.  Have dropped 2 of 2 messages.
Enough packets have been dropped for message 4, replying to client 1.
Ignoring message 7 from client 0.  Have dropped 1 of 2 messages.
Ignoring message 7 from client 0.  Have dropped 2 of 2 messages.
Enough packets have been dropped for message 7, replying to client 0.
Ignoring message 5 from client 1.  Have dropped 1 of 5 messages.
Ignoring message 5 from client 1.  Have dropped 2 of 5 messages.
Ignoring message 5 from client 1.  Have dropped 3 of 5 messages.
Ignoring message 5 from client 1.  Have dropped 4 of 5 messages.
Ignoring message 5 from client 1.  Have dropped 5 of 5 messages.
Enough packets have been dropped for message 5, replying to client 1.
Client 2 measured RTT.
Client 2 measured RTT.
Client 2 measured RTT.
Client 2 measured RTT.
Client 2 measured RTT.
Client 2 measured RTT.
Client 2 measured RTT.
Client 2 measured RTT.
Client 2 measured RTT.
Client 2 measured RTT.
Ignoring message 0 from client 2.  Have dropped 1 of 3 messages.
Ignoring message 0 from client 2.  Have dropped 2 of 3 messages.
Ignoring message 0 from client 2.  Have dropped 3 of 3 messages.
Enough packets have been dropped for message 0, replying to client 2.
Ignoring message 1 from client 2.  Have dropped 1 of 2 messages.
Ignoring message 1 from client 2.  Have dropped 2 of 2 messages.
Enough packets have been dropped for message 1, replying to client 2.
Ignoring message 2 from client 2.  Have dropped 1 of 8 messages.
Ignoring message 2 from client 2.  Have dropped 2 of 8 messages.
Ignoring message 2 from client 2.  Have dropped 3 of 8 messages.
Ignoring message 2 from client 2.  Have dropped 4 of 8 messages.
Ignoring message 2 from client 2.  Have dropped 5 of 8 messages.
Ignoring message 2 from client 2.  Have dropped 6 of 8 messages.
Ignoring message 2 from client 2.  Have dropped 7 of 8 messages.
Ignoring message 2 from client 2.  Have dropped 8 of 8 messages.
Enough packets have been dropped for message 2, replying to client 2.
Ignoring message 3 from client 2.  Have dropped 1 of 4 messages.
Ignoring message 3 from client 2.  Have dropped 2 of 4 messages.
Ignoring message 3 from client 2.  Have dropped 3 of 4 messages.
Ignoring message 3 from client 2.  Have dropped 4 of 4 messages.
Enough packets have been dropped for message 3, replying to client 2.
Client 3 measured RTT.
Client 3 measured RTT.
Client 3 measured RTT.
Client 3 measured RTT.
Client 3 measured RTT.
Client 3 measured RTT.
Client 3 measured RTT.
Client 3 measured RTT.
Client 3 measured RTT.
Client 3 measured RTT.
Ignoring message 0 from client 3.  Have dropped 1 of 3 messages.
Ignoring message 0 from client 3.  Have dropped 2 of 3 messages.
Ignoring message 0 from client 3.  Have dropped 3 of 3 messages.
Enough packets have been dropped for message 0, replying to client 3.
Ignoring message 1 from client 3.  Have dropped 1 of 4 messages.
Ignoring message 1 from client 3.  Have dropped 2 of 4 messages.
Ignoring message 1 from client 3.  Have dropped 3 of 4 messages.
Ignoring message 1 from client 3.  Have dropped 4 of 4 messages.
Enough packets have been dropped for message 1, replying to client 3.
Ignoring message 2 from client 3.  Have dropped 1 of 4 messages.
Ignoring message 2 from client 3.  Have dropped 2 of 4 messages.
Ignoring message 2 from client 3.  Have dropped 3 of 4 messages.
Ignoring message 2 from client 3.  Have dropped 4 of 4 messages.
Enough packets have been dropped for message 2, replying to client 3.
Ignoring message 3 from client 3.  Have dropped 1 of 5 messages.
Ignoring message 3 from client 3.  Have dropped 2 of 5 messages.
Ignoring message 3 from client 3.  Have dropped 3 of 5 messages.
Ignoring message 3 from client 3.  Have dropped 4 of 5 messages.
Ignoring message 3 from client 3.  Have dropped 5 of 5 messages.
Enough packets have been dropped for message 3, replying to client 3.
Ignoring message 4 from client 3.  Have dropped 1 of 1 messages.
Enough packets have been dropped for message 4, replying to client 3.
Ignoring message 5 from client 3.  Have dropped 1 of 3 messages.
Ignoring message 5 from client 3.  Have dropped 2 of 3 messages.
Ignoring message 5 from client 3.  Have dropped 3 of 3 messages.
Enough packets have been dropped for message 5, replying to client 3.
Ignoring message 6 from client 3.  Have dropped 1 of 6 messages.
Ignoring message 6 from client 3.  Have dropped 2 of 6 messages.
Ignoring message 6 from client 3.  Have dropped 3 of 6 messages.
Ignoring message 6 from client 3.  Have dropped 4 of 6 messages.
Ignoring message 6 from client 3.  Have dropped 5 of 6 messages.
Ignoring message 6 from client 3.  Have dropped 6 of 6 messages.
Enough packets have been dropped for message 6, replying to client 3.
Ignoring message 4 from client 2.  Have dropped 1 of 5 messages.
Ignoring message 4 from client 2.  Have dropped 2 of 5 messages.
Ignoring message 4 from client 2.  Have dropped 3 of 5 messages.
Ignoring message 4 from client 2.  Have dropped 4 of 5 messages.
Ignoring message 4 from client 2.  Have dropped 5 of 5 messages.
Enough packets have been dropped for message 4, replying to client 2.
Ignoring message 8 from client 0.  Have dropped 1 of 4 messages.
Ignoring message 8 from client 0.  Have dropped 2 of 4 messages.
Ignoring message 8 from client 0.  Have dropped 3 of 4 messages.
Ignoring message 8 from client 0.  Have dropped 4 of 4 messages.
Enough packets have been dropped for message 8, replying to client 0.
Ignoring message 6 from client 1.  Have dropped 1 of 1 messages.
Enough packets have been dropped for message 6, replying to client 1.
Ignoring message 7 from client 1.  Have dropped 1 of 6 messages.
Ignoring message 7 from client 1.  Have dropped 2 of 6 messages.
Ignoring message 7 from client 1.  Have dropped 3 of 6 messages.
Ignoring message 7 from client 1.  Have dropped 4 of 6 messages.
Ignoring message 7 from client 1.  Have dropped 5 of 6 messages.
Ignoring message 7 from client 1.  Have dropped 6 of 6 messages.
Enough packets have been dropped for message 7, replying to client 1.
Ignoring message 9 from client 0.  Have dropped 1 of 2 messages.
Ignoring message 9 from client 0.  Have dropped 2 of 2 messages.
Enough packets have been dropped for message 9, replying to client 0.
Ignoring message 5 from client 2.  Have dropped 1 of 1 messages.
Enough packets have been dropped for message 5, replying to client 2.
Ignoring message 8 from client 1.  Have dropped 1 of 3 messages.
Ignoring message 8 from client 1.  Have dropped 2 of 3 messages.
Ignoring message 8 from client 1.  Have dropped 3 of 3 messages.
Enough packets have been dropped for message 8, replying to client 1.
Ignoring message 10 from client 0.  Have dropped 1 of 5 messages.
Ignoring message 10 from client 0.  Have dropped 2 of 5 messages.
Ignoring message 10 from client 0.  Have dropped 3 of 5 messages.
Ignoring message 10 from client 0.  Have dropped 4 of 5 messages.
Ignoring message 10 from client 0.  Have dropped 5 of 5 messages.
Enough packets have been dropped for message 10, replying to client 0.
Ignoring message 11 from client 0.  Have dropped 1 of 1 messages.
Enough packets have been dropped for message 11, replying to client 0.
Ignoring message 6 from client 2.  Have dropped 1 of 3 messages.
Ignoring message 6 from client 2.  Have dropped 2 of 3 messages.
Ignoring message 6 from client 2.  Have dropped 3 of 3 messages.
Enough packets have been dropped for message 6, replying to client 2.
Ignoring message 12 from client 0.  Have dropped 1 of 6 messages.
Ignoring message 12 from client 0.  Have dropped 2 of 6 messages.
Ignoring message 12 from client 0.  Have dropped 3 of 6 messages.
Ignoring message 12 from client 0.  Have dropped 4 of 6 messages.
Ignoring message 12 from client 0.  Have dropped 5 of 6 messages.
Ignoring message 12 from client 0.  Have dropped 6 of 6 messages.
Enough packets have been dropped for message 12, replying to client 0.
Ignoring message 13 from client 0.  Have dropped 1 of 3 messages.
Ignoring message 13 from client 0.  Have dropped 2 of 3 messages.
Ignoring message 13 from client 0.  Have dropped 3 of 3 messages.
Enough packets have been dropped for message 13, replying to client 0.
Ignoring message 14 from client 0.  Have dropped 1 of 15 messages.
Ignoring message 14 from client 0.  Have dropped 2 of 15 messages.
Ignoring message 14 from client 0.  Have dropped 3 of 15 messages.
Ignoring message 14 from client 0.  Have dropped 4 of 15 messages.
Ignoring message 14 from client 0.  Have dropped 5 of 15 messages.
Ignoring message 14 from client 0.  Have dropped 6 of 15 messages.
Ignoring message 14 from client 0.  Have dropped 7 of 15 messages.
Ignoring message 14 from client 0.  Have dropped 8 of 15 messages.
Ignoring message 14 from client 0.  Have dropped 9 of 15 messages.
Ignoring message 14 from client 0.  Have dropped 10 of 15 messages.
Ignoring message 14 from client 0.  Have dropped 11 of 15 messages.
Ignoring message 14 from client 0.  Have dropped 12 of 15 messages.
Ignoring message 14 from client 0.  Have dropped 13 of 15 messages.
Ignoring message 14 from client 0.  Have dropped 14 of 15 messages.
Ignoring message 14 from client 0.  Have dropped 15 of 15 messages.
Enough packets have been dropped for message 14, replying to client 0.
Ignoring message 15 from client 0.  Have dropped 1 of 2 messages.
Ignoring message 15 from client 0.  Have dropped 2 of 2 messages.
Enough packets have been dropped for message 15, replying to client 0.
Ignoring message 16 from client 0.  Have dropped 1 of 3 messages.
Ignoring message 16 from client 0.  Have dropped 2 of 3 messages.
Ignoring message 16 from client 0.  Have dropped 3 of 3 messages.
Enough packets have been dropped for message 16, replying to client 0.
Ignoring message 17 from client 0.  Have dropped 1 of 4 messages.
Ignoring message 17 from client 0.  Have dropped 2 of 4 messages.
Ignoring message 17 from client 0.  Have dropped 3 of 4 messages.
Ignoring message 17 from client 0.  Have dropped 4 of 4 messages.
Enough packets have been dropped for message 17, replying to client 0.
Enough packets have been dropped for message 18, replying to client 0.
Ignoring message 19 from client 0.  Have dropped 1 of 1 messages.
Enough packets have been dropped for message 19, replying to client 0.
Ignoring message 20 from client 0.  Have dropped 1 of 2 messages.
Ignoring message 20 from client 0.  Have dropped 2 of 2 messages.
Enough packets have been dropped for message 20, replying to client 0.
Ignoring message 21 from client 0.  Have dropped 1 of 3 messages.
Ignoring message 21 from client 0.  Have dropped 2 of 3 messages.
Ignoring message 21 from client 0.  Have dropped 3 of 3 messages.
Enough packets have been dropped for message 21, replying to client 0.
Enough packets have been dropped for message 22, replying to client 0.
Ignoring message 23 from client 0.  Have dropped 1 of 4 messages.
Ignoring message 23 from client 0.  Have dropped 2 of 4 messages.
Ignoring message 23 from client 0.  Have dropped 3 of 4 messages.
Ignoring message 23 from client 0.  Have dropped 4 of 4 messages.
Enough packets have been dropped for message 23, replying to client 0.
Enough packets have been dropped for message 24, replying to client 0.
Ignoring message 25 from client 0.  Have dropped 1 of 1 messages.
Enough packets have been dropped for message 25, replying to client 0.
Ignoring message 26 from client 0.  Have dropped 1 of 2 messages.
Ignoring message 26 from client 0.  Have dropped 2 of 2 messages.
Enough packets have been dropped for message 26, replying to client 0.
Enough packets have been dropped for message 27, replying to client 0.
Enough packets have been dropped for message 27, replying to client 0.
Ignoring message 28 from client 0.  Have dropped 1 of 3 messages.
Ignoring message 29 from client 0.  Have dropped 1 of 4 messages.
Ignoring message 29 from client 0.  Have dropped 2 of 4 messages.
Ignoring message 29 from client 0.  Have dropped 3 of 4 messages.
Ignoring message 29 from client 0.  Have dropped 4 of 4 messages.
Enough packets have been dropped for message 29, replying to client 0.
Ignoring message 30 from client 0.  Have dropped 1 of 5 messages.
Ignoring message 30 from client 0.  Have dropped 2 of 5 messages.
Ignoring message 30 from client 0.  Have dropped 3 of 5 messages.
Ignoring message 30 from client 0.  Have dropped 4 of 5 messages.
Ignoring message 30 from client 0.  Have dropped 5 of 5 messages.
Enough packets have been dropped for message 30, replying to client 0.
Ignoring message 31 from client 0.  Have dropped 1 of 1 messages.
Enough packets have been dropped for message 31, replying to client 0.
Ignoring message 32 from client 0.  Have dropped 1 of 2 messages.
Ignoring message 32 from client 0.  Have dropped 2 of 2 messages.
Enough packets have been dropped for message 32, replying to client 0.
Ignoring message 33 from client 0.  Have dropped 1 of 4 messages.
Ignoring message 33 from client 0.  Have dropped 2 of 4 messages.
Ignoring message 33 from client 0.  Have dropped 3 of 4 messages.
Ignoring message 33 from client 0.  Have dropped 4 of 4 messages.
Enough packets have been dropped for message 33, replying to client 0.
Ignoring message 34 from client 0.  Have dropped 1 of 2 messages.
Ignoring message 34 from client 0.  Have dropped 2 of 2 messages.
Enough packets have been dropped for message 34, replying to client 0.
Ignoring message 35 from client 0.  Have dropped 1 of 5 messages.
Ignoring message 35 from client 0.  Have dropped 2 of 5 messages.
Ignoring message 35 from client 0.  Have dropped 3 of 5 messages.
Ignoring message 35 from client 0.  Have dropped 4 of 5 messages.
Ignoring message 35 from client 0.  Have dropped 5 of 5 messages.
Enough packets have been dropped for message 35, replying to client 0.
Ignoring message 36 from client 0.  Have dropped 1 of 1 messages.
Enough packets have been dropped for message 36, replying to client 0.
Ignoring message 37 from client 0.  Have dropped 1 of 6 messages.
Ignoring message 37 from client 0.  Have dropped 2 of 6 messages.
Ignoring message 37 from client 0.  Have dropped 3 of 6 messages.
Ignoring message 37 from client 0.  Have dropped 4 of 6 messages.
Ignoring message 37 from client 0.  Have dropped 5 of 6 messages.
Ignoring message 37 from client 0.  Have dropped 6 of 6 messages.
Enough packets have been dropped for message 37, replying to client 0.
Ignoring message 38 from client 0.  Have dropped 1 of 3 messages.
Ignoring message 38 from client 0.  Have dropped 2 of 3 messages.
Ignoring message 38 from client 0.  Have dropped 3 of 3 messages.
Enough packets have been dropped for message 38, replying to client 0.
Ignoring message 39 from client 0.  Have dropped 1 of 15 messages.
Ignoring message 39 from client 0.  Have dropped 2 of 15 messages.
Ignoring message 39 from client 0.  Have dropped 3 of 15 messages.
Ignoring message 39 from client 0.  Have dropped 4 of 15 messages.
Ignoring message 39 from client 0.  Have dropped 5 of 15 messages.
Ignoring message 39 from client 0.  Have dropped 6 of 15 messages.
Ignoring message 39 from client 0.  Have dropped 7 of 15 messages.
Ignoring message 39 from client 0.  Have dropped 8 of 15 messages.
Ignoring message 39 from client 0.  Have dropped 9 of 15 messages.
Ignoring message 39 from client 0.  Have dropped 10 of 15 messages.
Ignoring message 39 from client 0.  Have dropped 11 of 15 messages.
Ignoring message 39 from client 0.  Have dropped 12 of 15 messages.
Ignoring message 39 from client 0.  Have dropped 13 of 15 messages.
Ignoring message 39 from client 0.  Have dropped 14 of 15 messages.
Ignoring message 39 from client 0.  Have dropped 15 of 15 messages.
Enough packets have been dropped for message 39, replying to client 0.
Ignoring message 40 from client 0.  Have dropped 1 of 2 messages.
Ignoring message 40 from client 0.  Have dropped 2 of 2 messages.
Enough packets have been dropped for message 40, replying to client 0.
Ignoring message 41 from client 0.  Have dropped 1 of 3 messages.
Ignoring message 41 from client 0.  Have dropped 2 of 3 messages.
Ignoring message 41 from client 0.  Have dropped 3 of 3 messages.
Enough packets have been dropped for message 41, replying to client 0.
Ignoring message 42 from client 0.  Have dropped 1 of 4 messages.
Ignoring message 42 from client 0.  Have dropped 2 of 4 messages.
Ignoring message 42 from client 0.  Have dropped 3 of 4 messages.
Ignoring message 42 from client 0.  Have dropped 4 of 4 messages.
Enough packets have been dropped for message 42, replying to client 0.

C:\temp>











--- Client 0 Output ---

C:\temp>java UDPClient 0 localhost
Measuring server RTT....
Average RTT for 10 measurements: 8ms.
Setting RTT to twice measured average (16 ms).
Message (or "quit"): hello, world!
Sending message 0 to server.
request timed out.  Retrying...
successfully received message 0.

Message (or "quit"): sample msg
Sending message 1 to server.
request timed out.  Retrying...
request timed out.  Retrying...
successfully received message 1.

Message (or "quit"): test
Sending message 2 to server.
successfully received message 2.

Message (or "quit"): blah
Sending message 3 to server.
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
successfully received message 3.

Message (or "quit"): foo
Sending message 4 to server.
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
successfully received message 4.

Message (or "quit"): bar
Sending message 5 to server.
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
successfully received message 5.

Message (or "quit"): asd
Sending message 6 to server.
request timed out.  Retrying...
successfully received message 6.

Message (or "quit"): sdf
Sending message 7 to server.
request timed out.  Retrying...
request timed out.  Retrying...
successfully received message 7.

Message (or "quit"): we
Sending message 8 to server.
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
successfully received message 8.

Message (or "quit"): asdf
Sending message 9 to server.
request timed out.  Retrying...
request timed out.  Retrying...
successfully received message 9.

Message (or "quit"): test
Sending message 10 to server.
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
successfully received message 10.

Message (or "quit"):
Sending message 11 to server.
request timed out.  Retrying...
successfully received message 11.

Message (or "quit"): a
Sending message 12 to server.
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
successfully received message 12.

Message (or "quit"): a
Sending message 13 to server.
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
successfully received message 13.

Message (or "quit"): a
Sending message 14 to server.
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
successfully received message 14.

Message (or "quit"): a
Sending message 15 to server.
request timed out.  Retrying...
request timed out.  Retrying...
successfully received message 15.

Message (or "quit"): a
Sending message 16 to server.
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
successfully received message 16.

Message (or "quit"): a
Sending message 17 to server.
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
successfully received message 17.

Message (or "quit"): a
Sending message 18 to server.
successfully received message 18.

Message (or "quit"): a
Sending message 19 to server.
request timed out.  Retrying...
successfully received message 19.

Message (or "quit"): a
Sending message 20 to server.
request timed out.  Retrying...
request timed out.  Retrying...
successfully received message 20.

Message (or "quit"): a
Sending message 21 to server.
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
successfully received message 21.

Message (or "quit"): a
Sending message 22 to server.
successfully received message 22.

Message (or "quit"): a
Sending message 23 to server.
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
successfully received message 23.

Message (or "quit"): a
Sending message 24 to server.
successfully received message 24.

Message (or "quit"): a
Sending message 25 to server.
request timed out.  Retrying...
successfully received message 25.

Message (or "quit"): a
Sending message 26 to server.
request timed out.  Retrying...
request timed out.  Retrying...
successfully received message 26.

Message (or "quit"): a
Sending message 27 to server.
request timed out.  Retrying...
successfully received message 27.

Message (or "quit"): a
Sending message 28 to server.
successfully received message 27.

Message (or "quit"): a
Sending message 29 to server.
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
successfully received message 29.

Message (or "quit"): a
Sending message 30 to server.
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
successfully received message 30.

Message (or "quit"): a
Sending message 31 to server.
request timed out.  Retrying...
successfully received message 31.

Message (or "quit"): a
Sending message 32 to server.
request timed out.  Retrying...
request timed out.  Retrying...
successfully received message 32.

Message (or "quit"): a
Sending message 33 to server.
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
successfully received message 33.

Message (or "quit"): a
Sending message 34 to server.
request timed out.  Retrying...
request timed out.  Retrying...
successfully received message 34.

Message (or "quit"): a
Sending message 35 to server.
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
successfully received message 35.

Message (or "quit"): a
Sending message 36 to server.
request timed out.  Retrying...
successfully received message 36.

Message (or "quit"): a
Sending message 37 to server.
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
successfully received message 37.

Message (or "quit"): a
Sending message 38 to server.
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
successfully received message 38.

Message (or "quit"): a
Sending message 39 to server.
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
successfully received message 39.

Message (or "quit"): a
Sending message 40 to server.
request timed out.  Retrying...
request timed out.  Retrying...
successfully received message 40.

Message (or "quit"): a
Sending message 41 to server.
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
successfully received message 41.

Message (or "quit"): a
Sending message 42 to server.
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
successfully received message 42.

Message (or "quit"): quit

C:\temp>







--- Client 1 Output ---


C:\temp> java UDPClient 1 localhost
C:\Projects\CS5351 and CS5352 notes\Distributed Computing\Homework\Assignment3>java
Measuring server RTT....
Average RTT for 10 measurements: 7ms.
Setting RTT to twice measured average (14 ms).
Message (or "quit"): Hello
Sending message 0 to server.
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
successfully received message 0.

Message (or "quit"): some msg
Sending message 1 to server.
request timed out.  Retrying...
request timed out.  Retrying...
successfully received message 1.

Message (or "quit"): test
Sending message 2 to server.
request timed out.  Retrying...
request timed out.  Retrying...
successfully received message 2.

Message (or "quit"): blah
Sending message 3 to server.
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
successfully received message 3.

Message (or "quit"): blah
Sending message 4 to server.
request timed out.  Retrying...
request timed out.  Retrying...
successfully received message 4.

Message (or "quit"): hi
Sending message 5 to server.
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
successfully received message 5.

Message (or "quit"): adf
Sending message 6 to server.
request timed out.  Retrying...
successfully received message 6.

Message (or "quit"): asdf
Sending message 7 to server.
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
successfully received message 7.

Message (or "quit"): test
Sending message 8 to server.
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
successfully received message 8.

Message (or "quit"): quit

C:\temp> 





--- Client 2 Output ---

C:\temp> java UDPClient 2 localhost
Measuring server RTT....
Average RTT for 10 measurements: 7ms.
Setting RTT to twice measured average (14 ms).
Message (or "quit"): hi
Sending message 0 to server.
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
successfully received message 0.

Message (or "quit"): blah
Sending message 1 to server.
request timed out.  Retrying...
request timed out.  Retrying...
successfully received message 1.

Message (or "quit"): blah
Sending message 2 to server.
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
successfully received message 2.

Message (or "quit"): blah
Sending message 3 to server.
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
successfully received message 3.

Message (or "quit"): asdf
Sending message 4 to server.
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
successfully received message 4.

Message (or "quit"): asdf
Sending message 5 to server.
request timed out.  Retrying...
successfully received message 5.

Message (or "quit"): test
Sending message 6 to server.
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
successfully received message 6.

Message (or "quit"): quit

C:\temp> 








--- Client 3 Output ---

C:\temp> java UDPClient 3 localhost
Measuring server RTT....
Average RTT for 10 measurements: 6ms.
Setting RTT to twice measured average (12 ms).
Message (or "quit"): some other message
Sending message 0 to server.
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
successfully received message 0.

Message (or "quit"): asdf
Sending message 1 to server.
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
successfully received message 1.

Message (or "quit"): asdf
Sending message 2 to server.
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
successfully received message 2.

Message (or "quit"): asdf
Sending message 3 to server.
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
successfully received message 3.

Message (or "quit"): asdf
Sending message 4 to server.
request timed out.  Retrying...
successfully received message 4.

Message (or "quit"): asdf
Sending message 5 to server.
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
successfully received message 5.

Message (or "quit"): asdf
Sending message 6 to server.
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
request timed out.  Retrying...
successfully received message 6.

Message (or "quit"): quit

C:\temp> 
