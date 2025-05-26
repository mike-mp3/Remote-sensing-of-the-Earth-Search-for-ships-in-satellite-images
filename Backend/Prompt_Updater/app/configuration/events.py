"""``on_startup`` function will be called when server trying to start."""
import asyncio

from app.internal.workers.prompt.run import run as run_worker


async def on_startup() -> None:
    """Run code on server startup.

    Warnings:
        **Don't use this function for insert default data in database.
        For this action, we have scripts/migrate.py.**

    Returns:
        None
    """
    asyncio.create_task(run_worker())


async def on_shutdown() -> None:
    """Run code on server shutdown. Use this function for close all
    connections, etc.

    Returns:
        None
    """
