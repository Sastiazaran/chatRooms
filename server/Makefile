CC ?= gcc
CFLAGS ?= -Wall -Wextra -O2
TARGET = tcpserver

.PHONY: all clean

all: $(TARGET)

$(TARGET): tcpserver.c authentication.h chats.h utilities.h
	$(CC) $(CFLAGS) tcpserver.c -o $(TARGET)

clean:
	rm -f $(TARGET)
