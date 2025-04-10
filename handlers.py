from aiogram import Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils import SoundCloud

async def start_handler(message: types.Message):
    await message.reply("Привіт! 👋 Введи назву пісні або виконавця, щоб я міг її знайти.")

async def search_handler(message: types.Message):
    query = message.text.strip()
    logging.info(f"🔎 Запит користувача: {query}")

    # Ініціалізуємо об'єкт SoundCloud
    soundcloud = SoundCloud(client_id="muVdh3UofeKxfL9C801bVZpAa2RLBVW1")  # Твій SoundCloud API Key
    url = f"https://soundcloud.com/{query}"
    
    # Завантажуємо пісню
    soundcloud.download_song(url)

    # Надсилаємо результат користувачу
    await message.reply("Файл завантажено! Відправляю вам посилання...")

    # Завантажуємо файл для надсилання
    with open(f"track_{url}.mp3", "rb") as file:
        await message.answer_audio(file)

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=["start"])
    dp.register_message_handler(search_handler, content_types=types.ContentType.TEXT)
