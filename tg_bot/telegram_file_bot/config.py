import os
from dotenv import load_dotenv

# Должен хендлить все загрузки файлов и сохранять в себя
# После этого прогоняем по пайплайну, дальше в опенсерч

load_dotenv()

# Bot token (from @BotFather in Telegram)
API_TOKEN = os.environ['BOT_TOKEN']
DOWNLOAD_PATH = os.getenv("DOWNLOAD_PATH", "downloads")  # Путь для сохранения файлов

# Получение конфигураций из переменных окружения
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0")