OBJ = main.o connect.o escape.o flyer.o hero.o view.o spectator.o
EXE = a5
CC = gcc -Wall -g

$(EXE):	$(OBJ)
	$(CC) -o $(EXE) $(OBJ)

main.o:	main.c defs.h
	$(CC) -c main.c

connect.o:	connect.c defs.h
	$(CC) -c connect.c

flyer.o:	flyer.c defs.h
	$(CC) -c flyer.c

hero.o:	hero.c defs.h
	$(CC) -c hero.c

escape.o: escape.c defs.h
	$(CC) -c escape.c

view.o: view.c defs.h
	$(CC) -c view.c

spectator.o: spectator.c defs.h
	$(CC) -c spectator.c

clean:
	rm -f $(EXE) $(OBJ)

