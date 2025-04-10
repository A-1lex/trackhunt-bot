import aiohttp
from bs4 import BeautifulSoup
import logging

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
}

async def search_music_links(query: str) -> list:
    all_links = []
    for parser in [parse_muzmix, parse_muzzofor, parse_muzon]:
        try:
            results = await parser(query)
            logging.info(f"🔍 {parser.__name__} знайшов {len(results)} посилань")
            all_links.extend(results)
        except Exception as e:
            logging.warning(f"⚠️ Парсер {parser.__name__} не спрацював: {e}")
    logging.info(f"🔗 Загалом зібрано {len(all_links)} посилань для: {query}")
    return all_links


async def parse_muzmix(query: str) -> list:
    search_url = f"https://muzmix.net/search?q={query.replace(' ', '+')}"
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        async with session.get(search_url, timeout=10) as resp:
            html = await resp.text()
            soup = BeautifulSoup(html, "html.parser")
            links = []
            for div in soup.select("div.music-content"):
                a = div.find("a", class_="btn-download")
                if a and a.get("href"):
                    links.append(f"https://muzmix.net{a['href']}")
            return links


async def parse_muzzofor(query: str) -> list:
    search_url = f"https://muzzofor.me/index.php?do=search&subaction=search&story={query.replace(' ', '+')}"
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        async with session.get(search_url, timeout=10) as resp:
            html = await resp.text()
            soup = BeautifulSoup(html, "html.parser")
            links = []
            for a in soup.select("a.short-poster__download"):
                if a.get("href"):
                    links.append(a["href"])
            return links


async def parse_muzon(query: str) -> list:
    search_url = f"https://muzon.fm/search/{query.replace(' ', '+')}"
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        async with session.get(search_url, timeout=10) as resp:
            html = await resp.text()
            soup = BeautifulSoup(html, "html.parser")
            links = []
            for a in soup.select("a.music-download"):
                if a.get("href"):
                    links.append(f"https://muzon.fm{a['href']}")
            return links
