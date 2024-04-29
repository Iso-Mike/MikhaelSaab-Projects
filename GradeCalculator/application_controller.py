from user import User
from course import Course
from grade import Grade
from gpa_calculator import GPACalculator
from view import TerminalView

# Orchestrates user interactions and manages the flow of the application, delegating tasks to specific classes.


class ApplicationController:
    def __init__(self):
        self.user = None
        self.view = TerminalView()

    def run(self):
        while True:
            choice = self.view.display_main_menu()
            if choice == '1':
                self.register_user()
            elif choice == '2':
                self.login_user()
            elif choice == '3':
                self.view.display_message("Exiting the application.")
                break
            else:
                self.view.display_message("Invalid choice, please try again.")

    def register_user(self):
        username = self.view.get_user_input("Enter a username: ")
        password = self.view.get_user_input("Enter a password: ")
        email = self.view.get_user_input("Enter an email: ")
        user = User(username, password, email)
        if user.register():
            self.view.display_message("Registration successful.")
        else:
            self.view.display_message("Registration failed.")

    def login_user(self):
        username = self.view.get_user_input("Enter your username: ")
        password = self.view.get_user_input("Enter your password: ")
        user_data = User.login(username, password)
        if user_data:
            self.user = user_data
            self.view.display_message("Login successful.")
            self.user_menu()
        else:
            self.view.display_message("Login failed. Please check your credentials.")

    def user_menu(self):
        while True:
            self.view.display_message("\nUser Menu:")
            self.view.display_message("1: View Courses")
            self.view.display_message("2: Add Course")
            self.view.display_message("3: View Grades")
            self.view.display_message("4: Add Grade")
            self.view.display_message("5: Calculate GPA")
            self.view.display_message("6: Log out")
            choice = self.view.get_user_input("Enter your choice: ")
            if choice == '1':
                self.display_courses()
            elif choice == '2':
                self.add_course()
            elif choice == '3':
                self.display_grades()
            elif choice == '4':
                self.add_grade()
            elif choice == '5':
                self.calculate_gpa()
            elif choice == '6':
                self.view.display_message("Logging out...")
                self.user = None
                break
            else:
                self.view.display_message("Invalid choice, please try again.")

    def display_courses(self):
        courses_data = Course.get_courses_for_user(self.user['UserID'])
        courses = [dict(course) for course in courses_data]
        for course in courses:
            course['Average'] = Course.calculate_course_average(course['CourseID'])
        self.view.display_courses_with_options(courses)
        if self.view.get_user_input("Do you want to remove a course? (yes/no): ").lower() == 'yes':
            self.remove_course(courses)

    def remove_course(self, courses):
        self.view.display_courses_with_options(courses)
        course_id = self.view.get_course_selection_for_removal(courses)
        if course_id:
            Grade.remove_grades_with_course(course_id)
            Course.remove_course(course_id)
            self.view.display_message("Course and all associated grades removed successfully.")
        else:
            self.view.display_message("Course removal cancelled.")

    def add_course(self):
        course_name = self.view.get_user_input("Enter course name: ")
        year = self.view.get_user_input("Enter the year of the course: ")
        semester = self.view.get_user_input("Enter the semester of the course: ")
        while True:
            credits_str = self.view.get_user_input("Enter the credit value of the course (0.5 or 1.0): ")
            try:
                credits = float(credits_str)
                if credits in (0.5, 1.0):
                    break
                else:
                    self.view.display_message("Credits must be 0.5 or 1.0.")
            except ValueError:
                self.view.display_message("Invalid input. Please enter a valid number.")
        new_course = Course(self.user['UserID'], course_name, year, semester, credits)
        new_course.add_course()
        self.view.display_message("Course added successfully.")

    def display_grades(self):
        courses_data = Course.get_courses_for_user(self.user['UserID'])
        courses = [dict(course) for course in courses_data]
        course_id = self.view.select_course_from_list(courses)
        if not course_id:
            self.view.display_message("Grade viewing cancelled.")
            return
        grades = Grade.get_grades_for_course(course_id)
        if not grades:
            self.view.display_message("No grades available for this course.")
            return
        self.view.display_grades_with_indices(grades)
        if self.view.get_user_input("Do you want to remove a grade? (yes/no): ").lower() == 'yes':
            self.remove_grade(grades)

    def remove_grade(self, grades):
        grade_id = self.view.select_grade_to_remove(grades)
        if grade_id:
            Grade.remove_grade(grade_id)
            course_id = next((grade['CourseID'] for grade in grades if grade['GradeID'] == grade_id), None)

            if course_id:
                self.update_course_average(course_id)

            self.view.display_message("Grade removed successfully.")
        else:
            self.view.display_message("Grade removal cancelled.")

    def update_course_average(self, course_id):
        grades = Grade.get_grades_for_course(course_id)
        if grades:
            total_weighted_score = sum(grade['Score'] * grade['Weight'] for grade in grades)
            total_weight = sum(grade['Weight'] for grade in grades)
            if total_weight > 0:
                new_average = total_weighted_score / total_weight
            else:
                new_average = 0
            Course.update_course_average(course_id, new_average)
        else:
            Course.update_course_average(course_id, None)

        self.display_courses()

    def add_grade(self):
        courses_data = Course.get_courses_for_user(self.user['UserID'])
        courses = [dict(course) for course in courses_data]
        course_id = self.view.select_course(courses)
        if course_id is None:
            self.view.display_message("Grade addition cancelled.")
            return
        grade_type = self.view.get_user_input("Enter the type of grade (e.g., 'exam', 'assignment'): ")
        score = self.view.get_user_input("Enter the score: ")
        weight = self.view.get_user_input("Enter the weight of the grade (as a decimal): ")
        try:
            score = float(score)
            weight = float(weight)
            new_grade = Grade(self.user['UserID'], course_id, grade_type, score, weight)
            new_grade.add_grade()
            new_average = Course.calculate_course_average(course_id)
            Course.update_course_average(course_id, new_average)
            self.view.display_message("Grade added successfully.")
        except ValueError:
            self.view.display_message("Invalid input for score or weight. Please enter valid numbers.")

    def calculate_gpa(self):
        courses = Course.get_courses_for_user(self.user['UserID'])
        grades = [Grade.get_grades_for_course(course['CourseID']) for course in courses]
        flat_grades = [grade for sublist in grades for grade in sublist]
        grade_scores = [grade['Score'] for grade in flat_grades]
        grade_weights = [grade['Weight'] for grade in flat_grades]
        gpa = GPACalculator.calculate_gpa(grade_scores, grade_weights)
        self.view.display_gpa(gpa)


if __name__ == '__main__':
    controller = ApplicationController()
    controller.run()
