import sqlite3
import os

DB_FILE = "backend/nutritrack_v2.db"

def migrate_v2():
    print(f"Migrating {DB_FILE}...")
    if not os.path.exists(DB_FILE):
        print(f"Database {DB_FILE} not found.")
        return

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        # 1. Add is_public
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN is_public BOOLEAN DEFAULT 1")
            print("Added is_public column.")
        except sqlite3.OperationalError as e:
            print(f"is_public might already exist: {e}")

        # 2. Add streak_count
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN streak_count INTEGER DEFAULT 0")
            print("Added streak_count column.")
        except sqlite3.OperationalError as e:
            print(f"streak_count might already exist: {e}")

        # 3. Add last_logged_date
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN last_logged_date DATE")
            print("Added last_logged_date column.")
        except sqlite3.OperationalError as e:
            print(f"last_logged_date might already exist: {e}")

        # 4. Create social_connections table
        print("Creating social_connections table...")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS social_connections (
            follower_id INTEGER NOT NULL,
            followed_id INTEGER NOT NULL,
            PRIMARY KEY (follower_id, followed_id),
            FOREIGN KEY(follower_id) REFERENCES users(id),
            FOREIGN KEY(followed_id) REFERENCES users(id)
        )
        """)
        print("Done.")

        conn.commit()
        print("Migration v2 successful!")

    except Exception as e:
        print(f"Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_v2()
