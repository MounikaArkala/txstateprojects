client: client.c
	gcc client.c -o client -lm

server: server.c
	gcc server.c -lpthread -lnsl -o server

clean:
	rm -f client server