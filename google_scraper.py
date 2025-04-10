import asyncio
from search_sources import search_music_links as new_search_music_links

async def search_music_links(query: str):
    """
    DEPRECATED: Будь ласка, використовуйте функцію з модуля search_sources.py.
    """
    return await new_search_music_links(query)
