import logging
from aiogram import Bot, Dispatcher, types, executor
from config import BOT_TOKEN
from handlers import register_handlers
from utils import setup_webhook

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

register_handlers(dp)

if __name__ == "__main__":
    import asyncio
    from aiogram import executor

    loop = asyncio.get_event_loop()
    loop.run_until_complete(setup_webhook(bot))
    executor.start_polling(dp, skip_updates=True)
