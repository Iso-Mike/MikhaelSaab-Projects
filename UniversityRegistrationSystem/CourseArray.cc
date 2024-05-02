#include <iostream>
using namespace std;

#include "CourseArray.h"

CourseArray::CourseArray()
{
  size = 0;
}

CourseArray::~CourseArray() 
{
  for(int i = 0; i < size; ++i)
    delete elements[i];
}

void CourseArray::add(Course* c) 
{
  if(c == nullptr) {
    cout << "Null pointer provided to add function in CourseArray.cc" << endl;
    return;
  }

  if(size >= MAX_ARR) return;

  int insertionPoint = size;
  for(int i = 0; i < size; i++) {
    if(!elements[i]->lessThan(c)) {
      insertionPoint = i;
      break;
    }
  }

  for(int j = size; j > insertionPoint; j--) {
    elements[j] = elements[j - 1];
  }

  elements[insertionPoint] = c;
  size++;
}

bool CourseArray::find(int id, Course** c) 
{
  for(int i = 0; i < size; ++i) {
    if(elements[i]->getId() == id) {
      *c = elements[i];
      return true;
    }
  }
  *c = nullptr;
  return false;
}

void CourseArray::print(string t) 
{
  for(int i = 0; i < size; ++i) {
    if(elements[i]->getTerm() == t) {
      elements[i]->print();
      cout << endl;
    }
  }
}

void CourseArray::print()
{
  for (int i = 0; i < size; ++i) {
    elements[i]->print();
    cout << endl;
  }
}
