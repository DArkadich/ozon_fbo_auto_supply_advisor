import pytest
from src.ozon_api import fetch_paginated

class DummyResponse:
    def __init__(self, data):
        self._data = data
    def json(self):
        return {"result": self._data}
    def raise_for_status(self):
        pass

def test_fetch_paginated(monkeypatch):
    monkeypatch.setattr("requests.Session.post", lambda *a, **k: DummyResponse([{"id": 1}, {"id": 2}]))
    data = fetch_paginated("/v3/product/info/stocks", page_size=2)
    assert isinstance(data, list)
    assert len(data) == 2

def test_fetch_paginated_empty(monkeypatch):
    monkeypatch.setattr("requests.Session.post", lambda *a, **k: DummyResponse([]))
    result = fetch_paginated("/v3/product/info/stocks")
    assert result == []
