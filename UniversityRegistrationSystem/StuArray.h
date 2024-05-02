#ifndef STUARRAY_H
#define STUARRAY_H

#include "Student.h"

/*
   Purpose: Maintains a statically allocated array of Student objects, facilitating the management and retrieval of student information 
            within the university's registration system
*/
class StuArray
{
  public:
    StuArray();
    ~StuArray();
    void add(Student*);
    bool find(string, Student**);
    void print();
    
  private:
    int size;
    Student* elements[MAX_ARR];

};

#endif

