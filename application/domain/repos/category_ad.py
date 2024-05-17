from abc import ABC, abstractmethod
from typing import Any, Optional

from application.domain.entities.category_ad import Category as DomainCategory


class AbstractCategoryAdRepository(ABC):

    @abstractmethod
    async def add(self, category_ad: DomainCategory) -> DomainCategory:
        raise NotImplemented

    @abstractmethod
    async def get(self, category_oid: str) -> DomainCategory | None:
        raise NotImplemented

    @abstractmethod
    async def delete(self, category_oid: str) -> None:
        raise NotImplemented

    @abstractmethod
    async def get_by_params(self, params: dict[str, Any]) -> Optional[DomainCategory]:
        raise NotImplemented
