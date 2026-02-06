import sqlite3

DB_NAME = "users.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_tables():
    try:
        with get_connection() as conn:
            conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER UNIQUE,
                ism TEXT,
                familya TEXT,
                sharif TEXT,
                telefon TEXT
            )
            """)

            conn.execute("""
            CREATE TABLE IF NOT EXISTS videos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_id TEXT,
                caption TEXT,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
    except Exception as e:
        print(e)
    

def save_user(telegram_id, ism, familya, sharif, telefon):
    print("DB ga qo'shildi", telegram_id, ism, familya, sharif, telefon)
    try:
        with get_connection() as conn:
            conn.execute("""
            INSERT INTO users
            (telegram_id, ism, familya, sharif, telefon)
            VALUES (?, ?, ?, ?, ?)
            """, (telegram_id, ism, familya, sharif, telefon))
    except Exception as e:
        print(e)


def save_video(file_id, caption):
    try:
        with get_connection() as conn:
            conn.execute("""
            INSERT INTO videos (file_id, caption)
            VALUES (?, ?)
            """, (file_id, caption))
    except Exception as e:
        print(e)

def get_videos():
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT file_id, caption FROM videos")
            return cur.fetchall()
    except Exception as e:
        print(e)