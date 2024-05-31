import json
import logging
from typing import Any, Callable, Coroutine

logger = logging.getLogger(__name__)


class MessageHandler:
    def __init__(self):
        self.handlers = {}

    def register_handler(self, message_type: str, predicate: Callable[[dict], bool]):
        def decorator(handler: Callable[[Any], Coroutine[Any, Any, None]]):
            self.handlers[message_type] = (handler, predicate)
            return handler

        return decorator

    async def handle_message(self, message_type: str, message: str):
        if message_type in self.handlers:
            handler, predicate = self.handlers[message_type]
            decoded_message: dict = json.loads(message)
            if predicate and predicate(decoded_message):
                await handler(decoded_message)
            else:
                logger.error(f"Predicate check failed for message: {message_type}")
        else:
            logger.error(f"No handler registered for message type {message_type}")
