#include <iostream>
using namespace std;
#include <string>

#include "Control.h"

Control::Control()
{
  school = new School("Carleton U."); 
}

Control::~Control()
{
  delete school;
}

void Control::launch()
{
  int adminChoice;
  View view;
  initCourses(school);
  initStudents(school);

  do {
    view.showAdminMenu(adminChoice);

    switch(adminChoice) {
      case 1: { 
        school->printStudents();
        break;
      }
      case 2: { 
        school->printCourses();
        break;
      }
      case 3: {
        school->printRegistrations();
        break;
      }
      case 4: {
        int studentChoice;
        string studentNum;
        Student* selectedStudent = nullptr;

        cout << endl;
        view.printStr("Please enter student number: ");

        while(true) {
          view.readStr(studentNum);
          if(school->findStudent(studentNum, &selectedStudent)) {
            break;
          } else {
            view.printStr("ERROR:  Student number not found, please try again: ");
          }
        }

        do {
          view.showStudentMenu(selectedStudent->getName(), studentChoice);

          switch(studentChoice) {
            case 1: {
              string term;
              view.printStr("Please enter term: ");
              view.readStr(term);
              school->printCoursesByTerm(term);
              break;
            }
            case 2: {
              school->printRegistrationsByStu(selectedStudent);
              break;
            }
            case 3: {
              int courseId;
              view.printStr("Please enter the course id: ");
              view.readInt(courseId);
              Course* course = nullptr;
              if (school->findCourse(courseId, &course)) {
                school->addRegistration(selectedStudent, course);
              } else {
                view.printStr("ERROR:  Course not found");
              }
              break;
            }
            case 0: {
              break;
            }
          }
        } while(studentChoice != 0);
        break;
      }
      case 0: 
        break;
      default:
        break;
      }
  } while (adminChoice != 0);
  
}

void Control::initStudents(School* sch)
{
  sch->addStu(new Student("100567888", "Matilda", "CS"));
  sch->addStu(new Student("100333444", "Harold", "Geography"));
  sch->addStu(new Student("100444555", "Joe", "Physics"));
  sch->addStu(new Student("100775588", "Timmy", "CS"));
  sch->addStu(new Student("100111222", "Amy", "Math"));
  sch->addStu(new Student("100222333", "Stanley", "Art History"));
}

void Control::initCourses(School* sch)
{
  sch->addCourse(new Course("F23", "COMP", 2401, 'A', "Laurendeau"));
  sch->addCourse(new Course("F23", "COMP", 2401, 'B', "Hillen"));
  sch->addCourse(new Course("F23", "COMP", 2401, 'C', "Laurendeau"));
  sch->addCourse(new Course("F23", "COMP", 2401, 'D', "Hillen"));
  sch->addCourse(new Course("F23", "COMP", 2402, 'A', "Shaikhet"));
  sch->addCourse(new Course("F23", "COMP", 2402, 'B', "Shaikhet"));
  sch->addCourse(new Course("F23", "COMP", 2404, 'A', "Hill"));
  sch->addCourse(new Course("F23", "COMP", 2404, 'B', "Hill"));
  sch->addCourse(new Course("F23", "COMP", 2406, 'A', "Nel"));
  sch->addCourse(new Course("F23", "COMP", 2406, 'B', "Shaikhet"));
  sch->addCourse(new Course("F23", "COMP", 2804, 'A', "Morin"));
  sch->addCourse(new Course("F23", "COMP", 2804, 'B', "Hill"));

  sch->addCourse(new Course("W24", "COMP", 2401, 'A', "CI"));
  sch->addCourse(new Course("W24", "COMP", 2401, 'B', "Lanthier"));
  sch->addCourse(new Course("W24", "COMP", 2402, 'A', "Sharp"));
  sch->addCourse(new Course("W24", "COMP", 2402, 'B', "Sharp"));
  sch->addCourse(new Course("W24", "COMP", 2404, 'A', "Hill"));
  sch->addCourse(new Course("W24", "COMP", 2404, 'B', "Laurendeau"));
  sch->addCourse(new Course("W24", "COMP", 2404, 'C', "Laurendeau"));
  sch->addCourse(new Course("W24", "COMP", 2406, 'A', "Nel"));
  sch->addCourse(new Course("W24", "COMP", 2406, 'B', "Nel"));
  sch->addCourse(new Course("W24", "COMP", 2804, 'A', "Hill"));
  sch->addCourse(new Course("W24", "COMP", 2804, 'B', "Hill"));
}


