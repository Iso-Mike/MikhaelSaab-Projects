#ifndef SCHOOL_H
#define SCHOOL_H

#include <string>
using namespace std;

#include "StuArray.h"
#include "CourseArray.h"
#include "RegList.h"

/*
   Purpose: Serves as the central hub for the university's registration system
*/
class School
{
  public:
    School(string="Unknown");
    ~School();
    void addStu(Student*);
    void addCourse(Course*);
    void addRegistration(Student*, Course*);
    bool findStudent(string, Student**);
    bool findCourse(int, Course**);
    void printStudents();
    void printCourses();
    void printCoursesByTerm(string);
    void printRegistrations();
    void printRegistrationsByStu(Student*);

  private:
    string name;
    StuArray students;
    CourseArray courses;
    RegList registrations;

};

#endif
