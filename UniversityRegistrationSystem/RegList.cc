#include <iostream>
using namespace std;

#include "RegList.h"

RegList::RegList()
{ 
  head = nullptr;
  tail = nullptr;
}

RegList::RegList(RegList& otherList, Student* stu)
{
  head = nullptr;
  tail = nullptr;
  Node* current = otherList.head;
  while(current != nullptr) {
    if(current->data->getStudent() == stu) {
      Node* newNode = new Node{current->data, nullptr};
      if(tail) {
        tail->next = newNode;
      } else { 
        head = newNode;
      }
      tail = newNode; 
    }
    current = current->next; 
  }
}

RegList::~RegList()
{
  Node* currNode = head;
  Node* nextNode;

  while (currNode != nullptr) {
    nextNode = currNode->next;
    delete currNode;
    currNode = nextNode;
  }
}

void RegList::add(Registration* r)
{
  Node* newNode = new Node;
  newNode->data = r;
  newNode->next = nullptr;

  if(head == nullptr || !head->data->lessThan(r)) {
    newNode->next = head;
    head = newNode;
    if(tail == nullptr) {
      tail = newNode;
    }
  } else {
    Node* currNode = head;

    while(currNode->next != nullptr) {
      if(!currNode->next->data->lessThan(r))
        break;
      currNode = currNode->next;
    }

    newNode->next = currNode->next;
    currNode->next = newNode;
    if(newNode->next == nullptr) {
      tail = newNode;
    }
  }
}

void RegList::cleanData() 
{
  Node* currNode = head;
  Node* nextNode;

  while(currNode != nullptr) {
    nextNode = currNode->next;
    delete currNode->data;
    currNode = nextNode;
  }
}

void RegList::print()
{
  Node* current = head;

  while(current != nullptr) {
    current->data->print();
    current = current->next;
  }

  cout << "HEAD: ";
  if(head != nullptr) {
    head->data->print();
  } else {
    cout << "NONE\n";
  }

  cout << "TAIL: ";
  if(tail != nullptr) {
    tail->data->print();
  } else {
    cout << "NONE";
  }
  cout << endl;
}