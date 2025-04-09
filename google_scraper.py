<<<<<<< HEAD
import aiohttp
from bs4 import BeautifulSoup
import logging

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/110.0.0.0 Safari/537.36"
}

GOOGLE_SEARCH_URL = "https://www.google.com/search?q={query}+site:zaycev.net+OR+site:myzuka.club+OR+site:mp3party.net"

async def fetch(session, url):
    try:
        async with session.get(url, headers=HEADERS, timeout=10) as response:
            if response.status == 200:
                return await response.text()
            return None
    except Exception as e:
        logging.warning(f"Помилка запиту до Google: {e}")
        return None

async def search_music_links(query):
    async with aiohttp.ClientSession() as session:
        url = GOOGLE_SEARCH_URL.format(query=query.replace(" ", "+"))
        html = await fetch(session, url)
        if not html:
            return []

        soup = BeautifulSoup(html, "html.parser")
        links = []
        for g in soup.find_all("a"):
            href = g.get("href")
            if href and ("zaycev.net" in href or "myzuka.club" in href or "mp3party.net" in href):
                if href.startswith("/url?q="):
                    clean = href.split("/url?q=")[1].split("&sa=")[0]
                    links.append(clean)

        logging.info(f"🔗 Знайдено {len(links)} посилань з Google для: {query}")
=======
import aiohttp
from bs4 import BeautifulSoup
import logging

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/110.0.0.0 Safari/537.36"
}

GOOGLE_SEARCH_URL = "https://www.google.com/search?q={query}+site:zaycev.net+OR+site:myzuka.club+OR+site:mp3party.net"

async def fetch(session, url):
    try:
        async with session.get(url, headers=HEADERS, timeout=10) as response:
            if response.status == 200:
                return await response.text()
            return None
    except Exception as e:
        logging.warning(f"Помилка запиту до Google: {e}")
        return None

async def search_music_links(query):
    async with aiohttp.ClientSession() as session:
        url = GOOGLE_SEARCH_URL.format(query=query.replace(" ", "+"))
        html = await fetch(session, url)
        if not html:
            return []

        soup = BeautifulSoup(html, "html.parser")
        links = []
        for g in soup.find_all("a"):
            href = g.get("href")
            if href and ("zaycev.net" in href or "myzuka.club" in href or "mp3party.net" in href):
                if href.startswith("/url?q="):
                    clean = href.split("/url?q=")[1].split("&sa=")[0]
                    links.append(clean)

        logging.info(f"🔗 Знайдено {len(links)} посилань з Google для: {query}")
>>>>>>> 5852130ac5d032ece869f1de256e3f764e45de32
        return links