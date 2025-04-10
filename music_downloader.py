import aiohttp
import os
import logging
from bs4 import BeautifulSoup

TEMP_DIR = "temp_downloads"
os.makedirs(TEMP_DIR, exist_ok=True)


async def extract_mp3_link(page_url: str) -> str:
    """
    Видобуває пряме mp3-посилання зі сторінок mp3xa.fm або mp3uk.net.
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(page_url, timeout=10) as resp:
                if resp.status != 200:
                    return ""

                html = await resp.text()
                soup = BeautifulSoup(html, "html.parser")

                # mp3xa.fm → <source src="..." type="audio/mpeg">
                source = soup.find("source", {"src": True})
                if source and source["src"].endswith(".mp3"):
                    return source["src"]

                # mp3uk.net → <a class="download-btn" href="...mp3">
                for a in soup.find_all("a", href=True):
                    href = a["href"]
                    if href.endswith(".mp3"):
                        return href

    except Exception as e:
        logging.error(f"❌ Помилка при видобуванні mp3 з {page_url}: {e}")
    return ""


async def download_mp3(page_url: str, filename: str = "track.mp3") -> str:
    """
    Завантажує mp3-файл із посилання на сторінку, де знаходиться трек.
    """
    try:
        mp3_link = await extract_mp3_link(page_url)
        if not mp3_link:
            logging.warning(f"⚠️ Не знайдено mp3 на сторінці: {page_url}")
            return ""

        filepath = os.path.join(TEMP_DIR, filename)
        async with aiohttp.ClientSession() as session:
            async with session.get(mp3_link, timeout=20) as resp:
                if resp.status == 200 and "audio" in resp.headers.get("Content-Type", ""):
                    with open(filepath, "wb") as f:
                        f.write(await resp.read())
                    logging.info(f"⬇️ Завантажено: {mp3_link}")
                    return filepath
                else:
                    logging.warning(f"⚠️ Невірна відповідь при спробі завантаження: {mp3_link}")
    except Exception as e:
        logging.warning(f"❌ Завантаження не вдалося: {e}")
    return ""
