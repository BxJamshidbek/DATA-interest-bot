import asyncio
import logging
from aiogram import Bot , Dispatcher
from config import token
from handlers import Registration , reg_router , admin_router
from utils import create_tables

create_tables()

logging.basicConfig(level=logging.INFO)
bot = Bot(token=token)
dp = Dispatcher()

dp.include_router(reg_router)
dp.include_router(admin_router)

async def main():

    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except:
        print("Xato")