#include "defs.h"

int main(int argc, char *argv[])
{
  srand((unsigned)time(NULL));
  if (argc == 1) {
    runEscape();
  } else {
    viewEscape(argv[1]);
  }
  
  return 0; 
}

/*
  Function:  randomInt
   Purpose:  Generates a random integer from 0 up to (but not including) a specified maximum value
        in:  max - The maximum value for the random integer generation (exclusive)
    return:  A random integer between 0 and max - 1
*/
int randomInt(int max)
{
  return(rand() % max);
}

