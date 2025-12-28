import pandas as pd
from src.google_sheets import upload_to_sheet

def test_upload_to_sheet_empty(monkeypatch):
    monkeypatch.setattr("gspread.authorize", lambda *a, **k: None)
    df = pd.DataFrame()
    upload_to_sheet(df)  # не должно упасть
