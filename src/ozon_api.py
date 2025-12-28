import requests
import logging
import time
from requests.adapters import HTTPAdapter, Retry
from typing import List, Dict, Any
import os

BASE_URL = "https://api-seller.ozon.ru"


def get_session() -> requests.Session:
    """Создаёт HTTP-сессию с повторными запросами."""
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1,
                    status_forcelist=[429, 500, 502, 503, 504])
    session.mount("https://", HTTPAdapter(max_retries=retries))
    return session


def get_headers() -> Dict[str, str]:
    """Заголовки авторизации Ozon API."""
    return {
        "Client-Id": os.getenv("OZON_CLIENT_ID"),
        "Api-Key": os.getenv("OZON_API_KEY"),
        "Content-Type": "application/json"
    }


def fetch_paginated(endpoint: str, key: str = "result",
                    page_size: int = 100) -> List[Dict[str, Any]]:
    """Постранично получает данные из Ozon API."""
    session = get_session()
    offset, data = 0, []
    while True:
        payload = {"page_size": page_size, "page": offset // page_size + 1}
        try:
            r = session.post(f"{BASE_URL}{endpoint}",
                             headers=get_headers(), json=payload, timeout=10)
            r.raise_for_status()
            chunk = r.json().get(key, [])
            if not chunk:
                logging.info(f"Pagination complete for {endpoint}")
                break
            data.extend(chunk)
            offset += len(chunk)
        except requests.RequestException as e:
            logging.error(f"API request failed: {e}")
            break
        time.sleep(0.3)
    if not data:
        logging.warning(f"No data returned from {endpoint}")
    return data


def get_stocks() -> List[Dict[str, Any]]:
    """Возвращает остатки товаров (FBS/FBO)."""
    return fetch_paginated("/v3/product/info/stocks")


def get_recommendations() -> List[Dict[str, Any]]:
    """Возвращает рекомендации по поставкам FBO на склады."""
    return fetch_paginated("/v3/supply/recommendations")
