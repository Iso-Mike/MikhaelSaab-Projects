#include <iostream>
#include <iomanip>

#include "Student.h"

Student::Student(string num, string nam, string maj)
{
  number = num;
  name = nam;
  majorPgm = maj;
}

string Student::getNumber() 
{
  return number;
}

string Student::getName()
{
  return name;
}

bool Student::lessThan(Student *s) 
{
  if(s == nullptr) {
    cout << "Null reference provided to lessthan function in Student.cc" << endl;
    return false;
  }
  return name < s->name;
}

void Student::print() 
{
  cout << setw(10) << left << number << " " << setw(10) << left << name << " " << setw(5) << left << majorPgm;
}