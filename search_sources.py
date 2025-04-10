import aiohttp
import logging
from bs4 import BeautifulSoup
import urllib.parse

# Робочі сайти, які ми перевіряємо через Google
SEARCH_SITES = [
    "mp3xa.fm",
    "mp3uk.net"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
}


async def search_music_links(query: str) -> list:
    """
    Шукає сторінки з mp3 на mp3xa.fm і mp3uk.net через Google з покращеним запитом.
    """
    results = []

    for site in SEARCH_SITES:
        # ✅ Покращений запит: точна фраза + фільтр типу файлу
        search_query = f'"{query}" site:{site} filetype:mp3'
        encoded_query = urllib.parse.quote_plus(search_query)
        search_url = f"https://www.google.com/search?q={encoded_query}"

        try:
            async with aiohttp.ClientSession(headers=HEADERS) as session:
                async with session.get(search_url, timeout=10) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, "html.parser")
                        for a in soup.find_all("a"):
                            href = a.get("href", "")
                            if site in href and "/url?q=" in href:
                                clean_url = href.split("/url?q=")[1].split("&")[0]
                                if clean_url not in results:
                                    results.append(clean_url)
        except Exception as e:
            logging.warning(f"🔍 Помилка запиту до Google для {site}: {e}")

    logging.info(f"🔗 Знайдено {len(results)} посилань для: {query}")
    return results
