from app.pkg.settings import settings
from celery import Celery

__all__ = ["celery_app"]


celery_app = Celery(
    __name__,
    broker=str(settings.REDIS.DSN),
)
