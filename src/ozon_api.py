import os
import time
import logging
from typing import Any, Dict, List, Optional
import requests
from requests.adapters import HTTPAdapter, Retry

BASE_URL = "https://api-seller.ozon.ru"


def get_headers() -> Dict[str, str]:
    """Возвращает заголовки авторизации для Ozon API."""
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
    """Создаёт и настраивает HTTP-сессию с повторными попытками."""
    session = requests.Session()
    retries = Retry(
        total=3,
        backoff_factor=0.5,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("https://", adapter)
    return session


def fetch_paginated(
    endpoint: str, key: str = "result", page_size: int = 100
) -> List[Dict[str, Any]]:
    """Постранично получает данные из Ozon API (универсальный метод)."""
    session = get_session()
    offset = 0
    all_data: List[Dict[str, Any]] = []

    logging.info(f"Fetching data from {endpoint} ...")

    while True:
        payload = {"page_size": page_size, "page": offset // page_size + 1}
        try:
            response = session.post(
                f"{BASE_URL}{endpoint}",
                headers=get_headers(),
                json=payload,
                timeout=10,
            )
            response.raise_for_status()
            result_json = response.json()

            if key in result_json:
                items = result_json[key]
            elif "result" in result_json and isinstance(result_json["result"], list):
                items = result_json["result"]
            else:
                items = []

            if not items:
                logging.warning(f"No data returned from {endpoint}")
                break

            all_data.extend(items)
            offset += len(items)

        except requests.RequestException as e:
            logging.error(f"API request failed: {e}")
            break

        time.sleep(0.3)  # уважаем лимиты API

    logging.info(f"Fetched {len(all_data)} items from {endpoint}")
    return all_data


def get_stocks() -> List[Dict[str, Any]]:
    """Возвращает остатки товаров (FBO/FBS)."""
    return fetch_paginated("/v4/product/info/stocks")


def get_recommendations() -> List[Dict[str, Any]]:
    """Возвращает рекомендации по поставкам FBO."""
    data = fetch_paginated("/v4/supply/recommendations")

    # В некоторых версиях API данные могут быть словарём с ключом result
    if isinstance(data, dict) and "result" in data:
        return data["result"]

    return data
