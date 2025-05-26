import asyncio
import os
import aio_pika


HOST = os.getenv("RABBIT__HOST")
PORT = os.getenv("RABBIT__PORT")
USER = os.getenv("RABBIT__USER")
PASSWORD = os.getenv("RABBIT__PASSWORD")
VIRTUAL_HOST = os.getenv("RABBIT__VIRTUAL_HOST")
URL = f"amqp://{USER}:{PASSWORD}@{HOST}:{PORT}/{VIRTUAL_HOST}"


DLX_EXCHANGE_NAME = os.getenv("RABBIT__DLX_EXCHANGE_NAME")
DLQ_NAME = os.getenv("RABBIT__DLQ_NAME")
DLQ_ROUTING_KEY = os.getenv("RABBIT__DLQ_ROUTING_KEY")


async def setup_dlx(channel):
    dlx_exchange = await channel.declare_exchange(
        name=DLX_EXCHANGE_NAME,
        type="direct",
        durable=True
    )
    dlq = await channel.declare_queue(
        name=DLQ_NAME,
        durable=True,
    )
    await dlq.bind(dlx_exchange, routing_key=DLQ_ROUTING_KEY)
    print("DLX and Dead Letter Queue setup complete.")

async def main():
    connection = await aio_pika.connect_robust(URL)
    async with connection:
        channel = await connection.channel()
        await setup_dlx(channel)

if __name__ == "__main__":
    asyncio.run(main())
