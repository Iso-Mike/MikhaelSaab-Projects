#include <stdio.h>
#include <string.h>

#include "defs.h"

int main() {
  RestaurantType myRestaurant;
  char name[MAX_STR] = "Mike's Steakhouse";
  initRestaurant(&myRestaurant, name);

  loadPatronData(&myRestaurant);
  loadResData(&myRestaurant);

  int userChoice;
  int keepRunning = 1;

  while(keepRunning) {
    printMenu(&userChoice);
    switch(userChoice) {
      case 1:
        printf("\nREGISTERED PATRONS at %s:\n", name);
        printPatrons(&myRestaurant.patrons);
        break;
    
      case 2:
        printf("\nRESERVATIONS at %s:\n", name);
        printReservations(&myRestaurant.reservations);
        break;

      case 3:
        printf("Enter the patron's ID: ");
        int iD;
        scanf("%d", &iD);
        printResByPatron(&myRestaurant, iD);
        break;

      case 0:
        printf("Exiting program.\n");
        keepRunning = 0;
        break;

      default:
        printf("Invalid choice, please enter a number between 0 and 3.\n");
        break;
    }
  }

  cleanupRestaurant(&myRestaurant);
  return 0;
}

/*
  Function:  printMenu
   Purpose:  Displays a menu with various options and prompts the user to make a selection
       out:  choice - A pointer to an integer where the user's menu selection will be stored
*/
void printMenu(int *choice) {
  int c = -1;
  int numOptions = 3;

  printf("\nMAIN MENU\n");
  printf("  (1) Print patrons\n");
  printf("  (2) Print reservations\n");
  printf("  (3) Print reservations by patron\n");
  printf("  (0) Exit\n\n");

  printf("Please enter your selection: ");
  scanf("%d", &c);

  if(c == 0) {
    *choice = c;
    return;
  }

  while(c < 0 || c > numOptions) {
    printf("Please enter your selection: ");
    scanf("%d", &c);
  }

  *choice = c;
}