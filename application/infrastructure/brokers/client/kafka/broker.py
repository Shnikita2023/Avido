import logging
from typing import Any, Callable, Coroutine, Optional

import aiokafka

from application.exceptions.broker import KafkaError

logger = logging.getLogger(__name__)


class KafkaConsumer:

    def __init__(self, group_id: str, topics: tuple) -> None:
        self.consumer: Optional[aiokafka.AIOKafkaConsumer] = None
        self.group_id = group_id
        self.topics = topics

    async def connect(self, url: str) -> aiokafka.AIOKafkaConsumer:
        self.consumer = aiokafka.AIOKafkaConsumer(*self.topics, bootstrap_servers=url, group_id=self.group_id)
        await self.consumer.start()
        logger.info("Успешное подключение к Kafka(consumers)")
        return self.consumer

    async def disconnect(self) -> None:
        if self.consumer:
            await self.consumer.stop()
            logger.info("Соединение с Kafka(consumers) закрыто успешно")

    async def get_message(self, handling_message: Callable[..., Coroutine[Any, Any, None]]) -> None:

        try:
            if self.consumer:
                async for message in self.consumer:
                    await handling_message(message)

        except aiokafka.errors.KafkaError:
            raise KafkaError

