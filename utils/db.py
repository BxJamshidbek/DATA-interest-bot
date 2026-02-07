import sqlite3

DB_NAME = "users.db"


# Ma'lumotlar bazasiga ulanish yaratish
def get_connection():
    return sqlite3.connect(DB_NAME)


# Barcha kerakli jadvallarni va migratsiyalarni yaratish
def create_tables():
    try:
        with get_connection() as conn:
            conn.execute(
                """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER UNIQUE,
                ism TEXT,
                familya TEXT,
                sharif TEXT,
                telefon TEXT
            )
            """
            )

            conn.execute(
                """
            CREATE TABLE IF NOT EXISTS videos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_id TEXT,
                caption TEXT,
                subject_id INTEGER,
                min_score INTEGER,
                max_score INTEGER,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(subject_id) REFERENCES subjects(id)
            )
            """
            )

            cursor = conn.cursor()
            cursor.execute("PRAGMA table_info(videos)")
            columns = [column[1] for column in cursor.fetchall()]
            if "subject_id" not in columns:
                conn.execute("ALTER TABLE videos ADD COLUMN subject_id INTEGER")
            if "min_score" not in columns:
                conn.execute("ALTER TABLE videos ADD COLUMN min_score INTEGER")
            if "max_score" not in columns:
                conn.execute("ALTER TABLE videos ADD COLUMN max_score INTEGER")

            conn.execute(
                """
            CREATE TABLE IF NOT EXISTS subjects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE
            )
            """
            )

            conn.execute(
                """
            CREATE TABLE IF NOT EXISTS tests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject_id INTEGER,
                question TEXT,
                option_a TEXT,
                option_b TEXT,
                option_c TEXT,
                correct_answer TEXT,
                FOREIGN KEY(subject_id) REFERENCES subjects(id)
            )
            """
            )
    except Exception as e:
        print(e)


# Yangi foydalanuvchini bazaga saqlash
def save_user(telegram_id, ism, familya, sharif, telefon):
    try:
        with get_connection() as conn:
            conn.execute(
                """
            INSERT INTO users
            (telegram_id, ism, familya, sharif, telefon)
            VALUES (?, ?, ?, ?, ?)
            """,
                (telegram_id, ism, familya, sharif, telefon),
            )
    except Exception as e:
        print(e)


# Video bazada bor-yo'qligini tekshirish
def check_video_exists(file_id):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT id FROM videos WHERE file_id = ?", (file_id,))
            return cur.fetchone() is not None
    except Exception as e:
        print(e)
        return False


# Yangi videoni barcha parametrlari bilan saqlash
def save_video(file_id, caption, subject_id=None, min_score=None, max_score=None):
    if check_video_exists(file_id):
        return False

    try:
        with get_connection() as conn:
            conn.execute(
                """
            INSERT INTO videos (file_id, caption, subject_id, min_score, max_score)
            VALUES (?, ?, ?, ?, ?)
            """,
                (file_id, caption, subject_id, min_score, max_score),
            )
        return True
    except Exception as e:
        print(e)
        return False


# Barcha videolarni bazadan olish
def get_videos():
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT file_id, caption, subject_id, min_score, max_score FROM videos"
            )
            return cur.fetchall()
    except Exception as e:
        print(e)
        return []


# Berilgan fan va ball oralig'iga mos videolarni olish
def get_videos_by_score(subject_id, score):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT file_id, caption FROM videos 
                WHERE subject_id = ? AND min_score <= ? AND max_score >= ?
                """,
                (subject_id, score, score),
            )
            return cur.fetchall()
    except Exception as e:
        print(e)
        return []


# Foydalanuvchi ro'yxatdan o'tganligini tekshirish
def check_user(telegram_id):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
            if cur.fetchone():
                return True
            else:
                return False
    except Exception as e:
        print(e)
        return False


# Yangi fan qo'shish
def add_subject(name):
    try:
        with get_connection() as conn:
            conn.execute("INSERT INTO subjects (name) VALUES (?)", (name,))
        return True
    except Exception as e:
        print(e)
        return False


# Barcha fanlar ro'yxatini olish
def get_subjects():
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM subjects")
            return cur.fetchall()
    except Exception as e:
        print(e)
        return []


# Fanni nomi orqali o'chirish
def delete_subject(name):
    try:
        with get_connection() as conn:
            conn.execute("DELETE FROM subjects WHERE name = ?", (name,))
        return True
    except Exception as e:
        print(e)
        return False


# Fan ma'lumotlarini nomi orqali olish
def get_subject_by_name(name):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM subjects WHERE name = ?", (name,))
            return cur.fetchone()
    except Exception as e:
        print(e)
        return None


# Yangi test savolini saqlash
def add_test(subject_id, question, a, b, c, correct):
    try:
        with get_connection() as conn:
            conn.execute(
                """
            INSERT INTO tests (subject_id, question, option_a, option_b, option_c, correct_answer)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
                (subject_id, question, a, b, c, correct),
            )
        return True
    except Exception as e:
        print(e)
        return False


# Fan bo'yicha barcha test savollarini olish
def get_tests(subject_id):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM tests WHERE subject_id = ?", (subject_id,))
            return cur.fetchall()
    except Exception as e:
        print(e)
        return []
