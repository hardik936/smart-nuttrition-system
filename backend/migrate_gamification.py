import sqlite3
import os

DB_FILE = "nutritrack_v2.db" # Default, will verify after reading database.py

def migrate():
    if not os.path.exists(DB_FILE):
        print(f"Database {DB_FILE} not found.")
        return

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        # Add streak_count
        cursor.execute("ALTER TABLE users ADD COLUMN streak_count INTEGER DEFAULT 0")
        print("Added streak_count column.")
    except sqlite3.OperationalError as e:
        print(f"streak_count might already exist: {e}")

    try:
        # Add last_logged_date
        cursor.execute("ALTER TABLE users ADD COLUMN last_logged_date DATE")
        print("Added last_logged_date column.")
    except sqlite3.OperationalError as e:
        print(f"last_logged_date might already exist: {e}")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    migrate()
