# GPA and Course Management System

## Author
Mikhael Saab

## Overview
The GPA and Course Management System is a desktop application developed to help students and educational institutions manage course records, grades, and GPA calculations efficiently. It offers a user-friendly terminal-based interface that supports various functionalities tailored to handle academic records comprehensively.

## Features
- **Course Management:** Allows users to add, update, and remove courses along with detailed attributes such as course name, year, semester, and credits.
- **Grade Management:** Facilitates adding, updating, and removing grades for specific courses, supporting detailed academic performance tracking.
- **GPA Calculation:** Integrates a robust GPA calculator that adheres to specific grading scales and calculates cumulative GPAs based on user data.
- **User Authentication:** Manages user registration and login processes, ensuring data security and personalized user experiences.
- **Detailed Views:** Provides comprehensive views of courses and grades, enabling users to monitor their academic progress effectively.
- **Error Handling:** Implements advanced error handling strategies to manage user inputs and system operations securely and reliably.

## Source Files
- `application_controller.py`: Main application controller managing user flows and interactions.
- `user.py`: Manages user-specific functionalities like registration and login.
- `course.py`: Handles all course-related operations.
- `grade.py`: Manages functionalities related to grades within courses.
- `gpa_calculator.py`: Contains logic for calculating GPAs based on course grades.
- `view.py`: Manages all terminal-based user interactions and displays.

## Additional Files and Directories
- `database.py`: Contains database connection and management functionalities.
- `schema.py`: Defines and initializes the database schema.

## How to Compile and Run
- **Installation:** Run `python schema.py` to set up the database schema initially.
- **Execution:** Start the application by running `python application_controller.py`.

## Usage Instructions
- **Starting the Application:** Execute `python application_controller.py` to launch the application.
- **Navigating the Interface:** Follow on-screen prompts to interact with the system, manage courses, enter grades, and calculate GPA.
- **Exiting the Application:** Use the exit option in the main menu to safely close the application.
