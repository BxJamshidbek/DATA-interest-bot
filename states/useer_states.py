from aiogram.fsm.state import State , StatesGroup

class Registration_state(StatesGroup):
    ism = State()
    familyasi = State()
    sharifi = State()
    telefon_raqami = State()
    