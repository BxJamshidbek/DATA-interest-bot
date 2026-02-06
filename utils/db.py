import sqlite3

DB_NAME = "users.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_tables():
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
    

def save_user(telegram_id, ism, familya, sharif, telefon):
    print("DB ga qo'shildi", telegram_id, ism, familya, sharif, telefon)
    with get_connection() as conn:
        conn.execute("""
        INSERT INTO users
        (telegram_id, ism, familya, sharif, telefon)
        VALUES (?, ?, ?, ?, ?)
        """, (telegram_id, ism, familya, sharif, telefon))
    