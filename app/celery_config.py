from celery import Celery
from app.config import settings

celery_app = Celery(
    "booking_tasks",
    broker=settings.redis_url,
    backend=settings.redis_url
)

celery_app.autodiscover_tasks(["app.modules.notifications"])

celery_app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    enable_utc=True,  
    timezone='Europe/Moscow',  
    broker_connection_retry_on_startup=True,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    include=["app.modules.notifications.tasks"],
)