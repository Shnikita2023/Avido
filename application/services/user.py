from typing import Optional
from uuid import UUID

from pydantic import EmailStr

from application.domain.user.user import User as DomainUser
from application.exceptions.domain import UserNotFoundError, UserAlreadyExistsError
from application.infrastructure.unit_of_work_manager import get_unit_of_work
from .uof.unit_of_work import AbstractUnitOfWork
from application.web.views.user.schemas import UserOutput, UserInput


class UserService:

    uow: AbstractUnitOfWork

    def __init__(self, uow=None):
        self.uow = uow if uow else get_unit_of_work()

    async def get_user_by_id(self, user_oid: UUID) -> UserOutput:
        async with self.uow:
            user: Optional[DomainUser] = await self.uow.users.get(user_oid)
            if user:
                return user

            raise UserNotFoundError

    async def get_multi_users_by_id(self, user_oids: list[UUID]) -> list[UserOutput]:
        async with self.uow:
            users: list[DomainUser] = await self.uow.users.get_multi(user_oids)
            if users:
                return users

            raise UserNotFoundError

    async def get_all_users(self) -> list[UserOutput]:
        async with self.uow:
            users: list[DomainUser] = await self.uow.users.all()
            if users:
                return users

            raise UserNotFoundError

    async def update_user(self, user_oid: UUID, data: UserInput) -> UserOutput:
        user_entity: DomainUser = DomainUser.to_entity(data)
        user_entity.oid = user_oid
        async with self.uow:
            await self.uow.users.update(user=user_entity)
            await self.uow.commit()
            return user_entity

    async def delete_user_by_id(self, user_oid: UUID) -> None:
        await self.get_user_by_id(user_oid)
        async with self.uow:
            await self.uow.users.delete(user_oid)
            await self.uow.commit()

    async def create_user(self, data: UserInput) -> UserOutput:
        async with self.uow:
            await self._check_existing_user(user_email=data.email, phone=data.number_phone)
            user_entity: DomainUser = DomainUser.to_entity(data)
            await self.uow.users.add(user_entity)
            await self.uow.commit()
            return user_entity

    async def _check_existing_user(self, user_email: EmailStr, phone: str) -> None:
        params = {"email": user_email, "number_phone": phone}
        fields = ("email", "number_phone")
        user = await self.uow.users.get_by_params(params, fields)
        if user:
            raise UserAlreadyExistsError


user_service = UserService()
