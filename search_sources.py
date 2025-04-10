import aiohttp
from bs4 import BeautifulSoup
import logging

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
}

async def search_music_links(query: str) -> list:
    all_links = []
    for parser in [parse_z1fm, parse_musify, parse_muzmo, parse_mp3party, parse_hitmotop]:
        try:
            results = await parser(query)
            logging.info(f"🔍 {parser.__name__} знайшов {len(results)} посилань")
            all_links.extend(results)
        except Exception as e:
            logging.warning(f"⚠️ Парсер {parser.__name__} не спрацював: {e}")
    logging.info(f"🔗 Загалом зібрано {len(all_links)} посилань для: {query}")
    return all_links


async def parse_z1fm(query: str) -> list:
    search_url = f"https://z1.fm/search?keywords={query.replace(' ', '+')}"
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        async with session.get(search_url, timeout=10) as response:
            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")
            return [f"https://z1.fm{a.get('href')}" for a in soup.select(".track__download-btn") if a.get("href")]


async def parse_musify(query: str) -> list:
    search_url = f"https://musify.club/search?q={query.replace(' ', '+')}"
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        async with session.get(search_url, timeout=10) as response:
            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")
            return [f"https://musify.club{a.get('href')}" for a in soup.select("a.block__download") if a.get("href")]


async def parse_muzmo(query: str) -> list:
    search_url = f"https://muzmo.cc/search?q={query.replace(' ', '+')}"
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        async with session.get(search_url, timeout=10) as response:
            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")
            return [f"https://muzmo.cc{a.get('href')}" for a in soup.select("a.download-btn") if a.get("href")]


async def parse_mp3party(query: str) -> list:
    search_url = f"https://mp3party.net/search?query={query.replace(' ', '+')}"
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        async with session.get(search_url, timeout=10) as response:
            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")
            return [f"https://mp3party.net{a.get('href')}" for a in soup.select("a.download") if a.get("href")]


async def parse_hitmotop(query: str) -> list:
    search_url = f"https://ru.hitmotop.com/search?q={query.replace(' ', '+')}"
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        async with session.get(search_url, timeout=10) as response:
            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")
            return [f"https://ru.hitmotop.com{a.get('href')}" for a in soup.select(".track__download-btn") if a.get("href")]