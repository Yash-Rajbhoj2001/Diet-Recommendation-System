import sqlite3
from contextlib import contextmanager
from pathlib import Path
import bcrypt

DB_PATH = Path(__file__).parent / "diet_recommendation.db"  # Change the database name if needed

# Context manager for database connection
@contextmanager
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
    finally:
        conn.close()

# Check and initialize the database
def check_and_initialize_db():
    try:
        init_db()
    except Exception as e:
        print(f"Error initializing database: {e}")

# Initialize the database with proper table structure
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        
        # Creating tables for Users, Diet Recommendations, Custom Food Recommendations, and Feedback
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS diet_recommendations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            recommendation TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS custom_food_recommendations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            food_recommendation TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            feedback_text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """)

        conn.commit()

# Check if the tables are created successfully
def test_tables():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        print("Tables in DB:", cursor.fetchall())

# Add a new user to the database
def add_user(email: str, password_hash: str):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (email, password_hash) VALUES (?, ?)",
            (email, password_hash)
        )
        conn.commit()

# Get a user by email
def get_user_by_email(email: str):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, email, password_hash FROM users WHERE email = ?",
            (email,)
        )
        return cursor.fetchone()

# Add diet recommendation for a user
def add_diet_recommendation(user_id: int, recommendation: str):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO diet_recommendations (user_id, recommendation) VALUES (?, ?)",
            (user_id, recommendation)
        )
        conn.commit()

# Add custom food recommendation for a user
def add_custom_food_recommendation(user_id: int, food_recommendation: str):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO custom_food_recommendations (user_id, food_recommendation) VALUES (?, ?)",
            (user_id, food_recommendation)
        )
        conn.commit()

# Add feedback for a user
def add_feedback(user_id: int, feedback_text: str):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO feedback (user_id, feedback_text) VALUES (?, ?)",
            (user_id, feedback_text)
        )
        conn.commit()

# Fetch diet recommendations by user_id
def get_diet_recommendations(user_id: int):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT recommendation FROM diet_recommendations WHERE user_id = ?",
            (user_id,)
        )
        return cursor.fetchall()

# Fetch custom food recommendations by user_id
def get_custom_food_recommendations(user_id: int):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT food_recommendation FROM custom_food_recommendations WHERE user_id = ?",
            (user_id,)
        )
        return cursor.fetchall()

# Fetch feedback by user_id
def get_feedback(user_id: int):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT feedback_text FROM feedback WHERE user_id = ?",
            (user_id,)
        )
        return cursor.fetchall()

# Check if a test user exists, if not, create one
def create_temp_user():
    email = "test@example.com"
    raw_password = "test123"  # Temporary password
    password_hash = bcrypt.hashpw(raw_password.encode(), bcrypt.gensalt()).decode()

    if get_user_by_email(email):
        print("Test user already exists.")
    else:
        add_user(email, password_hash)
        print(f"Temporary user created: {email} / {raw_password}")


# Run this once to check if tables are created
test_tables()

# At the bottom of the file
if __name__ == "__main__":
    check_and_initialize_db()
    print("Database created at:", DB_PATH)
