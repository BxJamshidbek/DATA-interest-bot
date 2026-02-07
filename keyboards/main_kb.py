from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    WebAppInfo,
)


def phone_request():
    phone_btn = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 Telefon raqamni yuborish", request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    return phone_btn


inline_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Qiziqishlarni o'zim tasvirlayman",
                callback_data="self_description",
            ),
            InlineKeyboardButton(
                text="Test orqali bilib olish", callback_data="test_option"
            ),
        ]
    ]
)


def yes_or_no():
    choice_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="1️⃣ Yes", callback_data="yes"),
                InlineKeyboardButton(text="2️⃣ no", callback_data="no"),
            ]
        ]
    )
    return choice_keyboard


def interest_choice_keyboard():
    choice_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✍️ O'zim yozaman", callback_data="self_description"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🧪 Test orqali aniqlash", callback_data="test_interest"
                )
            ],
            [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_yes_no")],
        ]
    )
    return choice_keyboard


def back_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_yes_no")]
        ]
    )


def return_to_menu_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔙 Asosiy menu", callback_data="back_to_yes_no"
                )
            ]
        ]
    )
