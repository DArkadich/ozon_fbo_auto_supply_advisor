FROM python:3.11.8-slim

WORKDIR /app
COPY ./src /app
COPY requirements.txt /app

# Опционально: копируем .env и service_account.json, если они не в .dockerignore
# COPY .env /app
# COPY service_account.json /app

RUN pip install --no-cache-dir -r requirements.txt

HEALTHCHECK CMD ["python", "-c", "print('healthy')"]

CMD ["python", "main.py"]
