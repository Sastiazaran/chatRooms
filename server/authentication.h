#include <stdlib.h> 
#include <string.h>
#include <time.h>


char *itoa(int n)
{
  static char   buf[32];
  sprintf(buf,"%d ",n);
  return  buf;
}

void auth(dir)
  char *dir;
{
    FILE *fp;
    char *line = 0;
    size_t len = 0;
    ssize_t read;
    int result;

    printf("\nPalabra descifrada %s \n", dir);

    fp = fopen("credentials.txt", "r");
    if (fp == NULL) {
        return;
    }

    while ((read = getline(&line, &len, fp)) != -1) {        
        line[strlen(line)-2] = '\0';
        result = strcmp(dir,line);
        if (result == 0) {          
            strcpy(dir,"Granted\n");
            return;
        }
    }
    free(line);
    strcpy(dir,"Denied\n");
}

void getusers(dir) char *dir;
{
    FILE *fp;
    char *line = 0;
    size_t len = 0;
    ssize_t read;
    int line_len;
    char pch[1000];
    int j = 0;
    char it;

    fp = fopen("credentials.txt", "r");
    if (fp == NULL)
    {
        return;
    }

    int skip = 0;
    while ((read = getline(&line, &len, fp)) != -1)
    {
        if (skip == 0)
        {
            skip++;
            continue;
        }
        line_len = strlen(line);
        for (int i = 0; i < line_len; i++)
        {
            pch[j] = line[i];
            if (line[i] == '|')
            {
                i = line_len;
            }
            j++;
        }
    }
    pch[j-1] = '\0';
    strcpy(dir, pch);
    strcat(dir, "\0");
    return;
}

