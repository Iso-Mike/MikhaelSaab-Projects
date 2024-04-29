from database import get_db_connection


# Handles operations related to student grades, including adding, retrieving, updating, and deleting grades from the
# database.


class Grade:
    def __init__(self, user_id, course_id, grade_type, score, weight):
        self.user_id = user_id
        self.course_id = course_id
        self.grade_type = grade_type
        self.score = score
        self.weight = weight

    def set_course(self, course_id):
        self.course_id = course_id

    def add_grade(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Grades (UserID, CourseID, Type, Score, Weight) VALUES (?, ?, ?, ?, ?)',
                       (self.user_id, self.course_id, self.grade_type, self.score, self.weight))
        conn.commit()
        conn.close()

    @staticmethod
    def get_grades_for_course(course_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT GradeID, CourseID, Type, Score, Weight FROM Grades WHERE CourseID = ?', (course_id,))
        grades = [{'GradeID': row[0], 'CourseID': row[1], 'Type': row[2], 'Score': row[3], 'Weight': row[4]} for row in
                  cursor.fetchall()]
        conn.close()
        return grades

    @staticmethod
    def update_grade(grade_id, new_score, new_weight):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE Grades SET Score = ?, Weight = ? WHERE GradeID = ?',
                       (new_score, new_weight, grade_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete_grade(grade_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Grades WHERE GradeID = ?', (grade_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def update_course_average(course_id, new_average):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE Courses SET Average = ? WHERE CourseID = ?',
                       (new_average, course_id))
        conn.commit()
        conn.close()

    @staticmethod
    def remove_grade(grade_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Grades WHERE GradeID = ?', (grade_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def remove_grades_with_course(course_id):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM Grades WHERE CourseID = ?', (course_id,))
            conn.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
            conn.rollback()
        finally:
            conn.close()
