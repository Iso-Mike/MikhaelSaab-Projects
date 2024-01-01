#include "defs.h"

pthread_mutex_t hollowMutex;
int runCommManager = 1;

void* communicationsManager(void *arg);

/*
  Function:  runEscape
   Purpose:  Executes the main loop for an escape scenario, handling flyer spawns, hero movements, and collisions
*/
void runEscape() {
  EscapeType *esc = malloc(sizeof(EscapeType));
  pthread_t commThread;

  pthread_mutex_init(&hollowMutex, NULL);

  initEscape(esc);

  pthread_create(&commThread, NULL, communicationsManager, esc);

  while(!escapeIsOver(esc)) {
    pthread_mutex_lock(&hollowMutex);
    int birdSpawn = randomInt(100);
    int monkSpawn = randomInt(100);

    if(birdSpawn < BIRD_SPAWN_RATE) {
      int birdRow = randomInt(5);
      int birdStr = randomInt(2) + 3;
      spawnFlyer(esc, 'v', birdStr, randomInt(MAX_COL), birdRow);
    } 
    
    if(monkSpawn < MONKEY_SPAWN_RATE) {
      int monkRow = randomInt(15);
      int monkStr = randomInt(4) + 8;
      spawnFlyer(esc, '@', monkStr, randomInt(MAX_COL), monkRow);
    }
    
    for(int i = 0; i < esc->heroes.size; i++) {
      moveHero(esc->heroes.elements[i], esc);
    }

    for(int i = 0; i < esc->flyers.size; i++) {
      if(esc->flyers.elements[i]) {
        moveFlyer(esc->flyers.elements[i], esc);
      }
      if(checkForCollision(&esc->flyers.elements[i]->partInfo.pos, esc)) {
        incurDamage(checkForCollision(&esc->flyers.elements[i]->partInfo.pos, esc), esc->flyers.elements[i]);
      }
    }
    
    outputHollow(esc); 
    pthread_mutex_unlock(&hollowMutex);
    usleep(300000);
  }
  printf("\n");
  runCommManager = 0;
  pthread_join(commThread, NULL);

  handleEscapeResult(esc);
  cleanupEscape(esc);

  pthread_mutex_destroy(&hollowMutex);
}

/*
  Function:  escapeIsOver
   Purpose:  Determines if an escape scenario is over, based on the status of heroes involved
        in:  *esc - A pointer to the EscapeType structure representing the escape scenario
    return:  An integer indicating whether the escape is over (C_TRUE) or not (C_FALSE)
*/
int escapeIsOver(EscapeType *esc) {
  if(!esc) {
    return C_TRUE;
  }

  for(int i = 0; i < esc->heroes.size; i++) {
    if(esc->heroes.elements[i]->dead == C_FALSE && heroIsSafe(esc->heroes.elements[i]) == C_FALSE) {
      return C_FALSE;
    }
  }
  
  return C_TRUE;
}

/*
  Function:  initEscape
   Purpose:  Initializes an escape scenario by setting up hero elements, allocating memory, and ensuring unique hero characteristics
        in:  *esc - A pointer to the EscapeType structure representing the escape scenario to be initialized
*/
void initEscape(EscapeType *esc) {
  if(!esc) {
    printf("Error: NULL pointer provided to initEscape.\n");
    return;
  }

  esc->heroes.elements = malloc(MAX_ARR*sizeof(HeroType*));
  if (!esc->heroes.elements) {
    printf("Error: Memory allocation failed for the heroes elements.\n");
    return;
  }

  esc->heroes.size = 0;
  esc->flyers.size = 0;

  int tCol = randomInt(4);
  int hCol = randomInt(4);
  while(tCol == hCol) {
    hCol = randomInt(4);
  }

  HeroType *t, *h;

  initHero(&t, 'T', tCol, "Timmy");
  if(!t) {
    printf("Error: Failed to initialize hero Timmy.\n");
    free(esc->heroes.elements);
    return;
  }

  initHero(&h, 'H', hCol, "Harold");
  if(!h) {
    printf("Error: Failed to initialize hero Harold.\n");
    free(t);
    free(esc->heroes.elements);
    return;
  }

  addHero(&esc->heroes, t);
  addHero(&esc->heroes, h);

  setupServerSocket(&esc->listenSocket);
  acceptConnection(esc->listenSocket, &esc->viewSocket);
}

/*
  Function:  cleanupEscape
   Purpose:  Frees allocated memory and cleans up resources used in an escape scenario
        in:  *esc - A pointer to the EscapeType structure representing the escape scenario to be cleaned up
*/
void cleanupEscape(EscapeType *esc) {
  if(!esc) {
    printf("Error: NULL pointer provided to cleanupEscape.\n");
    return;
  }

  if(esc->listenSocket > 0) {
    close(esc->listenSocket);
  }

  if(esc->viewSocket > 0) {
    close(esc->viewSocket);
  }

  if(esc->heroes.elements) {
    for(int i = 0; i < esc->heroes.size; i++) {
      if(esc->heroes.elements[i]) {
        free(esc->heroes.elements[i]);
        esc->heroes.elements[i] = NULL;
      }
    }
    free(esc->heroes.elements);
    esc->heroes.elements = NULL;
  }

  esc->heroes.size = 0;

  for(int i = 0; i < esc->flyers.size; i++) {
    if(esc->flyers.elements[i]) {
      free(esc->flyers.elements[i]);
      esc->flyers.elements[i] = NULL;
    }
  }

  free(esc);
}

/*
  Function:  setPos
   Purpose:  Sets the position of an object, ensuring it stays within the grid boundaries
        in:  *pos - A pointer to the PositionType structure representing the position to be set
        in:  row - The row number to set the position to
        in:  col - The column number to set the position to
*/
void setPos(PositionType *pos, int row, int col) {
  if(!pos) {
    printf("Error: NULL pointer provided to setPos.\n");
    return;
  }
  
  if(col < 0) {
    pos->col = 0;
  } else if (col >= MAX_COL) {
    pos->col = MAX_COL - 1;
  } else {
    pos->col = col;
  }

  if(row < 0) {
    pos->row = 0;
  } else if (row >= MAX_ROW) {
    pos->row = MAX_ROW;
  } else {
    pos->row = row;
  }
}

void* communicationsManager(void *arg) {
    EscapeType *esc = (EscapeType*) arg;

    while(runCommManager) {
        pthread_mutex_lock(&hollowMutex);
        outputHollow(esc);  // Assuming this is the function that outputs the Hollow
        pthread_mutex_unlock(&hollowMutex);
        usleep(500000);  // Output at intervals of 500,000 microseconds
    }

    return NULL;
}