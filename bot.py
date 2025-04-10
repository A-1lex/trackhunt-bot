import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.utils.executor import start_webhook
from config import BOT_TOKEN, WEBHOOK_URL
from handlers import register_handlers
from utils import setup_webhook
from database import init_db  # 👈 додай цей імпорт

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

register_handlers(dp)

init_db()  # 👈 і цей виклик перед запуском

async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)
    logging.info(f"✅ Webhook встановлено: {WEBHOOK_URL}")
    await setup_webhook(bot)

async def on_shutdown(dp):
    logging.info("⛔ Вимкнення бота...")
    await bot.delete_webhook()

if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path='/webhook',
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
    )
