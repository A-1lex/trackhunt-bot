import logging
from aiogram import Bot, Dispatcher, executor, types
from config import BOT_TOKEN
from handlers import register_handlers
from inline import register_inline
from database import init_db

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/bot.log"),
        logging.StreamHandler()
    ]
)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

init_db()
register_handlers(dp)
register_inline(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
