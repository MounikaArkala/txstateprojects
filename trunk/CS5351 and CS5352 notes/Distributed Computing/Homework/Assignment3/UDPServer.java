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
import java.util.Scanner;
public class UDPServer
{
	// Lets the client know when to stop reading data.
    static String EOFStr = Character.toString((char) 0x04);
    static byte[] EOF = EOFStr.getBytes();
    


    public static void main(String args[])
    {
        try
        {
            DatagramSocket aSocket = new DatagramSocket(6789);// to receive msgs
            byte[] buffer;// temporary request storage.
            
            System.out.println("Attempting to open file...");
            try
            {
                BufferedReader reader = new BufferedReader(new FileReader(filename));
                //... Loop as long as there are input lines.
                while ((line=reader.readLine()) != null)
                {
                    System.out.println(line);
                    reply = new DatagramPacket(line.getBytes(), line.length(),
                                                          request.getAddress(), request.getPort());
                    aSocket.send(reply);
                }
                // send an EOF so client knows file is over.
                reply = new DatagramPacket(EOF, EOFStr.length(),
                                                      request.getAddress(), request.getPort());
                aSocket.send(reply);
                
                reader.close();  // Close to unlock file.
            }
            catch (FileNotFoundException e)
            {
                errmsg(aSocket, request, "Could not find file on server.");
            }
            catch (IOException e)
            {
                errmsg(aSocket, request, "Unable to open file due to unknown IO error.");
            }
            catch (Exception e)
            {
                errmsg(aSocket, request, "Unable to open file due to unknown error.");
            }
            
            
            
            /*
            while(true)
            {
                buffer = new byte[1000];
                System.out.println("Waiting for client request...");
                DatagramPacket request = new DatagramPacket(buffer, buffer.length);
                DatagramPacket reply = null;
                aSocket.receive(request);
                String filename = new String(request.getData());
                filename = filename.trim();
				// allow client to kill server if they want to.
                if (filename.toLowerCase().equals("quit") ||
                    filename.toLowerCase().equals("exit"))
                {
                    break;
                }
				// allow client to list current directory, makes it easier
				// to choose a file to list.
                else if (filename.toLowerCase().equals("dir") ||
                         filename.toLowerCase().equals("ls"))
                {
					System.out.println("Listing directories...");
                    File dir = new File(".");
                    File[] children = dir.listFiles();
                    if (children != null)
                    {
                        for (int i = 0; i < children.length; i++)
                        {
                            if (children[i].isFile())
                            {
                                String child = children[i].getName();
								// send them the filename for each file.
                                reply = new DatagramPacket(child.getBytes(), child.length(),
                                                                  request.getAddress(), request.getPort());
                                aSocket.send(reply);
                            }
                        }
                    }
					String temp = "End of Listing" + EOFStr;
                    reply = new DatagramPacket(temp.getBytes(), temp.length(),
                                                                  request.getAddress(), request.getPort());
                    aSocket.send(reply);
                    continue;
                }
                
                System.out.println("Client requested file: " + filename);
                
                String line = null;
                
                // Try to open file.
                System.out.println("Attempting to open file...");
                try
                {
                    BufferedReader reader = new BufferedReader(new FileReader(filename));
                    System.out.println("File opened successfully!");
                    System.out.println("File Contents:");
                    //... Loop as long as there are input lines.
                    while ((line=reader.readLine()) != null)
                    {
                        System.out.println(line);
                        reply = new DatagramPacket(line.getBytes(), line.length(),
                                                              request.getAddress(), request.getPort());
                        aSocket.send(reply);
                    }
                    // send an EOF so client knows file is over.
                    reply = new DatagramPacket(EOF, EOFStr.length(),
                                                          request.getAddress(), request.getPort());
                    aSocket.send(reply);
                    
                    reader.close();  // Close to unlock file.
                }
                catch (FileNotFoundException e)
                {
                    errmsg(aSocket, request, "Could not find file on server.");
                }
                catch (IOException e)
                {
                    errmsg(aSocket, request, "Unable to open file due to unknown IO error.");
                }
                catch (Exception e)
                {
                    errmsg(aSocket, request, "Unable to open file due to unknown error.");
                }
                
                System.out.println("");
                System.out.println("");
            }
			aSocket.close();
        }
        catch (SocketException e)
        {
            System.out.println("Socket:" + e.getMessage());
        }
        catch (IOException e)
        {
            System.out.println("IO:" + e.getMessage());
        }
        */
    }
}