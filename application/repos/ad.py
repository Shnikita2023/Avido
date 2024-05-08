from typing import Optional
from uuid import UUID

from sqlalchemy import select, delete, update, Result
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from application.domain.ad.ad import Advertisement as DomainAdvertisement
from application.domain.ad.ad_repository import AbstractAdvertisementRepository
from application.exceptions.db import DBError
from application.repos.models import Advertisement


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

    async def all(self) -> list[DomainAdvertisement]:
        try:
            result: Result = await self.session.execute(select(Advertisement))
            return [advertisement.to_entity() for advertisement in result.scalars().all()]

        except SQLAlchemyError as exc:
            raise DBError(exc)

    async def get_by_params(self, params: dict[str, str | UUID]) -> list[DomainAdvertisement]:
        try:
            query = select(Advertisement).filter_by(**params)
            result = await self.session.execute(query)
            return [advertisement.to_entity() for advertisement in result.scalars().all()]

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
