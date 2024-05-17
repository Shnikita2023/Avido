from typing import Optional, Any
from uuid import UUID

from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from application.domain.entities.category_ad import Category as DomainCategory
from application.domain.repos.category_ad import AbstractCategoryAdRepository
from application.exceptions.db import DBError
from application.repos.models import Category


class SQLAlchemyCategoryAdRepository(AbstractCategoryAdRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, category_ad: DomainCategory) -> DomainCategory:
        try:
            category_model: Category = Category.from_entity(category_ad)
            self.session.add(category_model)
            return category_ad

        except SQLAlchemyError as exc:
            raise DBError(exc)

    async def get(self, category_oid: str) -> DomainCategory | None:
        try:
            query = select(Category).where(Category.oid == category_oid)
            result = await self.session.execute(query)
            category_model: Optional[Category] = result.scalar_one_or_none()
            if category_model:
                return category_model.to_entity()

        except SQLAlchemyError as exc:
            raise DBError(exc)

    async def delete(self, category_oid: str) -> None:
        try:
            stmt = delete(Category).where(Category.oid == category_oid)
            await self.session.execute(stmt)

        except SQLAlchemyError as exc:
            raise DBError(exc)

    async def get_by_params(self, params: dict[str, Any]) -> Optional[DomainCategory]:
        try:
            query = select(Category).filter_by(**params)
            result = await self.session.execute(query)
            category_model: Optional[Category] = result.scalar_one_or_none()
            if category_model:
                return category_model.to_entity()

        except SQLAlchemyError as exc:
            raise DBError(exc)
