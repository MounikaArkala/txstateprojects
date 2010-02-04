/*
CBP Server by Luke Paireepinart
for Networks Programming, Fall 2009, Wuxu Peng, Texas State University

based on a threaded server tutorial I found online somewhere, but heavily modified.

*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <pthread.h>

#define PORTNUMBER 19850

// Since this program is multithreaded we need to use a mutex when accessing certain global variables
// to ensure we don't have any race conditions.
pthread_mutex_t mp = PTHREAD_MUTEX_INITIALIZER; 
pthread_mutexattr_t mattr; 
int ret, j, k, l; 

// Help us keep track of the currently-connected users and the socket filedescriptors for each
// so we can write back to them whenever a collision happens and they're involved.
int connected_clients[10] = {-1,-1,-1,-1,-1,-1,-1,-1,-1,-1};
int clients_fds[10] = {-1,-1,-1,-1,-1,-1,-1,-1,-1,-1};

int CBPOrigin = -1, CBPDest = -1, CBPFrame = -1;




// structure containing the file descriptor of the socket connection.
struct serverParm {
           int connectionDesc;
       };

// This is a thread function that is spawned for every connection made.
void *serverThread(void *parmPtr) {
#define PARMPTR ((struct serverParm *) parmPtr)
    int recievedMsgLen;
    char messageBuf[1025];

    /* Server thread code to deal with message processing */
    printf("DEBUG: connection made, connectionDesc=%d\n",
            PARMPTR->connectionDesc);
    if (PARMPTR->connectionDesc < 0) {
        printf("Accept failed\n");
        return(0);    /* Exit thread */
    }
    
    /* Receive messages from sender... */
    while ((recievedMsgLen=
            read(PARMPTR->connectionDesc,messageBuf,sizeof(messageBuf)-1)) > 0) 
    {
        recievedMsgLen[messageBuf] = '\0';
        //printf("Received Message: %s\n",messageBuf);
        fflush(stdout);
        /* try to process the message.*/
        int tokenval = 0;
        char *token[255]; //user input and array to hold max possible tokens.

        token[0] = strtok(messageBuf, " "); //get pointer to first token found and store in 0
                                           //place in array
        while(token[tokenval]!= NULL) {   //ensure a pointer was found
            tokenval++;
            token[tokenval] = strtok(NULL, " "); //continue to tokenize the string
        }
        
        if (strcmp(token[0], "identify") == 0)
        {
            int clival = atoi(token[1]);
            printf("Registering a new client.\n");
            // loop through our connected clients and find a place to put him.
            int foundspot = 0;
            pthread_mutex_lock(&mp);
            for (j = 0; j < 10; j++)
            {
                if (connected_clients[j] == clival)
                {
                    foundspot = 0; // duplicate client.
                    break;
                }
                if (connected_clients[j] < 0)
                {
                    foundspot = 1; // found an empty spot.
                    connected_clients[j] = clival;
                    clients_fds[j] = PARMPTR->connectionDesc;
                    break;
                }
            }
            if (!foundspot)
            {
                break; // something went wrong, maybe too many clients or duplicate client.
            }
            fflush(stdout);
            pthread_mutex_unlock(&mp);
        }
        
        else if (strcmp(token[0], "listclients") == 0) // inquire about # of connected clients.
        {
            printf("Client enquired about connected clients.\n");
            int clients = 0;
            for (j = 0; j < 10; j++)
            {
                if (connected_clients[j] >= 0)
                {
                    clients += 1;
                }
            }
            char temp[10];
            sprintf(temp, "%i", clients);
            // send them a message with the # of clients connected.
            send(PARMPTR->connectionDesc, temp, 5, 0);
        }
        else if (strcmp(token[0], "sendmsg") == 0)
        {
            // A client is trying to send a message between himself and some other user through our CBP.
            int clientid = atoi(token[1]), dest=atoi(token[2]), framenum=atoi(token[3]), end=atoi(token[4]);
            if(end)
            {
                printf("Received message from %i to %i, frame # %i, part 2.\n", clientid, dest, framenum);
            }
            else
            {
                printf("Received message from %i to %i, frame # %i, part 1.\n", clientid, dest, framenum);
            }
            
            pthread_mutex_lock(&mp);
            if (CBPOrigin == -1) // There is currently not a frame stored so we can store the frame we just received.
            {
                CBPOrigin = clientid;
                CBPDest = dest;
                CBPFrame = framenum;
                if (write(PARMPTR->connectionDesc,"\0",7) < 0) {
                       perror("Server: write error");
                       return(0);
                   }
            }
            else
            {   // it's the end of a packet.
                if (CBPOrigin == clientid && CBPDest == dest && CBPFrame == framenum)
                {
                    CBPOrigin = -1;
                    if (write(PARMPTR->connectionDesc,"\0",7) < 0) {
                           perror("Server: write error");
                           return(0);
                       }
                    printf("Message frame # %i from %i to %i sent successfully.\n", framenum, clientid, dest);
                }
                 // or... a collision occured. 
                // inform whoever just sent us this packet and also inform the person who sent the other packet.
                else
                {
                    printf("Inform %i and %i of a collision.\n", PARMPTR->connectionDesc, CBPOrigin);
                    if (write(PARMPTR->connectionDesc,"COLLISION\0",10) < 0) {
                           perror("Server: write error");
                           return(0);
                    }
                    
                    // search through our client list and find out the FD that refers to the client.
                    for (j = 0; j < 10; j++)
                    {
                        if (connected_clients[j] == CBPOrigin)
                        {
                            if (write(clients_fds[j],"COLLISION\0",10) < 0) {
                            //perror("Server: write error2");
                            //return(0);
                            }
                        } 
                    }
                    CBPOrigin = -1;
                }
            }
            
            pthread_mutex_unlock(&mp);
        
        
        
        }
        else if (strcmp(token[0], "logout") == 0)
        {
            // we don't depend on them logging out but it's nice just to make sure we get everything cleaned up.
            
            pthread_mutex_lock(&mp);
            for (j = 0; j < 10; j++)
            {
                if (connected_clients[j] == PARMPTR->connectionDesc)
                {
                    connected_clients[j] = -1;
                    clients_fds[j] = -1;
                }
            }
            pthread_mutex_unlock(&mp);
        }
        else
        {
            
            if (write(PARMPTR->connectionDesc,"\0",7) < 0) {
                   perror("Server: write error");
                   return(0);
               }
       }
    }
    
    pthread_mutex_lock(&mp);
    // thread is done so get rid of the client from our file descriptor table so we don't have values hanging around
    // after the user's gone.
    for (j = 0; j < 10; j++)
    {
        if (connected_clients[j] == PARMPTR->connectionDesc)
        {
            connected_clients[j] = -1;
            clients_fds[j] = -1;
        }
    }
    pthread_mutex_unlock(&mp);
    
    close(PARMPTR->connectionDesc);  /* Avoid descriptor leaks */
    free(PARMPTR);                   /* And memory leaks */
    
    
    return(0);                       /* Exit thread */
}

main () {
    int listenDesc;
    struct sockaddr_in myAddr;
    struct serverParm *parmPtr;
    int connectionDesc;
    pthread_t threadID;
    ret = pthread_mutex_init(&mp, NULL);
    

    /* For testing purposes, make sure process will terminate eventually */
    //alarm(600);  /* Terminate in 600 seconds */

    /* Create socket from which to read */
    if ((listenDesc = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        perror("open error on socket");
        exit(1);
    }

    /* Create "name" of socket */
    myAddr.sin_family = AF_INET;
    myAddr.sin_addr.s_addr = INADDR_ANY;
    myAddr.sin_port = htons(PORTNUMBER);
        
    if (bind(listenDesc, (struct sockaddr *) &myAddr, sizeof(myAddr)) < 0) {
        perror("bind error");
        exit(1);
    }

    /* Start accepting connections.... */
    /* Up to 5 requests for connections can be queued... */
    listen(listenDesc,5);

    while (1) /* Do forever */ {
        /* Wait for a client connection */
        connectionDesc = accept(listenDesc, NULL, NULL);

        /* Create a thread to actually handle this client */
        parmPtr = (struct serverParm *)malloc(sizeof(struct serverParm));
        parmPtr->connectionDesc = connectionDesc;
        if (pthread_create(&threadID, NULL, serverThread, (void *)parmPtr) 
              != 0) {
            perror("Thread create error");
            close(connectionDesc);
            close(listenDesc);
            exit(1);
        }

        printf("Parent ready for another connection\n");
    }

}
