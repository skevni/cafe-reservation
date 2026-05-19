#!/bin/bash

set -e  # выход при ошибке

echo "Ожидание доступности PostgreSQL..."

# Ждём, пока порт 5432 станет доступен
until nc -z -v -w30 db 5432; do
  echo "Подключение к db:5432 не установлено. Повтор..."
  sleep 5
done

echo "PostgreSQL доступен"

# Применяем миграции Alembic
echo "Применение миграций Alembic..."
alembic upgrade head
if [ $? -ne 0 ]; then
  echo "Ошибка применения миграций"
  exit 1
fi
echo "Миграции успешно применены"

# Запуск приложения
echo "Запуск приложения..."
if [ "$ENVIRONMENT" = "prod" ]; then
  echo "Запуск в режиме production (gunicorn + uvicorn)"
  exec gunicorn \
    --worker-class uvicorn.workers.UvicornWorker \
    --workers 4 \
    --bind 0.0.0.0:8000 \
    --timeout 120 \
    --keep-alive 5 \
    "app.main:app"
else
  echo "Запуск в режиме разработки (uvicorn с reload)"
  exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
fi