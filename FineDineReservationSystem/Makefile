# Makefile for FineDine Reservation System

CC = gcc
CFLAGS = -Wall -std=c11
EXEC_NAME = FineDineManager
SRC = main.c patrons.c resv.c load.c restaurant.c
OBJ = $(SRC:.c=.o)

all: $(EXEC_NAME)

$(EXEC_NAME): $(OBJ)
	$(CC) $(CFLAGS) -o $(EXEC_NAME) $(OBJ)

%.o: %.c
	$(CC) $(CFLAGS) -c $<

clean:
	rm -f $(OBJ) $(EXEC_NAME)

.PHONY: all clean
