import os
import time
import asyncio
import logging
from aiogram import types, Bot
from functools import wraps
from collections import defaultdict, deque
from fuzzywuzzy import fuzz

from config import CHANNEL_ID
from database import get_cached_track, save_track, get_all_queries
from search_sources import search_music_links
from music_downloader import download_mp3

# Для збереження інстансу бота
bot_instance: Bot = None

# Антиспам-контроль
user_requests = defaultdict(lambda: deque(maxlen=20))


def rate_limiter(seconds: int = 2, max_per_minute: int = 10):
    user_timestamps = {}

    def decorator(func):
        @wraps(func)
        async def wrapped(message: types.Message, *args, **kwargs):
            user_id = message.from_user.id
            now = time.time()

            # Перевірка затримки між запитами
            if user_id in user_timestamps and (now - user_timestamps[user_id]) < seconds:
                await message.reply("⏳ Занадто швидко. Зачекайте кілька секунд.")
                return

            # Ліміт за хвилину
            user_requests[user_id].append(now)
            recent = [t for t in user_requests[user_id] if now - t < 60]
            if len(recent) > max_per_minute:
                await message.reply("🚫 Забагато запитів. Зачекайте трохи.")
                return

            user_timestamps[user_id] = now
            return await func(message, *args, **kwargs)

        return wrapped
    return decorator


def find_similar_query(query: str, all_queries: list, threshold: int = 85):
    best_match = None
    best_score = 0
    for q in all_queries:
        score = fuzz.ratio(query.lower(), q.lower())
        if score > best_score and score >= threshold:
            best_match = q
            best_score = score
    return best_match


async def get_audio_from_google(query: str, user_id: int):
    from bot import bot  # імпортуємо інстанс

    logging.info(f"🔍 Запит користувача {user_id}: {query}")

    # Кешований трек
    cached = get_cached_track(query)
    if not cached:
        all_qs = get_all_queries()
        similar = find_similar_query(query, all_qs)
        if similar:
            logging.info(f"🔄 Fuzzy-результат: {similar}")
            cached = get_cached_track(similar)

    if cached:
        logging.info(f"📦 Кешований результат для '{query}': {cached['title']} — {cached['artist']}")
        return cached

    # Пошук через Google
    logging.info(f"🌐 Google-пошук для: {query}")
    links = await search_music_links(query)

    if not links:
        logging.warning(f"🚫 Результатів не знайдено для: {query}")
        await bot.send_message(user_id, "❌ Не знайдено жодного результату. Спробуйте іншу назву пісні.")
        return None

    for idx, link in enumerate(links):
        filename = f"track_{user_id}_{idx}.mp3"
        path = await download_mp3(link, filename)
        if path:
            try:
                with open(path, "rb") as audio_file:
                    msg = await bot.send_audio(
                        chat_id=CHANNEL_ID,
                        audio=audio_file,
                        title=query,
                        performer="",
                        caption=f"🎵 {query}"
                    )
                os.remove(path)
                logging.info(f"✅ Успішно збережено в канал: {msg.audio.file_id}")
                save_track(query, msg.audio.file_id, msg.audio.title or query, msg.audio.performer or "", user_id)
                return {
                    "title": msg.audio.title or query,
                    "artist": msg.audio.performer or "",
                    "file_id": msg.audio.file_id
                }
            except Exception as e:
                logging.error(f"❌ Помилка при надсиланні у канал: {e}")

    logging.warning(f"❌ Не вдалося обробити жодне посилання для: {query}")
    await bot.send_message(user_id, "⚠️ Пісню не вдалося завантажити. Спробуйте іншу.")
    return None


# Якщо потрібно використовувати глобальний бот інстанс
async def setup_webhook(bot: Bot):
    global bot_instance
    bot_instance = bot
