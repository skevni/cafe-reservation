#!/bin/bash
echo "Запуск в режиме продакшена (PostgreSQL)"
export COMPOSE_FILE=docker-compose.yml:docker-compose.prod.yml
ENVIRONMENT=prod docker compose up --build