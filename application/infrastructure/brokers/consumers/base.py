from abc import ABC, abstractmethod
from typing import Any, Callable

from typing_extensions import Coroutine


class Consumer(ABC):
    @abstractmethod
    async def initialization(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_message(self, handling_message: Callable[..., Coroutine[Any, Any, None]]) -> None:
        raise NotImplementedError

    @abstractmethod
    async def finalization(self) -> None:
        raise NotImplementedError
