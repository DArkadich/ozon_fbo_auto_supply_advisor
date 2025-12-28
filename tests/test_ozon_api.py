# tests/test_ozon_api.py
import os
from src.ozon_api import fetch_paginated


class DummyResponse:
    def __init__(self, data):
        self._data = data

    def json(self):
        return {"result": self._data}

    def raise_for_status(self):
        pass


def test_fetch_paginated(monkeypatch):
    monkeypatch.setattr(
        "requests.Session.post", lambda *a, **k: DummyResponse([{"id": 1}])
    )
    monkeypatch.setenv("OZON_CLIENT_ID", "123")
    monkeypatch.setenv("OZON_API_KEY", "abc")
    result = fetch_paginated("/v3/product/info/stocks")
    assert isinstance(result, list)


def test_fetch_paginated_handles_empty(monkeypatch):
    monkeypatch.setattr("requests.Session.post", lambda *a, **k: DummyResponse([]))
    monkeypatch.setenv("OZON_CLIENT_ID", "123")
    monkeypatch.setenv("OZON_API_KEY", "abc")
    result = fetch_paginated("/v3/product/info/stocks")
    assert result == []
