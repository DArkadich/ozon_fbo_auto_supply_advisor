# src/utils.py
import os
import json
import logging


def load_config(path: str | None = None) -> dict:
    """Загружает конфиг из JSON-файла (по умолчанию config.json)."""
    try:
        file_path: str = (
            path or os.getenv("CONFIG_PATH", "config.json") or "config.json"
        )
        if not os.path.exists(file_path):
            logging.warning(f"Config file not found: {file_path}")
            return {}
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading config: {e}")
        return {}


def setup_logging() -> logging.Logger:
    """Настраивает логирование и возвращает logger."""
    logger = logging.getLogger("ozon_fbo_advisor")
    if not logger.handlers:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[logging.StreamHandler()],
        )
    return logger
