from aiogram.fsm.state import State, StatesGroup


# Foydalanuvchi ro'yxatdan o'tishi uchun holatlar guruhi
class Registration_state(StatesGroup):
    ism = State()
    familyasi = State()
    sharifi = State()
    telefon_raqami = State()
    user_interests = State()


# Test topshirish jarayoni uchun holatlar guruhi
class TestState(StatesGroup):
    subject_id = State()
    current_question = State()
    score = State()
    answers = State()
