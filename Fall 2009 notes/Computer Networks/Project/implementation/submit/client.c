/*
SP Client by Luke Paireepinart
for Networks Programming, Fall 2009, Wuxu Peng, Texas State University

based on a tcp client tutorial I found online somewhere (example for a textbook's resources), but heavily modified.

*/

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <netdb.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <time.h>
#include <arpa/inet.h>
#include <math.h>

#define PORT "19850" // the port client will be connecting to 

#define MAXDATASIZE 100 // max number of bytes we can get at once 

#define CLIENTS 3 // how many clients we wait for until we start running the simulation.

// get sockaddr, IPv4 or IPv6:
void *get_in_addr(struct sockaddr *sa)
{
    if (sa->sa_family == AF_INET) {
        return &(((struct sockaddr_in*)sa)->sin_addr);
    }

    return &(((struct sockaddr_in6*)sa)->sin6_addr);
}

int main(int argc, char *argv[])
{
    // seed our random function so we can have random delays to help our packet simulation be less rigid.
    srand(time(0));
    
    // file descriptors, various data structures.
    int sockfd, numbytes;  
    char buf[MAXDATASIZE];
    struct addrinfo hints, *servinfo, *p;
    int rv;
    char s[INET6_ADDRSTRLEN];

    if (argc != 2) {
        fprintf(stderr,"usage: client hostname\n");
        exit(1);
    }
    // Set up our socket specs
    memset(&hints, 0, sizeof hints);
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;

    if ((rv = getaddrinfo(argv[1], PORT, &hints, &servinfo)) != 0) {
        fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(rv));
        return 1;
    }

    // loop through all the results and connect to the first we can
    for(p = servinfo; p != NULL; p = p->ai_next) {
        if ((sockfd = socket(p->ai_family, p->ai_socktype,
                p->ai_protocol)) == -1) {
            perror("client: socket");
            continue;
        }

        if (connect(sockfd, p->ai_addr, p->ai_addrlen) == -1) {
            close(sockfd);
            perror("client: connect");
            continue;
        }

        break;
    }
    // couldn't find a socket that we can use.
    if (p == NULL) {
        fprintf(stderr, "client: failed to connect\n");
        return 2;
    }
    // we have a socket now.
    inet_ntop(p->ai_family, get_in_addr((struct sockaddr *)p->ai_addr),
            s, sizeof s);
            
    // Connecting to the server...
    printf("client: connecting to %s\n", s);
    
    freeaddrinfo(servinfo); // all done with this structure
    
    
    char buff[50], string[100];
    int ret;
    printf("Client Number: ");
    scanf("%s", &string);  // read from stdin our client number so we will know which client we are.
    int clientid = atoi(string);
    ret = sprintf(buff, "identify %i" , clientid);

    // this is a pretty generic func call, it just sends and if there's an error it will perror and exit main.
    if (send(sockfd, buff, 10, 0) == -1) {
        perror("send");
        exit(1);
    }
    
    sleep(1);
    
    // give ourselves an 8s socket timeout, so we don't have to wait around forever
    // to find out something's hung.
    struct timeval tv;
    tv.tv_sec = 8;
    tv.tv_usec = 0;
    if (setsockopt(sockfd, SOL_SOCKET, SO_RCVTIMEO, (char *)&tv,  sizeof tv))
    {
        perror("setsockopt");
        return -1;
    }
    
    // infinite loop until there are enough clients connected to run sim.
    // based on that CLIENTS #define above.
    while (1)
    {
        if (send(sockfd, "listclients", 15, 0) == -1) {
            perror("send");
            exit(1);
        }
        if ((numbytes = recv(sockfd, buf, MAXDATASIZE-1, 0)) == -1) {
            numbytes = 0;
            //perror("recv");
            //exit(1);
        }
        buf[numbytes] = '\0';
        int client_count = atoi(buf);
        printf("current client count: %i, loop until client count: %i\n", client_count, CLIENTS);
        fflush(stdout);
        sleep(1);
        if (client_count >= CLIENTS)
            break;
    }
    
    int t, len;
    char str[100];
    int frame = 0;

    
    // read in the value to send each iteration.
    while(printf(""), fgets(str, 100, stdin), !feof(stdin)) {
        // get rid of the newline so when the server receives it and prints it his output won't be all messed up.
        if (str[strlen(str) - 2] == '\n') {
            str[strlen(str) - 2] == '\0';
        }
        
        // makes it more straightforward to coerce ints to floats.
        float RAND_MAX_FLOAT = RAND_MAX;
        float randval;
        
        // our binary-exponential backoff amount.  This increases linearly
        // and it is used as an exponential function for the time delay, causing
        // a binary-exponential backoff.
        int bebo = 1;
        // just loop and keep BEBO'ing until we get through the whole frame without a collision.
        while (1)
        { 
            
            char buff[100];
            int ret;
            ret = sprintf(buff, "sendmsg %i %s %i %i" , clientid, str, frame, 0); // from / to / frame# start/end.
            
            printf("Sending part 1 of frame %i.\n", frame, str);
            if (send(sockfd, buff, strlen(buff), 0) == -1) {
                perror("send");
                exit(1);
            }
            
            
            if ((numbytes = recv(sockfd, buf, MAXDATASIZE-1, 0)) == -1) {
                perror("recv");
                exit(1);
            }
            
            buf[numbytes] = '\0';
            
                     
            // if we receive a message containing "COLLISION" we must do a backoff.
            if (strcmp(buf, "COLLISION") == 0)
            {
                printf("Client received collision notification on frame, BEBO value is currently at %i.\n", bebo);
                fflush(stdout);
                // sleep for a BEBO and then repeat.
                
                randval = RAND_MAX_FLOAT / rand();
                int maxval = pow((double)2, (double)bebo);
                // maxval will be 2, 4, 8, 16, etc...
                // we multiply it by our random value and then typecast it back to int and it will be our sleep factor.
                int sleepval = maxval * randval;
                printf("Sleeping for %i microseconds.\n", 100*sleepval);
                usleep((100 * sleepval));
                bebo += 1;
                if (bebo > 10)
                {
                    bebo = 10;
                }
                continue;
            }
            // random sleep to emulate a large frame being sent.
            float randval = RAND_MAX_FLOAT / rand();
            usleep(6000 + (10000 * randval));
            
            // and now on to part 2.
            printf("Sending part 2 of frame %i.\n", frame, str);
            
            ret = sprintf(buff, "sendmsg %i %s %i %i" , clientid, str, frame, 1); // from / to / frame# start/end.

            if (send(sockfd, buff, strlen(buff), 0) == -1) {
                perror("send");
                exit(1);
            }
            
            if ((numbytes = recv(sockfd, buf, MAXDATASIZE-1, 0)) == -1) {
                perror("recv");
                exit(1);
            }
            
            buf[numbytes] = '\0';
            
            // Collision occured with second packet.
            if (strcmp(buf, "COLLISION") == 0)
            {
                printf("Client received collision notification on frame, BEBO value is currently at %i.\n", bebo);
                fflush(stdout);
                // sleep for a BEBO and then repeat.
                
                randval = RAND_MAX_FLOAT / rand();
                int maxval = pow((double)2, (double)bebo);
                // maxval will be 2, 4, 8, 16, etc...
                // we multiply it by our random value and then typecast it back to int and it will be our sleep factor.
                int sleepval = maxval * randval;
                printf("Sleeping for %i microseconds.\n", 100*sleepval);
                usleep((100 * sleepval));
                bebo += 1;
                if (bebo > 10)
                {
                    bebo = 10;
                }
                continue;
            }
            
            
            break;
        }
        printf("Client successfully sent frame %i.\n", frame);
        fflush(stdout);
        frame += 1;
        // random sleep to encourage collisions.
        randval = RAND_MAX_FLOAT / rand();
        usleep(6000 + (1000 * randval));
    }
    
    // Send a final logout message before we go just to be polite.
    if (send(sockfd, "logout", 8, 0) == -1) {
        perror("send");
        exit(1);
    }

    close(sockfd);

    return 0;
}
