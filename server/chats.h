#include <stdlib.h> 
#include <unistd.h>
#include <string.h>
#include <stdbool.h>
#include "utilities.h"

void creargrupo(dir)
  char *dir;
{
    FILE *convFile;
    FILE *usersFile;

    char conv[1000];
    char users [1000];
    
    char* target = strdup(dir);
    char *groupName = strstr(target, "|");
    char *user = strremove(target, groupName);
    groupName = strremove(dir, user);
    memmove(groupName, groupName + 1, strlen(groupName));
    
    strcpy(conv,groupName);
    strcpy(users,groupName);
    strcat(conv,".conv");
    strcat(users,".users");

    convFile = fopen(conv, "w");
    usersFile = fopen(users, "w");
    fprintf(usersFile,"%s",user);
    fclose(convFile);
    fclose(usersFile);

    strcpy(target,user);
    strcat(target,"|");
    strcat(target,groupName);
    strcat(target,"|True");
    strcpy(dir, target);    
}

void getchats(dir) char *dir;
{
    DIR *d;
    struct dirent *direct;
    d = opendir(".");
    char direc[1000] = "";
    char ret[1000] = "";
    char *dic;
    char empty[2] = "\0" ;
    strcpy(dir,empty);
    if (d)
    {
        while ((direct = readdir(d)) != NULL)
        {
            strcpy(direc,direct->d_name); 
            char *pch = strstr(direc, ".conv");
            if (pch) {            
                dic = strremove(direc,".conv");
                strcat(ret,dic);
                strcat(ret,"|");
            }            
        }
        closedir(d);
        ret[strlen(ret)-1] = '\0';
        strcpy(dir,ret);
    }
}

void getuserchats(dir) char *dir;
{
    FILE *fp;
    char *line = 0;
    size_t len = 0;
    ssize_t read;
    int result;
    DIR *d;
    struct dirent *direct;
    d = opendir(".");
    char direc[1000] = "";
    char ret[1000] = "";
    char *dic;
    char empty[2] = "\0";
    if (d)
    {
        while ((direct = readdir(d)) != NULL)
        {
            strcpy(direc, direct->d_name);
            char *pch = strstr(direc, ".users");
            if (pch)
            {
                fp = fopen(direc, "r");
                if (fp == NULL)
                {
                    break;
                }

                while ((read = getline(&line, &len, fp)) != -1)
                {
                    line[strlen(line)] = '\0';
                    result = strcmp(dir, line);
                    if (result == 0)
                    {
                        strcat(ret, strremove(direc, ".users"));
                        strcat(ret, "|");
                        continue;
                    }
                }
            }
        }
        closedir(d);
        ret[strlen(ret) - 1] = '\0';
        strcpy(dir, ret);
    }
}

void getadminchats(dir) char *dir;
{
    FILE *fp;
    char *line = 0;
    size_t len = 0;
    ssize_t read;
    int result;
    DIR *d;
    struct dirent *direct;
    d = opendir(".");
    char direc[1000] = "";
    char ret[1000] = "";
    char *dic;
    char empty[2] = "\0";
    if (d)
    {
        while ((direct = readdir(d)) != NULL)
        {
            strcpy(direc, direct->d_name);
            char *pch = strstr(direc, ".users");
            if (pch)
            {
                fp = fopen(direc, "r");
                if (fp == NULL)
                {
                    break;
                }

                while ((read = getline(&line, &len, fp)) != -1)
                {
                    line[strlen(line)] = '\0';
                    result = strcmp(dir, line);
                    if (result == 0)
                    {
                        strcat(ret, strremove(direc, ".users"));
                        strcat(ret, "|");
                    }
                    break;
                }
            }
        }
        closedir(d);
        ret[strlen(ret) - 1] = '\0';
        strcpy(dir, ret);
    }
}

void getchat(dir) char *dir;
{
    FILE *fp;
    char *line = 0;
    size_t len = 0;
    ssize_t read;
    int result;
    char filename[1000] = "";
    char send[99999] = "";

    strcat(filename,dir);
    strcat(filename,".conv");
    fp = fopen(filename, "r");
    if (fp == NULL) {
        strcpy(dir,"Null");
    }

    while ((read = getline(&line, &len, fp)) != -1) {        
        line[strlen(line)] = '\0';        
        strcat(send,line);
    }
    strcpy(dir,send);
}

void addUser(dir)
  char *dir;
{
    FILE *usersFile;

    char users [1000];
    
    char* target = strdup(dir);
    char *groupName = strstr(target, "|");
    char *user = strremove(target, groupName);
    groupName = strremove(dir, user);
    memmove(groupName, groupName + 1, strlen(groupName));
    
    strcpy(users,groupName);
    strcat(users,".users");

    usersFile = fopen(users, "a");
    fprintf(usersFile,"\n%s",user);
    fclose(usersFile);

    strcpy(target,user);
    strcat(target,"|");
    strcat(target,groupName);
    strcat(target,"|Added");
    strcpy(dir, target);    
}

void deleteUser(dir) char *dir;
{
    FILE *usersFile;

    char users [1000];
    char *line = 0;
    size_t len = 0;
    ssize_t read;
    char send[99999] = "";
    
    char* target = strdup(dir);
    char *groupName = strstr(target, "|");
    char *user = strremove(target, groupName);
    groupName = strremove(dir, user);
    memmove(groupName, groupName + 1, strlen(groupName));
    
    strcpy(users,groupName);
    strcat(users,".users");

    usersFile = fopen(users, "r");
    if (usersFile == NULL) {
        strcpy(dir,"Null");
    }

    while ((read = getline(&line, &len, usersFile)) != -1) {        
        line[strlen(line)] = '\0';     
        if(strcmp(user, line) != 0 || strcmp(user, line) != -10) {
            strcat(send,line);            
        }
    }
    fclose(usersFile);
    char *newFile = strremove(send,user);
    char file[9999] = "";
    strcpy(file,newFile);
    
    usersFile = fopen(users, "w");
    fprintf(usersFile,"%s",file);
    strcpy(target,user);
    strcat(target,"|");
    strcat(target,groupName);
    strcat(target,"|Deleted");
    strcpy(dir, target);    
}

void messageSent(dir) char *dir;
{
    FILE *convFile;

    char conv [1000];
    
    char* target = strdup(dir);
    char *groupName = strstr(target, "|");
    char *message = strremove(target, groupName);
    groupName = strremove(dir, message);
    memmove(groupName, groupName + 1, strlen(groupName));
    
    strcpy(conv,groupName);
    strcat(conv,".conv");

    convFile = fopen(conv, "a");
    fprintf(convFile,"\n%s",message);
    fclose(convFile);

    strcpy(dir, "Message sent!");
}