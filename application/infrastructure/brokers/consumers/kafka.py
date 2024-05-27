import asyncio
import sys
from typing import Any, Callable, Coroutine

from application.infrastructure.brokers.client.kafka.broker import KafkaConsumer
from application.infrastructure.brokers.client.schemas import data_connect_kafka, ConnectionParamsKafka
from application.logging_config import init_logger
from .base import Consumer
from .utils import process_message_kafka


class ConsumerKafka(Consumer):
    def __init__(self, data: ConnectionParamsKafka):
        self.data = data
        self.consumer = KafkaConsumer(group_id=data.group_id, topics=data.topic)

    async def initialization(self) -> None:
        await self.consumer.connect(url=self.data.url)

    async def get_message(self, handling_message: Callable[..., Coroutine[Any, Any, None]]) -> None:
        await self.consumer.get_message(handling_message=handling_message)

    async def finalization(self) -> None:
        await self.consumer.disconnect()


async def kafka_message_flow() -> None:
    consumer = ConsumerKafka(data=data_connect_kafka)
    try:
        await consumer.initialization()
        await consumer.get_message(process_message_kafka)
    finally:
        await consumer.finalization()


if __name__ == "__main__":
    try:
        init_logger(pathname="app", filename="kafka.log")
        asyncio.run(kafka_message_flow())
    except KeyboardInterrupt:
        sys.exit(0)
