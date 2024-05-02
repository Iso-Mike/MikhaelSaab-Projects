#ifndef STUDENT_H
#define STUDENT_H

#include <string>
using namespace std;

#include "defs.h"

/*
   Purpose: Encapsulates information about individual students, including their identification number, name, and major program, serving 
            as a foundational element in the university's registration system.
*/
class Student
{
  public:
    Student(string="Unknown", string="Unknown", string="Unknown");
    string getNumber();
    string getName();
    bool lessThan(Student*);
    void print();

  private:
    string number;
    string name;
    string majorPgm;

};

#endif
