import pytest
from src import ozon_api

def test_headers_present(monkeypatch):
    monkeypatch.setenv("OZON_CLIENT_ID", "123")
    monkeypatch.setenv("OZON_API_KEY", "abc")
    headers = ozon_api.get_headers()
    assert "Client-Id" in headers
    assert "Api-Key" in headers

def test_fetch_paginated_handles_empty(monkeypatch):
    class DummyResp:
        def json(self): return {"result": []}
        def raise_for_status(self): pass
    monkeypatch.setattr("requests.Session.post", lambda *a, **k: DummyResp())
    result = ozon_api.fetch_paginated("/v3/product/info/stocks")
    assert result == []

def test_get_stocks_and_recommendations(monkeypatch):
    monkeypatch.setattr(ozon_api, "fetch_paginated", lambda *a, **k: [{"id": 1}])
    assert isinstance(ozon_api.get_stocks(), list)
    assert isinstance(ozon_api.get_recommendations(), list)
