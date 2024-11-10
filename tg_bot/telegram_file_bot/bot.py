
import logging
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, Document, PhotoSize
import aiohttp
from config import API_TOKEN, DOWNLOAD_PATH
from pipelines import find
from process_pdf import process_and_save
from aiogram.types import FSInputFile

from seed_by_file import seed_by_file

# ---------------------- Configuration ----------------------

# Параметры обработки PDF
# (Настраиваются внутри processing.py)

# Убедитесь, что директория для загрузок существует
os.makedirs(DOWNLOAD_PATH, exist_ok=True)

# ---------------------- Logging Setup ----------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# ---------------------- Bot Initialization ----------------------

bot = Bot(token=API_TOKEN, parse_mode="HTML")
dp = Dispatcher()

# ---------------------- Helper Functions ----------------------


async def download_file(bot: Bot, file_id: str, file_path: str) -> str:
    """
    Загружает файл с Telegram серверов и сохраняет его локально.

    :param bot: Экземпляр Telegram бота.
    :param file_id: Идентификатор файла в Telegram.
    :param file_path: Путь для сохранения файла.
    :return: Путь к сохраненному файлу или пустая строка при ошибке.
    """
    try:
        # Получение объекта файла из Telegram
        file = await bot.get_file(file_id)
        file_url = f"https://api.telegram.org/file/bot{API_TOKEN}/{file.file_path}"

        logger.info(f"Скачивание файла с {file_url} в {file_path}")

        async with aiohttp.ClientSession() as session:
            async with session.get(file_url) as response:
                if response.status == 200:
                    with open(file_path, 'wb') as f:
                        while True:
                            chunk = await response.content.read(1024)
                            if not chunk:
                                break
                            f.write(chunk)
                    logger.info(f"Файл сохранен в {file_path}")
                    return file_path
                else:
                    logger.error(f"Не удалось скачать файл: HTTP {response.status}")
                    return ""
    except Exception as e:
        logger.error(f"Произошла ошибка при скачивании файла: {e}")
        return ""

# ---------------------- Handlers ----------------------


@dp.message(Command(commands=["start", "help"]))
async def send_welcome(message: Message):
    """
    Ответ на команды /start и /help приветственным сообщением.
    """
    welcome_text = (
        "Привет! 👋\n\n"
        "Отправьте мне PDF файл, и я обработаю его для вас. 📄"
    )
    await message.answer(welcome_text)

@dp.message(F.text)
async def handle_other_messages(message: Message):
    """
    Handles all other messages.
    """

    found = find(message.text)
    logger.info("Found", found)

    for card in found:
        title = card['fields']['fileName'][0]
        description = card['fields']['description'][0]
        slide = card['fields']['slide'][0]
        await message.answer(f'Файл: {title}\nСлайд: {slide}\nОписание: {description}')
        
        # TODO FIX IT
        # file_path = './content/0.pdf'
        file_path = f'./content/{title}'
        file = FSInputFile(file_path)
        await bot.send_document(chat_id=message.chat.id, document=file)


@dp.message(F.document)
async def handle_document(message: Message):
    """
    Обрабатывает входящие документы (файлы).
    """
    document: Document = message.document
    file_id = document.file_id
    filename = document.file_name or f"document_{file_id}"
    file_extension = os.path.splitext(filename)[1].lower()

    if file_extension != '.pdf':
        await message.answer("⚠️ Пожалуйста, отправьте PDF файл.")
        return

    sanitized_filename = f"{file_id}{file_extension}"
    file_path = os.path.join(DOWNLOAD_PATH, sanitized_filename)

    logger.info(f"Получен документ: {filename} (ID: {file_id})")

    saved_path = await download_file(bot, file_id, file_path)

    if saved_path:
        await message.answer("📄 PDF файл был успешно сохранен и отправлен на обработку.")
        logger.info(f"Начало обработки файла: {file_path}")
        json_output = process_and_save(file_path)
        seed_by_file(f'{sanitized_filename}_processed.json', DOWNLOAD_PATH)
        logger.info(f"Завершена обработка файла: {file_path}")
    else:
        await message.answer("⚠️ Не удалось сохранить PDF файл.")


@dp.message(F.photo)
async def handle_photo(message: Message):
    """
    Обрабатывает входящие фотографии.
    """
    photo_sizes: list[PhotoSize] = message.photo
    # Получение фото наивысшего разрешения
    photo = photo_sizes[-1]
    file_id = photo.file_id
    file_extension = '.jpg'  # Обычно фотографии JPEG
    sanitized_filename = f"{file_id}{file_extension}"
    file_path = os.path.join(DOWNLOAD_PATH, sanitized_filename)

    logger.info(f"Получено фото: ID {file_id}")

    saved_path = await download_file(bot, file_id, file_path)

    if saved_path:
        await message.answer("📸 Фото было успешно сохранено!")
    else:
        await message.answer("⚠️ Не удалось сохранить фото.")


@dp.message()
async def handle_other_messages(message: Message):
    """
    Обрабатывает все остальные сообщения.
    """
    await message.answer("🤔 Пожалуйста, отправьте PDF файл для обработки.")

# ---------------------- Startup and Shutdown ----------------------


async def on_startup():
    logger.info("Бот запускается...")


async def on_shutdown():
    await bot.session.close()
    logger.info("Бот выключен.")


# ---------------------- Main ----------------------

if __name__ == '__main__':
    try:
        dp.startup.register(on_startup)
        dp.shutdown.register(on_shutdown)
        logger.info("Запуск бота...")
        dp.run_polling(bot, allow_updates=True)
    except (KeyboardInterrupt, SystemExit):
        logger.error("Бот остановлен!")