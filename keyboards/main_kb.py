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