import json
import logging
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from aiokafka import ConsumerRecord

from application.commands.user import message_handler

logger = logging.getLogger(__name__)
T = TypeVar("T")


class DecodeMessage(Generic[T], ABC):

    @abstractmethod
    def decode(self, message: T) -> str:
        raise NotImplementedError


class DecodeKafkaMessage(DecodeMessage[ConsumerRecord]):

    def decode(self, message: ConsumerRecord) -> str:
        return message.value.decode("utf-8")


def definition_message_type(decode_message: str) -> str:
    data_message = json.loads(decode_message)
    return data_message.get('type')


async def process_message_kafka(message: ConsumerRecord) -> None:
    decode_message: str = DecodeKafkaMessage().decode(message=message)
    message_type: str = definition_message_type(decode_message)
    await message_handler.handle_message(message_type, decode_message)


