# Provides a terminal-based interface for user interaction, handling input/output operations.


def display_courses_with_averages(courses):
    print("\nYour Courses and Averages:")
    for idx, course in enumerate(courses, 1):
        avg_display = f"Average: {course.get('Average', 'No grades yet'):.2f}%" \
            if course.get('Average') is not None \
            else "No grades yet"
        print(f"{idx}. {course['CourseName']} - Year {course['Year']} - Semester {course['Semester']} - {avg_display}")


class TerminalView:
    @staticmethod
    def display_main_menu():
        print("\nMain Menu:")
        print("1: Register")
        print("2: Login")
        print("3: Exit")
        choice = input("Enter your choice: ")
        return choice

    @staticmethod
    def display_courses_with_options(courses):
        print("\nYour Courses:")
        for idx, course in enumerate(courses, 1):
            avg_display = f"Average: {course['Average']:.2f}%" if course['Average'] is not None else "No grades yet"
            print(f"{idx}. {course['CourseName']} - "
                  f"Year: {course['Year']} - "
                  f"Semester: {course['Semester']} - "
                  f"{avg_display}")
        print("0: Return to User Menu")

    @staticmethod
    def get_course_selection_for_removal(courses):
        while True:
            choice = int(input("Enter the number of the course to remove or 0 to cancel: "))
            if choice == 0:
                return None
            if 1 <= choice <= len(courses):
                return courses[choice - 1]['CourseID']
            else:
                print("Invalid choice, please try again.")

    @staticmethod
    def display_courses(courses):
        print("\nYour Courses:")
        for course in courses:
            print(
                f"{course['CourseID']}: {course['CourseName']} - "
                f"Year {course['Year']} - "
                f"Semester {course['Semester']} - "
                f"Credits: {course['Credits']}")

    @staticmethod
    def display_grades(grades):
        print("\nYour Grades:")
        for grade in grades:
            print(f"Type: {grade['Type']}, Score: {grade['Score']}, Weight: {grade['Weight']}")

    @staticmethod
    def display_gpa(gpa):
        print(f"\nYour GPA is: {gpa:.2f}")

    @staticmethod
    def get_user_input(prompt):
        return input(prompt)

    @staticmethod
    def display_message(message):
        print(message)

    def select_course(self, courses):
        display_courses_with_averages(courses)
        while True:
            try:
                choice = int(self.get_user_input("Select a course by number or 0 to cancel: "))
                if choice == 0:
                    return None
                if 1 <= choice <= len(courses):
                    return courses[choice - 1]['CourseID']
                else:
                    self.display_message("Invalid choice, please try again.")
            except ValueError:
                self.display_message("Please enter a number.")

    @staticmethod
    def select_course_from_list(courses):
        if not courses:
            print("No courses available.")
            return None
        display_courses_with_averages(courses)
        print("Select a course by number to view grades, or enter 0 to cancel:")
        while True:
            try:
                choice = int(input("Enter your choice: "))
                if choice == 0:
                    return None
                if 1 <= choice <= len(courses):
                    return courses[choice - 1]['CourseID']
                else:
                    print("Invalid choice, please try again.")
            except ValueError:
                print("Please enter a number.")

    def display_grades_with_indices(self, grades):
        if not grades:
            print("No grades to display.")
            return
        print("\nGrades for the selected course:")
        for idx, grade in enumerate(grades, 1):
            print(f"{idx}. {grade['Type']} - Score: {grade['Score']} - Weight: {grade['Weight']}%")

    def select_grade_to_remove(self, grades):
        self.display_grades_with_indices(grades)
        print("Select a grade to remove by number, or enter 0 to cancel:")
        while True:
            try:
                choice = int(input("Enter your choice: "))
                if choice == 0:
                    return None
                if 1 <= choice <= len(grades):
                    return grades[choice - 1]['GradeID']
                else:
                    print("Invalid choice, please try again.")
            except ValueError:
                print("Please enter a number.")
