#ifndef VIEW_H
#define VIEW_H

#include <iostream>
#include <string>
using namespace std;

/*
   Purpose: Acts as the user interface for the university registration system, handling the presentation of menus and the collection of 
            input from users

*/
class View
{
  public:
    void showAdminMenu(int&);
    void showStudentMenu(string, int&);
    void printStr(string);
    void readInt(int&);
    void readStr(string&);
};

#endif
