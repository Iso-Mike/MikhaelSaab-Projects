import sqlite3
from database import get_db_connection
import hashlib


# Manages user data and authentication, supporting operations like registration, login, and profile updates.

class User:
    def __init__(self, username, password, email):
        self.username = username
        self.email = email
        self.password = self.hash_password(password)

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO Users (Username, Password, Email) VALUES (?, ?, ?)',
                           (self.username, self.password, self.email))
            conn.commit()
        except sqlite3.IntegrityError:
            print("Error: That username is already taken. Please choose a different username.")
            return False
        finally:
            conn.close()
        return True

    @staticmethod
    def login(username, password):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Users WHERE Username = ?', (username,))
        user = cursor.fetchone()
        conn.close()

        if user and User.hash_password(password) == user['Password']:
            return user
        else:
            return None

    @staticmethod
    def update_profile(user_id, email, new_password):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE Users SET Email = ?, Password = ? WHERE UserID = ?',
                       (email, User.hash_password(new_password), user_id))
        conn.commit()
        conn.close()
