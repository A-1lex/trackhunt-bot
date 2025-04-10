import aiohttp
import os
import logging
from bs4 import BeautifulSoup

TEMP_DIR = "cache"
os.makedirs(TEMP_DIR, exist_ok=True)

async def download_mp3(url: str, filename: str = "track.mp3") -> str:
    try:
        real_mp3_link = await extract_mp3_link(url)
        if not real_mp3_link:
            logging.warning(f"❌ Не вдалося знайти mp3 на сторінці: {url}")
            return ""

        filepath = os.path.join(TEMP_DIR, filename)
        async with aiohttp.ClientSession() as session:
            async with session.get(real_mp3_link, timeout=20) as resp:
                if resp.status == 200 and "audio" in resp.headers.get("Content-Type", ""):
                    with open(filepath, "wb") as f:
                        f.write(await resp.read())
                    logging.info(f"⬇ Успішно завантажено: {real_mp3_link}")
                    return filepath
    except Exception as e:
        logging.warning(f"⚠️ Завантаження не вдалося: {e}")
    return ""


async def extract_mp3_link(page_url: str) -> str:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(page_url, timeout=10) as resp:
                html = await resp.text()
                soup = BeautifulSoup(html, "html.parser")
                for a in soup.find_all("a"):
                    href = a.get("href", "")
                    if href.endswith(".mp3"):
                        return href
    except Exception as e:
        logging.error(f"🔍 Не вдалося отримати mp3 зі сторінки: {e}")
    return ""
