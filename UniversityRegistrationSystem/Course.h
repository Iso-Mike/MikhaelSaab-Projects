#ifndef COURSE_H
#define COURSE_H

#include <string>
using namespace std;

#include "defs.h"

/*
   Purpose: Represents a single course offering, with the usual information: a unique id, the academic term when the course is offered, 
            subject, course code, section, instructor, time and day.
*/
class Course
{
  public:
    Course(string="Unknown", string="Unknown", int=0, char=' ', string="Unknown");
    int getId();
    string getTerm();
    string getCourseCode();
    bool lessThan(Course*);
    void print();

  private:
    static int nextId;
    int id;
    string term;
    string subject;
    int code;
    char section;
    string instructor;

};

#endif
