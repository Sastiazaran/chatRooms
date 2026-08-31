/*
 * Chatbook TCP server
 *
 * Multi-client chat-room server using fork() and a simple XOR-obfuscated
 * pipe-delimited protocol. Educational project for distributed computing.
 *
 * Build:    make -C server
 * Run:      ./server/tcpserver [port]
 * Default port: 5000
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <netdb.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <signal.h>
#include <unistd.h>
#include <stdbool.h>
#include <dirent.h>
#include <errno.h>
#include <arpa/inet.h>

#include "authentication.h"
#include "chats.h"

#define DIRSIZE 65536
#define DEFAULT_PORT 5000

int sd = -1;
int sd_actual = -1;

void aborta_handler(int sig)
{
    printf("\nShutting down Chatbook server (%d)\n", sig);
    if (sd_actual != -1) {
        close(sd_actual);
    }
    if (sd != -1) {
        close(sd);
    }
    exit(0);
}

static void dispatch(int eventInt, char *dir)
{
    switch (eventInt) {
    case 1:
        auth(dir);
        break;
    case 2:
        creargrupo(dir);
        break;
    case 3:
        getusers(dir);
        break;
    case 4:
        getuserchats(dir);
        break;
    case 5:
        getchats(dir);
        break;
    case 6:
        creargrupo(dir);
        break;
    case 7:
        getadminchats(dir);
        break;
    case 8:
        addUser(dir);
        break;
    case 9:
        deleteUser(dir);
        break;
    case 10:
        getchat(dir);
        break;
    case 11:
        messageSent(dir);
        break;
    case 12:
        registerUser(dir);
        break;
    case 13:
        getchatusers(dir);
        break;
    default:
        strcpy(dir, "Error|Unknown command");
        break;
    }
}

int main(int argc, char *argv[])
{
    int port = DEFAULT_PORT;
    if (argc > 1) {
        port = atoi(argv[1]);
        if (port <= 0 || port > 65535) {
            fprintf(stderr, "Invalid port: %s\n", argv[1]);
            return 1;
        }
    }

    if (signal(SIGINT, aborta_handler) == SIG_ERR) {
        perror("Could not set signal handler");
        return 1;
    }
    signal(SIGCHLD, SIG_IGN); /* avoid zombie children */

    if ((sd = socket(AF_INET, SOCK_STREAM, 0)) == -1) {
        perror("socket");
        return 1;
    }

    int opt = 1;
    if (setsockopt(sd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt)) == -1) {
        perror("setsockopt");
    }

    struct sockaddr_in sind;
    memset(&sind, 0, sizeof(sind));
    sind.sin_family = AF_INET;
    sind.sin_addr.s_addr = INADDR_ANY;
    sind.sin_port = htons((uint16_t)port);

    if (bind(sd, (struct sockaddr *)&sind, sizeof(sind)) == -1) {
        perror("bind");
        close(sd);
        return 1;
    }

    if (listen(sd, 16) == -1) {
        perror("listen");
        close(sd);
        return 1;
    }

    printf("Chatbook server listening on port %d\n", port);

    for (;;) {
        struct sockaddr_in pin;
        socklen_t addrlen = sizeof(pin);
        sd_actual = accept(sd, (struct sockaddr *)&pin, &addrlen);
        if (sd_actual == -1) {
            if (errno == EINTR) {
                continue;
            }
            perror("accept");
            close(sd);
            return 1;
        }

        pid_t child_pid = fork();
        if (child_pid == 0) {
            close(sd);
            break;
        }
        if (child_pid < 0) {
            perror("fork");
            close(sd_actual);
            continue;
        }
        close(sd_actual);
        sd_actual = -1;
    }

    char dir[DIRSIZE];
    for (;;) {
        memset(dir, 0, sizeof(dir));
        ssize_t n = recv(sd_actual, dir, sizeof(dir) - 1, 0);
        if (n <= 0) {
            break;
        }
        dir[n] = '\0';

        cypher(dir, (size_t)n);
        printf("Request: %s\n", dir);

        int eventInt = event(dir);
        printf("Event: %d\n", eventInt);
        dispatch(eventInt, dir);

        printf("Response: %s\n", dir);
        size_t out_len = strlen(dir);
        if (out_len == 0) {
            dir[0] = ' ';
            dir[1] = '\0';
            out_len = 1;
        }
        cypher(dir, out_len);

        if (send(sd_actual, dir, out_len, 0) == -1) {
            perror("send");
            break;
        }
    }

    close(sd_actual);
    printf("Connection closed\n");
    return 0;
}
