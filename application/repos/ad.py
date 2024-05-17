from typing import Optional, Any

from sqlalchemy import select, delete, update, Result, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from application.domain.entities.ad import Advertisement as DomainAdvertisement
from application.domain.repos.ad import AbstractAdvertisementRepository
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

    async def get(self, advertisement_oid: str) -> DomainAdvertisement | None:
        try:
            query = select(Advertisement).where(Advertisement.oid == advertisement_oid)
            result = await self.session.execute(query)
            advertisement_model: Optional[Advertisement] = result.scalar_one_or_none()
            if advertisement_model:
                return advertisement_model.to_entity()

        except SQLAlchemyError as exc:
            raise DBError(exc)

    async def delete(self, advertisement_oid: str) -> None:
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

    async def get_all_by_params(self, params: dict[str, Any], offset: int, limit: int) -> list[DomainAdvertisement]:
        try:
            mapping_filter = {
                "price_from": lambda value_params: Advertisement.price >= value_params,
                "price_to": lambda value_params: Advertisement.price <= value_params,
                "category": lambda value_params: Advertisement.category == value_params,
                "city": lambda value_params: Advertisement.city == value_params,
            }
            filters = [Advertisement.status == "ACTIVE"]

            for name_field, value in params.items():
                if name_field in mapping_filter:
                    filters.append(mapping_filter[name_field](value))

            query = select(Advertisement).filter(and_(*filters)).offset(offset).limit(limit)
            result = await self.session.execute(query)
            return [advertisement.to_entity() for advertisement in result.scalars().all()]

        except SQLAlchemyError as exc:
            raise DBError(exc)

    async def get_one_by_all_params(self, params: dict[str, Any]) -> Optional[Advertisement]:
        try:
            query = select(Advertisement).filter_by(**params)
            result = await self.session.execute(query)
            ad_model: Optional[Advertisement] = result.scalar_one_or_none()
            if ad_model:
                return ad_model.to_entity()

        except SQLAlchemyError as exc:
            raise DBError(exc)

    async def update(self, advertisement: DomainAdvertisement) -> DomainAdvertisement:
        try:
            updated_ad: dict[str, str] = Advertisement.to_dict(advertisement=advertisement)
            stmt = update(Advertisement).where(Advertisement.oid == advertisement.oid).values(updated_ad)
            await self.session.execute(stmt)
            return advertisement

        except SQLAlchemyError as exc:
            raise DBError(exc)
