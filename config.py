import os

BOT_TOKEN = "8046318140:AAG7FPa1qmJc_3j7Nk63PdgT0N97tTRP7FI"
CHANNEL_ID = 1002559409885

DB_PATH = "app/database.db"

# URL для вебхуку – встановлюється через змінні середовища або використовується значення за замовчуванням
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://trackhunt-bot.onrender.com/webhook")
