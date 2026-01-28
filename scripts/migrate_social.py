import sqlite3

def migrate():
    print("Migrating database for Social Features...")
    conn = sqlite3.connect('backend/nutritrack.db')
    cursor = conn.cursor()

    try:
        # Add is_public column to users
        print("Adding is_public column to users table...")
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN is_public BOOLEAN DEFAULT 1")
            print("Done.")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("Column is_public already exists.")
            else:
                raise e

        # Create social_connections table
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
        print("Migration successful!")

    except Exception as e:
        print(f"Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
