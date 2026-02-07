from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from states import TestState
from utils.db import get_tests, get_subject_by_name, get_videos_by_score
import random
from keyboards import (
    test_options_keyboard,
    return_to_menu_keyboard,
    test_start_keyboard,
)

test_router = Router()


# Test boshlashdan oldin ogohlantirish xabarini ko'rsatish
@test_router.callback_query(F.data.startswith("start_test_"))
async def start_test_warning(call: CallbackQuery, state: FSMContext):
    subject_id = int(call.data.split("_")[-1])
    await state.update_data(subject_id=subject_id)

    tests = get_tests(subject_id)
    if len(tests) < 10:
        await call.message.answer(
            f"Ushbu fan bo'yicha testlar yetarli emas (kamida 10 ta bolishi kerak). Hozirda: {len(tests)} ta.",
            reply_markup=return_to_menu_keyboard(),
        )
        await call.answer()
        return

    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

    start_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🚀 Boshlash", callback_data="confirm_start_test"
                )
            ],
            [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_yes_no")],
        ]
    )

    await call.message.delete()
    await call.message.answer(
        "DIQQAT! ⚠️\n\n"
        "Siz hozir test topshirishni boshlaysiz.\n"
        "• Jami 10 ta savol.\n"
        "• Har bir to'g'ri javob uchun 10 ball.\n"
        "• Maksimal ball: 100.\n\n"
        "Tayyormisiz?",
        reply_markup=start_kb,
    )
    await call.answer()


# Test savollarini tayyorlash va jarayonni boshlash
@test_router.callback_query(F.data == "confirm_start_test")
async def start_test_process(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    subject_id = data.get("subject_id")

    tests = get_tests(subject_id)
    if not tests:
        await call.message.answer("Testlar topilmadi.")
        return

    selected_tests = random.sample(tests, min(len(tests), 10))

    await state.update_data(
        selected_tests=selected_tests,
        current_index=0,
        score=0,
        total_questions=len(selected_tests),
    )

    await ask_question(call.message, state)
    await call.answer()


# Navbatdagi savolni foydalanuvchiga taqdim etish
async def ask_question(message: Message, state: FSMContext):
    data = await state.get_data()
    index = data["current_index"]
    tests = data["selected_tests"]

    if index >= len(tests):
        await finish_test(message, state)
        return

    question_data = tests[index]

    options = [
        (question_data[3], "answer_A"),
        (question_data[4], "answer_B"),
        (question_data[5], "answer_C"),
    ]
    random.shuffle(options)

    q_text = f"Savol {index + 1}/{len(tests)}:\n\n{question_data[2]}"

    await message.edit_text(q_text, reply_markup=test_options_keyboard(options))
    await state.set_state(TestState.answers)


# Foydalanuvchi javobini tekshirish va keyingi savolga o'tish
@test_router.callback_query(TestState.answers, F.data.startswith("answer_"))
async def check_answer(call: CallbackQuery, state: FSMContext):
    answer = call.data.split("_")[-1]
    data = await state.get_data()
    index = data["current_index"]
    tests = data["selected_tests"]
    current_test = tests[index]

    correct_answer = current_test[6]

    if answer == correct_answer:
        await state.update_data(score=data["score"] + 10)

    await state.update_data(current_index=index + 1)
    await ask_question(call.message, state)
    await call.answer()


# Test natijalarini hisoblash va video tavsiyalarini yuborish
async def finish_test(message: Message, state: FSMContext):
    data = await state.get_data()
    score = data["score"]
    subject_id = data["subject_id"]
    total = data["total_questions"] * 10

    result_text = f"🏁 Test yakunlandi!\n\nSizning natijangiz: {score} / {total}\n\n"

    if score == total:
        result_text += "🎉 Ajoyib natija! Siz bu sohani yaxshi bilasiz."
    elif score >= total * 0.7:
        result_text += "✅ Yaxshi natija. Bilimlaringizni mustahkamlashni davom eting."
    else:
        result_text += "📚 O'rganishda davom eting. Sizga quyidagi video qo'llanmalarni tavsiya qilamiz:"

    await message.delete()
    await message.answer(result_text, reply_markup=return_to_menu_keyboard())

    videos = get_videos_by_score(subject_id, score)
    if videos:
        for file_id, caption in videos:
            await message.bot.send_video(
                chat_id=message.chat.id, video=file_id, caption=caption
            )

    await state.clear()
