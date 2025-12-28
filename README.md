# 🧠 Ozon FBO Auto Supply Advisor

Автоматический бот для анализа остатков и поставок по модели FBO на Ozon.
Отправляет ежедневный отчёт в Telegram и Google Sheets.

## 🚀 Возможности
- Получение остатков и рекомендаций поставок через Ozon API
- Формирование отчёта с фильтрацией товаров по остаткам
- Отправка отчёта в Telegram и Google Sheets
- Полностью контейнеризирован (Docker)
- Планировщик запуска (schedule)

## ⚙️ Полная установка и запуск
git clone https://github.com/yourusername/ozon-fbo-advisor.git
cd ozon-fbo-advisor
cp .env.example .env
docker compose up -d --build


Проверка логов:

docker compose logs -f ozon_fbo_advisor


Описание переменных окружения
Переменная	Назначение	Пример
OZON_API_KEY	API-ключ Ozon Seller	eyJhbGc...
OZON_CLIENT_ID	ID клиента Ozon	123456
TELEGRAM_TOKEN	Токен Telegram бота	1234:ABCD
TELEGRAM_CHAT_ID	ID чата для уведомлений	987654321
GOOGLE_SA_PATH	Путь к сервисному аккаунту Google	/app/service_account.json
GOOGLE_SHEET_NAME	Название таблицы в Sheets	Ozon FBO Recommendations
UPDATE_TIME	Время ежедневного запуска	09:00
LOG_LEVEL	Уровень логирования	INFO
TZ	Часовой пояс	Europe/Moscow
APP_MODE	Режим работы (dev/prod)	prod


Примеры использования
Ручной запуск отчёта:
docker exec ozon_fbo_advisor python src/main.py

Просмотр последних логов:
docker logs -n 50 ozon_fbo_advisor

Проверка статуса контейнера:
docker inspect --format='{{.State.Health.Status}}' ozon_fbo_advisor
