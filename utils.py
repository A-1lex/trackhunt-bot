import os
import logging
from aiogram import Bot
from config import CHANNEL_ID, CACHE_FOLDER, PAGE_SIZE
from database import get_cached_track, save_track, log_query, get_all_queries
from search_sources import search_music_links
from music_downloader import download_mp3
import asyncio
from functools import wraps
from fuzzywuzzy import fuzz

bot_instance: Bot = None  # буде призначено у setup_webhook

async def get_track(query: str, user_id: int) -> dict:
    log_query(query)

    # 1. Пробуємо точний кеш
    cached = get_cached_track(query)
    if not cached:
        # 2. Пробуємо знайти схожий запит через Fuzzy
        similar = find_similar_query(query)
        if similar:
            logging.info(f"🔁 Fuzzy-результат: {similar}")
            cached = get_cached_track(similar)

    if cached:
        return cached

    # 3. Якщо кеш не знайдено — парсимо напряму
    links = await search_music_links(query)
    for idx, url in enumerate(links):
        filename = f"{user_id}_{idx}.mp3"
        path = await download_mp3(url, filename)

        if path and os.path.exists(path):
            try:
                with open(path, "rb") as audio_file:
                    msg = await bot_instance.send_audio(
                        chat_id=CHANNEL_ID,
                        audio=audio_file,
                        caption=f"🎵 {query}"
                    )

                file_id = msg.audio.file_id
                title = msg.audio.title or query
                artist = msg.audio.performer or ""
                save_track(query, file_id, title, artist, user_id)
                os.remove(path)

                return {"file_id": file_id, "title": title, "artist": artist}
            except Exception as e:
                logging.error(f"❌ Не вдалося надіслати аудіо: {e}")

    return {}


def find_similar_query(new_query: str) -> str:
    all_queries = get_all_queries()
    best_match = None
    best_score = 0

    for saved in all_queries:
        score = fuzz.partial_ratio(new_query.lower(), saved.lower())
        if score > best_score and score >= 80:
            best_match = saved
            best_score = score

    return best_match


def rate_limiter(delay):
    user_times = {}

    def decorator(func):
        @wraps(func)
        async def wrapper(message):
            user_id = message.from_user.id
            now = asyncio.get_event_loop().time()
            if user_id in user_times and now - user_times[user_id] < delay:
                await message.reply("⏳ Занадто швидко. Зачекайте кілька секунд.")
                return
            user_times[user_id] = now
            return await func(message)
        return wrapper
    return decorator


async def setup_webhook(bot: Bot):
    global bot_instance
    bot_instance = bot