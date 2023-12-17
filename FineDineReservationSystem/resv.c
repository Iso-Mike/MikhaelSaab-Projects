#include "defs.h"

/*
  Function:  initResvList
   Purpose:  Initializes the reservation list to an empty state
    in-out:  list - A pointer to the ResvListType structure that is to be initialized
*/
void initResvList(ResvListType *list) {
  if(!list) {
    printf("Error: NULL pointer provided to initResvList.\n");
    return;
  }
  list->head = NULL;
  list->nextID = RES_IDS;
}

/*
  Function:  initResvTime
   Purpose:  Allocates and initializes a reservation time structure
       out:  rt - A double pointer to ResvTimeType to store the dynamically allocated and initialized structure
        in:  yr - The year of the reservation time
        in:  mth - The month of the reservation time
        in:  day - The day of the reservation time
        in:  hr - The hour of the reservation time
        in:  min - The minute of the reservation time
*/
void initResvTime(ResvTimeType **rt, int yr, int mth, int day, int hr, int min) {
  if(!rt) {
    printf("Error: NULL pointer provided to initResvTime.\n");
    return;
  }

  *rt = (ResvTimeType *)malloc(sizeof(ResvTimeType));
  if(*rt == NULL) {
    printf("Error: Memory allocation failed in initResvTime.\n");
    return;
  }

  (*rt)->year = yr;
  (*rt)->month = mth;
  (*rt)->day = day;
  (*rt)->hours = hr;
  (*rt)->minutes = min;
}

/*
  Function:  initResv
   Purpose:  Allocates and initializes a reservation structure
       out:  r - A double pointer to ResvType to store the dynamically allocated and initialized reservation
        in:  p - A pointer to a PatronType structure representing the patron making the reservation
        in:  rt - A pointer to a ResvTimeType structure representing the reservation time
*/
void initResv(ResvType **r, PatronType *p, ResvTimeType *rt) {
  if(!r || !p || !rt) {
    printf("Error: NULL pointer provided to initResv.\n");
    return;
  }
  
  *r = (ResvType *)malloc(sizeof(ResvType));
  if(*r == NULL) {
    printf("Error: Memory allocation failed in initResv.\n");
    return;
  }

  (*r)->id = 0;
  (*r)->patron = p;
  (*r)->resvTime = rt;
}

/*
  Function:  lessThan
   Purpose:  Compares two reservation times to determine their chronological order
        in:  r1 - A pointer to the first ResvTimeType structure for comparison
        in:  r2 - A pointer to the second ResvTimeType structure for comparison
    return:  An integer indicating whether the first reservation time is earlier than the second
*/
int lessThan(ResvTimeType *r1, ResvTimeType *r2) {
  if(r1->year != r2->year) {
    return r1->year < r2->year ? C_TRUE : C_FALSE;
  }
  
  if(r1->month != r2->month) {
    return r1->month < r2->month ? C_TRUE : C_FALSE;
  }
  
  if(r1->day != r2->day) {
    return r1->day < r2->day ? C_TRUE : C_FALSE;
  }
  
  if(r1->hours != r2->hours) {
    return r1->hours < r2->hours ? C_TRUE : C_FALSE;
  }
  
  return r1->minutes < r2->minutes ? C_TRUE : C_FALSE;
}

/*
  Function:  addResv
   Purpose:  Adds a new reservation to a reservation list in sorted order
    in-out:  list - A pointer to the ResvListType structure where the new reservation will be added
        in:  r - A pointer to a ResvType structure representing the reservation to be added
*/
void addResv(ResvListType *list, ResvType *r) {
  if(!list || !r) {
    printf("Error: NULL pointer provided to addResv.\n");
    return;
  }

  r->id = list->nextID;
  list->nextID++;

  NodeType *newNode = (NodeType *)malloc(sizeof(NodeType));
  if(newNode == NULL) {
    printf("Error: Memory allocation failed in addResv.\n");
    return;
  }
  newNode->data = r;
  newNode->next = NULL;
  newNode->prev = NULL;
  
  NodeType *current = list->head;
  NodeType *previous = NULL;
  while(current != NULL && lessThan(current->data->resvTime, r->resvTime)) {
    previous = current;
    current = current->next;
  }

  newNode->next = current;
  newNode->prev = previous;
  
  if(previous == NULL) {
    list->head = newNode;
  } else {
    previous->next = newNode;
    if(current != NULL) {
      current->prev = newNode; 
    }
  }
}

/*
  Function:  printReservation
   Purpose:  Prints the details of a single reservation
        in:  r - A pointer to the ResvType structure representing the reservation to be printed
*/
void printReservation(ResvType *r) {
  printf("%d :: %d-%02d-%02d @ %02d:%02d :: %s\n", r->id, r->resvTime->year, r->resvTime->month, r->resvTime->day, r->resvTime->hours, r->resvTime->minutes, r->patron->name);
}

/*
  Function:  printReservations
   Purpose:  Prints all reservations in a list in both forward and backward directions
        in:  list - A pointer to the ResvListType structure containing the reservations
*/
void printReservations(ResvListType *list) {
  printf("--- FORWARD:\n");

  NodeType *current = list->head;

  while(current != NULL) {
    if(current->data != NULL) {
      printReservation(current->data);
    }
    current = current->next;
  }

  if(list->head != NULL) {
    current = list->head;
    while(current->next != NULL) {
      current = current->next;
    }

    printf("\n--- BACKWARD:\n");

    while(current != NULL) {
      if(current->data != NULL) {
        printReservation(current->data);
      }
      current = current->prev;  
    }
  }
}

/*
  Function:  cleanupResvList
   Purpose:  Frees all dynamically allocated memory in a reservation list
    in-out:  list - A pointer to the ResvListType structure to be cleaned up
*/
void cleanupResvList(ResvListType *list) {
  if(!list) {
    printf("Error: NULL pointer provided to cleanupResvList.\n");
    return;
  }

  NodeType *current = list->head;
  while(current) {
    NodeType *temp = current->next;
    free(current->data->resvTime);
    free(current->data);
    free(current);
    current = temp;
  }
  list->head = NULL;
}