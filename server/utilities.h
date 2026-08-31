#ifndef CHATBOOK_UTILITIES_H
#define CHATBOOK_UTILITIES_H

#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <stdio.h>

/* XOR with 'K' — educational obfuscation, not real cryptography. */
static void cypher(char *dir, size_t n)
{
    const char key = 'K';
    for (size_t i = 0; i < n; i++) {
        dir[i] = (char)(dir[i] ^ key);
    }
}

static void trim_inplace(char *s)
{
    if (!s) {
        return;
    }
    size_t n = strlen(s);
    while (n > 0 && (s[n - 1] == '\n' || s[n - 1] == '\r' || isspace((unsigned char)s[n - 1]))) {
        s[--n] = '\0';
    }
    char *start = s;
    while (*start && isspace((unsigned char)*start)) {
        start++;
    }
    if (start != s) {
        memmove(s, start, strlen(start) + 1);
    }
}

/* Split at the first '|'. Copies the head into `head` and returns a pointer
   to the remainder inside `s` (after the pipe). If there is no pipe, the
   whole string is copied to head and an empty remainder is returned. */
static char *split_pipe(char *s, char *head, size_t head_sz)
{
    if (!s || !head || head_sz == 0) {
        return s;
    }
    char *bar = strchr(s, '|');
    if (!bar) {
        strncpy(head, s, head_sz - 1);
        head[head_sz - 1] = '\0';
        trim_inplace(head);
        s[0] = '\0';
        return s;
    }
    size_t n = (size_t)(bar - s);
    if (n >= head_sz) {
        n = head_sz - 1;
    }
    memcpy(head, s, n);
    head[n] = '\0';
    trim_inplace(head);
    return bar + 1;
}

static int valid_room_name(const char *s)
{
    if (!s || !*s) {
        return 0;
    }
    if (strchr(s, '/') || strchr(s, '\\') || strstr(s, "..")) {
        return 0;
    }
    return 1;
}

static char *strremove(char *str, const char *sub)
{
    char *p, *q, *r;
    if (str && sub && *sub && (q = r = strstr(str, sub)) != NULL) {
        size_t len = strlen(sub);
        while ((r = strstr(p = r + len, sub)) != NULL) {
            memmove(q, p, (size_t)(r - p));
            q += r - p;
        }
        memmove(q, p, strlen(p) + 1);
    }
    return str;
}

static int event(char *dir)
{
    if (!dir) {
        return 0;
    }

    char serv[64];
    char *payload = split_pipe(dir, serv, sizeof(serv));
    if (payload != dir) {
        memmove(dir, payload, strlen(payload) + 1);
    }
    trim_inplace(dir);

    if (strcmp(serv, "auth") == 0) {
        return 1;
    }
    if (strcmp(serv, "create") == 0 || strcmp(serv, "creargrupo") == 0) {
        return 2;
    }
    if (strcmp(serv, "getUsers") == 0) {
        return 3;
    }
    if (strcmp(serv, "getUserChatrooms") == 0) {
        return 4;
    }
    if (strcmp(serv, "getAllChatrooms") == 0) {
        return 5;
    }
    if (strcmp(serv, "createChatRoom") == 0) {
        return 6;
    }
    if (strcmp(serv, "getAdminChat") == 0) {
        return 7;
    }
    if (strcmp(serv, "addUser") == 0) {
        return 8;
    }
    if (strcmp(serv, "deleteUser") == 0) {
        return 9;
    }
    if (strcmp(serv, "getChat") == 0) {
        return 10;
    }
    if (strcmp(serv, "messageSent") == 0) {
        return 11;
    }
    if (strcmp(serv, "registrarUsuario") == 0) {
        return 12;
    }
    if (strcmp(serv, "getChatUsers") == 0) {
        return 13;
    }
    return 0;
}

#endif /* CHATBOOK_UTILITIES_H */
