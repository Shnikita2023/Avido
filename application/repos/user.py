from typing import Optional, Any
from uuid import UUID

from sqlalchemy import select, Result, update, delete, or_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from application.domain.entities.user import User as DomainUser
from application.domain.repos.user import AbstractUserRepository
from application.exceptions.db import DBError
from application.repos.models.user import User


class SQLAlchemyUserRepository(AbstractUserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, user: DomainUser) -> DomainUser:
        try:
            user_model: User = User.from_entity(user)
            self.session.add(user_model)
            return user

        except SQLAlchemyError as exc:
            raise DBError(exc)

    async def get(self, user_oid: str) -> DomainUser | None:
        try:
            query = select(User).where(User.oid == user_oid)
            result = await self.session.execute(query)
            user_model: Optional[User] = result.scalar_one_or_none()
            if user_model:
                return user_model.to_entity()

        except SQLAlchemyError as exc:
            raise DBError(exc)

    async def get_one_by_any_params(self, params: dict[str, Any]) -> Optional[DomainUser]:
        try:
            filters = [getattr(User, field) == value for field, value in params.items()]
            query = select(User).where(or_(*filters))
            result = await self.session.execute(query)
            user_model: Optional[User] = result.scalar_one_or_none()
            if user_model:
                return user_model.to_entity()

        except SQLAlchemyError as exc:
            raise DBError(exc)

    async def get_one_by_all_params(self, params: dict[str, Any]) -> Optional[DomainUser]:
        try:
            query = select(User).filter_by(**params)
            result = await self.session.execute(query)
            user_model: Optional[User] = result.scalar_one_or_none()
            if user_model:
                return user_model.to_entity()

        except SQLAlchemyError as exc:
            raise DBError(exc)

    async def get_multi(self, user_oids: list[UUID]) -> list[DomainUser]:
        try:
            query = select(User).where(User.oid.in_(user_oids))
            result: Result = await self.session.execute(query)
            return [user.to_entity() for user in result.scalars().all()]

        except SQLAlchemyError as exc:
            raise DBError(exc)

    async def all(self) -> list[DomainUser]:
        try:
            result: Result = await self.session.execute(select(User))
            return [user.to_entity() for user in result.scalars().all()]

        except SQLAlchemyError as exc:
            raise DBError(exc)

    async def update(self, user: DomainUser) -> DomainUser:
        try:
            updated_user: dict[str, str] = User.to_dict(user=user)
            stmt = update(User).where(User.oid == user.oid).values(updated_user)
            await self.session.execute(stmt)
            return user

        except SQLAlchemyError as exc:
            raise DBError(exc)

    async def delete(self, user_oid: UUID) -> None:
        try:
            stmt = delete(User).where(User.oid == user_oid)
            await self.session.execute(stmt)

        except SQLAlchemyError as exc:
            raise DBError(exc)

    async def search_all(self, offset: int = 0, limit: int = 1, **params: dict) -> list[DomainUser]:
        try:
            query = select(User).filter_by(**params).offset(offset).limit(limit)
            result: Result = await self.session.execute(query)
            return [user.to_entity() for user in result.scalars().all()]

        except SQLAlchemyError as exc:
            raise DBError(exc)
