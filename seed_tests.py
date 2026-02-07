from utils.db import add_test, get_subjects, get_connection


# Bazadagi barcha mavjud testlarni to'liq tozalash
def clear_tests():
    with get_connection() as conn:
        conn.execute("DELETE FROM tests")
    print("🗑 Eski testlar o'chirildi.")


# Bazaga namunaviy test savollarini qo'shish (Seeding)
def seed_tests():
    subjects = get_subjects()
    subject_map = {name.lower(): id for id, name in subjects}

    def add_bulk_tests(subject_name, tests_list):
        s_id = subject_map.get(subject_name.lower())
        if s_id:
            for q, a, b, c, cor in tests_list:
                add_test(s_id, q, a, b, c, cor)
            print(f"✅ {subject_name} uchun 10 ta test qo'shildi.")
        else:
            print(f"⚠️ {subject_name} topilmadi!")

    math_tests = [
        ("15 + 27 = ?", "42", "32", "52", "A"),
        ("12 * 8 = ?", "86", "96", "106", "B"),
        ("144 / 12 = ?", "12", "14", "10", "A"),
        ("9² + 10 = ?", "81", "91", "100", "B"),
        ("x + 15 = 40. x = ?", "25", "35", "15", "A"),
        ("3 ta olmaning narxi 15 so'm. 7 ta olmaniki qancha?", "30", "35", "40", "B"),
        (
            "To'g'ri to'rtburchakning tomonlari 4 va 6. Yuzini toping.",
            "10",
            "24",
            "20",
            "B",
        ),
        ("2x - 10 = 20. x = ?", "15", "10", "5", "A"),
        ("Doira yuzi formulasi qaysi?", "S=πr²", "S=2πr", "S=πd", "A"),
        ("log2(8) = ?", "2", "3", "4", "B"),
    ]

    fiz_tests = [
        ("Vaqt birligi nima?", "Metr", "Sekund", "Kilogram", "B"),
        ("F = m * a qaysi qonun?", "Nyuton 1", "Nyuton 2", "Nyuton 3", "B"),
        ("Zichlik formulasi?", "ρ = m/V", "ρ = m*V", "ρ = V/m", "A"),
        ("Elektr kuchlanish birligi?", "Amper", "Ohm", "Volt", "C"),
        ("Erkin tushish tezlanishi g taxminan?", "10 m/s²", "5 m/s²", "20 m/s²", "A"),
        ("Qarshilik birligi nima?", "Volt", "Ohm", "Vatt", "B"),
        ("Issiqlik miqdori birligi?", "Joul", "Paskal", "Nyuton", "A"),
        (
            "Yorug'lik tezligi (c) qancha?",
            "3*10^8 m/s",
            "3*10^5 m/s",
            "3*10^10 m/s",
            "A",
        ),
        ("Bosim qanday harf bilan belgilanadi?", "P", "F", "E", "A"),
        ("Guk qonuni formulasi?", "F = -kx", "F = mg", "F = ma", "A"),
    ]

    eng_tests = [
        ("He ___ a student.", "is", "am", "are", "A"),
        ("I ___ to school every day.", "go", "goes", "going", "A"),
        ("She ___ a book yesterday.", "read", "reads", "red", "A"),
        ("Wait! I ___ you.", "will help", "help", "helped", "A"),
        ("Find the synonym for 'Happy'", "Sad", "Glad", "Angry", "B"),
        ("They ___ English for 2 years.", "have studied", "studied", "studying", "A"),
        ("If I ___ rich, I would buy a car.", "am", "was", "were", "C"),
        ("Which one is an adjective?", "Run", "Quickly", "Beautiful", "C"),
        ("The book is ___ the table.", "on", "in", "at", "A"),
        ("Choose the correct spelling:", "Beautiful", "Beatiful", "Beautifull", "A"),
    ]

    py_tests = [
        (
            "Python-da o'zgaruvchi qanday e'lon qilinadi?",
            "var x = 5",
            "x = 5",
            "int x = 5",
            "B",
        ),
        ("Ro'yxat (list) qanday yaratiladi?", "x = []", "x = {}", "x = ()", "A"),
        ("Qaysi biri funksiya kalit so'zi?", "function", "def", "func", "B"),
        ("3 ** 2 natijasi nima?", "6", "9", "5", "B"),
        ("Python-da izoh (comment) belgisi?", "//", "/*", "#", "C"),
        (
            "String uzunligini qaysi funksiya topadi?",
            "len()",
            "length()",
            "size()",
            "A",
        ),
        ("List-ga element qo'shish metodi?", "add()", "append()", "plus()", "B"),
        ("Foydalanuvchidan ma'lumot olish?", "print()", "input()", "get()", "B"),
        ("Qaysi ma'lumot turi o'zgarmas (immutable)?", "list", "dict", "tuple", "C"),
        ("Lug'at (dictionary) qanday yaratiladi?", "{}", "[]", "()", "A"),
    ]

    front_tests = [
        ("HTML nima?", "Dasturlash tili", "Belgilash tili", "Ma'lumotlar bazasi", "B"),
        ("Eng katta sarlavha tegi?", "<h6>", "<h1>", "<head>", "B"),
        ("CSS-da rang berish xususiyati?", "font-color", "color", "text-color", "B"),
        (
            "Javascript-da o'zgaruvchi e'lon qilish?",
            "let",
            "var",
            "Ikkala javob ham to'g'ri",
            "C",
        ),
        ("Havola (link) yaratish tegi?", "<a>", "<link>", "<href>", "A"),
        (
            "CSS-da elementni markazga keltirish?",
            "text-align: center",
            "margin: 0 auto",
            "Ikkala javob ham to'g'ri",
            "C",
        ),
        ("Javascript-da ogohlantirish oynasi?", "msg()", "alert()", "popup()", "B"),
        ("HTML fayl kengaytmasi?", ".html", ".css", ".js", "A"),
        ("In-line elementni toping:", "<div>", "<span>", "<p>", "B"),
        ("CSS-da ID selector belgisi?", ".", "#", "*", "B"),
    ]

    clear_tests()
    add_bulk_tests("Matematika", math_tests)
    add_bulk_tests("Fizika", fiz_tests)
    add_bulk_tests("Ingiliz tili", eng_tests)
    add_bulk_tests("IT ( backend ) PYTHON", py_tests)
    add_bulk_tests("Frontend", front_tests)


if __name__ == "__main__":
    seed_tests()
