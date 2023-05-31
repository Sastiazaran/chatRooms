#include <stdlib.h>
#include <unistd.h>
#include <string.h>
// #include "conversations.h"

void cypher(char *dir)
{
    char llave = 'K';
    char *resultado = malloc(sizeof(char) * (strlen(dir) + 1));

    for (int i = 0; i < strlen(dir); i++)
    {
        char letra = dir[i];
        resultado[i] = letra ^ llave;
    }

    resultado[strlen(dir)] = '\0';
    strcpy(dir, resultado);
}

char *strremove(char *str, const char *sub)
{
    char *p, *q, *r;
    if (*sub && (q = r = strstr(str, sub)) != NULL)
    {
        size_t len = strlen(sub);
        while ((r = strstr(p = r + len, sub)) != NULL)
        {
            memmove(q, p, r - p);
            q += r - p;
        }
        memmove(q, p, strlen(p) + 1);
    }
    return str;
}

int event(dir)
char *dir;
{
    char *target = strdup(dir);
    char *serv;
    char *res;

    char *pch = strstr(target, "|");
    serv = strremove(target, pch);
    pch = strremove(dir, serv);
    memmove(pch, pch + 1, strlen(pch));

    if (strcmp(serv, "auth") == 0)
    {
        return 1;
    }
    else if (strcmp(serv, "create") == 0)
    {
        return 2;
    }
    else if (strcmp(serv, "getUsers") == 0)
    {
        return 3;
    }
    else if (strcmp(serv, "getUserChatrooms") == 0)
    {
        return 4;
    }
    else if (strcmp(serv, "getAllChatrooms") == 0)
    {
        return 5;
    }
    else if (strcmp(serv, "createChatRoom") == 0)
    {
        return 6;
    }
    else if (strcmp(serv, "getAdminChat") == 0)
    {
        return 7;
    }
    else if (strcmp(serv, "addUser") == 0)
    {
        return 8;
    }
    else if (strcmp(serv, "deleteUser") == 0)
    {
        return 9;
    }
    else if (strcmp(serv, "getChat") == 0)
    {
        return 10;
    }
    else if (strcmp(serv, "messageSent") == 0)
    {
        return 11;
    }
    else if(strcmp(serv, "registrarUsuario" == 0))
    {
        return 12;
    }
    
    

    
}