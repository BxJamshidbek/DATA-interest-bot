from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from utils import save_video , get_videos
from config import baza_kanal , ADMINS
from aiogram.types import BotCommand

admin_router = Router()

ADMIN_COMMANDS = [
    BotCommand(command="/start", description="Botni boshlash"),
    BotCommand(command="/upload_video", description="Video yuklash"),
    BotCommand(command="/help", description="Yordam"),
]

@admin_router.message(Command("upload_video"))
async def upload_video_start(msg: Message):
    if msg.from_user.id not in ADMINS:
        await msg.answer("❌ Siz admin emassiz!")
        return
    await msg.answer("📤 Iltimos, videoni caption bilan yuboring:")

@admin_router.message(F.video)
async def video_handler(msg: Message):
    if msg.from_user.id not in ADMINS:
        await msg.answer("❌ Siz admin emassiz!")
        return

    video = msg.video
    caption = msg.caption

    if not caption:
        await msg.answer("❌ Siz videoga izoh (caption) qo‘shmadingiz. Iltimos, caption bilan yuboring!")
        return

    save_video(file_id=video.file_id, caption=caption)

    await msg.bot.send_video(chat_id=baza_kanal, video=video.file_id, caption=caption)
    await msg.answer("✅ Video saqlandi va kanalga yuborildi!")