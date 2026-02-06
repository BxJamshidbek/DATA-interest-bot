import asyncio
from aiogram import Router ,F
from aiogram.types import Message
from aiogram.filters import CommandStart 
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from states import Registration_state
from keyboards import phone_request
from utils import save_user , create_tables


router = Router()
create_tables()

@router.message(CommandStart())
async def Registration(msg : Message , state :FSMContext):
    user_id = msg.from_user.id
    await msg.answer("Assalomu aleykum DATA talim stantsiyasining botiga xush kelibsiz!")
    await msg.answer(f"Ro'yxatdan o'tish boshlandi!\nIsmingizni kiriting:")
    
    await state.set_state(Registration_state.ism)


@router.message(F.text , Registration_state.ism)
async def familyasi(msg : Message , state : FSMContext):
    ism = msg.text
    await state.update_data(ism = ism)
    await msg.answer(f"Iltimos familyangizni kiriting:")
    
    await state.set_state(Registration_state.familyasi)


@router.message(F.text , Registration_state.familyasi)
async def sharifi(msg : Message , state : FSMContext):
    familyasi = msg.text
    await state.update_data(familyasi = familyasi)
    await msg.answer(f"Iltimos sharifingizni kiriting:")
    await state.set_state(Registration_state.sharifi)

@router.message(F.text , Registration_state.sharifi)
async def sharifi(msg : Message , state : FSMContext):
    sharifi = msg.text
    await state.update_data(sharifi = sharifi)
    await msg.answer(f"Telefon raqamingizni tastiqlang:" , reply_markup = phone_request())
    await state.set_state(Registration_state.telefon_raqami)

@router.message(F.contact , Registration_state.telefon_raqami)
async def telfon_raqami(msg : Message , state : FSMContext):
    telefon_raqami = msg.contact.phone_number
    await state.update_data(telefon_raqami = telfon_raqami)
    await msg.answer(f"Ro'yxatga olish yakunlandi botimizdan to'liq foydalanishingiz mumkin.")
    
    data = await state.get_data()
    ismi = data.get("ism")
    familyasi = data.get("familyasi")
    sharifi = data.get("sharifi")

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
