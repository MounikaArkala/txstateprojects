


    To clean up the compiled files use
    
[vp1021@zeus New Folder]$ make clean
rm -f client server


    To compile the client use
    
[vp1021@zeus New Folder]$ make client
gcc client.c -o client -lm


    To compile the server use
    
[vp1021@zeus New Folder]$ make server
gcc server.c -lpthread -lnsl -o server




    To run the server type
    
[vp1021@zeus New Folder]$ ./server


    To run the client type
    
[vp1021@zeus New Folder]$ ./client localhost < client1.txt





NOTE: to run the server and the client you may have to give them executable permissions:

chmod 755 server
chmod 755 client