from abc import ABC, abstractmethod
from uuid import UUID

from .user import User as DomainUser


class AbstractUserRepository(ABC):

    @abstractmethod
    async def add(self, user: DomainUser) -> DomainUser:
        raise NotImplemented

    @abstractmethod
    async def get(self, user_oid: UUID) -> DomainUser | None:
        raise NotImplemented

    @abstractmethod
    async def get_multi(self, user_oids: list[UUID]) -> list[DomainUser]:
        raise NotImplemented

    @abstractmethod
    async def get_by_params(self, params: dict, fields: tuple) -> list[DomainUser]:
        raise NotImplemented

    @abstractmethod
    async def update(self, user: DomainUser) -> DomainUser:
        raise NotImplemented

    @abstractmethod
    async def delete(self, user_oid: UUID) -> None:
        raise NotImplemented

    @abstractmethod
    async def all(self) -> list[DomainUser] | None:
        raise NotImplemented

    @abstractmethod
    async def search(self, offset: int, limit: int, **params) -> DomainUser | None:
        raise NotImplemented
