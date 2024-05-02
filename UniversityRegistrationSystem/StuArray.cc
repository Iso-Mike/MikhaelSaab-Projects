#include <iostream>
using namespace std;

#include "StuArray.h"

StuArray::StuArray()
{
  size = 0;
}

StuArray::~StuArray() 
{
  for(int i = 0; i < size; ++i)
    delete elements[i];
}

void StuArray::add(Student* s) 
{
  if(s == nullptr) {
    cout << "Null pointer provided to add function in StuArray.cc" << endl;
    return;
  }

  if(size >= MAX_ARR) return;

  int insertionPoint = size;
  for(int i = 0; i < size; i++) {
    if(!elements[i]->lessThan(s)) {
      insertionPoint = i;
      break;
    }
  }

  for(int j = size; j > insertionPoint; j--) {
    elements[j] = elements[j - 1];
  }

  elements[insertionPoint] = s;
  size++;
}

bool StuArray::find(string num, Student **s) 
{
  for(int i = 0; i < size; ++i) {
    if(elements[i]->getNumber() == num) {
      *s = elements[i];
      return true;
    }
  }
  *s = nullptr;
  return false;
}

void StuArray::print()
{
  for (int i = 0; i < size; ++i) {
    elements[i]->print();
    cout << endl;
  }
}