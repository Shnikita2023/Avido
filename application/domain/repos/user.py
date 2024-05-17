from abc import ABC, abstractmethod
from typing import Optional, Any

from application.domain.entities.user import User as DomainUser


class AbstractUserRepository(ABC):

    @abstractmethod
    async def add(self, user: DomainUser) -> DomainUser:
        raise NotImplemented

    @abstractmethod
    async def get(self, user_oid: str) -> DomainUser | None:
        raise NotImplemented

    @abstractmethod
    async def get_multi(self, user_oids: list[str]) -> list[DomainUser]:
        raise NotImplemented

    @abstractmethod
    async def get_one_by_any_params(self, params: dict[str, Any]) -> Optional[DomainUser]:
        raise NotImplemented

    @abstractmethod
    async def get_one_by_all_params(self, params: dict[str, Any]) -> Optional[DomainUser]:
        raise NotImplemented

    @abstractmethod
    async def all(self) -> list[DomainUser] | None:
        raise NotImplemented

    @abstractmethod
    async def update(self, user: DomainUser) -> DomainUser:
        raise NotImplemented

    @abstractmethod
    async def delete(self, user_oid: str) -> None:
        raise NotImplemented

    @abstractmethod
    async def search_all(self, offset: int, limit: int, **params) -> DomainUser | None:
        raise NotImplemented
