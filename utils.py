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

    if not links:
        logging.warning(f"🚫 Результатів не знайдено для: {query}")
        await bot.send_message(user_id, "❌ Не знайдено жодного результату. Спробуйте іншу назву пісні.")
        return None

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

    logging.warning(f"❌ Не вдалося обробити жодне посилання для: {query}")
    await bot.send_message(user_id, "⚠️ Пісню не вдалося завантажити. Спробуйте іншу.")
    return None
