import aiohttp
import os
import logging

TEMP_DIR = "temp_downloads"
os.makedirs(TEMP_DIR, exist_ok=True)

async def download_mp3(url: str, filename: str = "track.mp3") -> str:
    try:
        filepath = os.path.join(TEMP_DIR, filename)
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=20) as resp:
                if resp.status == 200 and "audio" in resp.headers.get("Content-Type", ""):
                    with open(filepath, "wb") as f:
                        f.write(await resp.read())
                    logging.info(f"⬇️ Успішно завантажено: {url}")
                    return filepath
    except Exception as e:
        logging.warning(f"❌ Завантаження не вдалося: {e}")
    return ""