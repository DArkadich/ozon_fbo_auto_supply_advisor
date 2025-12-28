import pandas as pd
import logging
from typing import List, Dict

def prepare_report(stocks: List[Dict], recos: List[Dict]) -> pd.DataFrame:
    """Объединяет данные остатков и рекомендаций, фильтрует товары с низким запасом."""
    if not stocks or not recos:
        logging.warning("Empty data received from Ozon API.")
        return pd.DataFrame()

    df_stocks = pd.DataFrame(stocks)
    df_recos = pd.DataFrame(recos)

    if "product_id" not in df_stocks.columns or "product_id" not in df_recos.columns:
        logging.error("Missing product_id field in Ozon API data.")
        return pd.DataFrame()

    merged = pd.merge(df_stocks, df_recos, on="product_id", how="outer").fillna(0)

    if "days_of_stock_left" in merged.columns:
        merged = merged[merged["days_of_stock_left"] < 7]

    logging.info(f"Prepared report with {len(merged)} rows.")
    return merged
