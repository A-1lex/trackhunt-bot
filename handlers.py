# -*- coding: utf-8 -*-
from aiogram import Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils import rate_limiter, get_audio_from_google
from database import get_top_queries, save_favorite, get_favorites
import logging


@rate_limiter(3)
async def handle_message(message: types.Message):
    query = message.text.strip()
    track = await get_audio_from_google(query, message.from_user.id)

    if not track:
        await message.reply("Не знайдено результатів. Спробуйте інший запит.")
        return

    keyboard = InlineKeyboardMarkup().add(
        InlineKeyboardButton("⭐ Додати в обране", callback_data=f"fav:{track['file_id']}")
    )

    await message.answer_audio(
        audio=track["file_id"],
        title=track["title"],
        performer=track["artist"],
        caption=f"🎵 {track['title']} — {track['artist']}",
        reply_markup=keyboard
    )


async def popular_command(message: types.Message):
    top = get_top_queries(limit=10)
    if not top:
        await message.reply("Немає даних для статистики.")
        return

    response = "🔥 Найпопулярніші запити:\n\n"
    for i, row in enumerate(top, 1):
        response += f"{i}. {row[0]} — {row[1]} раз(ів)\n"
    await message.reply(response)


async def favorites_command(message: types.Message):
    favs = get_favorites(message.from_user.id)
    if not favs:
        await message.reply("У вас немає обраних треків.")
        return

    for row in favs:
        await message.answer_audio(
            audio=row[0],
            title=row[1],
            performer=row[2],
            caption=f"🎵 {row[1]} — {row[2]}"
        )


async def callback_handler(callback: types.CallbackQuery):
    data = callback.data
    if data.startswith("fav:"):
        file_id = data.split(":")[1]
        user_id = callback.from_user.id
        message = callback.message
        title = getattr(message.audio, "title", "") or ""
        performer = getattr(message.audio, "performer", "") or ""
        save_favorite(user_id, file_id, title, performer)
        logging.info(f"⭐ {user_id} додав в обране: {title} — {performer}")
        await callback.answer("✅ Додано в обране")


# ✅ Команда для отримання numeric channel ID
async def get_channel_id(message: types.Message):
    if message.forward_from_chat:
        await message.reply(f"📌 Chat ID: `{message.forward_from_chat.id}`", parse_mode="Markdown")
    else:
        await message.reply("ℹ️ Перешли мені повідомлення з каналу.")


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(handle_message, content_types=types.ContentType.TEXT)
    dp.register_message_handler(popular_command, commands=["popular"])
    dp.register_message_handler(favorites_command, commands=["favorites"])
    dp.register_callback_query_handler(callback_handler, lambda c: c.data and c.data.startswith("fav:"))
    dp.register_message_handler(get_channel_
