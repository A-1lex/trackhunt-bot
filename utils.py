import time
from aiogram import types
from collections import defaultdict, deque
from functools import wraps

# Антиспам контроль: останні запити користувача
user_requests = defaultdict(lambda: deque(maxlen=20))

def rate_limiter(seconds: int = 2, max_per_minute: int = 10):
    user_timestamps = {}

    def decorator(func):
        @wraps(func)
        async def wrapped(message: types.Message, *args, **kwargs):
            user_id = message.from_user.id
            now = time.time()

            # Перевірка затримки між запитами
            if user_id in user_timestamps and (now - user_timestamps[user_id]) < seconds:
                await message.reply("⏳ Занадто швидко. Зачекайте кілька секунд.")
                return

            # Ліміт за хвилину
            user_requests[user_id].append(now)
            recent = [t for t in user_requests[user_id] if now - t < 60]
            if len(recent) > max_per_minute:
                await message.reply("🚫 Забагато запитів. Зачекайте трохи.")
                return

            user_timestamps[user_id] = now
            return await func(message, *args, **kwargs)

        return wrapped
    return decorator
