/*
UDPClient.java by Virpobe Paireepinart
for CS5352, Summer 2009
Texas State University

A simple client that connects to a user-specified hostname,
and does a continuous loop, accepting user input, until it reaches
either a "quit", "exit" or a Ctrl-D (EOF) character.

Client sends each line of user input to the server via UDP,
and the server replies with the same message.

The server is assumed to be running whenever the client issues a command to the server.
If the server is not running, the behavior is not defined.
*/


import java.net.*;
import java.io.*;
import java.lang.System;
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
            aSocket.setSoTimeout(400); // initial socket delay very high so we don't timeout our RTT measurements accidentally.
            BufferedReader c = new BufferedReader(new InputStreamReader(System.in));
            
            // Prompt user for hostname & resolve it
            InetAddress aHost = InetAddress.getByName(hostname);
            
			byte[] buffer;
            
            // Talk to server, figure out RTT.  Assume server will not 
            System.out.println("Measuring server RTT....");
            try
            {
                int RTT = 0, measurements = 10;
                for (int i = 0; i < measurements; i++) // measure RTT multiple times to get better estimate.
                {
                    long startTime = System.nanoTime();
                    String message = client + ":-1:RTT";
                    DatagramPacket request = new DatagramPacket(message.getBytes(), message.length(), aHost, serverPort);
                    aSocket.send(request);
                    buffer = new byte[1000]; // To store reply temporarily
                    DatagramPacket reply = new DatagramPacket(buffer, buffer.length);
                    aSocket.receive(reply);
                    String result = new String(reply.getData());
                    long estimatedTime = (System.nanoTime() - startTime) / 1000000;
                    RTT += estimatedTime;
                }
                RTT /= measurements;
                System.out.println("Average RTT for " + measurements + " measurements: " +RTT + "ms.");
                System.out.println("Setting RTT to twice measured average (" + (RTT*2) + " ms).");
                aSocket.setSoTimeout(RTT * 2);
            }
            catch (IOException e)
            {
                System.out.println("Unable to calculate estimated RTT, server is probably down!  Exiting!");
                return;
            }
            
			int currmsg = 0;
            while (true)
            {
                System.out.print("Message (or \"quit\"): ");
                String message = c.readLine();
                if (message.toLowerCase().equals("quit") ||
                    message.toLowerCase().equals("exit"))
                {
                    break;
                }
                message = client + ":" + currmsg + ":" + message;
                
                
                        
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
                        System.out.println("successfully received message " + msgid +".");
                        System.out.println("");
                        break;
                    }
                    catch(IOException e)
                    {
                        System.out.println("request timed out.  Retrying...");
                    }
                }
                currmsg += 1;
                
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
        