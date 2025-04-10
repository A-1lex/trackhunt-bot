from aiogram import Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils import get_track, rate_limiter
from database import get_favorites, save_favorite, get_top_queries
import logging


async def start_handler(message: types.Message):
    await message.reply("Привіт! 👋 Введи назву пісні або виконавця, щоб я міг її знайти.")


async def getid_handler(message: types.Message):
    if message.forward_from_chat:
        await message.reply(f"📌 Chat ID: `{message.forward_from_chat.id}`", parse_mode="Markdown")
    else:
        await message.reply("ℹ️ Перешли мені повідомлення з каналу, і я скажу тобі його Chat ID.")


async def popular_handler(message: types.Message):
    top = get_top_queries()
    if not top:
        await message.reply("Поки немає популярних запитів.")
        return

    result = "🔥 Найпопулярніші запити:\n\n"
    for i, (query, count) in enumerate(top, start=1):
        result += f"{i}. {query} — {count} раз(ів)\n"
    await message.reply(result)


async def favorites_handler(message: types.Message):
    favs = get_favorites(message.from_user.id)
    if not favs:
        await message.reply("У вас поки немає обраних треків.")
        return

    for file_id, title, artist in favs:
        await message.answer_audio(
            audio=file_id,
            title=title,
            performer=artist,
            caption=f"🎵 {title} — {artist}"
        )


async def callback_handler(callback: types.CallbackQuery):
    data = callback.data
    if data.startswith("fav:"):
        file_id = data.split(":")[1]
        user_id = callback.from_user.id
        title = callback.message.audio.title if callback.message.audio else ""
        performer = callback.message.audio.performer if callback.message.audio else ""
        save_favorite(user_id, file_id, title, performer)
        await callback.answer("✅ Додано в обране")


@rate_limiter(3)
async def search_handler(message: types.Message):
    query = message.text.strip()
    logging.info(f"🔎 Запит користувача: {query}")
    track = await get_track(query, message.from_user.id)

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


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=["start"])
    dp.register_message_handler(getid_handler, commands=["getid"])
    dp.register_message_handler(popular_handler, commands=["popular"])
    dp.register_message_handler(favorites_handler, commands=["favorites"])
    dp.register_callback_query_handler(callback_handler, lambda c: c.data and c.data.startswith("fav:"))
    dp.register_message_handler(search_handler, content_types=types.ContentType.TEXT)

