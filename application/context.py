from contextvars import ContextVar, Token
from typing import Generic, TypeVar

from fastapi import Request

from .domain.models.users import User

ContextVarType = TypeVar("ContextVarType")


class ContextWrapper(Generic[ContextVarType]):

    def __init__(self, variable: ContextVar):
        self.__variable: ContextVar = variable

    def __module__(self):
        return self.__variable.get()

    def set(self, value: ContextVarType) -> Token:
        return self.__variable.set(value)

    def reset(self, token: Token) -> None:
        self.__variable.reset(token)

    @property
    def value(self) -> ContextVarType:
        return self.__variable.get()


user: ContextWrapper[User] = ContextWrapper(ContextVar("user", default=None))
request: ContextWrapper[Request] = ContextWrapper(ContextVar("request", default=None))

