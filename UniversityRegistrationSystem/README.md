# University Registration System

## Author
Mikhael Saab

## Overview
The University Registration System is a comprehensive software application designed to manage student and course registrations efficiently. This system is capable of handling a large volume of data, offering a robust solution for universities to maintain student records, course details, and enrollment information. It is developed with modularity and scalability in mind, ensuring that it can be adapted to the growing needs of educational institutions.

## Features
- **Efficient Data Management:** Utilizes custom data structures and dynamic arrays for optimal performance in data manipulation and retrieval.
- **Advanced Registration Logic:** Supports complex registration scenarios, including course prerequisites, registration limits, and waitlist management.
- **User-Friendly Interface:** Provides a simple and intuitive interface for both administrative staff and students to navigate and use the system effectively.
- **Modular Design:** Features a clear separation of concerns, dividing the system into core components such as student management, course management, and registration control.
- **Robust Error Handling:** Includes comprehensive error checking to prevent and manage exceptions, ensuring reliable system performance.
- **Data Persistence:** Designed to interface with external data storage solutions, facilitating easy data backup and retrieval.

## Source Files
- `main.cc`: The main driver of the application.
- `Control.cc`, `View.cc`, `School.cc`: Coordinate the flow of the application and handle the user interface.
- `Student.cc`, `Course.cc`, `Registration.cc`, `RegList.cc`: Handle the business logic related to students, courses, registrations, and registration lists respectively.
- `CourseArray.cc`, `StuArray.cc`: Manage arrays of courses and students.

## Header Files
- `defs.h`: Defines essential constants and structures used across the system.
- `Control.h`, `View.h`, `School.h`, `Student.h`, `Course.h`, `Registration.h`, `RegList.h`, `CourseArray.h`, `StuArray.h`: Header files declaring the classes and their methods for managing various aspects of the system.

## How to Compile and Run
- **Compilation:** `make` (ensure your Makefile is set up to compile these files)
- **Execution:** `./UniRegSystem`

## Usage Instructions
- **Execute the Application:** Run `./UniRegSystem` in the terminal to start the system.
- **Interact with the System:** Follow the on-screen prompts to navigate through the registration process, manage student profiles, and handle course offerings.
