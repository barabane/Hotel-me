from datetime import timedelta

from celery import Celery

from config import settings

celery_app = Celery(
    "tasks",
    broker=settings.REDIS_URL,
    include=["app.tasks.tasks", "app.tasks.scheduled"]
)
celery_app.autodiscover_tasks()
celery_app.conf.update(
    timezone='Asia/Yekaterinburg',
    enable_utc=True,
    broker_connection_retry_on_startup=True
)


celery_app.conf.beat_schedule = {
    "reminder": {
        "task": "tomorrow_checkin_reminder",
        "schedule": timedelta(hours=9)
    }
}

celery_app.conf.beat_schedule = {
    "reminder": {
        "task": "three_days_checkin_reminder",
        "schedule": timedelta(hours=3, minutes=30)
    }
}
