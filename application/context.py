from contextvars import ContextVar, Token
from typing import Generic, TypeVar

ContextVarType = TypeVar("ContextVarType")


class ContextWrapper(Generic[ContextVarType]):

    def __init__(self, variable: ContextVar):
        self.__variable: ContextVar = variable

    def set(self, value: ContextVarType) -> Token:
        return self.__variable.set(value)

    @property
    def value(self) -> ContextVarType:
        return self.__variable.get()


user: ContextWrapper[dict] = ContextWrapper(ContextVar("user", default=None))


def get_payload_current_user() -> dict | None:
    if not user:
        return None

    return user.value
