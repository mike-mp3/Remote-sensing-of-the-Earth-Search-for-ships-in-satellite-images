"""``on_startup`` function will be called when server trying to start."""
from app.internal.workers.background import background_worker

async def on_startup() -> None:
    """Run code on server startup.

    Warnings:
        **Don't use this function for insert default data in database.
        For this action, we have scripts/migrate.py.**

    Returns:
        None
    """
    await background_worker.start()


async def on_shutdown() -> None:
    """Run code on server shutdown. Use this function for close all
    connections, etc.

    Returns:
        None
    """
    await background_worker.stop()
