from celery import Celery

from app.pkg.settings import settings

__all__ = ["celery_app"]


celery_app = Celery(
    __name__,
    broker=str(settings.REDIS.DSN)
)
