from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from states import Registration_state
from keyboards import (
    phone_request,
    interest_choice_keyboard,
    yes_or_no,
    back_keyboard,
)
from utils.db import save_user, check_user
from config import admin_group, ADMINS

reg_router = Router()


from .admin import ADMIN_COMMANDS
from .interest import USER_COMMANDS


# Yordam menyusini ko'rsatish
@reg_router.message(Command("help"))
async def help_command(msg: Message):
    user_id = msg.from_user.id
    if user_id in ADMINS:
        help_text = (
            "👨‍💻 **Admin buyruqlari:**\n\n"
            "/start - Botni ishga tushirish\n"
            "/fan_qoshish - Yangi fan qo'shish\n"
            "/fan_ochirish - Fanni o'chirish\n"
            "/fanlar - Mavjud fanlar ro'yxati\n"
            "/test_qoshish - Test savollarini qo'shish\n"
            "/upload_video - Video yuklash\n"
            "/stop - Jarayonni to'xtatish"
        )
    else:
        help_text = (
            "👤 **Foydalanuvchi buyruqlari:**\n\n"
            "/start - Botni ishga tushirish\n"
            "/help - Yordam\n"
            "/stop - Jarayonni to'xtatish"
        )
    await msg.answer(help_text, parse_mode="Markdown")


from aiogram.types import BotCommandScopeChat


# Foydalanuvchi turiga qarab buyruqlar menyusini (Custom Menu) o'rnatish
async def set_commands(bot, user_id: int):
    if user_id in ADMINS:
        await bot.set_my_commands(
            ADMIN_COMMANDS, scope=BotCommandScopeChat(chat_id=user_id)
        )
    else:
        await bot.set_my_commands(
            USER_COMMANDS, scope=BotCommandScopeChat(chat_id=user_id)
        )


# Botni va joriy holatni to'xtatish
@reg_router.message(Command("stop"))
async def stop_bot(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer(
        "Bot to'xtatildi. Qayta ishga tushirish uchun /start ni bosing.",
        reply_markup=ReplyKeyboardRemove(),
    )


# Ro'yxatdan o'tish jarayonini boshlash (/start)
@reg_router.message(CommandStart())
async def Registration(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    await set_commands(msg.bot, user_id)

    if user_id in ADMINS:
        await state.clear()
        await msg.answer(
            "Salom Admin! Xush kelibsiz. 👨‍💻\n\nBuyruqlarni ko'rish uchun /help ni bosing yoki menudan foydalaning."
        )
        return
    else:
        await msg.answer(
            "Assalomu aleykum DATA talim stantsiyasining botiga xush kelibsiz!"
        )

    if check_user(user_id):
        await msg.answer("Siz allaqachon ro'yxatdan o'tgansiz.")
        await msg.answer(
            "Iltimos video qo'llanmalarni olish ucuhn so'rovda qatnashishni tasdiqlang:",
            reply_markup=yes_or_no(),
        )
        await state.set_state(Registration_state.user_interests)
        return

    await msg.answer(f"Ro'yxatdan o'tish boshlandi!\nIsmingizni kiriting:")
    await state.set_state(Registration_state.ism)


# Ismni qabul qilish
@reg_router.message(F.text, Registration_state.ism)
async def get_name(msg: Message, state: FSMContext):
    ism = msg.text
    await state.update_data(ism=ism)
    await msg.answer(f"Iltimos familyangizni kiriting:")
    await state.set_state(Registration_state.familyasi)


# Familiyani qabul qilish
@reg_router.message(F.text, Registration_state.familyasi)
async def get_surname(msg: Message, state: FSMContext):
    familyasi = msg.text
    await state.update_data(familyasi=familyasi)
    await msg.answer(f"Iltimos sharifingizni kiriting:")
    await state.set_state(Registration_state.sharifi)


# Sharifni qabul qilish
@reg_router.message(F.text, Registration_state.sharifi)
async def get_patronymic(msg: Message, state: FSMContext):
    sharifi = msg.text
    await state.update_data(sharifi=sharifi)
    await msg.answer(f"Telefon raqamingizni tastiqlang:", reply_markup=phone_request())
    await state.set_state(Registration_state.telefon_raqami)


# Telefon raqamini qabul qilish va ro'yxatdan o'tishni tugatish
@reg_router.message(F.contact, Registration_state.telefon_raqami)
async def get_phone(msg: Message, state: FSMContext):

    telefon_raqami = msg.contact.phone_number
    await state.update_data(telefon=telefon_raqami)
    await msg.answer(
        f"Ro'yxatga olish yakunlandi botimizdan to'liq foydalanishingiz mumkin."
    )

    data = await state.get_data()
    ismi = data.get("ism")
    familyasi = data.get("familyasi")
    sharifi = data.get("sharifi")

    user_info = (
        f"📌 Yangi foydalanuvchi ro‘yxatdan o‘tdi:\n\n"
        f"Ism: {data.get('ism')}\n"
        f"Familya: {data.get('familyasi')}\n"
        f"Sharif: {data.get('sharifi')}\n"
        f"Telefon: {data.get('telefon')}\n"
        f"Telegram ID: {msg.from_user.id}"
    )

    if not check_user(msg.from_user.id):
        await msg.bot.send_message(chat_id=admin_group, text=user_info)

    await msg.answer(
        f"Sizning malumotlaringiz:\nIsm : {ismi}\nFamilya : {familyasi}\nSharif : {sharifi}\nTelefon raqam : {telefon_raqami}",
        reply_markup=ReplyKeyboardRemove(),
    )
    save_user(
        telegram_id=msg.from_user.id,
        ism=data.get("ism"),
        familya=data.get("familyasi"),
        sharif=data.get("sharifi"),
        telefon=telefon_raqami,
    )

    await state.set_state(Registration_state.user_interests)
    await msg.answer(
        "Iltimos video qo'llanmalarni olish ucuhn so'rovda qatnashishni tasdiqlang:",
        reply_markup=yes_or_no(),
    )


# Video qo'llanma olish so'roviga javobni qayta ishlash
@reg_router.callback_query(F.data.in_(["yes", "no"]))
async def yes_no_callback(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    if call.data == "yes":
        await call.message.answer(
            "Siz qiziqishlaringizni qanday bildirmoqchisiz?\n\n"
            "1️⃣ *O'zim yozaman* - Qiziqishlarni o'z qo'lingiz bilan yozish va hech qanday test tekshiruvlardan o'tmaslik.\n"
            "2️⃣ *Test orqali* - Tegishli kurslarning testlaridan o'tish orqali o'z darajasini bilib, o'ziga mos video qo'llanmalarni olish.",
            reply_markup=interest_choice_keyboard(),
        )

    elif call.data == "no":
        await call.message.answer(
            "Sizga boshqa xizmatlardan foydalanishni taklif qilamiz.",
            reply_markup=back_keyboard(),
        )
        await state.clear()

    await call.answer()


# Asosiy menyuga (Xush kelibsiz xabariga) qaytish
@reg_router.callback_query(F.data == "back_to_yes_no")
async def back_to_main_menu(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    user_id = call.from_user.id
    if user_id in ADMINS:
        await state.clear()
        await call.message.answer(
            "Salom Admin! Xush kelibsiz. 👨‍💻\n\nBuyruqlarni ko'rish uchun /help ni bosing yoki menudan foydalaning."
        )
    else:
        await call.message.answer(
            "Iltimos video qo'llanmalarni olish ucuhn so'rovda qatnashishni tasdiqlang:",
            reply_markup=yes_or_no(),
        )
        await state.set_state(Registration_state.user_interests)
    await call.answer()
