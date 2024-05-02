#include <iostream>
#include <iomanip>

#include "School.h"

School::School(string n)
{
  name = n;
}

School::~School()
{
  registrations.cleanData();
}

void School::addStu(Student *s)
{
  students.add(s);
}

void School::addCourse(Course *c)
{
  courses.add(c);
}

void School::addRegistration(Student *s, Course *c)
{
  Registration* r = new Registration{s, c};
  registrations.add(r);
}

bool School::findStudent(string num, Student **s)
{
  return students.find(num, s);
}

bool School::findCourse(int num, Course **c)
{
  return courses.find(num, c);
}

void School::printStudents()
{
  cout << "\nSTUDENTS OF " << name << " School of Computer Science" << endl;
  students.print();
  cout << endl;
}

void School::printCourses()
{
  cout << "\nCOURSES OF " << name << " School of Computer Science" << endl;
  courses.print();
  cout << endl;
}

void School::printCoursesByTerm(string term)
{
  cout << "\nCOURSES OF " << name << " School of Computer Science FOR TERM " << term << endl;
  courses.print(term);
  cout << endl;
}

void School::printRegistrations()
{
  cout << "\nREGISTRATIONS OF " << name << " School of Computer Science" << endl;
  registrations.print();
}

void School::printRegistrationsByStu(Student* stu) 
{
  RegList reg(registrations, stu);

  cout << "\nREGISTRATIONS FOR " << stu->getName() << endl; 
  reg.print();
}