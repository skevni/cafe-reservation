# Бронирование мест в кафе

[![Python](https://img.shields.io/badge/Python-3.12%2B-blue)]()
[![FastAPI](https://img.shields.io/badge/FastAPI-0.136.0-green)]()
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.49+-orange)]()
[![UVICORN](https://img.shields.io/badge/UVICORN-0.47.0-brown)]()
[![GUNICORN](https://img.shields.io/badge/GUNICORN-26.0.0-olive)]()

## Технологии

- **FastAPI** — современный веб-фреймворк для создания API
- **FastAPI Users** — быстрая и гибкая система аутентификации для FastAPI.
- **SQLAlchemy** — ORM для работы с базой данных
- **AsyncIO** — асинхронная обработка запросов
- **Pydantic** — валидация данных
- **Alembic** — миграции базы данных
- **SQLite** — файловая база данных (в режиме разработки и тестирования)
- **PostgeSQL** — система управления базами данных (используется в продакшене)

## Структура проекта

```
app/
├── api/                # API эндпоинты
├── core/               # Основная конфигурация
├── models/             # Модели SQLAlchemy
├── repositories/       # Репозитории для работы с БД
├── schemas/            # Pydantic-схемы
├── services/           # Бизнес-логика
└── tests/              # Тесты
```

## Установка и запуск

1.Клонируйте репозиторий:

```bash
git clone https://github.com/skevni/cafe-reservation.git
cd cafe-reservation
```

2.Создайте виртуальное окружение:

```bash
python -m venv venv
```

3.Активируйте виртуальное окружение:

- Windows:

```bash
source venv\Scripts\activate
```

- Linux/MacOS:

```bash
source venv/bin/activate
```

4.Установите зависимости:

```bash
pip install -r requirements.txt
```

5.Настроить переменные окружения
Создайте файл `.env` и `.env.dev` в корне проекта:

```env

```

`.env.dev`

```env

```

6.Примените миграции

```bash
alembic upgrade head
```

7.Запустите приложение:

```bash
uvicorn app.main:app --reload
```

Сервер будет доступен по адресу [http://127.0.0.1:8000](http://127.0.0.1:8000)

## API Documentation

После запуска приложения:

Документация доступна по адресу:

- [Technical Specification Swagger](http://127.0.0.1:8000/tech_spec/docs)
- [Technical Specification ReDoc](http://127.0.0.1:8000/tech_spec/redoc)

- [Swagger UI](http://127.0.0.1:8000/api/v1/docs)
- [ReDoc](http://127.0.0.1:8000/api/v1/redoc)

Разработано в рамках курса Яндекс.Практикум по Python-разработке.
