from database import get_db_connection


# Initializes the database and creates the necessary tables for the application.

def init_db():
    schema = """
    -- First, drop existing tables if they exist
    DROP TABLE IF EXISTS Grades;
    DROP TABLE IF EXISTS Courses;
    DROP TABLE IF EXISTS Users;

    -- User table schema
    CREATE TABLE Users (
        UserID INTEGER PRIMARY KEY AUTOINCREMENT,
        Username TEXT NOT NULL UNIQUE,
        Password TEXT NOT NULL,
        Email TEXT NOT NULL
    );

    -- Course table schema
    CREATE TABLE Courses (
        CourseID INTEGER PRIMARY KEY AUTOINCREMENT,
        UserID INTEGER NOT NULL,
        CourseName TEXT NOT NULL,
        Year INTEGER NOT NULL,
        Semester TEXT NOT NULL,
        Credits REAL NOT NULL,
        Average REAL, -- This line adds the Average column to the table
        FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
    );

    -- Grade table schema
    CREATE TABLE Grades (
        GradeID INTEGER PRIMARY KEY AUTOINCREMENT,
        UserID INTEGER NOT NULL,
        CourseID INTEGER NOT NULL,
        Type TEXT NOT NULL,
        Score REAL NOT NULL,
        Weight REAL NOT NULL,
        FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE,
        FOREIGN KEY (CourseID) REFERENCES Courses(CourseID) ON DELETE CASCADE
    );
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.executescript(schema)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    init_db()
