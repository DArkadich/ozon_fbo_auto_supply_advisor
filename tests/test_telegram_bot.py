# tests/test_telegram_bot.py
import pytest
import pandas as pd
from src.telegram_bot import send_report


@pytest.mark.asyncio
async def test_send_report_empty(monkeypatch):
    async def fake_send_message(*a, **k):
        return None

    monkeypatch.setattr("telegram.Bot.send_message", fake_send_message)
    monkeypatch.setenv("TELEGRAM_TOKEN", "dummy_token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "12345")
    df = pd.DataFrame()
    await send_report(df)


@pytest.mark.asyncio
async def test_send_report_with_data(monkeypatch):
    async def fake_send_message(*a, **k):
        return None

    async def fake_send_document(*a, **k):
        return None

    monkeypatch.setattr("telegram.Bot.send_message", fake_send_message)
    monkeypatch.setattr("telegram.Bot.send_document", fake_send_document)
    monkeypatch.setenv("TELEGRAM_TOKEN", "dummy_token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "12345")
    df = pd.DataFrame([{"id": 1, "name": "Test"}])
    await send_report(df)
