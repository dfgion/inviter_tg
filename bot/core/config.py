from aiogram import Bot, Dispatcher

import os

class Config:
    SUPER_ADMIN = os.getenv("SUPER_ADMIN")
    REDIS_DSN = os.getenv("REDIS_DSN")
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    DATABASE_DSN = os.getenv("DATABASE_DSN")


bot = Bot(token=Config.BOT_TOKEN)
dp = Dispatcher()