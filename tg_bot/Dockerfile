
# Используем официальный образ Python как базовый
FROM python:3.10-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    poppler-utils \
    tesseract-ocr-all \
    ffmpeg libsm6 libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы зависимостей в контейнер
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальную часть приложения в контейнер
COPY . .

# Создаем директорию для загрузок
RUN mkdir -p downloads

# Указываем команду по умолчанию (телеграм-бот)
CMD ["python", "telegram_file_bot/bot.py"]