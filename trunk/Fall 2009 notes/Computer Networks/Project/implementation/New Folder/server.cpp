#include <stdio.h>
    #include <stdlib.h>
    #include <errno.h>
    #include <string.h>
    #include <sys/types.h>
    #include <sys/socket.h>
    #include <sys/un.h>

    #define SOCK_PATH "echo_socket"

    int main(void)
    {
        int s, s2, t, len;
        struct sockaddr_un local, remote;
        char str[100];

        if ((s = socket(AF_UNIX, SOCK_STREAM, 0)) == -1) {
            perror("socket");
            exit(1);
        }

        local.sun_family = AF_UNIX;
        strcpy(local.sun_path, SOCK_PATH);
        unlink(local.sun_path);
        len = strlen(local.sun_path) + sizeof(local.sun_family);
        if (bind(s, (struct sockaddr *)&local, len) == -1) {
            perror("bind");
            exit(1);
        }

        if (listen(s, 5) == -1) {
            perror("listen");
            exit(1);
        }

        for(;;) {
            int done, n;
            printf("Waiting for a connection...\n");
            t = sizeof(remote);
            if ((s2 = accept(s, (struct sockaddr *)&remote, &t)) == -1) {
                perror("accept");
                exit(1);
            }

            printf("Connected.\n");

            done = 0;
            do {
                n = recv(s2, str, 100, 0);
                if (n <= 0) {
                    if (n < 0) perror("recv");
                    done = 1;
                }

                if (!done) 
                    if (send(s2, str, n, 0) < 0) {
                        perror("send");
                        done = 1;
                    }
            } while (!done);

            close(s2);
        }

        return 0;
    }
/*

//#include "unp.h"
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/un.h>

void str_echo(int sockfd)
{
    ssize_t n;
    char buf[MAXLINE];
    again:
        while (( n = read(sockfd, buf, MAXLINE)) > 0)
            writen(sockfd, buf, n);
        if (n < 0 && errno == EINTR)
            goto again;
        else if (n < 0)
            errsys("str_echo: read error");
}

int main(int argc, char **argv)
{
    int listenfd, connfd;
    pid_t childpid;
    socklen_t clilen;
    struct sockaddr_in cliaddr, servaddr;
    listenfd = Socket(AF_INET, SOCK_STREAM, 0);
    
    bzero(&servaddr, sizeof(servaddr));
    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = htonl(INADDR_ANY);
    servaddr.sin_port = htons(SERV_PORT);
    
    bind(listenfd, (SA *) &servaddr, sizeof(servaddr));
    listen(listenfd, LISTENQ);
    
    for ( ; ; )
    {
        clilen = sizeof(cliaddr);
        connfd = accept(listenfd, (SA *) &cliaddr, &clilen);
        
        if ((childpid = fork()) == 0) {
            // child process
            close(listenfd); // close listening socket
            str_echo(connfd); // process request
            exit(0);
        }
        close(connfd);
    }
}*/
