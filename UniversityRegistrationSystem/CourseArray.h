#ifndef COURSEARRAY_H
#define COURSEARRAY_H

#include "Course.h"

/*
   Purpose: This class represents the array that holds all of the courses.
*/
class CourseArray
{
  public:
    CourseArray();
    ~CourseArray();
    void add(Course*);
    bool find(int, Course**);
    void print(string);
    void print();

  private:
    int size;
    Course* elements[MAX_ARR];

};

#endif

