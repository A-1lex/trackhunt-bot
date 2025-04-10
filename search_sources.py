import aiohttp
from bs4 import BeautifulSoup
import logging

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
}

async def search_music_links(query: str) -> list:
    all_links = []
    for parser in [parse_z3fm, parse_mp3wr, parse_meloua, parse_sefon, parse_drivemusic]:
        try:
            results = await parser(query)
            logging.info(f"🔍 {parser.__name__} знайшов {len(results)} посилань")
            all_links.extend(results)
        except Exception as e:
            logging.warning(f"⚠️ Парсер {parser.__name__} не спрацював: {e}")
    logging.info(f"🔗 Загалом зібрано {len(all_links)} посилань для: {query}")
    return all_links


async def parse_z3fm(query: str) -> list:
    search_url = f"https://z3.fm/mp3/search?keywords={query.replace(' ', '+')}"
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        async with session.get(search_url, timeout=10) as resp:
            html = await resp.text()
            soup = BeautifulSoup(html, "html.parser")
            links = []
            for a in soup.find_all("a", class_="download"):
                href = a.get("href")
                if href:
                    links.append(f"https://z3.fm{href}")
            return links


async def parse_mp3wr(query: str) -> list:
    search_url = f"https://mp3wr.com/?s={query.replace(' ', '+')}"
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        async with session.get(search_url, timeout=10) as resp:
            html = await resp.text()
            soup = BeautifulSoup(html, "html.parser")
            links = []
            for a in soup.find_all("a", class_="btn-download"):  # Змінили селектор
                href = a.get("href")
                if href:
                    links.append(href)
            return links


async def parse_meloua(query: str) -> list:
    search_url = f"https://meloua.com/?s={query.replace(' ', '+')}"
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        async with session.get(search_url, timeout=10) as resp:
            html = await resp.text()
            soup = BeautifulSoup(html, "html.parser")
            links = []
            for a in soup.find_all("a", class_="btn-download"):  # Змінили селектор
                href = a.get("href")
                if href:
                    links.append(href)
            return links


async def parse_sefon(query: str) -> list:
    search_url = f"https://sefon.pro/?s={query.replace(' ', '+')}"
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        async with session.get(search_url, timeout=10) as resp:
            html = await resp.text()
            soup = BeautifulSoup(html, "html.parser")
            links = []
            for a in soup.find_all("a", class_="download__btn"):  # Змінили селектор
                href = a.get("href")
                if href:
                    links.append(href)
            return links


async def parse_drivemusic(query: str) -> list:
    search_url = f"https://drivemusic.club/?s={query.replace(' ', '+')}"
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        async with session.get(search_url, timeout=10) as resp:
            html = await resp.text()
            soup = BeautifulSoup(html, "html.parser")
            links = []
            for a in soup.find_all("a", class_="download__btn"):  # Змінили селектор
                href = a.get("href")
                if href:
                    links.append(href)
            return links