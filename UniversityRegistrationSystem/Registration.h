#ifndef REGISTRATION_H
#define REGISTRATION_H

#include <string>
using namespace std;

#include "Course.h"
#include "Student.h"

/*
   Purpose: Represents the association between students and courses, encapsulating the details of a student's enrollment in a specific 
            course within the university's registration system.
*/
class Registration
{
  public:
    Registration(Student* = nullptr, Course* = nullptr);
    Student* getStudent();
    bool lessThan(Registration *);
    void print();

  private:
    static int nextId;
    int id;
    Student* stu;
    Course* course;

};

#endif
