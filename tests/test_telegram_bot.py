import pytest
import pandas as pd
from src.telegram_bot import send_report
import asyncio

@pytest.mark.asyncio
async def test_send_report_empty(monkeypatch):
    monkeypatch.setattr("telegram.Bot.send_message", lambda *a, **k: None)
    df = pd.DataFrame()
    await send_report(df)  # не должно вызвать исключений

@pytest.mark.asyncio
async def test_send_report_with_data(monkeypatch):
    monkeypatch.setattr("telegram.Bot.send_message", lambda *a, **k: None)
    monkeypatch.setattr("telegram.Bot.send_document", lambda *a, **k: None)
    df = pd.DataFrame([{"id": 1, "name": "Test"}])
    await send_report(df)
