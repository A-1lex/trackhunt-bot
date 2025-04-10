import aiohttp
import logging
from bs4 import BeautifulSoup
import urllib.parse

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
}


async def search_music_links(query: str) -> list:
    """
    Пошук треків на mp3xa.fm.
    Шукає всі <a href="/...html"> посилання, які ведуть на сторінки з треками.
    """
    results = []
    encoded_query = urllib.parse.quote_plus(query)
    search_url = f"https://mp3xa.fm/search/?q={encoded_query}"

    try:
        async with aiohttp.ClientSession(headers=HEADERS) as session:
            async with session.get(search_url, timeout=10) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, "html.parser")

                    # Шукаємо всі посилання на сторінки з треками
                    for a in soup.find_all("a", href=True):
                        href = a["href"]
                        if href.startswith("/") and href.endswith(".html"):
                            full_url = f"https://mp3xa.fm{href}"
                            if full_url not in results:
                                results.append(full_url)

    except Exception as e:
        logging.warning(f"❌ Помилка при пошуку на mp3xa.fm: {e}")

    logging.info(f"🔗 Знайдено {len(results)} результатів для '{query}'")
    return results
