#include <iostream>
#include <iomanip>

#include "Course.h"

int Course::nextId = COURSE_ID;

Course::Course(string t, string s, int c, char sec, string i)
{
  id = nextId++;
  term = t;
  subject = s;
  code = c;
  section = sec;
  instructor = i;
}

int Course::getId() 
{
  return id;
}

string Course::getTerm() 
{
  return term;
}

string Course::getCourseCode() 
{
  stringstream ss;
  ss << subject << " " << code << "-" << section;
  return ss.str();
}

bool Course::lessThan(Course *c)
{
  if(c == nullptr) {
    cout << "Null reference provided to lessthan function in Course.cc" << endl;
    return false;
  }

  if(term != c->term) {
    return term < c->term;
  } else if(subject != c->subject) {
    return subject < c->subject;
  } else if(code != c->code) {
    return code < c->code;
  }

  return section < c->section;
}

void Course::print()
{
  //cout << id << " " << "Term: " << term << "  " << subject << " " << getCourseCode() << " " << section << "  " << "Instr: " << instructor << endl;
  cout << setw(5) << left << id << " " << "Term: " << setw(6) << left << term << "" << setw(3) << left << subject << " " << code << " " << setw(3) << left << section << " " << "Instr: " << left << instructor;
}