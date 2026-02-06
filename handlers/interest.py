from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from states import Registration_state
from utils import get_videos

interest_router = Router()

@interest_router.callback_query(F.data == "self_description")
async def self_description_choice(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Iltimos, qiziqishlaringizni so‘z bilan tasvirlab bering (Masalan: Matematika, Fizika, Dasturlash):")
    await state.set_state(Registration_state.user_interests)

@interest_router.callback_query(F.data == "test_interest")
async def test_interest_choice(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Test orqali qiziqishlaringizni aniqlash funksiyasi hozir tayyor emas 😅")

@interest_router.message(F.text, Registration_state.user_interests)
async def get_user_interests(msg, state: FSMContext):
    interests = [x.strip() for x in msg.text.split(",")]
    await state.update_data(user_interests=interests)

    await msg.answer(f"Sizning qiziqishlaringiz qabul qilindi: {', '.join(interests)}\nVideolar tayyorlanmoqda...")

    data = await state.get_data()
    user_interests = data["user_interests"]

    all_videos = get_videos()
    for video in all_videos:
        if any(subject in video['caption'] for subject in user_interests):
            await msg.bot.send_video(msg.from_user.id, video=video['file_id'], caption=video['caption'])

    await state.clear()