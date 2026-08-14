[Русский](README.md) | **English**

# Booking Service

## Tech Stack
- Python
- FastAPI
- PostgreSQL
- Redis
- Celery
- Docker

## Architecture Features
- **Race Condition Protection:** Room booking utilizes database-level `SELECT FOR UPDATE` locks to eliminate double-booking issues.
- **Background Tasks:** Email notifications and PDF generation are offloaded to Celery background workers via Redis.
- **JWT Auth:** Implements Access/Refresh token authentication mechanism.

## Project Structure
```
app/
├── main.py              # FastAPI initialization, Celery, and router registration
├── config.py            # Configuration settings (DATABASE_URL, REDIS_URL, JWT_SECRET)
├── database.py          # SQLAlchemy session setup
├── dependencies.py      # Dependencies (get_current_user, get_admin_user)
├── celery_app.py        # Celery instance configuration
└── modules/
├── auth/                # Token management logic (Access/Refresh)
│   ├── router.py
│   ├── models.py

│   ├── schemas.py
│   └── security.py
├── rooms/               # Meeting rooms, filtering, and search
│   ├── router.py
│   ├── models.py
│   ├── schemas.py
│   └── crud.py
├── bookings/            # Transactions, SELECT FOR UPDATE, booking logic
│   ├── router.py
│   ├── models.py
│   ├── schemas.py
│   └── services.py      # Race Condition protection logic
└── notifications/       # Background tasks (Celery)
└── tasks.py             # Email sending and PDF generation
```

## Quick Start

### With Docker (Recommended)
```bash
# Clone repository
git clone https://github.com/banana-whyyy/booking-service.git
cd booking-service

# Create .env file
cp .env.example .env

# Run containers
docker-compose up --build
```

API will be available at: http://localhost:8000

Swagger UI documentation: http://localhost:8000/docs

### Local Setup (Without Docker)
```
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env and update DATABASE_URL for local PostgreSQL

# Apply database migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload
```

## API Endpoints

### Authentication

| Method | Endpoint | Description |
| :---: | :--- | :--- |
| POST | /auth/register | Register a new user |
| POST | /auth/login | Authenticate and retrieve token pair |
| POST | /auth/refresh | Refresh Access token using Refresh token |

### Rooms

| Method | Endpoint | Description | Access |
| :---: | :--- | :--- | :--- |
| GET | /rooms | List rooms (pagination, filtering) | Public |
| GET | /rooms/{id} | Get room details | User & Admin |
| POST | /rooms | Create a room | Admin |
| PUT | /rooms/{id} | Update room details | Admin |
| DELETE | /rooms/{id} | Delete a room | Admin |

### Bookings
| Method |Endpoint | Description | Access |
| :---: | :--- | :--- | :--- |
GET | /bookings | Listbookings | User & Admin
GET | /bookings/{id} | Get booking details | User & Admin
POST | /bookings | Create a booking | User & Admin
DELETE | /bookings/{id} | Cancel/Delete a booking | User & Admin

## Request Examples

### User Registration
``` bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "supersecretpassword"
  }'
```

### Login
``` bash
curl -X POST http://localhost:8000/auth/login \
  -F "username=string" \
  -F "password=string"
```

### Refresh Access token
``` bash
curl -X POST http://localhost:8000/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{
    "refresh_token": "YOUR_REFRESH_TOKEN_FROM_LOGIN_RESPONSE"
  }'
```

### Get Available Rooms
``` bash
curl -X GET "http://localhost:8000/rooms?limit=10&offset=0"
```

### Create Booking (Authorization Required)
``` bash
curl -X POST http://localhost:8000/bookings \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_REFRESH_TOKEN_FROM_LOGIN_RESPONSE" \
  -d '{
    "room_id": 1,
    "start_time": "2026-09-01T10:00:00Z",
    "end_time": "2026-09-01T12:00:00Z"
  }'
```

## Переменные окружения
| Variable | Description |	Default Value |
| :--- | :--- | :--- |
| DATABASE_URL | PostgreSQL async connection URL | postgresql+asyncpg://postgres:postgres@db:5432/Booking_DB |
| SYNC_DATABASE_URL | PostgreSQL sync connection URL | postgresql+psycopg://postgres:postgres@db:5432/Booking_DB |
| REDIS_URL | Redis connection URL | redis://:redis_password@redis:6379/0 |
| SECRET_KEY | Secret key for JWT signing | secret-key-change-me |
| ALGORITHM | JWT signing algorithm | HS256 |
| ACCESS_TOKEN_EXPIRE_MINUTES | Access token expiration time | 30 (Minutes) |
| REFRESH_TOKEN_EXPIRE_DAYS | Refresh token expiration time | 30 (Days) |


## Database Migrations
``` bash
# Generate a new migration
alembic revision --autogenerate -m "description"

# Apply all migrations
alembic upgrade head

# Rollback last migration
alembic downgrade -1
```

## Author
- GitHub: [@banana-whyyy](https://github.com/banana-whyyy)