import logging
from typing import Optional, Any

from fastapi import Form

from application.context import user as user_context
from application.domain.entities.user import User as DomainUser
from application.exceptions.domain import (
    UserNotFoundError, UserAlreadyExistsError,
    AccessDeniedError, InvalidUserDataError,
)
from application.infrastructure.unit_of_work_manager import get_unit_of_work
from application.repos.uow.unit_of_work import AbstractUnitOfWork
from application.web.views.user.schemas import UserOutput, UserInput

logger = logging.getLogger(__name__)


class UserService:
    uow: AbstractUnitOfWork

    def __init__(self, uow=None):
        self.uow = uow if uow else get_unit_of_work()

    async def get_user_by_id(self, user_oid: str) -> UserOutput:
        async with self.uow:
            user: Optional[DomainUser] = await self.uow.users.get(user_oid)
            if user:
                return UserOutput.to_schema(user)

            raise UserNotFoundError

    async def get_multi_users_by_id(self, user_oids: list[str]) -> list[UserOutput]:
        async with self.uow:
            users: list[DomainUser] = await self.uow.users.get_multi(user_oids)
            if users:
                return [user.to_schema() for user in users]

            raise UserNotFoundError

    async def get_all_users(self) -> list[UserOutput]:
        async with self.uow:
            users: list[DomainUser] = await self.uow.users.all()
            if users:
                return [user.to_schema() for user in users]

            raise UserNotFoundError

    async def update_user(self, user_oid: str, data: UserInput) -> UserOutput:
        user_entity: DomainUser = DomainUser.to_entity(data)
        user_entity.oid = user_oid
        async with self.uow:
            await self.uow.users.update(user=user_entity)
            await self.uow.commit()
            return user_entity.to_schema()

    async def delete_user_by_id(self, user_oid: str) -> None:
        await self.get_user_by_id(user_oid)
        async with self.uow:
            await self.uow.users.delete(user_oid)
            await self.uow.commit()
            return None

    async def create_user(self, user_schema: UserInput) -> UserOutput:
        async with self.uow:
            params_search = {"email": user_schema.email, "number_phone": user_schema.number_phone}
            existing_user = await self._check_existing_user(params_search)
            if existing_user:
                raise UserAlreadyExistsError

            user: DomainUser = user_schema.to_domain()
            user.encrypt_password()
            await self.uow.users.add(user)
            await self.uow.commit()
            await self._on_after_create_user(user_schema)
            logger.info(f"Пользователь с id {user.oid} успешно создан. Status: 201")
            return UserOutput.to_schema(user)

    @staticmethod
    async def _on_after_create_user(user_schema: UserInput) -> None:
        pass

    async def _check_existing_user(self, params_search: dict[str, Any]) -> Optional[DomainUser]:
        return await self.uow.users.get_one_by_any_params(params_search)

    async def validate_auth_user(self,
                                 email: str = Form(),
                                 password: str = Form()) -> UserOutput:
        async with self.uow:
            params_search = {"email": email, "status": "ACTIVE"}
            user: DomainUser | None = await self.uow.users.get_one_by_all_params(params_search)
            if not user or email != user.email.value or not user.is_password_valid(password):
                raise InvalidUserDataError
            logger.info(f"Успешно пройдена валидация пользователя '{user.first_name}'. Status: 200")
            return UserOutput.to_schema(user)

    @staticmethod
    async def check_role(role: tuple = ("USER",)) -> None:
        user_current = user_context.value
        if user_current.get("role") not in role:
            raise AccessDeniedError


def get_user_service() -> UserService:
    return UserService()
