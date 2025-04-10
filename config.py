import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
WEBHOOK_URL = os.getenv("WEBHOOK_URL") or "https://your-webhook-url.com/webhook"

# Папка кешованих аудіофайлів
CACHE_FOLDER = "cache"
if not os.path.exists(CACHE_FOLDER):
    os.makedirs(CACHE_FOLDER)

# Кількість треків на сторінку при пагінації
PAGE_SIZE = 10
