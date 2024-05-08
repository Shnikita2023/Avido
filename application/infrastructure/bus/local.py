import asyncio
import datetime as dt
import itertools as it
import logging
import typing as t
from dataclasses import dataclass, field
from functools import wraps

logger = logging.getLogger(__name__)


@dataclass
class Event:
    timestamp: dt.datetime | None = field(default_factory=dt.datetime.utcnow)

    def __hash__(self):
        return hash(tuple(it.chain(self.__dict__.items(), [type(self)])))


@dataclass
class DomainEvent(Event):
    ...


@dataclass
class DomainCommand(Event):
    ...


_HANDLERS = {}


def subscribe(event_predicate: t.Callable, subscriber: t.Optional[t.Callable] = None) -> t.Optional[t.Callable]:
    """Subscribe to events.

    Args:
        event_predicate: A callable predicate which is used to identify the events to which to subscribe.
        subscriber: A unary callable function which handles the passed event (function-based).
    """
    @wraps(event_predicate)
    def wrapper(func):
        """
        Args:
            func: A unary callable function which handles the passed event (decorator-based).
        """
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



async def publish(event):
    """Send an event to all subscribers.

    Each subscriber will receive each event only once, even if it has been subscribed multiple
    times, possibly with different predicates.

    Args:
        event: The object to be tested against by all registered predicate functions and sent to
            all matching subscribers.
    """
    matching_handlers = set()
    for event_predicate, handlers in _HANDLERS.items():
        if event_predicate(event):
            matching_handlers.update(handlers)

    for handler in matching_handlers:
        if asyncio.iscoroutinefunction(handler):
            await handler(event)
        else:
            handler(event)
