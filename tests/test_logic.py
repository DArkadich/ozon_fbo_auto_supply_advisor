import pandas as pd
from src.logic import prepare_report

def test_prepare_report_valid_merge():
    stocks = [{"product_id": 1, "days_of_stock_left": 3}]
    recos = [{"product_id": 1, "recommended_amount": 50}]
    df = prepare_report(stocks, recos)
    assert not df.empty
    assert "recommended_amount" in df.columns

def test_prepare_report_empty_inputs():
    df = prepare_report([], [])
    assert df.empty

def test_prepare_report_missing_column():
    stocks = [{"wrong_field": 1}]
    recos = [{"product_id": 1}]
    df = prepare_report(stocks, recos)
    assert df.empty
