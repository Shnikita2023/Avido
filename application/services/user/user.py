import logging
from typing import Optional, Any

from application.context import get_payload_current_user
from application.domain.entities.user import User as DomainUser
from application.exceptions.domain import (
    UserNotFoundError, UserAlreadyExistsError,
    AccessDeniedError
)
from application.infrastructure.unit_of_work_manager import get_unit_of_work
from application.repos.uow.unit_of_work import AbstractUnitOfWork

logger = logging.getLogger(__name__)


class UserService:
    uow: AbstractUnitOfWork

    def __init__(self, uow=None):
        self.uow = uow if uow else get_unit_of_work()

    async def get_user_by_id(self, user_oid: str) -> DomainUser:
        async with self.uow:
            user: Optional[DomainUser] = await self.uow.users.get(user_oid)
            if user:
                return user

            raise UserNotFoundError

    async def get_multi_users_by_id(self, user_oids: list[str]) -> list[DomainUser]:
        async with self.uow:
            users: list[DomainUser] = await self.uow.users.get_multi(user_oids)
        return users

    async def get_all_users(self) -> list[DomainUser]:
        async with self.uow:
            users: list[DomainUser] = await self.uow.users.all()
        return users

    async def update_user(self, user_oid: str, new_user: DomainUser) -> DomainUser:
        new_user.oid = user_oid
        async with self.uow:
            await self.uow.users.update(new_user)
            await self.uow.commit()
        return new_user

    async def delete_user_by_id(self, user_oid: str) -> None:
        await self.get_user_by_id(user_oid)
        async with self.uow:
            await self.uow.users.delete(user_oid)
            await self.uow.commit()

    async def create_user(self, user: DomainUser) -> DomainUser:
        params_search = {"email": user.email, "number_phone": user.number_phone}
        async with self.uow:
            existing_user = await self._check_existing_user(params_search)
            if existing_user:
                raise UserAlreadyExistsError

            user.encrypt_password()
            await self.uow.users.add(user)
            await self.uow.commit()
            await self._on_after_create_user(user)
            logger.info(f"Пользователь с id {user.oid} успешно создан. Status: 201")
        return user

    @staticmethod
    async def _on_after_create_user(user_schema: DomainUser) -> None:
        pass

    async def _check_existing_user(self, params_search: dict[str, Any]) -> Optional[DomainUser]:
        return await self.uow.users.get_one_by_any_params(params_search)

    @staticmethod
    def check_role(role: tuple = ("USER",)) -> None:
        user_current = get_payload_current_user()
        if user_current.get("role") not in role:
            raise AccessDeniedError


def get_user_service() -> UserService:
    return UserService()
