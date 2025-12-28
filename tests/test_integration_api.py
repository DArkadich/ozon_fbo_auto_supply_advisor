# tests/test_integration_api.py
import os
from src import ozon_api


def test_fetch_paginated_handles_empty(monkeypatch):
    class DummyResp:
        def json(self):
            return {"result": []}

        def raise_for_status(self):
            pass

    # фикс: задаём фиктивные переменные окружения
    monkeypatch.setenv("OZON_CLIENT_ID", "dummy")
    monkeypatch.setenv("OZON_API_KEY", "dummy")

    monkeypatch.setattr("requests.Session.post", lambda *a, **k: DummyResp())
    payload = {"page_size": 100}
    result = ozon_api.fetch_paginated("/v3/product/info/stocks", payload)
    assert result == []
