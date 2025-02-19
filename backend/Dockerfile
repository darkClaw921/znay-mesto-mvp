# Используем официальный образ Python
FROM python:3.12-slim
ENV TZ=Europe/Moscow
# Устанавливаем рабочую директорию
WORKDIR /app
RUN apt-get update && apt-get install -y nano htop vim default-libmysqlclient-dev build-essential
# Устанавливаем зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# # Копируем requirements.txt и устанавливаем зависимости
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app

COPY . /app
# COPY .env /app/.env
RUN pip3 install poetry
RUN pip3 install --upgrade setuptools
RUN poetry install




CMD ["poetry", "run", "python3", "app/main2.py"]