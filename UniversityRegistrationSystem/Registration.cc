#include <iostream>
#include <iomanip>

#include "Registration.h"

int Registration::nextId = REG_ID;

Registration::Registration(Student *s, Course *c)
{
  id = nextId++;
  stu = s;
  course = c;
}

Student* Registration::getStudent() 
{
  return stu;
}

bool Registration::lessThan(Registration *reg)
{
  if(reg == nullptr) {
    cout << "Null reference provided to lessthan function in Registration.cc" << endl;
    return false;
  }
  if(course == nullptr || reg->course == nullptr) {
    cout << "One of the course pointers in Registration.cc is Null" << endl;
    return false;
  }
  return course->lessThan(reg->course);
}

void Registration::print()
{
  cout << setw(7) << left << id << setw(14) << left << stu->getName() << setw(5) << left << course->getTerm() << setw(10) << left << course->getCourseCode() << endl;
}
