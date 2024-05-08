from abc import ABC, abstractmethod
from uuid import UUID

from .category_ad import Category as DomainCategory


class AbstractCategoryAdRepository(ABC):

    @abstractmethod
    async def add(self, category_ad: DomainCategory) -> DomainCategory:
        raise NotImplemented

    @abstractmethod
    async def get(self, category_oid: UUID) -> DomainCategory | None:
        raise NotImplemented

    @abstractmethod
    async def delete(self, category_oid: UUID) -> None:
        raise NotImplemented

    @abstractmethod
    async def get_by_params(self, params: dict, fields: tuple) -> list[DomainCategory]:
        raise NotImplemented
