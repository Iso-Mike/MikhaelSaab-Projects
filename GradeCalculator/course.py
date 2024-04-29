from database import get_db_connection
from grade import Grade

# Manages course data and interactions with the database, such as adding, updating, and removing courses.


class Course:
    def __init__(self, user_id, course_name, year, semester, credits):
        self.user_id = user_id
        self.course_name = course_name
        self.year = year
        self.semester = semester
        self.credits = credits

    def add_course(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Courses (UserID, CourseName, Year, Semester, Credits) VALUES (?, ?, ?, ?, ?)',
                       (self.user_id, self.course_name, self.year, self.semester, self.credits))
        conn.commit()
        conn.close()

    @staticmethod
    def update_course(course_id, course_name, year, semester):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE Courses SET CourseName = ?, Year = ?, Semester = ? WHERE CourseID = ?',
                       (course_name, year, semester, course_id))
        conn.commit()
        conn.close()

    @staticmethod
    def remove_course(course_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Courses WHERE CourseID = ?', (course_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def get_courses_for_user(user_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Courses WHERE UserID = ?', (user_id,))
        courses = cursor.fetchall()
        conn.close()
        return courses

    @staticmethod
    def calculate_course_average(course_id):
        grades = Grade.get_grades_for_course(course_id)
        if grades:
            total_weighted_score = sum(grade['Score'] * grade['Weight'] for grade in grades)
            total_weight = sum(grade['Weight'] for grade in grades)
            return total_weighted_score / total_weight if total_weight else 0
        return None

    @staticmethod
    def update_course_average(course_id, new_average):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE Courses SET Average = ? WHERE CourseID = ?', (new_average, course_id))
        conn.commit()
        conn.close()
