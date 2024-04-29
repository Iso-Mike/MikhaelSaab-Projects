import sqlite3

DATABASE_PATH = 'grade_calculator.db'


# Provides a connection to the SQLite database and configures it to return rows as dictionary-like objects.

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn
