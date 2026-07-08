<!-- Пока не коммитить -->
# Booking Service

## Стек технологий
- Python
- FastAPI
- PostgreSQL
- Redis
- Celery
- Docker


## Структура проекта
```
app/
├── main.py              # Инициализация FastAPI, Celery и подключение роутеров
├── config.py            # Настройки (DATABASE_URL, REDIS_URL, JWT_SECRET)
├── database.py          # Сессия SQLAlchemy
├── celery_app.py        # Настройка инстанса Celery
└── modules/
    ├── auth/            # Логика токенов (Access/Refresh)
    │   ├── router.py
    │   ├── schemas.py
    │   └── security.py
    ├── rooms/           # Переговорки, фильтры и поиск
    │   ├── router.py
    │   ├── models.py
    │   ├── schemas.py
    │   └── crud.py
    ├── bookings/        # Транзакции, SELECT FOR UPDATE, логика брони
    │   ├── router.py
    │   ├── models.py
    │   ├── schemas.py
    │   └── services.py  # Защита от Race Conditions
    └── notifications/   # Фоновые задачи (Celery)
        └── tasks.py     # Отправка писем и генерация PDF
```
