from abc import ABC, abstractmethod
from uuid import UUID

from .ad import Advertisement as DomainAdvertisement


class AbstractAdvertisementRepository(ABC):

    @abstractmethod
    async def add(self, advertisement: DomainAdvertisement) -> DomainAdvertisement:
        raise NotImplemented

    @abstractmethod
    async def get(self, advertisement_oid: UUID) -> DomainAdvertisement | None:
        raise NotImplemented

    @abstractmethod
    async def all(self) -> list[DomainAdvertisement] | None:
        raise NotImplemented

    @abstractmethod
    async def delete(self, advertisement_oid: UUID) -> None:
        raise NotImplemented

    @abstractmethod
    async def get_by_params(self, params:  dict[str, str | UUID]) -> list[DomainAdvertisement]:
        raise NotImplemented

    @abstractmethod
    async def update(self, user: DomainAdvertisement) -> DomainAdvertisement:
        raise NotImplemented
