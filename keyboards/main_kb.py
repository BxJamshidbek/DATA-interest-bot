from aiogram.utils.keyboard import ReplyKeyboardBuilder , InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup , KeyboardButton , InlineKeyboardButton , InlineKeyboardMarkup , WebAppInfo

def phone_request():
    phone_btn = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📱 Telefon raqamni yuborish", request_contact=True)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
    return phone_btn


inline_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Qiziqishlarni o'zim tasvirlayman", callback_data="self_description"),
        InlineKeyboardButton(text="Test orqali bilib olish", callback_data="test_option")
    ]
])

def yes_or_no():
    choice_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="1️⃣ Yes", callback_data="yes"),
                InlineKeyboardButton(text="2️⃣ no", callback_data="no")
            ]
        ]
    )
    return choice_keyboard

def interest_choice_keyboard():
    choice_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="1️⃣ Qiziqishlarimni tasvirlab berish", callback_data="self_description"),
                InlineKeyboardButton(text="2️⃣ Test orqali qiziqishlarni aniqlash", callback_data="test_interest")
            ]
        ]
    )
    return choice_keyboard

