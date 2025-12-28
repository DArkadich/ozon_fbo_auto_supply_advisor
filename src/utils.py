import os
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

def setup_logging():
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    handler = RotatingFileHandler(f"{log_dir}/app.log", maxBytes=5_000_000, backupCount=3)
    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", "INFO"),
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[handler, logging.StreamHandler()]
    )

def load_config():
    load_dotenv()
    required_vars = [
        "OZON_API_KEY", "OZON_CLIENT_ID", "TELEGRAM_TOKEN", 
        "TELEGRAM_CHAT_ID", "GOOGLE_SA_PATH", "GOOGLE_SHEET_NAME"
    ]
    missing = [v for v in required_vars if not os.getenv(v)]
    if missing:
        raise ValueError(f"❌ Missing environment variables: {missing}")
