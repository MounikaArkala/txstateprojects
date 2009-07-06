/*
UDPClient.java by Virpobe Paireepinart
for CS5352, Summer 2009
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
        String hostname = args[1];
        int client = Integer.parseInt(args[0]);
        
        try 
        {
            DatagramSocket aSocket = new DatagramSocket();
            aSocket.setSoTimeout(200);
            Console c = System.console();
            if (c == null)
            {
                System.err.println("No console.");
                System.exit(1);
            }
            
            // Prompt user for hostname & resolve it
            InetAddress aHost = InetAddress.getByName(hostname);
            
			byte[] buffer;
            
			int messages = 15;
            for (int currmsg = 0; currmsg < messages; currmsg++)
            {
                String message = client + ":" + currmsg + ":Dummymsg";
                
                
                        
                System.out.println("Sending message " + currmsg + " to server.");
                
				String result = new String("");
                // Loop until we get an EOF in the reply
                while(true)
                {
                    try
                    {
                
                        DatagramPacket request = new DatagramPacket(message.getBytes(), message.length(), aHost, serverPort);
                        aSocket.send(request);
                        
                        buffer = new byte[1000]; // To store reply temporarily
                        DatagramPacket reply = new DatagramPacket(buffer, buffer.length);
                        aSocket.receive(reply);
                        result = new String(reply.getData());
                        int msgid = Integer.parseInt(result.trim());
                        System.out.println("successfully received message " + msgid +"!");
                        System.out.println("");
                        System.out.println("");
                        break;
                    }
                    catch(IOException e)
                    {
                        System.out.println("request timed out.  Retrying...");
                    }
                }
                
            }
            aSocket.close(); // Close socket when finished with it.
        }
        catch (SocketException e) // Couldn't open socket
        {
            System.out.println("Socket:" + e.getMessage());
        }
        catch (IOException e) // IO error
        {
            System.out.println("IO:" + e.getMessage());
        }
    }
}
        