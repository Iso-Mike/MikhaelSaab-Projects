#include "defs.h"

/*
  Function:  viewEscape
   Purpose:  Establishes a client connection to the server at the given IP address and continuously receives and displays the escape until a quit command is received.
        in:  ip - A string representing the IP address of the server to connect to
*/
void viewEscape(char *ip) { 
  int viewSoc;
  char strBuff[MAX_BUFF];

  setupClientSocket(&viewSoc, ip);
  
  while(C_TRUE) {
    rcvData(viewSoc, strBuff);

    if(strcmp(strBuff, "q") == C_FALSE){
      system("clear");
      break;
    }
    
    system("clear");
    printf("%s\n", strBuff);
  }

  rcvData(viewSoc, strBuff);
  printf("%s\n", strBuff);

  rcvData(viewSoc, strBuff);
  printf("%s", strBuff);
}