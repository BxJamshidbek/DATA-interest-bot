from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from states import AdminSubjectState, AdminTestState
from utils.db import (
    add_subject,
    delete_subject,
    get_subjects,
    add_test,
)
from keyboards import subjects_keyboard, test_options_keyboard
from config import ADMINS

admin_test_router = Router()


# Yangi fan qo'shishni boshlash
@admin_test_router.message(Command("fan_qoshish", "fanqoshish"), StateFilter("*"))
async def add_subject_start(msg: Message, state: FSMContext):
    if msg.from_user.id not in ADMINS:
        await msg.answer("❌ Siz admin emassiz!")
        return
    await msg.answer("Yangi fan nomini kiriting:")
    await state.set_state(AdminSubjectState.name)


# Fan nomini qabul qilish va saqlash
@admin_test_router.message(AdminSubjectState.name)
async def add_subject_name(msg: Message, state: FSMContext):
    name = msg.text
    if add_subject(name):
        await msg.answer(f"✅ Fan qo'shildi: {name}")
    else:
        await msg.answer("❌ Xatolik yuz berdi. Balki bu fan allaqachon mavjuddir.")
    await state.clear()


# Fanni o'chirish uchun fanni tanlash menyusini ko'rsatish
@admin_test_router.message(Command("fan_ochirish", "fanochirish"), StateFilter("*"))
async def delete_subject_prompt(msg: Message, state: FSMContext):
    if msg.from_user.id not in ADMINS:
        return
    subjects = get_subjects()
    if not subjects:
        await msg.answer("Fanlar topilmadi.")
        return
    kb = subjects_keyboard(action="delete")
    await msg.answer("O'chiriladigan fanni tanlang:", reply_markup=kb)


# Barcha fanlar ro'yxatini ko'rsatish
@admin_test_router.message(Command("fanlar"), StateFilter("*"))
async def list_subjects(msg: Message):
    if msg.from_user.id not in ADMINS:
        return
    subjects = get_subjects()
    if not subjects:
        await msg.answer("Hozircha fanlar qo'shilmagan.")
        return
    text = "📚 **Mavjud fanlar ro'yxati:**\n\n"
    for i, sub in enumerate(subjects, 1):
        text += f"{i}. {sub[1]}\n"
    await msg.answer(text, parse_mode="Markdown")


# Tanlangan fanni o'chirishni qayta ishlash
@admin_test_router.callback_query(F.data.startswith("delete_"))
async def delete_subject_callback(call: CallbackQuery, state: FSMContext):
    if call.from_user.id not in ADMINS:
        await call.answer("❌ Siz admin emassiz!", show_alert=True)
        return
    subject_id = int(call.data.split("_")[-1])
    subjects = get_subjects()
    subject_name = next((sub[1] for sub in subjects if sub[0] == subject_id), None)
    if subject_name and delete_subject(subject_name):
        await call.message.edit_text(f"✅ Fan o'chirildi: {subject_name}")
    else:
        await call.message.edit_text("❌ Xatolik yuz berdi.")
    await call.answer()


# Yangi test qo'shishni boshlash: fanni tanlash
@admin_test_router.message(Command("test_qoshish", "testqoshish"), StateFilter("*"))
async def add_test_start(msg: Message, state: FSMContext):
    if msg.from_user.id not in ADMINS:
        return
    kb = subjects_keyboard(action="add_test")
    if not kb.inline_keyboard:
        await msg.answer("Avval fan qo'shing!")
        return
    await msg.answer("Test qo'shish uchun fanni tanlang:", reply_markup=kb)


# Tanlangan fanga test qo'shish uchun savol so'rash
@admin_test_router.callback_query(F.data.startswith("add_test_"))
async def add_test_subject(call: CallbackQuery, state: FSMContext):
    subject_id = int(call.data.split("_")[-1])
    await state.update_data(subject_id=subject_id)
    await call.message.answer("Savolni kiriting:")
    await state.set_state(AdminTestState.question)
    await call.answer()


# Test savolini qabul qilish va variantlarni so'rash
@admin_test_router.message(AdminTestState.question)
async def add_test_question(msg: Message, state: FSMContext):
    await state.update_data(question=msg.text)
    await msg.answer(
        "Variantlarni quyidagi formatda kiriting:\n\nVariant A | Variant B | Variant C\n\nMasalan: 4 | 5 | 6"
    )
    await state.set_state(AdminTestState.options)


# Variantlarni qabul qilish va to'g'ri javobni so'rash
@admin_test_router.message(AdminTestState.options)
async def add_test_options(msg: Message, state: FSMContext):
    try:
        a, b, c = map(str.strip, msg.text.split("|"))
        await state.update_data(options=(a, b, c))
        await msg.answer(
            f"To'g'ri javobni tanlang:\nA: {a}\nB: {b}\nC: {c}",
            reply_markup=test_options_keyboard(),
        )
        await state.set_state(AdminTestState.correct_answer)
    except ValueError:
        await msg.answer(
            "Format xato! Iltimos, qaytadan kiriting:\nVariant A | Variant B | Variant C"
        )


# To'g'ri javobni qabul qilish va testni bazaga saqlash
@admin_test_router.callback_query(
    AdminTestState.correct_answer, F.data.startswith("answer_")
)
async def add_test_finish(call: CallbackQuery, state: FSMContext):
    correct_answer = call.data.split("_")[-1]
    data = await state.get_data()
    if add_test(
        subject_id=data["subject_id"],
        question=data["question"],
        a=data["options"][0],
        b=data["options"][1],
        c=data["options"][2],
        correct=correct_answer,
    ):
        await call.message.answer("✅ Test muvaffaqiyatli qo'shildi!")
    else:
        await call.message.answer("❌ Xatolik yuz berdi.")
    await state.clear()
    await call.answer()
