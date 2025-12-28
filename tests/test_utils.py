from src.utils import setup_logging, load_config
import os


def test_load_config(monkeypatch):
    monkeypatch.setattr(os, "getenv", lambda x: "mock" if x else None)
    load_config()
