#ifndef CONTROL_H
#define CONTROL_H

#include "View.h"
#include "School.h"

/*
   Purpose: Allows the end user to manage multiple schedules, one for each academic term.
*/
class Control
{
  public:
    Control();
    ~Control();
    void launch();

  private:
    School* school;
    void initStudents(School*);
    void initCourses(School*);

};

#endif
