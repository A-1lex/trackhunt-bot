import aiohttp
from bs4 import BeautifulSoup
import logging

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
}

async def search_music_links(query: str) -> list:
    all_links = []
    for parser in [parse_z1fm, parse_musify, parse_muzmo, parse_mp3party]:
        try:
            results = await parser(query)
            all_links.extend(results)
        except Exception as e:
            logging.warning(f"⚠️ Парсер {parser.__name__} не спрацював: {e}")
    return all_links


async def parse_z1fm(query: str) -> list:
    search_url = f"https://z1.fm/search?keywords={query.replace(' ', '+')}"
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        async with session.get(search_url, timeout=10) as response:
            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")
            results = []
            for a in soup.select(".track__download-btn"):
                href = a.get("href")
                if href and href.startswith("/load"):
                    results.append(f"https://z1.fm{href}")
            return results


async def parse_musify(query: str) -> list:
    search_url = f"https://musify.club/search?q={query.replace(' ', '+')}"
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        async with session.get(search_url, timeout=10) as response:
            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")
            results = []
            for a in soup.select("a.block__download"):
                href = a.get("href")
                if href:
                    results.append(f"https://musify.club{href}")
            return results


async def parse_muzmo(query: str) -> list:
    search_url = f"https://muzmo.cc/search?q={query.replace(' ', '+')}"
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        async with session.get(search_url, timeout=10) as response:
            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")
            results = []
            for a in soup.select("a.download-btn"):
                href = a.get("href")
                if href:
                    results.append(f"https://muzmo.cc{href}")
            return results


async def parse_mp3party(query: str) -> list:
    search_url = f"https://mp3party.net/search?query={query.replace(' ', '+')}"
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        async with session.get(search_url, timeout=10) as response:
            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")
            results = []
            for a in soup.select("a.download"):
                href = a.get("href")
                if href:
                    results.append(f"https://mp3party.net{href}")
            return results