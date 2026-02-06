import asyncio
from aiogram import Router ,F
from aiogram.types import Message
from aiogram.filters import CommandStart 
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from states import Registration_state
from keyboards import phone_request
from utils import save_user , create_tables
from config import admin_group , ADMINS
from .user import USER_COMMANDS
from .admin import ADMIN_COMMANDS


reg_router = Router()
create_tables()

async def set_commands(bot, user_id: int):
    if user_id in ADMINS:
        await bot.set_my_commands(ADMIN_COMMANDS, scope=None)
    else:
        await bot.set_my_commands(USER_COMMANDS, scope=None)


@reg_router.message(CommandStart())
async def Registration(msg : Message , state :FSMContext):

    user_id = msg.from_user.id

    await set_commands(msg.bot, user_id)

    if user_id in ADMINS:
        await msg.answer("Salom Admin! ")
        return

    user_id = msg.from_user.id
    await msg.answer("Assalomu aleykum DATA talim stantsiyasining botiga xush kelibsiz!")
    await msg.answer(f"Ro'yxatdan o'tish boshlandi!\nIsmingizni kiriting:")
    
    await state.set_state(Registration_state.ism)

@reg_router.message(F.text , Registration_state.ism)
async def familyasi(msg : Message , state : FSMContext):
    ism = msg.text
    await state.update_data(ism = ism)
    await msg.answer(f"Iltimos familyangizni kiriting:")
    
    await state.set_state(Registration_state.familyasi)

@reg_router.message(F.text , Registration_state.familyasi)
async def sharifi(msg : Message , state : FSMContext):
    familyasi = msg.text
    await state.update_data(familyasi = familyasi)
    await msg.answer(f"Iltimos sharifingizni kiriting:")
    await state.set_state(Registration_state.sharifi)

@reg_router.message(F.text , Registration_state.sharifi)
async def sharifi(msg : Message , state : FSMContext):
    sharifi = msg.text
    await state.update_data(sharifi = sharifi)
    await msg.answer(f"Telefon raqamingizni tastiqlang:" , reply_markup = phone_request())
    await state.set_state(Registration_state.telefon_raqami)

@reg_router.message(F.contact , Registration_state.telefon_raqami)
async def telfon_raqami(msg : Message , state : FSMContext):

    telefon_raqami = msg.contact.phone_number
    await state.update_data(telefon_raqami = telfon_raqami)
    await msg.answer(f"Ro'yxatga olish yakunlandi botimizdan to'liq foydalanishingiz mumkin.")
    
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

    await msg.bot.send_message(chat_id=admin_group , text=user_info)

    await msg.answer(
        f"Sizning malumotlaringiz:\nIsm : {ismi}\nFamilya : {familyasi}\nSharif : {sharifi}\nTelefon raqam : {telefon_raqami}"
        , reply_markup=ReplyKeyboardRemove()
    )
    save_user(
        telegram_id=msg.from_user.id,
        ism=data.get("ism"),
        familya=data.get("familyasi"),
        sharif=data.get("sharifi"),
        telefon=telefon_raqami
    )

    state.clear()
