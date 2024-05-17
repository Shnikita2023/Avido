import asyncio
import logging
from functools import wraps
from typing import Callable, Optional

from application.events import Event

logger = logging.getLogger(__name__)


_HANDLERS = {}


def subscribe(event_predicate: Callable, subscriber: Optional[Callable] = None) -> Optional[Callable]:

    @wraps(event_predicate)
    def wrapper(func):
        if event_predicate not in _HANDLERS:
            _HANDLERS[event_predicate] = set()
        _HANDLERS[event_predicate].add(func)
        logger.info(
            f"Handler {func.__name__} registered with filter {event_predicate.__name__}"
        )
        return func

    if subscriber:
        return wrapper(subscriber)

    return wrapper


async def publish(event: Event):
    matching_handlers = set()
    for event_predicate, handlers in _HANDLERS.items():
        if event_predicate(event):
            matching_handlers.update(handlers)

    for handler in matching_handlers:
        if asyncio.iscoroutinefunction(handler):
            await handler(event)
        else:
            handler(event)

