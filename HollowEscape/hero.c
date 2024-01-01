#include "defs.h"

/*
  Function:  initHero
   Purpose:  Initializes a hero with specified attributes and allocates memory for it
        in:  **h - A double pointer to the HeroType structure for the hero to be initialized
        in:  av - The avatar character representing the hero
        in:  col - The initial column position of the hero
        in:  *n - A string representing the name of the hero
*/
void initHero(HeroType **h, char av, int col, char *n) {
  if(!h || !n) {
    printf("Error: NULL pointer provided to initHero.\n");
    return;
  }

  *h = (HeroType *)malloc(sizeof(HeroType));
  if(!(*h)) {
    printf("Error: Memory allocation failed for hero array.\n");
    return;
  }

  strncpy((*h)->name, n, MAX_STR - 1);
  (*h)->name[MAX_STR - 1] = '\0';

  (*h)->partInfo.avatar = av;
  (*h)->partInfo.pos.col = col;
  (*h)->partInfo.pos.row = MAX_ROW - 1;
  (*h)->health = MAX_HEALTH;
  (*h)->dead = C_FALSE;
}

/*
  Function:  addHero
   Purpose:  Adds a hero to the HeroArrayType array
        in:  *hArr - A pointer to the HeroArrayType structure representing the array of heroes
        in:  *h - A pointer to the HeroType structure representing the hero to be added
*/
void addHero(HeroArrayType *hArr, HeroType *h) {
  if(!hArr || !h) {
    printf("Error: NULL pointer provided to addHero.\n");
    return;
  }

  if(hArr->size >= MAX_ARR) {
    printf("Hero array is full.");
    return;
  }

  hArr->elements[hArr->size] = h;
  hArr->size++;
}

/*
  Function:  moveHero
   Purpose:  Moves a hero within the escape scenario based on random patterns and the hero's avatar
        in:  *h - A pointer to the HeroType structure representing the hero to be moved
        in:  *esc - A pointer to the EscapeType structure representing the escape scenario
*/
void moveHero(HeroType *h, EscapeType *esc) {
  if(!h || !esc) {
    printf("Error: NULL pointer provided to moveHero.\n");
    return;
  }
  
  if(h->dead || heroIsSafe(h)) {
    return;
  }

  int newPos = h->partInfo.pos.col;
  char shift = randomInt(100) + 1;

  if(h->partInfo.avatar == 'T') {
    if(shift <= 50) {
      newPos += 3; 
    } else if(shift <= 80) {
      newPos += 1;
    } else if(shift <= 100) {
      newPos -= 2;
    }
  } else if(h->partInfo.avatar == 'H') {
    if(shift <= 40)  {
      newPos += 4;
    } else if(shift <= 60) {
      newPos -= 2;
    } else if(shift <= 80) {
      newPos = h->partInfo.pos.col;
    } else if(shift <= 90) {
      newPos += 6;
    } else if(shift <= 100) {
      newPos -= 4;
    }
  }
    
  setPos(&h->partInfo.pos, MAX_ROW-1, newPos);
}

/*
  Function:  heroIsSafe
   Purpose:  Determines if a hero has reached a safe position in the grid
        in:  *h - A pointer to the HeroType structure representing the hero
    return:  An integer indicating whether the hero is in a safe position (C_TRUE) or not (C_FALSE)
*/
int heroIsSafe(HeroType *h) {
  if(!h) {
    printf("Error: NULL pointer provided to heroIsSafe.\n");
    return C_FALSE;
  }

  return (h->partInfo.pos.col >= MAX_COL - 1) ? C_TRUE : C_FALSE;
}