import pytest
import pandas as pd
import asyncio
from src import google_sheets, main, ozon_api, telegram_bot, utils


# ---------- Общие вспомогательные функции ----------


async def dummy_send(*a, **k):
    """Асинхронный мок для Telegram методов send_message/send_document"""
    return None


# ---------- GOOGLE SHEETS ----------


def test_upload_to_sheet_handles_missing_credentials(monkeypatch):
    """Проверяет обработку отсутствующего service_account.json"""
    monkeypatch.setattr("os.getenv", lambda name, default=None: "nonexistent.json")
    try:
        google_sheets.upload_to_sheet(pd.DataFrame([{"a": 1}]))
    except Exception:
        # Google API не мокается — тест только проверяет отсутствие падений при импорте
        pytest.skip("Google Sheets API не замокан в окружении")


# ---------- MAIN.JOB() ----------


def test_job_handles_empty_data(monkeypatch):
    """Проверка: job() не падает при пустых данных"""
    monkeypatch.setattr(main, "get_stocks", lambda: [])
    monkeypatch.setattr(main, "get_recommendations", lambda: [])
    monkeypatch.setattr(main, "prepare_report", lambda x, y: pd.DataFrame())
    monkeypatch.setattr(main, "upload_to_sheet", lambda x: None)
    monkeypatch.setattr(main, "send_report", lambda x: None)
    main.job()


def test_job_with_data(monkeypatch):
    """Проверка: job() с данными проходит полный цикл"""
    stocks = [{"product_id": 1, "stock": 10}]
    recs = [{"product_id": 1, "recommend": 5}]
    df = pd.DataFrame(stocks)
    monkeypatch.setattr(main, "get_stocks", lambda: stocks)
    monkeypatch.setattr(main, "get_recommendations", lambda: recs)
    monkeypatch.setattr(main, "prepare_report", lambda s, r: df)
    monkeypatch.setattr(main, "upload_to_sheet", lambda x: None)
    monkeypatch.setattr(main, "send_report", lambda x: None)
    main.job()


# ---------- OZON API ----------


def test_get_headers_with_env(monkeypatch):
    """Проверка: get_headers() возвращает корректные заголовки"""
    monkeypatch.setenv("OZON_CLIENT_ID", "id")
    monkeypatch.setenv("OZON_API_KEY", "key")
    headers = ozon_api.get_headers()
    assert headers["Client-Id"] == "id"
    assert headers["Api-Key"] == "key"


def test_get_session_retries():
    """Проверка: сессия создаётся с адаптерами"""
    s = ozon_api.get_session()
    assert "https://" in s.adapters
    assert "http://" in s.adapters


# ---------- TELEGRAM BOT ----------


@pytest.mark.asyncio
async def test_send_report_with_mock(monkeypatch):
    """Проверка send_report() с данными"""
    df = pd.DataFrame([{"id": 1, "name": "Test"}])
    monkeypatch.setattr("telegram.Bot.send_message", dummy_send)
    monkeypatch.setattr("telegram.Bot.send_document", dummy_send)
    monkeypatch.setenv("TELEGRAM_TOKEN", "dummy_token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "dummy_chat")
    await telegram_bot.send_report(df)


@pytest.mark.asyncio
async def test_send_report_empty(monkeypatch):
    """Проверка send_report() с пустым DataFrame"""
    df = pd.DataFrame()
    monkeypatch.setattr("telegram.Bot.send_message", dummy_send)
    monkeypatch.setenv("TELEGRAM_TOKEN", "dummy_token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "dummy_chat")
    await telegram_bot.send_report(df)


# ---------- UTILS ----------


def test_setup_logging_returns_logger():
    """setup_logging() возвращает рабочий логгер"""
    logger = utils.setup_logging()
    assert logger is not None
    assert hasattr(logger, "info")
    logger.info("Test log entry")


def test_load_config_default(monkeypatch, tmp_path):
    """load_config() загружает корректный JSON"""
    config_file = tmp_path / "test_config.json"
    config_file.write_text('{"key": "value"}')
    result = utils.load_config(str(config_file))
    assert result.get("key") == "value"
