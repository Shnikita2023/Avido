from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from sqlalchemy import select, delete, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from application.domain.entities.ad import Advertisement as DomainAdvertisement
from application.exceptions.db import DBError
from application.repos.models import Advertisement


class AbstractAdvertisementRepository(ABC):

    @abstractmethod
    async def add(self, advertisement: DomainAdvertisement) -> DomainAdvertisement:
        raise NotImplemented

    @abstractmethod
    async def get(self, advertisement_oid: UUID) -> DomainAdvertisement | None:
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


class SQLAlchemyAdvertisementRepository(AbstractAdvertisementRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, advertisement: DomainAdvertisement) -> DomainAdvertisement:
        try:
            advertisement_model: Advertisement = Advertisement.from_entity(advertisement)
            self.session.add(advertisement_model)
            return advertisement

        except SQLAlchemyError as exc:
            raise DBError(exc)

    async def get(self, advertisement_oid: UUID) -> DomainAdvertisement | None:
        try:
            query = select(Advertisement).where(Advertisement.oid == advertisement_oid)
            result = await self.session.execute(query)
            advertisement_model: Optional[Advertisement] = result.scalar_one_or_none()
            if advertisement_model:
                return advertisement_model.to_entity()

        except SQLAlchemyError as exc:
            raise DBError(exc)

    async def delete(self, advertisement_oid: UUID) -> None:
        try:
            stmt = delete(Advertisement).where(Advertisement.oid == advertisement_oid)
            await self.session.execute(stmt)

        except SQLAlchemyError as exc:
            raise DBError(exc)

    async def get_by_params(self, params: dict[str, str | UUID]) -> list[DomainAdvertisement]:
        try:
            query = select(Advertisement).filter_by(**params)
            result = await self.session.execute(query)
            return [category_ad.to_entity() for category_ad in result.scalars().all()]

        except SQLAlchemyError as exc:
            raise DBError(exc)

    async def update(self, advertisement: DomainAdvertisement) -> DomainAdvertisement:
        try:
            updated_user: dict[str, str] = Advertisement.to_dict(advertisement=advertisement)
            stmt = update(Advertisement).where(Advertisement.oid == advertisement.oid).values(updated_user)
            await self.session.execute(stmt)
            return advertisement

        except SQLAlchemyError as exc:
            raise DBError(exc)
