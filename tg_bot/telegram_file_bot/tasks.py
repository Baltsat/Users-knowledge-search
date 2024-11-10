# telegram_file_bot/tasks.py

import os
from celery_app import celery_app
from process_pdf import process_and_save
import logging
from aiogram import Bot
from dotenv import load_dotenv
import asyncio

from config import API_TOKEN

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=API_TOKEN)

@celery_app.task
def process_pdf_task(file_path: str, chat_id: int) -> str:
    try:
        logger.info(f"Начало обработки файла: {file_path}")
        json_output = process_and_save(file_path)
        logger.info(f"Завершена обработка файла: {file_path}")
        asyncio.run(send_message(chat_id, f"✅ Обработка файла `{os.path.basename(file_path)}` завершена."))
        return json_output
    except Exception as e:
        logger.error(f"Ошибка при обработке файла {file_path}: {e}")
        asyncio.run(send_message(chat_id, f"⚠️ Ошибка при обработке файла `{os.path.basename(file_path)}`."))
        return ""

async def send_message(chat_id: int, text: str):
    await bot.send_message(chat_id, text, parse_mode="HTML")