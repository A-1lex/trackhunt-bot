from aiogram.types import InlineQuery, InlineQueryResultAudio
from aiogram.dispatcher import Dispatcher
from database import get_top_queries, get_cached_track
from utils import get_audio_from_google
import uuid

async def inline_query_handler(inline_query: InlineQuery):
    query = inline_query.query.strip()
    user_id = inline_query.from_user.id
    results = []

    if not query:
        top = get_top_queries(limit=5)
        for q, _ in top:
            cached = get_cached_track(q)
            if cached:
                results.append(InlineQueryResultAudio(
                    id=str(uuid.uuid4()),
                    audio_file_id=cached["file_id"],
                    title=cached["title"],
                    performer=cached["artist"]
                ))
    else:
        cached = get_cached_track(query)
        if not cached:
            cached = await get_audio_from_google(query, user_id)
        if cached:
            results.append(InlineQueryResultAudio(
                id=str(uuid.uuid4()),
                audio_file_id=cached["file_id"],
                title=cached["title"],
                performer=cached["artist"]
            ))

    await inline_query.answer(results[:10], cache_time=1, is_personal=True)


def register_inline(dp: Dispatcher):
    from aiogram.types import InlineQuery, InlineQueryResultAudio
from aiogram.dispatcher import Dispatcher
from database import get_top_queries, get_cached_track
from utils import get_audio_from_google
import uuid

async def inline_query_handler(inline_query: InlineQuery):
    query = inline_query.query.strip()
    user_id = inline_query.from_user.id
    results = []

    if not query:
        top = get_top_queries(limit=5)
        for q, _ in top:
            cached = get_cached_track(q)
            if cached:
                results.append(InlineQueryResultAudio(
                    id=str(uuid.uuid4()),
                    audio_file_id=cached["file_id"],
                    title=cached["title"],
                    performer=cached["artist"]
                ))
    else:
        cached = get_cached_track(query)
        if not cached:
            cached = await get_audio_from_google(query, user_id)
        if cached:
            results.append(InlineQueryResultAudio(
                id=str(uuid.uuid4()),
                audio_file_id=cached["file_id"],
                title=cached["title"],
                performer=cached["artist"]
            ))

    await inline_query.answer(results[:10], cache_time=1, is_personal=True)


def register_inline(dp: Dispatcher):
    dp.register_inline_handler(inline_query_handler)