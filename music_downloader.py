import aiohttp
import os
import logging
from bs4 import BeautifulSoup

TEMP_DIR = "temp_downloads"
os.makedirs(TEMP_DIR, exist_ok=True)


async def extract_mp3_link(page_url: str) -> str:
    """
    Витягує пряме посилання на mp3 із сторінки треку на mp3xa.fm.
    Шукає <a itemprop="contentUrl" class="download_btn" href="...">
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(page_url, timeout=10) as resp:
                if resp.status != 200:
                    return ""

                html = await resp.text()
                soup = BeautifulSoup(html, "html.parser")

                # Знаходимо посилання на справжній mp3
                a = soup.find("a", class_="download_btn", itemprop="contentUrl", href=True)
                if a and a["href"].endswith(".mp3"):
                    return a["href"]

    except Exception as e:
        logging.error(f"❌ Помилка при вилученні mp3 з {page_url}: {e}")
    return ""


async def download_mp3(page_url: str, filename: str = "track.mp3") -> str:
    """
    Завантажує mp3-файл із витягнутого лінка.
    """
    try:
        mp3_url = await extract_mp3_link(page_url)
        if not mp3_url:
            logging.warning(f"⚠️ mp3 не знайдено на сторінці: {page_url}")
            return ""

        filepath = os.path.join(TEMP_DIR, filename)
        async with aiohttp.ClientSession() as session:
            async with session.get(mp3_url, timeout=20) as resp:
                if resp.status == 200 and "audio" in resp.headers.get("Content-Type", ""):
                    with open(filepath, "wb") as f:
                        f.write(await resp.read())
                    logging.info(f"⬇️ Завантажено: {mp3_url}")
                    return filepath
                else:
                    logging.warning(f"⚠️ Відповідь не містить mp3: {mp3_url}")
    except Exception as e:
        logging.warning(f"❌ Завантаження не вдалося: {e}")
    return ""
