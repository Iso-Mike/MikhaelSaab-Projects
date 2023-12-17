#include "defs.h"

/*
  Function:  initRestaurant
   Purpose:  Initializes a RestaurantType structure, setting up patron and reservation arrays
    in-out:  r - A pointer to the RestaurantType structure to be initialized
        in:  n - A character pointer representing the name of the restaurant
*/
void initRestaurant(RestaurantType *r, char *n) {
  if(!r || !n) {
    printf("Error: NULL pointer provided to initRestaurant.\n");
    return;
  }

  strncpy(r->name, n, MAX_STR - 1);
  r->name[MAX_STR - 1] = '\0'; 
  initPatronArray(&r->patrons);
  initResvList(&r->reservations);
}

/*
  Function:  validateResvTime
   Purpose:  Validates the provided date and time for a reservation
        in:  yr - An integer representing the year of the reservation
        in:  mth - An integer representing the month of the reservation
        in:  day - An integer representing the day of the reservation
        in:  hr - An integer representing the hour of the reservation
        in:  min - An integer representing the minute of the reservation
    return:  An integer flag indicating valid (C_OK) or invalid (C_NOK) time
*/
int validateResvTime(int yr, int mth, int day, int hr, int min) {
  int currentYear = 2023;
  
  if(yr < currentYear) {
    return C_NOK;
  }

  if(mth < 1 || mth > 12) {
    return C_NOK;
  }

  if(day > 31) {
    return C_NOK;
  }
  
  int maxDays[] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
  if(day < 1 || day > maxDays[mth - 1]) {
    return C_NOK;
  }
  
  if(hr < 0 || hr > 23) {
    return C_NOK;
  }

  if(min < 0 || min > 59) {
    return C_NOK;
  }

  return C_OK; 
}

/*
  Function:  createResv
   Purpose:  Creates a new reservation and adds it to a restaurant
    in-out:  r - A pointer to the RestaurantType structure where the reservation will be added
        in:  pId - An integer representing the ID of the patron making the reservation
        in:  yr - An integer representing the year of the reservation
        in:  mth - An integer representing the month of the reservation
        in:  day - An integer representing the day of the reservation
        in:  hr - An integer representing the hour of the reservation
        in:  min - An integer representing the minute of the reservation
*/
void createResv(RestaurantType *r, int pId, int yr, int mth, int day, int hr, int min) {
  if(!r) {
    printf("Error: NULL pointer provided to createResv.\n");
    return;
  }

  if(validateResvTime(yr, mth, day, hr, min) == C_NOK) {
    printf("ERROR: Date %d-%02d-%02d or time %02d:%02d is invalid\n", yr, mth, day, hr, min);
    return;
  }

  PatronType *patron = NULL;
  if(findPatron(&r->patrons, pId, &patron) == C_NOK) {
    printf("ERROR: Patron id %d was not found\n", pId);
    return;
  }

  ResvTimeType *resvTime = NULL;
  initResvTime(&resvTime, yr, mth, day, hr, min);
  if(!resvTime) {
    printf("Failed to allocate memory for reservation time.\n");
    return;
  }

  ResvType *newResv = NULL;
  initResv(&newResv, patron, resvTime);
  if(!newResv) {
    printf("Failed to allocate memory for reservation.\n");
    free(resvTime);
    return;
  }

  addResv(&r->reservations, newResv);
}

/*
  Function:  printResByPatron
   Purpose:  Prints all reservations made by a specific patron
        in:  r - A pointer to the RestaurantType structure containing the reservation data
        in:  id - An integer representing the patron's ID
*/
void printResByPatron(RestaurantType *r, int id) {
  if(!r) {
    printf("Error: NULL pointer provided to printResByPatron.\n");
    return;
  }

  printf("\nRESERVATIONS BY PATRON %d at %s:\n", id, r->name);
  NodeType *current = r->reservations.head;
  while(current != NULL) {
    if(current->data->patron->id == id) {
      printReservation(current->data);
    }
    current = current->next;
  }
}

/*
  Function:  cleanupRestaurant
   Purpose:  Frees all dynamically allocated memory associated with a restaurant
    in-out:  r - A pointer to the RestaurantType structure to be cleaned up
*/
void cleanupRestaurant(RestaurantType *r) {
  if(!r) {
    printf("Error: NULL pointer provided to cleanupRestaurant.\n");
    return;
  }

  cleanupPatronArray(&r->patrons);
  cleanupResvList(&r->reservations);
}