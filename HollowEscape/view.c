#include "defs.h"

/*
  Function:  initHollow
   Purpose:  Initializes a grid representation of the escape scenario, placing heroes and flyers in their positions
        in:  *esc - A pointer to the EscapeType structure representing the escape scenario
        in:  grid - A 2D array representing the grid of the escape scenario
*/
void initHollow(EscapeType *esc, char grid[][MAX_COL]) {
  if(!esc) {
    printf("Error: NULL pointer provided to initHollow.\n");
    return;
  }
  
  for(int i = 0; i < MAX_ROW; i++) {
    for(int j = 0; j < MAX_COL; j++) {
      grid[i][j] = ' ';
    }
  }

  for(int i = 0; i < esc->heroes.size; i++) {
    if(!heroIsSafe(esc->heroes.elements[i])) {
      grid[esc->heroes.elements[i]->partInfo.pos.row][esc->heroes.elements[i]->partInfo.pos.col] = esc->heroes.elements[i]->partInfo.avatar;
    }
  }

  for(int i = 0; i < esc->flyers.size; i++) {
    if(!flyerIsDone(esc->flyers.elements[i])) {
      grid[esc->flyers.elements[i]->partInfo.pos.row][esc->flyers.elements[i]->partInfo.pos.col] = esc->flyers.elements[i]->partInfo.avatar;
    }
  }
}

/*
  Function:  serializeHollow
   Purpose:  Converts the grid representation of the escape scenario into a string format
        in:  *esc - A pointer to the EscapeType structure representing the escape scenario
       out:  *hollow - A pointer to a char array where the serialized grid will be stored
*/
void serializeHollow(EscapeType *esc, char *hollow) {
  if(!esc) {
    printf("Error: NULL pointer provided to serializeHollow.\n");
    return;
  }
  
  char grid[MAX_ROW][MAX_COL];
  initHollow(esc, grid);

  int index = 0;
  int heroIndex = 0;

  for(int i = 0; i < MAX_COL+2; i++) {
    hollow[index++] = '-';
  }
  hollow[index++] = '\n';
  
  for(int i = 0; i < MAX_ROW; i++) {
    hollow[index++] = (i == MAX_ROW - 1) ? '=' : '|';

    for(int j = 0; j < MAX_COL; j++) {
      hollow[index++] = grid[i][j];

      if(j == MAX_COL - 1) {
        hollow[index++] = (i == MAX_ROW - 1) ? '=' : '|';

        if(i >= MAX_ROW - 2 && heroIndex < esc->heroes.size) {
          char tempStr[MAX_STR * 2];
          sprintf(tempStr, " %s health: %d", esc->heroes.elements[heroIndex]->name, esc->heroes.elements[heroIndex]->health);
          strcat(hollow, tempStr);
          index += strlen(tempStr);
          heroIndex++;
        }

        hollow[index++] = '\n';
      }
    }
  }

  for(int i = 0; i < MAX_COL+2; i++) {
    hollow[index++] = '-';
  }
  hollow[index++] = '\n';
}

/*
  Function:  outputHollow
   Purpose:  Outputs the serialized representation of the escape scenario grid
        in:  *esc - A pointer to the EscapeType structure representing the escape scenario
*/
void outputHollow(EscapeType *esc) {
  if(!esc) {
    printf("Error: NULL pointer provided to outputHollow.\n");
    return;
  }

  system("clear"); 

  char *str = calloc(sizeof(char), MAX_BUFF);
  if(!str) {
    printf("Error: Memory allocation failed for output buffer.\n");
    return;
  }

  serializeHollow(esc, str);

  printf("%s", str);
  
  sendData(esc->viewSocket, str);
  
  free(str);
}

/*
  Function:  handleEscapeResult
   Purpose:  Reports the final status (escaped or died) of each hero in the escape scenario
        in:  *esc - A pointer to the EscapeType structure representing the escape scenario
*/
void handleEscapeResult(EscapeType *esc) {
  if(!esc) {
    printf("Error: NULL pointer provided to handleEscapeResult.\n");
    return;
  }
  
  sendData(esc->viewSocket, "q");

  outputHollow(esc);

  char *result = calloc(esc->heroes.size, MAX_STR * 2);
  if(!result) {
    printf("Error: Memory allocation failed for result string.\n");
    return;
  }

  for(int i = 0; i < esc->heroes.size; i++) {
    printf("\n%-6s %s", esc->heroes.elements[i]->name, esc->heroes.elements[i]->dead ? "IS DEAD..." : "ESCAPED !!!");
    
    char tempStr[MAX_STR * 2];
    sprintf(tempStr, "%-6s %s\n", esc->heroes.elements[i]->name, esc->heroes.elements[i]->dead ? "IS DEAD..." : "ESCAPED !!!");
    strcat(result, tempStr);
  }
  printf("\n");

  sendData(esc->viewSocket, result);

  free(result);
}