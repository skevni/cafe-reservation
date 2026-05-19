@echo off
echo Запуск в режиме продакшена (PostgreSQL)
set COMPOSE_FILE=docker-compose.yml;docker-compose.prod.yml
set ENVIRONMENT=prod
docker compose up --build