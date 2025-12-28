import asyncio, logging, schedule, time, os
from utils import setup_logging, load_config
from ozon_api import get_stocks, get_recommendations
from logic import prepare_report
from telegram_bot import send_report
from google_sheets import upload_to_sheet

async def async_job():
    try:
        logging.info("Starting daily Ozon FBO job...")
        stocks, recos = get_stocks(), get_recommendations()
        if not stocks or not recos:
            logging.warning("Empty data received — skipping this cycle.")
            return
        df = prepare_report(stocks, recos)
        await send_report(df)
        upload_to_sheet(df)
        logging.info("✅ Job finished successfully.")
    except Exception as e:
        logging.exception(f"Critical job error: {e}")

def job():
    asyncio.run(async_job())

def main():
    setup_logging()
    load_config()
    update_time = os.getenv("UPDATE_TIME", "09:00")
    schedule.every().day.at(update_time).do(job)
    logging.info(f"Scheduler started, daily run at {update_time}")
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()
