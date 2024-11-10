import os
from celery import Celery
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()

# Получение конфигураций из переменных окружения
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0")

# Создание экземпляра Celery
celery_app = Celery(
    'telegram_file_bot',
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
)

# Автоматическое обнаружение задач в пакете 'telegram_file_bot'
celery_app.autodiscover_tasks(['telegram_file_bot'])