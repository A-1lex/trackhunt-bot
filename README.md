# 🎧 TrackHunt Bot

TrackHunt — це Telegram-бот, який знаходить музику за назвою, виконавцем або навіть словами з пісні. Він шукає MP3 через Google на безкоштовних сайтах, кешує результати, підтримує обране та inline-пошук.

## 🚀 Можливості

- 🔍 Пошук музики через Google (zaycev.net, myzuka.club, mp3party.net)
- 📥 Завантаження MP3 та надсилання у чат
- 💾 Кешування знайдених треків
- ⭐ Обране для кожного користувача
- 📊 /popular — найпопулярніші запити
- ⚡ Inline-пошук: вводиш @назва_бота у будь-якому чаті

---

## 🛠 Як встановити локально

1. Клонуй репозиторій:
    ```bash
    git clone https://github.com/yourusername/trackhunt-bot.git
    cd trackhunt-bot
    ```

2. Створи `.env` файл:
    ```env
    TELEGRAM_BOT_TOKEN=тут_твій_токен
    CHANNEL_ID=1001234567890
    ```

3. Запусти через Docker:
    ```bash
    docker build -t trackhunt .
    docker run -it --env-file .env trackhunt
    ```

---

## ☁️ Деплой на Render

1. Завантаж цей репозиторій на GitHub
2. Переконайся, що є `render.yaml` та `Dockerfile`
3. Перейди на [Render.com](https://render.com) → New → Web Service
4. Обери репозиторій → Render сам прочитає `render.yaml`
5. Бот автоматично запуститься з Webhook

---

## 📂 Структура проєкту

. ├── bot.py # Старт бота ├── config.py # Змінні середовища ├── handlers.py # Команди та відповіді ├── inline.py # Inline-пошук ├── utils.py # Завантаження, кешування ├── google_scraper.py # Пошук MP3 через Google ├── music_downloader.py # Завантаження MP3 ├── database.py # SQLite база ├── requirements.txt # Залежності ├── Dockerfile # Збірка образу ├── render.yaml # Інструкція для Render ├── .env # Токен бота (не додається в Git) └── .gitignore # Ігнорує конфіденційні файли

---

## 📩 Контакт

Автор: [Твій нікнейм або Telegram](https://t.me/твій_нік)

