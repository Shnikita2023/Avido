import logging
from typing import Any, Callable, Coroutine

logger = logging.getLogger(__name__)


class MessageHandler:
    def __init__(self):
        self.handlers = {}

    def register_handler(self, message_type: str):
        def decorator(handler: Callable[[Any], Coroutine[Any, Any, None]]):
            self.handlers[message_type] = handler
            return handler

        return decorator

    async def handle_message(self, message_type: str, message: str):
        if message_type in self.handlers:
            await self.handlers[message_type](message)
        else:
            logger.error(msg=f"No handler registered for message type {message_type}")
