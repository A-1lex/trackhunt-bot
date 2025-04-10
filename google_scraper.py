import aiohttp
import logging
from bs4 import BeautifulSoup

SEARCH_SITES = ["z1.fm", "musify.club", "mymp3.red", "muzmo.cc", "mp3party.net"]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
}

async def search_music_links(query: str):
    results = []
    for site in SEARCH_SITES:
        search_query = f"site:{site} {query} mp3"
        search_url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"

        try:
            async with aiohttp.ClientSession(headers=HEADERS) as session:
                async with session.get(search_url, timeout=10) as response:
                    if response.status == 200:
                        text = await response.text()
                        soup = BeautifulSoup(text, "html.parser")
                        for a in soup.select("a"):
                            href = a.get("href")
                            if href and site in href:
                                clean_url = extract_url(href)
                                if clean_url and clean_url not in results:
                                    results.append(clean_url)
        except Exception as e:
            logging.warning(f"🌐 Помилка запиту до Google для {site}: {e}")

    logging.info(f"🔗 Знайдено {len(results)} посилань з Google для: {query}")
    return results


def extract_url(href):
    import re
    match = re.search(r"url\?q=(.*?)&", href)
    return match.group(1) if match else None
