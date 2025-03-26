import asyncio
from typing import Callable
from app.pkg.logger import get_logger

logger = get_logger(__name__)

# TODO: техдолг - заменить этот ужасный воркер на Celery
class BackgroundWorker:
    def __init__(self, max_size: int = 200):
        self._queue = asyncio.Queue(maxsize=max_size)
        self._running = False
        self._task = None

    async def put(self, task: Callable, *args, **kwargs):
        logger.debug("Putting task '%s' to queue with args: %s", task.__name__, args)
        await self._queue.put((task, args, kwargs))

    async def start(self):
        logger.info("Starting background worker")
        self._running = True
        self._task = asyncio.create_task(self._run())

    async def stop(self):
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info("Background worker was stopped")

    async def _run(self):
        while self._running:
            task, args, kwargs = await self._queue.get()
            logger.debug("Processing task '%s' with args: %s", task.__name__, args)
            try:
                if asyncio.iscoroutinefunction(task):
                    await task(*args, **kwargs)
                else:
                    await asyncio.to_thread(task, *args, **kwargs)
                logger.debug(
                    "Task '%s' processed successfully. Args: %s",
                    task.__name__,
                    args
                )
            except Exception as e:
                logger.error(f"Task failed: %s", e)
            finally:
                self._queue.task_done()

background_worker = BackgroundWorker()
