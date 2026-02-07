from aiogram import Router, F
from aiogram.types import CallbackQuery, BotCommand, Message
from aiogram.fsm.context import FSMContext
from states import Registration_state
from utils.db import get_videos
from keyboards import return_to_menu_keyboard, subjects_keyboard

interest_router = Router()

USER_COMMANDS = [
    BotCommand(command="start", description="Botni boshlash"),
    BotCommand(command="help", description="Yordam"),
    BotCommand(command="stop", description="To'xtatish"),
]


# Foydalanuvchi o'z qiziqishlarini yozma ravishda bildirishi
@interest_router.callback_query(F.data == "self_description")
async def self_description_choice(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(
        "Siz qiziqishlaringizni yozma ravishda bildirishingiz mumkin.\n\n"
        "Masalan: *IT, Ingliz tili, Matematika, Fizika* kabi fanlar va yo'nalishlarga qiziqishingiz haqida yozishingiz mumkin.",
        reply_markup=return_to_menu_keyboard(),
    )
    await state.set_state(Registration_state.user_interests)


# Foydalanuvchi test topshirish orqali qiziqishini bildirishi
@interest_router.callback_query(F.data == "test_interest")
async def test_interest_choice(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    kb = subjects_keyboard(action="start_test")
    if not kb.inline_keyboard:
        await call.message.answer(
            "Hozircha testlar yo'q.", reply_markup=return_to_menu_keyboard()
        )
    else:
        await call.message.answer(
            "Qaysi fan bo'yicha test topshirmoqchisiz?", reply_markup=kb
        )


# Foydalanuvchi yozgan qiziqishlarni qabul qilish va mos videolarni qidirish
@interest_router.message(F.text, Registration_state.user_interests)
async def get_user_interests(msg: Message, state: FSMContext):
    user_text = msg.text.lower()
    await state.update_data(user_interests=user_text)

    await msg.answer(
        f"Sizning qiziqishlaringiz qabul qilindi. Videolar qidirilmoqda... 🔍"
    )

    all_videos = get_videos()
    found_videos = []

    for video in all_videos:
        file_id, caption, *rest = video
        if caption:
            caption_lower = caption.lower()

            words_in_caption = [
                w for w in caption_lower.replace(",", " ").split() if len(w) > 2
            ]

            match = False
            if caption_lower in user_text:
                match = True
            else:
                for word in words_in_caption:
                    if word in user_text:
                        match = True
                        break

            if match:
                found_videos.append((file_id, caption))

    if found_videos:
        for file_id, caption in found_videos:
            await msg.bot.send_video(msg.from_user.id, video=file_id, caption=caption)
        await msg.answer(
            "✅ Sizning qiziqishlaringizga mos videolar topildi!",
            reply_markup=return_to_menu_keyboard(),
        )
    else:
        await msg.answer(
            "😔 Afsuski, hozircha sizning qiziqishlaringizga mos videolar topilmadi. Keyinroq qayta urinib ko'ring yoki boshqa kalit so'zlarni kiriting.",
            reply_markup=return_to_menu_keyboard(),
        )

    await state.clear()
