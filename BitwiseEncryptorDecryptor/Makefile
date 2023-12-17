# Makefile for Custom Encryption and Decryption Tool

CC = gcc
CFLAGS = -Wall -std=c11
EXEC_NAME = CustomEncryptDecrypt
SRC = CustomEncryptDecrypt.c
OBJ = $(SRC:.c=.o)

all: $(EXEC_NAME)

$(EXEC_NAME): $(OBJ)
	$(CC) $(CFLAGS) -o $(EXEC_NAME) $(OBJ)

%.o: %.c
	$(CC) $(CFLAGS) -c $<

clean:
	rm -f $(OBJ) $(EXEC_NAME)

.PHONY: all clean
