import logging
from telegram import Bot
from telegram.error import TelegramError
import io, asyncio

async def send_report(df):
    import os
    bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if df.empty:
        await bot.send_message(chat_id=chat_id, text="⚠️ Нет данных для отчёта сегодня.")
        return
    message = f"📦 Отчёт Ozon FBO\nПозиции для пополнения: {len(df)}"
    try:
        await bot.send_message(chat_id=chat_id, text=message)
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)
        await bot.send_document(chat_id=chat_id, document=("ozon_report.csv", csv_buffer))
    except TelegramError as e:
        logging.error(f"Telegram send error: {e}")
