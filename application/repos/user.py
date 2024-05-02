import abc
from typing import Optional
from uuid import UUID

from sqlalchemy import select, Result, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from application.domain.entities.user import User as DomainUser
from application.repos.models.user import User


class AbstractUserRepository(abc.ABC):

    @abc.abstractmethod
    async def get(self, user_oid: UUID) -> Optional[DomainUser]:
        raise NotImplemented

    @abc.abstractmethod
    async def get_multi(self, user_oids: list[UUID]) -> list[DomainUser]:
        raise NotImplemented

    @abc.abstractmethod
    async def put(self, user: DomainUser) -> DomainUser:
        raise NotImplemented

    @abc.abstractmethod
    async def delete(self, user_oid: UUID) -> None:
        raise NotImplemented

    @abc.abstractmethod
    async def all(self) -> list[DomainUser]:
        raise NotImplemented


class SQLAlchemyUserRepository(AbstractUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, user_oid: UUID) -> Optional[DomainUser]:
        query = select(User).where(User.oid == user_oid)
        result = await self.session.execute(query)
        user_model: Optional[User] = result.scalar_one_or_none()
        if user_model:
            return user_model.to_entity()

    async def get_multi(self, user_oids: list[UUID]) -> list[DomainUser]:
        query = select(User).where(User.oid.in_(user_oids))
        result: Result = await self.session.execute(query)
        if result:
            return [user.to_entity() for user in result.scalars().all()]

    async def put(self, user: DomainUser) -> DomainUser:
        updated_user: dict[str, str] = User.to_dict(user=user)
        stmt = update(User).where(User.oid == user.oid).values(updated_user)
        await self.session.execute(stmt)
        return user

    async def delete(self, user_oid: UUID) -> None:
        stmt = delete(User).where(User.oid == user_oid)
        await self.session.execute(stmt)

    async def all(self) -> list[DomainUser]:
        result: Result = await self.session.execute(select(User))
        return [user.to_entity() for user in result.scalars().all()]
