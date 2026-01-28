import sqlite3
import os

def check_db():
    db_path = 'backend/nutritrack.db'
    print(f"Checking DB at: {os.path.abspath(db_path)}")
    if not os.path.exists(db_path):
        print("DB file not found!")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("PRAGMA table_info(users)")
        columns = cursor.fetchall()
        print("Users table columns:")
        found = False
        for col in columns:
            print(col)
            if col[1] == 'is_public':
                found = True
        
        if found:
            print("✅ is_public column FOUND.")
        else:
            print("❌ is_public column NOT FOUND.")

    except Exception as e:
        print(e)
    finally:
        conn.close()

if __name__ == "__main__":
    check_db()
