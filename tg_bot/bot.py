import logging
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, Document, PhotoSize
import aiohttp
import asyncio

from tg_bot.config import API_TOKEN

# ---------------------- Configuration ----------------------

DOWNLOAD_PATH = 'downloads'  # Directory to save downloaded files

# Ensure the download directory exists
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
    Downloads a file from Telegram servers and saves it locally.

    :param bot: The Telegram bot instance.
    :param file_id: The file_id of the Telegram file.
    :param file_path: The path where the file will be saved.
    :return: The path to the saved file.
    """
    try:
        # Get the file object from Telegram
        file = await bot.get_file(file_id)
        file_url = f"https://api.telegram.org/file/bot{API_TOKEN}/{file.file_path}"

        logger.info(f"Downloading file from {file_url} to {file_path}")

        async with aiohttp.ClientSession() as session:
            async with session.get(file_url) as response:
                if response.status == 200:
                    with open(file_path, 'wb') as f:
                        while True:
                            chunk = await response.content.read(1024)
                            if not chunk:
                                break
                            f.write(chunk)
                    logger.info(f"File saved to {file_path}")
                    return file_path
                else:
                    logger.error(f"Failed to download file: HTTP {response.status}")
                    return ""
    except Exception as e:
        logger.error(f"An error occurred while downloading the file: {e}")
        return ""

# ---------------------- Handlers ----------------------

@dp.message(Command(commands=["start", "help"]))
async def send_welcome(message: Message):
    """
    Responds to /start and /help commands with a welcome message.
    """
    welcome_text = (
        "Hello! 👋\n\n"
        "Send me any file or photo, and I'll store it for you. 📁📸"
    )
    await message.answer(welcome_text)

@dp.message(F.document)
async def handle_document(message: Message):
    """
    Handles incoming documents (files).
    """
    document: Document = message.document
    file_id = document.file_id
    filename = document.file_name or f"document_{file_id}"
    file_extension = os.path.splitext(filename)[1]
    sanitized_filename = f"{file_id}{file_extension}"
    file_path = os.path.join(DOWNLOAD_PATH, sanitized_filename)

    logger.info(f"Received document: {filename} (ID: {file_id})")

    saved_path = await download_file(bot, file_id, file_path)

    if saved_path:
        await message.answer(f"📄 Document '{filename}' has been saved successfully!")
    else:
        await message.answer("⚠️ Failed to save the document.")

@dp.message(F.photo)
async def handle_photo(message: Message):
    """
    Handles incoming photos.
    """
    photo_sizes: list[PhotoSize] = message.photo
    # Get the highest resolution photo
    photo = photo_sizes[-1]
    file_id = photo.file_id
    file_extension = '.jpg'  # Telegram photos are typically JPEG
    sanitized_filename = f"{file_id}{file_extension}"
    file_path = os.path.join(DOWNLOAD_PATH, sanitized_filename)

    logger.info(f"Received photo: ID {file_id}")

    saved_path = await download_file(bot, file_id, file_path)

    if saved_path:
        await message.answer("📸 Photo has been saved successfully!")
    else:
        await message.answer("⚠️ Failed to save the photo.")

@dp.message()
async def handle_other_messages(message: Message):
    """
    Handles all other messages.
    """
    await message.answer("🤔 Please send a document or a photo to store.")

# ---------------------- Startup and Shutdown ----------------------

async def on_startup():
    logger.info("Bot is starting...")

async def on_shutdown():
    await bot.session.close()
    logger.info("Bot has been shut down.")

# ---------------------- Main ----------------------

if __name__ == '__main__':
    try:
        dp.startup.register(on_startup)
        dp.shutdown.register(on_shutdown)
        logger.info("Starting polling...")
        dp.run_polling(bot, allow_updates=True)
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
