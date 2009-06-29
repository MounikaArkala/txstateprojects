/*
UDPServer.java by Virpobe Paireepinart
for CS5352, Spring 2009
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
    static String EOFStr = Character.toString((char) 0x04);
    static byte[] EOF = EOFStr.getBytes();
    
    public static void errmsg(DatagramSocket socket, DatagramPacket request, String msg) throws IOException
    {
        
        System.out.println(msg);
        String line = msg + EOFStr;
        DatagramPacket reply = new DatagramPacket(line.getBytes(), line.length(),
                                              request.getAddress(), request.getPort());
        socket.send(reply);
    }


    public static void main(String args[])
    {
        try
        {
            DatagramSocket aSocket = new DatagramSocket(6789);
            byte[] buffer;
            while(true)
            {
                buffer = new byte[1000];
                System.out.println("Waiting for client request...");
                DatagramPacket request = new DatagramPacket(buffer, buffer.length);
                DatagramPacket reply = null;
                aSocket.receive(request);
                String filename = new String(request.getData());
                filename = filename.trim();
                if (filename.toLowerCase().equals("quit") ||
                    filename.toLowerCase().equals("exit"))
                {
                    break;
                }
                else if (filename.toLowerCase().equals("dir") ||
                         filename.toLowerCase().equals("ls"))
                {
                    File dir = new File(".");
                    File[] children = dir.listFiles();
                    if (children != null)
                    {
                        for (int i = 0; i < children.length; i++)
                        {
                            if (children[i].isFile())
                            {
                                String child = children[i].getName();
                                reply = new DatagramPacket(child.getBytes(), child.length(),
                                                                  request.getAddress(), request.getPort());
                                aSocket.send(reply);
                            }
                        }
                    }
                    reply = new DatagramPacket(EOF, EOFStr.length(),
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
                    
                    //... Close reader and writer.
                    reader.close();  // Close to unlock.
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