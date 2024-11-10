from telegram import Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext, Application
from dotenv import load_dotenv
from asyncio import Queue
import os
from pathlib import Path


load_dotenv()

Path("uploads").mkdir(parents=True, exist_ok=True)

async def downloader(update, context):
  fileName = update.message.document.file_name
  new_file = await update.message.effective_attachment.get_file()

  await new_file.download_to_drive(f'uploads/{fileName}')
  await update.message.reply_text(f"Файл {fileName} сохранен")
  

bot = Application.builder().token(os.environ['BOT_TOKEN']).build()
bot.add_handler(MessageHandler(filters.ALL, downloader))

