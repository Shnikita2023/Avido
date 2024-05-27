import logging
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from aiokafka import ConsumerRecord

logger = logging.getLogger(__name__)
T = TypeVar("T")


class DecodeMessage(Generic[T], ABC):

    @abstractmethod
    def decode(self, message: T) -> str:
        raise NotImplementedError


class DecodeKafkaMessage(DecodeMessage[ConsumerRecord]):

    def decode(self, message: ConsumerRecord) -> str:
        return message.value.decode("utf-8")


async def register_user(decode_message: str) -> None:
    logger.info(msg=f"Пользователь зарегистрирован с данными: {decode_message}")


async def process_message_kafka(message: ConsumerRecord) -> None:
    decode_message: str = DecodeKafkaMessage().decode(message=message)
    await register_user(decode_message=decode_message)

