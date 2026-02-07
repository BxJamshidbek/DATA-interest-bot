from aiogram import Router, F
from aiogram.types import Message, BotCommand, CallbackQuery
from aiogram.filters import Command, StateFilter
from utils.db import save_video, get_subjects
from config import ADMINS, baza_kanal

admin_router = Router()

ADMIN_COMMANDS = [
    BotCommand(command="start", description="Botni boshlash"),
    BotCommand(command="help", description="Yordam"),
    BotCommand(command="fan_qoshish", description="Fan qo'shish"),
    BotCommand(command="fan_ochirish", description="Fan o'chirish"),
    BotCommand(command="fanlar", description="Fanlar ro'yxati"),
    BotCommand(command="test_qoshish", description="Test qo'shish"),
    BotCommand(command="upload_video", description="Video yuklash"),
    BotCommand(command="stop", description="To'xtatish"),
]


from aiogram.fsm.context import FSMContext
from states import AdminVideoState
from keyboards import subjects_keyboard


# Video yuklash jarayonini boshlash
@admin_router.message(Command("upload_video", "uploadvideo"), StateFilter("*"))
async def upload_video_start(msg: Message, state: FSMContext):
    if msg.from_user.id not in ADMINS:
        await msg.answer("❌ Siz admin emassiz!")
        return
    await msg.answer(
        "📤 Iltimos, videoni caption bilan yuboring.\n\n"
        "💡 *Eslatma:* Videoga izoh yozishda fanning nomini ham albatta yozib o'ting!",
        parse_mode="Markdown",
    )
    await state.set_state(AdminVideoState.video)


# Video faylini va captionni qabul qilish
@admin_router.message(F.video, AdminVideoState.video)
async def video_handler(msg: Message, state: FSMContext):
    if msg.from_user.id not in ADMINS:
        return

    if not msg.caption:
        await msg.answer(
            "❌ Siz videoga izoh (caption) qo‘shmadingiz. Iltimos, caption bilan birga yuboring!"
        )
        return

    await state.update_data(video_file_id=msg.video.file_id, caption=msg.caption)

    kb = subjects_keyboard(action="vid_sub")
    await msg.answer("Ushbu video qaysi fanga tegishli?", reply_markup=kb)
    await state.set_state(AdminVideoState.subject)


# Video tegishli bo'lgan fanni tanlashni qayta ishlash
@admin_router.callback_query(F.data.startswith("vid_sub_"), AdminVideoState.subject)
async def video_subject_handler(call: CallbackQuery, state: FSMContext):
    subject_id = int(call.data.split("_")[-1])
    await state.update_data(subject_id=subject_id)

    await call.message.answer(
        "Ushbu video qaysi ball oralig'i uchun? (Masalan: 0-50 yoki 70-100)"
    )
    await state.set_state(AdminVideoState.score_range)
    await call.answer()


# Ball oralig'ini qabul qilish va videoni saqlash
@admin_router.message(AdminVideoState.score_range)
async def video_score_handler(msg: Message, state: FSMContext):
    try:
        parts = msg.text.split("-")
        if len(parts) != 2:
            raise ValueError
        min_s, max_s = map(int, map(str.strip, parts))
    except ValueError:
        await msg.answer(
            "Format noto'g'ri! Iltimos, 'min-max' ko'rinishida yozing (Masalan: 0-50):"
        )
        return

    data = await state.get_data()
    if save_video(
        file_id=data["video_file_id"],
        caption=data["caption"],
        subject_id=data["subject_id"],
        min_score=min_s,
        max_score=max_s,
    ):
        await msg.bot.send_video(
            chat_id=baza_kanal, video=data["video_file_id"], caption=data["caption"]
        )
        await msg.answer("✅ Video muvaffaqiyatli saqlandi va kanalga yuborildi!")
    else:
        await msg.answer("⚠️ Xatolik yuz berdi yoki bu video allaqachon mavjud!")

    await state.clear()
