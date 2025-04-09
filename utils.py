import time
import asyncio
import logging
from functools import wraps
from aiogram import types
from config import CHANNEL_ID
from google_scraper import search_music_links
from music_downloader import download_mp3
from database import save_track, get_cached_track
import os
from fuzzywuzzy import fuzz
from collections import defaultdict, deque

# Антиспам контроль: останні запити користувача
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

            # Ліміт на кількість запитів за хвилину
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
    from bot import bot
    logging.info(f"🔍 Запит користувача {user_id}: {query}")

    cached = get_cached_track(query)
    if not cached:
        from database import get_all_queries
        all_qs = get_all_queries()
        similar = find_similar_query(query, all_qs)
        if similar:
            logging.info(f"🔄 Fuzzy-результат: {similar}")
            cached = get_cached_track(similar)

    if cached:
        logging.info(f"📦 Кешований результат для '{query}': {cached['title']} — {cached['artist']}")
        return cached

    logging.info(f"🌐 Google-пошук для: {query}")
    links = await search_music_links(query)
    for idx, link in enumerate(links):
        filename = f"track_{idx}.mp3"
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

    logging.warning(f"🚫 Результатів не знайдено для: {query}")
    return None