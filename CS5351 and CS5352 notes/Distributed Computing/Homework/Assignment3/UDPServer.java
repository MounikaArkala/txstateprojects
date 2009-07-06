/*
UDPServer.java by Virpobe Paireepinart
for CS5352, Summer 2009
Texas State University

A simple server that accepts connections on a hardcoded port.
Whenever it gets data, it tries to open the file specified in the data.
If the file exists, the server replies to the client with the text contained in the file.
If the file does not exist, the server replies to the client with an error message,
describing what went wrong.  
*/

import java.net.*;
import java.io.*;
import java.util.*;
public class UDPServer
{
	// Lets the client know when to stop reading data.
    static String EOFStr = Character.toString((char) 0x04);
    static byte[] EOF = EOFStr.getBytes();
    static int LOSSLEN = 25; // number of lines in a packetloss file.
    
    public static void main(String args[])
    {
        try
        {
            DatagramSocket aSocket = new DatagramSocket(6789);// to receive msgs
            byte[] buffer;// temporary request storage.
            String line = null;
                
            
            System.out.println("Attempting to open packetloss files...");
            Vector<String> filenames = new Vector<String>();
            filenames.add("packetloss1.txt");
            filenames.add("packetloss2.txt");
            filenames.add("packetloss3.txt");
            filenames.add("packetloss4.txt");
            Vector<Vector<Integer>> packetloss = new Vector<Vector<Integer>>();
            try
            {
                for (int i = 0; i < filenames.size(); i++)
                {
                    Vector<Integer> lines = new Vector<Integer>();
                    BufferedReader reader = new BufferedReader(new FileReader(filenames.get(i)));
                    //... Loop as long as there are input lines.
                    while ((line=reader.readLine()) != null)
                    {
                        lines.add(Integer.parseInt(line));
                    }
                    reader.close();  // Close to unlock file.
                    packetloss.add(lines);
                }
                
            }
            catch (Exception e)
            {
                System.out.println("A problem occurred while trying to input packetloss files.");
                return;
            }
            System.out.println("Successfully input all packetloss data.");
            
            int [] current = new int[4];
            current[0] = 0;
            current[1] = 0;
            current[2] = 0;
            current[3] = 0;
            int [] ignored = new int[4];
            ignored[0] = 0;
            ignored[1] = 0;
            ignored[2] = 0;
            ignored[3] = 0;
            System.out.println("Waiting for client messages...");
            while(true)
            {
                buffer = new byte[1000];
                DatagramPacket request = new DatagramPacket(buffer, buffer.length);
                DatagramPacket reply = null;
                aSocket.receive(request);
                String message = new String(request.getData());
                String [] items = null;
                message = message.trim();
                items = message.split(":");
                int client = Integer.parseInt(items[0]);
                int msgid = Integer.parseInt(items[1]);
                
                if (msgid != current[client])
                {
                    current[client] = msgid;
                    ignored[client] = 0;
                }
                int drops = packetloss.get(client).get(msgid % LOSSLEN);
                if (ignored[client] < drops)
                {
                    ignored[client] += 1;
                    System.out.println("Ignoring message " + msgid + " from client " + client + ".  Have dropped " + ignored[client] + " of " + drops + " messages.");
                }
                else
                {
                    System.out.println("Enough packets have been dropped for message " + msgid + ", replying to client " + client + ".");
                    String temp = msgid + EOFStr;
                    reply = new DatagramPacket(temp.getBytes(), temp.length(),
                                                              request.getAddress(), request.getPort());
                    aSocket.send(reply);
                }
                
            }
			//aSocket.close();
           
        }
        catch (SocketException e)
        {
            System.out.println("Socket:" + e.getMessage());
        }
        catch (IOException e)
        {
            System.out.println("IO:" + e.getMessage());
        }
    }
}