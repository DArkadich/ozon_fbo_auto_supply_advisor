import os
import time
import logging
from typing import Any, Dict, List, Optional
import requests
from requests.adapters import HTTPAdapter, Retry

BASE_URL = "https://api-seller.ozon.ru"


def get_headers() -> Dict[str, str]:
    """Заголовки авторизации для Ozon API."""
    client_id: Optional[str] = os.getenv("OZON_CLIENT_ID")
    api_key: Optional[str] = os.getenv("OZON_API_KEY")
    if not client_id or not api_key:
        raise EnvironmentError(
            "Missing OZON_CLIENT_ID or OZON_API_KEY in environment variables"
        )
    return {
        "Client-Id": client_id,
        "Api-Key": api_key,
        "Content-Type": "application/json",
    }


def get_session() -> requests.Session:
    """Создаёт и настраивает HTTP-сессию."""
    session = requests.Session()
    retries = Retry(
        total=3, backoff_factor=0.5, status_forcelist=[429, 500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("https://", adapter)
    return session


def fetch_paginated(
    endpoint: str, payload: Dict[str, Any], key: str = "result"
) -> List[Dict[str, Any]]:
    """Постранично получает данные из Ozon API."""
    session = get_session()
    all_data: List[Dict[str, Any]] = []
    logging.info(f"Fetching data from {endpoint} ...")

    while True:
        try:
            r = session.post(
                f"{BASE_URL}{endpoint}", headers=get_headers(), json=payload, timeout=10
            )
            r.raise_for_status()
            data = r.json().get(key, [])
            if not data:
                logging.warning(f"No data returned from {endpoint}")
                break
            all_data.extend(data)
            # пагинация по last_id, если есть
            if "last_id" in r.json():
                payload["last_id"] = r.json()["last_id"]
                if not payload["last_id"]:
                    break
            else:
                break
        except requests.RequestException as e:
            logging.error(f"API request failed: {e}")
            break
        time.sleep(0.3)

    logging.info(f"Fetched {len(all_data)} items from {endpoint}")
    return all_data


def get_stocks() -> List[Dict[str, Any]]:
    """Возвращает остатки товаров (FBO/FBS) через v4 API."""
    payload = {
        "filter": {"offer_id": [], "product_id": [], "visibility": "ALL"},
        "page_size": 100,
        "last_id": "",
    }
    return fetch_paginated("/v4/product/info/stocks", payload)


def get_recommendations() -> List[Dict[str, Any]]:
    """Возвращает рекомендации по поставкам FBO через рабочий v3 API."""
    payload = {"limit": 100, "offset": 0}
    return fetch_paginated("/v3/supplier/stock_recommendations", payload)
