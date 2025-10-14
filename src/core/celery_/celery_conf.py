from datetime import timedelta

from celery import Celery

from core.config import settings


celery_app = Celery(
    "celery_worker",
    broker=settings.redis.get_url_connect,
    backend=settings.redis.get_url_connect,
    include=[
        "core.celery_.tasks.tasks"
    ]
)

celery_app.conf.beat_schedule = {
    "background_task": {  # уникальное название задачи
        "task": 'core.celery_.tasks.tasks.background_task',  # путь к задаче
        "schedule": timedelta(seconds=15),  # интервал, через который будет выполняться задача
    },
}