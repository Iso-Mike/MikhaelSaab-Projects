#include "defs.h"

/*
  Function:  flyerIsDone
   Purpose:  Determines if a flyer has reached its final position in the grid
        in:  *f - A pointer to the FlyerType structure representing the flyer
    return:  An integer indicating whether the flyer has reached the final row (C_TRUE) or not (C_FALSE)
*/
int flyerIsDone(FlyerType *f) {
  if(!f) {
    printf("Error: NULL pointer provided to flyerIsDone.\n");
    return C_FALSE;
  }

  return (f->partInfo.pos.row >= MAX_ROW - 1) ? C_TRUE : C_FALSE;
}

/*
  Function:  incurDamage
   Purpose:  Applies damage to a hero based on the strength of a flyer
        in:  *h - A pointer to the HeroType structure representing the hero
        in:  *f - A pointer to the FlyerType structure representing the flyer
*/
void incurDamage(HeroType *h, FlyerType *f) {
  if(!h || !f) {
    printf("Error: NULL pointer provided to incurDamage.\n");
    return;
  }

  h->health -= f->strength;

  if(h->health <= 0) {
    h->health = 0;
    h->partInfo.avatar = '+';
    h->dead = C_TRUE;
  }
}

/*
  Function:  spawnFlyer
   Purpose:  Creates a new flyer and adds it to the escape scenario
        in:  *esc - A pointer to the EscapeType structure representing the escape scenario
        in:  av - The avatar character representing the flyer
        in:  str - The strength of the flyer
        in:  col - The column position where the flyer will be spawned
        in:  row - The row position where the flyer will be spawned
*/
void spawnFlyer(EscapeType *esc, char av, int str, int col, int row) {
  if(!esc) {
    printf("Error: NULL pointer provided to spawnFlyer.\n");
    return;
  }

  FlyerType *flyer = malloc(sizeof(FlyerType));
  if(!flyer) {
    printf("Error: Memory allocation failed for the flyer.\n");
    return;
  }
  
  flyer->strength = str;
  flyer->partInfo.avatar = av;
  flyer->partInfo.pos.col = col;
  flyer->partInfo.pos.row = row;

  addFlyer(&esc->flyers, flyer);
}

/*
  Function:  addFlyer
   Purpose:  Adds a flyer to the FlyerArrayType array
        in:  *fArr - A pointer to the FlyerArrayType structure representing the array of flyers
        in:  *f - A pointer to the FlyerType structure representing the flyer to be added
*/
void addFlyer(FlyerArrayType *fArr, FlyerType *f) {
  if(!fArr || !f) {
    printf("Error: NULL pointer provided to addFlyer.\n");
    return;
  }

  if(fArr->size >= MAX_ARR) {
    printf("Flyer array full.\n");
    return;
  }

  fArr->elements[fArr->size] = f;
  fArr->size++;
}

/*
  Function:  moveFlyer
   Purpose:  Moves a flyer within the escape scenario based on its type and random movement patterns
        in:  *f - A pointer to the FlyerType structure representing the flyer to be moved
        in:  *esc - A pointer to the EscapeType structure representing the escape scenario
*/
void moveFlyer(FlyerType *f, EscapeType *esc) {
  if(!f || !esc) {
    printf("Error: NULL pointer provided to moveFlyer.\n");
    return;
  }

  if(f->partInfo.avatar == 'v') {
    int birdRow = f->partInfo.pos.row + 1;
    int birdCol = f->partInfo.pos.col;
    int direction = randomInt(2);

    birdCol += (direction == 0) ? DIR_LEFT : DIR_RIGHT;

    setPos(&f->partInfo.pos, birdRow, birdCol);
  } else if(f->partInfo.avatar == '@') {
    int verticalMove = randomInt(7) - 3;
    int horizontalMove = randomInt(3) + 1;
    int direction = 0;

    int monkRow = f->partInfo.pos.row + verticalMove;
    int monkCol = f->partInfo.pos.col;
    computeHeroDir(esc, f, &direction);

    monkCol += direction * horizontalMove;

    setPos(&f->partInfo.pos, monkRow, monkCol);
  }
}

/*
  Function:  checkForCollision
   Purpose:  Checks if a given position corresponds to the position of any hero in the escape scenario
        in:  *fPos - A pointer to the PositionType structure representing the position to be checked for collision
        in:  *esc - A pointer to the EscapeType structure representing the escape scenario
    return:  A pointer to the HeroType structure of the collided hero, or NULL if no collision is detected
*/
HeroType* checkForCollision(PositionType *fPos, EscapeType *esc) {
  if(!fPos || !esc) {
    printf("Error: NULL pointer provided to checkForCollision.\n");
    return NULL;
  }

  for(int i = 0; i < esc->heroes.size; i++) {
    if(fPos->col == esc->heroes.elements[i]->partInfo.pos.col && fPos->row == esc->heroes.elements[i]->partInfo.pos.row) {
      return esc->heroes.elements[i];
    }
  }

  return NULL;
}

/*
  Function:  computeHeroDir
   Purpose:  Calculates the direction a flyer should move to approach the nearest hero
        in:  *esc - A pointer to the EscapeType structure representing the escape scenario
        in:  *f - A pointer to the FlyerType structure representing the flyer
       out:  *dir - A pointer to an integer where the computed direction will be stored (-1 for left, 1 for right, 0 for no horizontal movement)
*/
void computeHeroDir(EscapeType *esc, FlyerType *f, int *dir) {
  if(!esc || !f || !dir) {
    printf("Error: NULL pointer provided to spawnFlyer.\n");
    return;
  }

  int closestDistance = MAX_COL;

  for(int i = 0; i < esc->heroes.size; i++) {
    HeroType* hero = esc->heroes.elements[i];

    if(!hero->dead && !heroIsSafe(hero)) {
      int distance = hero->partInfo.pos.col - f->partInfo.pos.col;

      if(abs(distance) < abs(closestDistance)) {
        closestDistance = distance;
      }
    }
  }

  if(closestDistance < 0) {
    *dir = DIR_LEFT;
  } else if(closestDistance > 0) {
    *dir = DIR_RIGHT;
  } else {
    *dir = DIR_SAME;
  }
}