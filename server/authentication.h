#ifndef CHATBOOK_AUTHENTICATION_H
#define CHATBOOK_AUTHENTICATION_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "utilities.h"

static int is_comment_or_empty(const char *line)
{
    return !line || line[0] == '\0' || line[0] == '#';
}

static void auth(char *dir)
{
    FILE *fp = fopen("credentials.txt", "r");
    if (fp == NULL) {
        strcpy(dir, "Denied\n");
        return;
    }

    trim_inplace(dir);

    char *line = NULL;
    size_t len = 0;
    while (getline(&line, &len, fp) != -1) {
        trim_inplace(line);
        if (is_comment_or_empty(line) || (line[0] == '/' && line[1] == '/')) {
            continue;
        }
        if (strcmp(dir, line) == 0) {
            strcpy(dir, "Granted\n");
            free(line);
            fclose(fp);
            return;
        }
    }
    free(line);
    fclose(fp);
    strcpy(dir, "Denied\n");
}

static void getusers(char *dir)
{
    FILE *fp = fopen("credentials.txt", "r");
    if (fp == NULL) {
        strcpy(dir, "");
        return;
    }

    char *line = NULL;
    size_t len = 0;
    char out[4096] = "";
    int first = 1;

    while (getline(&line, &len, fp) != -1) {
        trim_inplace(line);
        if (is_comment_or_empty(line) || (line[0] == '/' && line[1] == '/')) {
            continue;
        }
        char *pipe = strchr(line, '|');
        if (pipe) {
            *pipe = '\0';
        }
        trim_inplace(line);
        if (line[0] == '\0') {
            continue;
        }
        if (!first) {
            strcat(out, "|");
        }
        strncat(out, line, sizeof(out) - strlen(out) - 1);
        first = 0;
    }

    free(line);
    fclose(fp);
    strcpy(dir, out);
}

static int user_exists(const char *username)
{
    FILE *fp = fopen("credentials.txt", "r");
    if (fp == NULL) {
        return 0;
    }

    char *line = NULL;
    size_t len = 0;
    int found = 0;
    while (getline(&line, &len, fp) != -1) {
        trim_inplace(line);
        if (is_comment_or_empty(line) || (line[0] == '/' && line[1] == '/')) {
            continue;
        }
        char copy[512];
        strncpy(copy, line, sizeof(copy) - 1);
        copy[sizeof(copy) - 1] = '\0';
        char *pipe = strchr(copy, '|');
        if (pipe) {
            *pipe = '\0';
        }
        if (strcmp(copy, username) == 0) {
            found = 1;
            break;
        }
    }
    free(line);
    fclose(fp);
    return found;
}

#endif /* CHATBOOK_AUTHENTICATION_H */
