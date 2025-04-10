import aiohttp
import logging
from bs4 import BeautifulSoup
import urllib.parse

# Актуальні сайти для пошуку музики (Free Music Archive, Jamendo, Internet Archive)
SEARCH_SITES = [
    "freemusicarchive.org",
    "jamendo.com",
    "archive.org/details/audio"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
}

async def search_music_links(query: str):
    """
    Шукає посилання на MP3-файли через Google для запиту query,
    обмежуючи пошук зазначеними сайтами з актуальних джерел.
    """
    results = []
    for site in SEARCH_SITES:
        search_query = f"site:{site} {query} mp3"
        encoded_query = urllib.parse.quote_plus(search_query)
        search_url = f"https://www.google.com/search?q={encoded_query}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(search_url, headers=HEADERS, timeout=10) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, "html.parser")
                        for a in soup.find_all("a"):
                            href = a.get("href")
                            if href and site in href:
                                # Обробка посилань у форматі /url?q=<url>&sa=...
                                if href.startswith("/url?q="):
                                    clean = href.split("/url?q=")[1].split("&sa=")[0]
                                    if clean not in results:
                                        results.append(clean)
                                else:
                                    if href not in results:
                                        results.append(href)
                    else:
                        logging.warning(f"Пошукова система повернула статус {response.status} для сайту {site}")
        except Exception as e:
            logging.warning(f"Помилка запиту до Google для {site}: {e}")
    logging.info(f"🔎 Знайдено {len(results)} посилань для запиту: '{query}'")
    return results
