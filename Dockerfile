# Вихідний образ
FROM python:3.11-slim

# Встановлення залежностей
WORKDIR /app
COPY . /app

# Встановлення залежностей із requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Створення папок для логів і тимчасових завантажень
RUN mkdir -p logs temp_downloads

# Стартова команда (використовує webhook)
CMD ["python", "bot.py"]
