import sqlite3
import os

def check_real_db():
    # consistent with database.py default
    db_path = 'backend/nutritrack_v2.db' 
    print(f"Checking DB at: {os.path.abspath(db_path)}")
    
    if not os.path.exists(db_path):
        print("❌ DB file not found!")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        # Check users table structure
        cursor.execute("PRAGMA table_info(users)")
        columns = cursor.fetchall()
        print("\n--- Users Table Columns ---")
        for col in columns:
            print(f"- {col[1]} ({col[2]})")

        # Check for test user
        print("\n--- Checking for test user ---")
        email = "test@example.com"
        cursor.execute("SELECT id, email, is_active, is_public FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        
        if user:
            print(f"✅ User FOUND: ID={user[0]}, Email={user[1]}, Active={user[2]}, Public={user[3]}")
        else:
            print(f"❌ User {email} NOT FOUND.")
            
            # List all users
            print("\n--- All Users ---")
            cursor.execute("SELECT id, email FROM users LIMIT 5")
            users = cursor.fetchall()
            for u in users:
                print(f"ID: {u[0]}, Email: {u[1]}")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    check_real_db()
