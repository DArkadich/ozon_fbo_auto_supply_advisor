# tests/test_ozon_api.py
from src.ozon_api import fetch_paginated


def test_fetch_paginated(monkeypatch):
    responses = [{"result": [{"id": 1}]}, {"result": []}]

    class DummyResponse:
        def __init__(self, data):
            self._data = data

        def json(self):
            return self._data

        def raise_for_status(self):
            pass

    # Подменяем post и sleep
    monkeypatch.setattr(
        "requests.Session.post", lambda *a, **k: DummyResponse(responses.pop(0))
    )
    monkeypatch.setattr("time.sleep", lambda _: None)
    monkeypatch.setenv("OZON_CLIENT_ID", "123")
    monkeypatch.setenv("OZON_API_KEY", "abc")

    result = fetch_paginated("/v3/product/info/stocks")
    assert len(result) == 1
