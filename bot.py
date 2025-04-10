# -*- coding: utf-8 -*-
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils.executor import start_webhook

from config import BOT_TOKEN
from handlers import register_handlers
from inline import register_inline
from database import init_db

WEBHOOK_HOST = os.getenv("RENDER_EXTERNAL_URL")  # Render автоматично створює це
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.getenv("PORT", 5000))

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

init_db()
register_handlers(dp)
register_inline(dp)

async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)
    logging.info(f"✅ Webhook встановлено: {WEBHOOK_URL}")

async def on_shutdown(dp):
    logging.info("⛔ Вимкнення бота...")
    await bot.delete_webhook()

if __name__ == "__main__":
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
