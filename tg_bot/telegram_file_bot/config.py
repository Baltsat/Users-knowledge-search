import os
from dotenv import load_dotenv

# Должен хендлить все загрузки файлов и сохранять в себя
# После этого прогоняем по пайплайну, дальше в опенсерч

load_dotenv()

# Bot token (from @BotFather in Telegram)
API_TOKEN = os.environ['BOT_TOKEN']
DOWNLOAD_PATH = os.getenv("DOWNLOAD_PATH", "downloads")  # Путь для сохранения файлов
OPENSEARCH_HOST = os.environ['OPENSEARCH_HOST']