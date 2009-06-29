/*
UDPClient.java by Virpobe Paireepinart
for CS5352, Spring 2009
Texas State University

A simple client that connects to a user-specified hostname,
and does a continuous loop, accepting user input, until it reaches
either a "quit", "exit" or a Ctrl-D (EOF) character.
Note, however, that a "quit" or "exit" message will be sent
to the server, so it will be exited as well.  If you do not wish to terminate
the server, exit the client using the Ctrl-D method.

Client sends each line of user input to the server via UDP,
and the server replies with the contents of the file
that has the same name as the line the user entered,
or with an error message.

The server is assumed to be running whenever the client issues a command to the server.
If the server is not running, the behavior is not defined.
*/


import java.net.*;
import java.io.*;

public class UDPClient
{
    public static void main(String args[])
    {
        int serverPort = 6789;
        
        try 
        {
            DatagramSocket aSocket = new DatagramSocket();
            Console c = System.console();
            if (c == null)
            {
                System.err.println("No console.");
                System.exit(1);
            }
            
            // Prompt user for hostname & resolve it
            InetAddress aHost = InetAddress.getByName(c.readLine("Server Hostname: "));
            
            String message = c.readLine("Filename (or \"ls\" or \"quit\"): ");
            while (message.indexOf((char) 0x04) < 0) // While no EOF character in the line
            {
                DatagramPacket request = new DatagramPacket(message.getBytes(), message.length(), aHost, serverPort);
                aSocket.send(request);
                byte[] buffer;
                
                if (message.toLowerCase().equals("quit") ||
                    message.toLowerCase().equals("exit"))
                {
                    break;
                }
                
                // Loop until we get an EOF in the reply
                String result = new String("");
                while(result.indexOf((char) 0x04) < 0)
                {
                    buffer = new byte[1000]; // To store reply temporarily
                    DatagramPacket reply = new DatagramPacket(buffer, buffer.length);
                    aSocket.receive(reply);
                    result = new String(reply.getData());
                    System.out.println(result.trim()); // Output line from file on server
                }
                
                message = c.readLine("Filename (or \"ls\" or \"quit\"): ");
            }
            aSocket.close(); // Close socket when finished with it.
        }
        catch (SocketException e) // Couldn't open socket
        {
            System.out.println("Socket:" + e.getMessage());
        }
        catch (IOException e) // Not sure how this would occur.
        {
            System.out.println("IO:" + e.getMessage());
        }
    }
}
        