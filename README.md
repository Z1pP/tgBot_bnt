# BNT Project

Монорепозиторий проекта BNT, содержащий бэкенд API и Telegram бот.

## Структура проекта

```
.
├── backend/           # FastAPI бэкенд
│   ├── app/          # Основной код бэкенда
│   ├── alembic/      # Миграции базы данных
│   └── pyproject.toml # Зависимости бэкенда
│
├── telegram_bot/      # Telegram бот
│   ├── bot/          # Код бота
│   └── pyproject.toml # Зависимости бота
│
└── pyproject.toml     # Общие настройки проекта
```

## Установка и запуск

### Бэкенд

```bash
cd backend
poetry install
poetry run alembic upgrade head
poetry run uvicorn app.main:app --reload
```

### Telegram бот

```bash
cd telegram_bot
poetry install
poetry run python -m bot
```

## Разработка

Каждый проект имеет свое виртуальное окружение и зависимости. Для разработки:

1. Установите Poetry: `curl -sSL https://install.python-poetry.org | python3 -`
2. Перейдите в нужную директорию (`backend/` или `telegram_bot/`)
3. Установите зависимости: `poetry install`
4. Активируйте окружение: `poetry shell`

## Конфигурация

### Бэкенд
Создайте файл `backend/.env`:
```env
DATABASE_URL=sqlite+aiosqlite:///./app.db
```

### Telegram бот
Создайте файл `telegram_bot/.env`:
```env
BOT_TOKEN=your_bot_token
API_URL=http://localhost:8000
```

## Линтинг и форматирование

Оба проекта используют:
- Black для форматирования
- MyPy для проверки типов

```bash
poetry run black .
poetry run mypy .
``` 