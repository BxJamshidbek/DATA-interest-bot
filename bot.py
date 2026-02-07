import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import token
from handlers import (
    Registration,
    reg_router,
    admin_router,
    admin_test_router,
    interest_router,
    test_router,
)
from utils.db import create_tables

create_tables()

logging.basicConfig(level=logging.DEBUG)
bot = Bot(token=token)
dp = Dispatcher()


# Kiruvchi xabarlarni terminalda ko'rsatuvchi middleware
@dp.message.outer_middleware()
async def debug_middleware(handler, event, data):
    print(f"DEBUG INCOMING: {event.text} from user {event.from_user.id}")
    return await handler(event, data)


dp.include_router(admin_router)
dp.include_router(admin_test_router)
dp.include_router(test_router)
dp.include_router(interest_router)
dp.include_router(reg_router)


# Botni ishga tushiruvchi asosiy funksiya
async def main():

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except:
        print("Xato")
