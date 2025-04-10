import aiohttp
import logging
from bs4 import BeautifulSoup
import urllib.parse

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
}


async def search_music_links(query: str) -> list:
    """
    Пошук треків на mp3xa.fm. Парсить кнопки "Скачать" з класом download_btn.
    Повертає список посилань на сторінки з піснями.
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

                    for a in soup.find_all("a", class_="download_btn", href=True):
                        href = a["href"]
                        if href.startswith("/"):
                            full_url = f"https://mp3xa.fm{href}"
                            if full_url not in results:
                                results.append(full_url)

    except Exception as e:
        logging.warning(f"❌ Помилка при пошуку на mp3xa.fm: {e}")

    logging.info(f"🔗 Знайдено {len(results)} результатів для '{query}'")
    return results
