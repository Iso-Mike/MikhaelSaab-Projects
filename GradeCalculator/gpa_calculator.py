
# Provides utilities for calculating GPA and specific course grades based on Carleton University's grading scale.


class GPACalculator:
    GRADE_POINTS = {
        'A+': 12, 'A': 11, 'A-': 10,
        'B+': 9,  'B': 8,  'B-': 7,
        'C+': 6,  'C': 5,  'C-': 4,
        'D+': 3,  'D': 2,  'D-': 1,
        'F': 0
    }

    @staticmethod
    def calculate_grade_point(percentage):
        if 90 <= percentage <= 100:
            return GPACalculator.GRADE_POINTS['A+']
        elif 85 <= percentage < 90:
            return GPACalculator.GRADE_POINTS['A']
        elif 80 <= percentage < 85:
            return GPACalculator.GRADE_POINTS['A-']
        elif 77 <= percentage < 80:
            return GPACalculator.GRADE_POINTS['B+']
        elif 73 <= percentage < 77:
            return GPACalculator.GRADE_POINTS['B']
        elif 70 <= percentage < 73:
            return GPACalculator.GRADE_POINTS['B-']
        elif 67 <= percentage < 70:
            return GPACalculator.GRADE_POINTS['C+']
        elif 63 <= percentage < 67:
            return GPACalculator.GRADE_POINTS['C']
        elif 60 <= percentage < 63:
            return GPACalculator.GRADE_POINTS['C-']
        elif 57 <= percentage < 60:
            return GPACalculator.GRADE_POINTS['D+']
        elif 53 <= percentage < 57:
            return GPACalculator.GRADE_POINTS['D']
        elif 50 <= percentage < 53:
            return GPACalculator.GRADE_POINTS['D-']
        else:
            return GPACalculator.GRADE_POINTS['F']

    @staticmethod
    def calculate_gpa(grades, credits):
        total_grade_points = sum(GPACalculator.calculate_grade_point(grade) * credit for grade, credit in zip(grades,
                                                                                                              credits))
        total_credits = sum(credits)
        return total_grade_points / total_credits if total_credits else 0

    @staticmethod
    def calculate_course_grade(assignments, midterm, final, lab=None):
        total_score = 0
        total_weight = 0
        for grade, weight in assignments:
            total_score += grade * weight
            total_weight += weight
        total_score += midterm[0] * midterm[1] + final[0] * final[1]
        total_weight += midterm[1] + final[1]
        if lab:
            total_score += lab[0] * lab[1]
            total_weight += lab[1]
        if total_weight == 0:
            return 0
        return (total_score / total_weight) * 100

    @staticmethod
    def calculate_needed_final_score(current_grades, final_exam_weight, desired_course_grade):
        current_score = sum(grade * weight for grade, weight in current_grades)
        current_weight = sum(weight for _, weight in current_grades)

        if current_weight + final_exam_weight > 1:
            raise ValueError("Total weight of all assessments including the final exceeds 100%")

        needed_final_score = (desired_course_grade - (current_score * (1 - final_exam_weight))) / final_exam_weight
        return needed_final_score
