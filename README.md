# Booking Service
[English](README.en.md) | **Русский**

## Стек технологий
- Python
- FastAPI
- PostgreSQL
- Redis
- Celery
- Docker

## Особенности архитектуры
- **Защита от Race Conditions:** Бронирование комнат использует блокировки `SELECT FOR UPDATE` на уровне БД, исключая двойное бронирование.
- **Фоновые задачи:** Отправка email-уведомлений и генерация PDF вынесены в фоновые воркеры Celery через Redis.
- **JWT Auth:** Реализован механизм Access/Refresh токенов.
- **Безопасность:** FastAPI работает в асинхронном режиме, пароли хэшируются через bcrypt 

## Структура проекта
```
app/
├── main.py              # Инициализация FastAPI, Celery и подключение роутеров
├── config.py            # Настройки (DATABASE_URL, REDIS_URL, JWT_SECRET)
├── database.py          # Сессия SQLAlchemy
├── dependencies.py      # Зависимости (get_current_user, get_admin_user)
├── celery_app.py        # Настройка инстанса Celery
└── modules/
    ├── auth/            # Логика токенов (Access/Refresh)
    │   ├── router.py
    │   ├── models.py    
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

## Быстрый старт

### С Docker (рекомендуется)
``` bash
# Клонировать репозиторий
git clone https://github.com/banana-whyyy/booking-service.git
cd booking-service

# Настроить переменные окружения
cp .env.example .env

# Запустить сервисы
docker compose up --build -d
```
API будет доступен по адресу: http://localhost:8000

Swagger UI: http://localhost:8000/docs

### Локально (без Docker)
``` bash
# Создать виртуальное окружение
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Установить зависимости
pip install -r requirements.txt

# Настроить переменные окружения
cp .env.example .env
# Отредактировать .env, указав DATABASE_URL для локальной PostgreSQL

# Применить миграции
alembic upgrade head

# Запустить сервер
uvicorn app.main:app --reload
```

## API Endpoints

### Аутентификация

| Метод | Endpoint | Описание |
| :---: | :--- | :--- |
| POST | /auth/register | Регистрация нового пользователя |
| POST | /auth/login | Аутентификация и получение пары токенов |
| POST | /auth/refresh | Обновление Access токена через Refresh токен |

### Комнаты

| Метод | Endpoint | Описание | Доступ |
| :---: | :--- | :--- | :--- |
| GET | /rooms | Список комнат (пагинация, фильтрация) | Все |
| GET | /rooms/{id} | Информация о комнате | Пользователь и Admin |
| POST | /rooms | Создать комнату | Admin |
| PUT | /rooms/{id} | Обновить комнату | Admin |
| DELETE | /rooms/{id} | Удалить комнату | Admin |

### Букинг

| Метод | Endpoint | Описание | Доступ |
| :---: | :--- | :--- | :--- |
| GET | /bookings | Список записей | Пользователь и Admin |
| GET | /bookings/{id} | Информация о записи | Пользователь и Admin |
| POST | /bookings | Создать запись | Пользователь и Admin |
| DELETE | /bookings/{id} | Удалить запись | Пользователь и Admin |

## Примеры запросов

### Регистрация
``` bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "supersecretpassword"
  }'
```

### Вход
``` bash
curl -X POST http://localhost:8000/auth/login \
  -F "username=string" \
  -F "password=string"
```

### Обновление Access токена (Refresh)
``` bash
curl -X POST http://localhost:8000/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{
    "refresh_token": "ВАШ_REFRESH_TOKEN_ИЗ_ОТВЕТА_LOGIN"
  }'
```

### Получение списка доступных комнат
``` bash
curl -X GET "http://localhost:8000/rooms?limit=10&offset=0"
```

### Создание бронирования (Требуется Авторизация)
``` bash
curl -X POST http://localhost:8000/bookings \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ВАШ_ACCESS_TOKEN" \
  -d '{
    "room_id": 1,
    "start_time": "2026-09-01T10:00:00Z",
    "end_time": "2026-09-01T12:00:00Z"
  }'
```


## Переменные окружения
| Переменная | Описание | По умолчанию |
| :--- | :--- | :--- |
| DATABASE_URL | URL подключения к PostgreSQL | postgresql+asyncpg://postgres:postgres@db:5432/Booking_DB |
| SYNC_DATABASE_URL | URL подключения к PostgreSQL синхронно | postgresql+psycopg://postgres:postgres@db:5432/Booking_DB |
| REDIS_URL | URL подключения к Redis | redis://:redis_password@redis:6379/0 |
| SECRET_KEY | Секретный ключ для JWT | secret-key-change-me |
| ALGORITHM | Алгоритм JWT | HS256 |
| ACCESS_TOKEN_EXPIRE_MINUTES | Время жизни токена | 30 (Минут) |
| REFRESH_TOKEN_EXPIRE_DAYS | Время жизни токена | 30 (Дней) |


## Тестирование
``` bash
# Установить зависимости для тестов
pip install -r requirements.txt

# Запустить тесты
pytest -v
```


## Миграции
``` bash
# Создать новую миграцию
alembic revision --autogenerate -m "description"

# Применить миграции
alembic upgrade head

# Откатить последнюю миграцию
alembic downgrade -1
```

## Автор
- GitHub: [@banana-whyyy](https://github.com/banana-whyyy)