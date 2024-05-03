from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from sqlalchemy import select, Result, update, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from application.domain.entities.user import User as DomainUser
from application.exceptions.repository.db import DBError
from application.repos.models.user import User


class AbstractUserRepository(ABC):

    @abstractmethod
    async def add(self, user: DomainUser) -> None:
        raise NotImplemented

    @abstractmethod
    async def get(self, user_oid: UUID) -> DomainUser | None:
        raise NotImplemented

    @abstractmethod
    async def get_multi(self, user_oids: list[UUID]) -> list[DomainUser]:
        raise NotImplemented

    @abstractmethod
    async def put(self, user: DomainUser) -> DomainUser:
        raise NotImplemented

    @abstractmethod
    async def delete(self, user_oid: UUID) -> None:
        raise NotImplemented

    @abstractmethod
    async def all(self) -> list[DomainUser] | None:
        raise NotImplemented

    @abstractmethod
    async def search(self, offset: int, limit: int, **params) -> DomainUser | None:
        raise NotImplemented


class SQLAlchemyUserRepository(AbstractUserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, user: DomainUser) -> None:
        try:
            user_model: User = User.from_entity(user)
            self.session.add(user_model)

        except SQLAlchemyError as exc:
            raise DBError(exc)

    async def get(self, user_oid: UUID) -> DomainUser | None:
        try:
            query = select(User).where(User.oid == user_oid)
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

    async def put(self, user: DomainUser) -> DomainUser:
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

    async def all(self) -> list[DomainUser]:
        try:
            result: Result = await self.session.execute(select(User))
            return [user.to_entity() for user in result.scalars().all()]

        except SQLAlchemyError as exc:
            raise DBError(exc)

    async def search(self, offset: int = 0, limit: int = 1, **params: dict) -> list[DomainUser]:
        try:
            query = select(User).filter_by(**params).offset(offset).limit(limit)
            result: Result = await self.session.execute(query)
            return [user.to_entity() for user in result.scalars().all()]

        except SQLAlchemyError as exc:
            raise DBError(exc)
