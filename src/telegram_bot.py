import logging
from telegram import Bot
from telegram.error import TelegramError
from telegram import InputFile
import io
import asyncio


async def send_report(df):
    import os

    token: str | None = os.getenv("TELEGRAM_TOKEN")
    chat_id: str | None = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        logging.error("TELEGRAM_TOKEN or TELEGRAM_CHAT_ID not set")
        return

    bot = Bot(token=token)
    if df.empty:
        await bot.send_message(chat_id=chat_id, text="⚠️ Нет данных для отчёта сегодня.")
        return
    message = f"📦 Отчёт Ozon FBO\nПозиции для пополнения: {len(df)}"
    try:
        await bot.send_message(chat_id=chat_id, text=message)
        csv_buffer = io.BytesIO()
        df.to_csv(csv_buffer, index=False, encoding="utf-8")
        csv_buffer.seek(0)
        document = InputFile(csv_buffer, filename="ozon_report.csv")
        await bot.send_document(chat_id=chat_id, document=document)
    except TelegramError as e:
        logging.error(f"Telegram send error: {e}")
