from abc import ABC, abstractmethod
from typing import Any, Optional

from application.domain.entities.ad import Advertisement as DomainAdvertisement


class AbstractAdvertisementRepository(ABC):

    @abstractmethod
    async def add(self, advertisement: DomainAdvertisement) -> DomainAdvertisement:
        raise NotImplemented

    @abstractmethod
    async def get(self, advertisement_oid: str) -> DomainAdvertisement | None:
        raise NotImplemented

    @abstractmethod
    async def all(self) -> list[DomainAdvertisement] | None:
        raise NotImplemented

    @abstractmethod
    async def delete(self, advertisement_oid: str) -> None:
        raise NotImplemented

    @abstractmethod
    async def get_all_by_params(self, params: dict[str, Any], offset: int, limit: int) -> list[DomainAdvertisement]:
        raise NotImplemented

    @abstractmethod
    async def get_one_by_all_params(self, params: dict[str, Any]) -> Optional[DomainAdvertisement]:
        raise NotImplemented

    @abstractmethod
    async def update(self, user: DomainAdvertisement) -> DomainAdvertisement:
        raise NotImplemented
