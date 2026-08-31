#ifndef CHATBOOK_CHATS_H
#define CHATBOOK_CHATS_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>
#include "utilities.h"
#include "authentication.h"

static void creargrupo(char *dir)
{
    char user[256];
    char *groupName = split_pipe(dir, user, sizeof(user));
    trim_inplace(groupName);

    if (!valid_room_name(groupName) || user[0] == '\0') {
        strcpy(dir, "Error|Invalid chat room name");
        return;
    }

    char conv[512];
    char users[512];
    snprintf(conv, sizeof(conv), "%s.conv", groupName);
    snprintf(users, sizeof(users), "%s.users", groupName);

    FILE *convFile = fopen(conv, "w");
    FILE *usersFile = fopen(users, "w");
    if (!convFile || !usersFile) {
        if (convFile) {
            fclose(convFile);
        }
        if (usersFile) {
            fclose(usersFile);
        }
        strcpy(dir, "Error|Could not create chat room");
        return;
    }
    fprintf(usersFile, "%s\n", user);
    fclose(convFile);
    fclose(usersFile);

    snprintf(dir, 2048, "%s|%s|True", user, groupName);
}

static void getchats(char *dir)
{
    DIR *d = opendir(".");
    char ret[4096] = "";
    dir[0] = '\0';
    if (!d) {
        return;
    }

    struct dirent *direct;
    int first = 1;
    while ((direct = readdir(d)) != NULL) {
        char *pch = strstr(direct->d_name, ".conv");
        if (!pch || strcmp(pch, ".conv") != 0) {
            continue;
        }
        char name[256];
        strncpy(name, direct->d_name, sizeof(name) - 1);
        name[sizeof(name) - 1] = '\0';
        strremove(name, ".conv");
        if (name[0] == '\0') {
            continue;
        }
        if (!first) {
            strcat(ret, "|");
        }
        strncat(ret, name, sizeof(ret) - strlen(ret) - 1);
        first = 0;
    }
    closedir(d);
    strcpy(dir, ret);
}

static void registerUser(char *dir)
{
    char username[256];
    char *password = split_pipe(dir, username, sizeof(username));
    trim_inplace(password);

    if (username[0] == '\0' || password[0] == '\0') {
        strcpy(dir, "Error|Username and password are required");
        return;
    }
    if (user_exists(username)) {
        strcpy(dir, "Error|Username already exists");
        return;
    }

    FILE *usersFile = fopen("credentials.txt", "a");
    if (!usersFile) {
        strcpy(dir, "Error|Could not save user");
        return;
    }
    fprintf(usersFile, "\n%s|%s", username, password);
    fclose(usersFile);
    strcpy(dir, "Register successful!");
}

static void getuserchats(char *dir)
{
    char username[256];
    strncpy(username, dir, sizeof(username) - 1);
    username[sizeof(username) - 1] = '\0';
    trim_inplace(username);

    DIR *d = opendir(".");
    char ret[4096] = "";
    dir[0] = '\0';
    if (!d) {
        return;
    }

    struct dirent *direct;
    int first = 1;
    while ((direct = readdir(d)) != NULL) {
        char *pch = strstr(direct->d_name, ".users");
        if (!pch || strcmp(pch, ".users") != 0) {
            continue;
        }
        FILE *fp = fopen(direct->d_name, "r");
        if (!fp) {
            continue;
        }
        char *line = NULL;
        size_t len = 0;
        int belongs = 0;
        while (getline(&line, &len, fp) != -1) {
            trim_inplace(line);
            if (strcmp(line, username) == 0) {
                belongs = 1;
                break;
            }
        }
        free(line);
        fclose(fp);
        if (!belongs) {
            continue;
        }
        char name[256];
        strncpy(name, direct->d_name, sizeof(name) - 1);
        name[sizeof(name) - 1] = '\0';
        strremove(name, ".users");
        if (!first) {
            strcat(ret, "|");
        }
        strncat(ret, name, sizeof(ret) - strlen(ret) - 1);
        first = 0;
    }
    closedir(d);
    strcpy(dir, ret);
}

static void getadminchats(char *dir)
{
    char username[256];
    strncpy(username, dir, sizeof(username) - 1);
    username[sizeof(username) - 1] = '\0';
    trim_inplace(username);

    DIR *d = opendir(".");
    char ret[4096] = "";
    dir[0] = '\0';
    if (!d) {
        return;
    }

    struct dirent *direct;
    int first = 1;
    while ((direct = readdir(d)) != NULL) {
        char *pch = strstr(direct->d_name, ".users");
        if (!pch || strcmp(pch, ".users") != 0) {
            continue;
        }
        FILE *fp = fopen(direct->d_name, "r");
        if (!fp) {
            continue;
        }
        char *line = NULL;
        size_t len = 0;
        int is_admin = 0;
        if (getline(&line, &len, fp) != -1) {
            trim_inplace(line);
            if (strcmp(line, username) == 0) {
                is_admin = 1;
            }
        }
        free(line);
        fclose(fp);
        if (!is_admin) {
            continue;
        }
        char name[256];
        strncpy(name, direct->d_name, sizeof(name) - 1);
        name[sizeof(name) - 1] = '\0';
        strremove(name, ".users");
        if (!first) {
            strcat(ret, "|");
        }
        strncat(ret, name, sizeof(ret) - strlen(ret) - 1);
        first = 0;
    }
    closedir(d);
    strcpy(dir, ret);
}

static void getchat(char *dir)
{
    trim_inplace(dir);
    if (!valid_room_name(dir)) {
        strcpy(dir, "");
        return;
    }

    char filename[512];
    snprintf(filename, sizeof(filename), "%s.conv", dir);

    FILE *fp = fopen(filename, "r");
    if (fp == NULL) {
        strcpy(dir, "");
        return;
    }

    char send[65536] = "";
    char *line = NULL;
    size_t len = 0;
    while (getline(&line, &len, fp) != -1) {
        if (strlen(send) + strlen(line) + 1 >= sizeof(send)) {
            break;
        }
        strcat(send, line);
    }
    free(line);
    fclose(fp);
    strcpy(dir, send);
}

static void getchatusers(char *dir)
{
    trim_inplace(dir);
    if (!valid_room_name(dir)) {
        strcpy(dir, "");
        return;
    }

    char filename[512];
    snprintf(filename, sizeof(filename), "%s.users", dir);
    FILE *fp = fopen(filename, "r");
    if (!fp) {
        strcpy(dir, "");
        return;
    }

    char ret[4096] = "";
    char *line = NULL;
    size_t len = 0;
    int first = 1;
    while (getline(&line, &len, fp) != -1) {
        trim_inplace(line);
        if (line[0] == '\0') {
            continue;
        }
        if (!first) {
            strcat(ret, "|");
        }
        strncat(ret, line, sizeof(ret) - strlen(ret) - 1);
        first = 0;
    }
    free(line);
    fclose(fp);
    strcpy(dir, ret);
}

static void addUser(char *dir)
{
    char user[256];
    char *groupName = split_pipe(dir, user, sizeof(user));
    trim_inplace(groupName);

    if (user[0] == '\0' || !valid_room_name(groupName)) {
        strcpy(dir, "Error|Invalid user or room");
        return;
    }

    char users[512];
    snprintf(users, sizeof(users), "%s.users", groupName);

    FILE *check = fopen(users, "r");
    if (check) {
        char *line = NULL;
        size_t len = 0;
        while (getline(&line, &len, check) != -1) {
            trim_inplace(line);
            if (strcmp(line, user) == 0) {
                free(line);
                fclose(check);
                snprintf(dir, 2048, "%s|%s|Already a member", user, groupName);
                return;
            }
        }
        free(line);
        fclose(check);
    }

    FILE *usersFile = fopen(users, "a");
    if (!usersFile) {
        strcpy(dir, "Error|Chat room not found");
        return;
    }
    fprintf(usersFile, "%s\n", user);
    fclose(usersFile);

    snprintf(dir, 2048, "%s|%s|Added", user, groupName);
}

static void deleteUser(char *dir)
{
    char user[256];
    char *groupName = split_pipe(dir, user, sizeof(user));
    trim_inplace(groupName);

    if (user[0] == '\0' || !valid_room_name(groupName)) {
        strcpy(dir, "Error|Invalid user or room");
        return;
    }

    char users[512];
    snprintf(users, sizeof(users), "%s.users", groupName);

    FILE *usersFile = fopen(users, "r");
    if (usersFile == NULL) {
        strcpy(dir, "Error|Chat room not found");
        return;
    }

    char send[8192] = "";
    char *line = NULL;
    size_t len = 0;
    while (getline(&line, &len, usersFile) != -1) {
        trim_inplace(line);
        if (line[0] == '\0') {
            continue;
        }
        if (strcmp(user, line) != 0) {
            strcat(send, line);
            strcat(send, "\n");
        }
    }
    free(line);
    fclose(usersFile);

    usersFile = fopen(users, "w");
    if (usersFile) {
        fputs(send, usersFile);
        fclose(usersFile);
    }

    snprintf(dir, 2048, "%s|%s|Deleted", user, groupName);
}

static void messageSent(char *dir)
{
    char message[4096];
    char *groupName = split_pipe(dir, message, sizeof(message));
    trim_inplace(groupName);

    if (message[0] == '\0' || !valid_room_name(groupName)) {
        strcpy(dir, "Error|Invalid message or room");
        return;
    }

    char conv[512];
    snprintf(conv, sizeof(conv), "%s.conv", groupName);

    FILE *convFile = fopen(conv, "a");
    if (!convFile) {
        strcpy(dir, "Error|Chat room not found");
        return;
    }
    fprintf(convFile, "%s\n", message);
    fclose(convFile);

    strcpy(dir, "Message sent!");
}

#endif /* CHATBOOK_CHATS_H */
