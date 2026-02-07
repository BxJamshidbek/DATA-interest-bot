from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils.db import get_subjects


# Fanlar ro'yxati uchun inline klaviatura yaratish
def subjects_keyboard(action="start_test"):
    subjects = get_subjects()
    keyboard = []
    for sub in subjects:
        callback = f"{action}_{sub[0]}"
        keyboard.append([InlineKeyboardButton(text=sub[1], callback_data=callback)])

    keyboard.append(
        [InlineKeyboardButton(text="🔙 Asosiy menu", callback_data="back_to_yes_no")]
    )
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


# Test savollari variantlari uchun klaviatura yaratish (Admin va User uchun moslashuvchan)
def test_options_keyboard(options=None, back_callback="back_to_yes_no"):
    keyboard = []
    if options:
        for text, callback in options:
            keyboard.append([InlineKeyboardButton(text=text, callback_data=callback)])
    else:
        keyboard.append(
            [
                InlineKeyboardButton(text="A", callback_data="answer_A"),
                InlineKeyboardButton(text="B", callback_data="answer_B"),
                InlineKeyboardButton(text="C", callback_data="answer_C"),
            ]
        )

    keyboard.append(
        [InlineKeyboardButton(text="🔙 Asosiy menu", callback_data=back_callback)]
    )
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


# Testni boshlashni tasdiqlash uchun klaviatura
def test_start_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🚀 Boshlash", callback_data="confirm_start_test"
                )
            ],
            [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_yes_no")],
        ]
    )
