from aiogram.fsm.state import State, StatesGroup


# Fan qo'shish uchun holatlar guruhi
class AdminSubjectState(StatesGroup):
    name = State()


# Test qo'shish uchun holatlar guruhi
class AdminTestState(StatesGroup):
    subject_id = State()
    question = State()
    options = State()
    correct_answer = State()


# Video yuklash uchun holatlar guruhi
class AdminVideoState(StatesGroup):
    video = State()
    subject = State()
    score_range = State()
