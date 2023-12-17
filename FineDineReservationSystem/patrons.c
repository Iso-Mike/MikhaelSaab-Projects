#include "defs.h"

/*
  Function:  initPatronArray
   Purpose:  Initializes a PatronArrayType structure, setting up a dynamic array for patrons
    in-out:  arr - A pointer to the PatronArrayType structure to be initialized
*/
void initPatronArray(PatronArrayType *arr) {
  if(!arr) {
    printf("Error: NULL pointer provided to initPatronArray.\n");
    return;
  }

  arr->customers = malloc(MAX_CAP * sizeof(PatronType));
  if(!arr->customers) {
    printf("Error: Memory allocation failed for customers.\n");
    return;
  }

  arr->nextID = PATRON_IDS;
  arr->size = 0;
}

/*
  Function:  addPatron
   Purpose:  Adds a new patron to an existing array of patrons
    in-out:  arr - A pointer to the PatronArrayType structure where the patron will be added
        in:  n - A character pointer representing the name of the new patron
*/
void addPatron(PatronArrayType *arr, char *n) {
  if(!arr || !n) {
    printf("Error: NULL pointer provided to addPatron.\n");
    return;
  }

  if(arr->size >= MAX_CAP) {
    printf("Array full");
    return;
  }
  
  strncpy(arr->customers[arr->size].name, n, MAX_STR-1);
  arr->customers[arr->size].name[MAX_STR - 1] = '\0';

  arr->customers[arr->size].id = arr->nextID;
  arr->nextID++;
  arr->size++;
}

/*
  Function:  findPatron
   Purpose:  Searches for a patron by their ID in a given array of patrons
        in:  arr - A pointer to the PatronArrayType structure to be searched
        in:  id - An integer representing the ID of the patron to find
       out:  p - A double pointer to a PatronType where the found patron's data will be stored
    return:  An integer flag indicating success (C_OK) or failure (C_NOK) of the operation
*/
int findPatron(PatronArrayType *arr, int id, PatronType **p) {
  if(!arr || !p) {
    printf("Error: NULL pointer provided to findPatron.\n");
    return C_NOK;
  }

  for(int i = 0; i < arr->size; i++) {
    if(arr->customers[i].id == id) {
      *p = &(arr->customers[i]);
      return C_OK;
    }
  }
  *p = NULL;
  return C_NOK;
}

/*
  Function:  printPatrons
   Purpose:  Prints all patron details from a given array of patrons
        in:  arr - A pointer to the PatronArrayType structure containing the patron data
*/
void printPatrons(PatronArrayType *arr) {
  if(!arr) {
    printf("Error: NULL pointer provided to printPatrons.\n");
    return;
  }

  for(int i = 0; i < arr->size; i++) {
    printf("Patron #%d %s\n", arr->customers[i].id, arr->customers[i].name);
  }
}

/*
  Function:  cleanupPatronArray
   Purpose:  Frees memory allocated for the dynamic array of patrons
    in-out:  arr - A pointer to the PatronArrayType structure whose memory is to be freed
*/
void cleanupPatronArray(PatronArrayType *arr) {
  if(!arr) {
    printf("Error: NULL pointer provided to cleanupPatronArray.\n");
    return;
  }

  if(arr->customers) {
    free(arr->customers);
    arr->customers = NULL;
  }
}