import logging
from typing import Optional, Any, Annotated

from fastapi import Form, Response, Depends

from application.domain.entities.user import User as DomainUser
from application.exceptions.domain import (
    UserNotFoundError, UserAlreadyExistsError, InvalidUserDataError,
    InvalidCookieError, AccessDeniedError
)
from application.infrastructure.unit_of_work_manager import get_unit_of_work
from application.repos.uow.unit_of_work import AbstractUnitOfWork
from application.services.user.security.password_utils import hash_password, compare_passwords
from application.services.user.token.token_jwt import token_work
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
                return user.to_schema()

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

            user: DomainUser = DomainUser.to_entity(user_schema)
            user.encrypt_password()
            await self.uow.users.add(user)
            await self.uow.commit()
            await self._on_after_create_user(user_schema)
            logger.info(f"Пользователь с id {user_entity.oid} успешно создан. Status: 201")
            return user_entity.to_schema()

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
            return user.to_schema()

    async def get_current_auth_user(self,
                                    payload: Annotated[Optional[dict], Depends(token_work.get_current_token_payload)]) -> dict:
        if payload:
            user_oid: str = payload.get("sub")
            async with self.uow:
                user: UserOutput = await self.get_user_by_id(user_oid)

            logger.info(f"Получение данных о пользователе '{user.first_name}'. Status: 200")
            return payload

        return {}

    @staticmethod
    async def check_authentication(user_current: dict, role_required: tuple = ("USER",)) -> None:
        if not user_current:
            raise InvalidCookieError

        if user_current.get("role") not in role_required:
            raise AccessDeniedError


user_service = UserService()
