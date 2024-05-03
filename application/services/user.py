from uuid import UUID

from pydantic import EmailStr

from application.domain.entities.user import User as DomainUser, Role, Status, User
from application.exceptions.domain.user import UserNotFoundError, UserAlreadyExistsError
from application.infrastructure.unit_of_work_manager import get_unit_of_work
from application.services.uof.unit_of_work import AbstractUnitOfWork
from application.web.schemas.user import UserCreate, UserShow, UserUpdate


class UserService:

    uow: AbstractUnitOfWork

    def __init__(self, uow=None):
        self.uow = uow if uow else await get_unit_of_work()

    async def get_user_by_id(self, user_oid: UUID) -> User:
        async with self.uow:
            user = await self.uow.users.get(user_oid)
            if user:
                return UserShow.from_entity(user)

            raise UserNotFoundError

    async def get_multi_users_by_id(self, user_oids: list[UUID]) -> list[User]:
        async with self.uow:
            users: list[DomainUser] = await self.uow.users.get_multi(user_oids)
            if users:
                return [UserShow.from_entity(user) for user in users]
            raise UserNotFoundError

    @staticmethod
    async def get_all_users(uow: AbstractUnitOfWork) -> list[User]:
        async with uow:
            users: list[DomainUser] = await uow.users.all()
            if users:
                return [UserShow.from_entity(user) for user in users]

            raise UserNotFoundError

    @staticmethod
    async def update_user(cls, user_oid: UUID, data: UserUpdate, uow: AbstractUnitOfWork) -> UserShow:
        user_entity: DomainUser = cls._create_domain_user(data)
        user_entity.oid = user_oid
        async with uow:
            user: DomainUser = await uow.users.put(user=user_entity)
            return UserShow.from_entity(user)

    @classmethod
    async def delete_user_by_id(cls, user_oid: UUID, uow: AbstractUnitOfWork) -> None:
        await cls.get_user_by_id(user_oid, uow)
        async with uow:
            await uow.users.delete(user_oid)
            await uow.commit()

    @classmethod
    async def create_user(cls, data: UserCreate, uow: AbstractUnitOfWork):
        async with uow:
            await cls._check_existing_user(user_email=data.email, uow=uow)
            user_entity: DomainUser = cls._create_domain_user(data)
            await uow.users.add(user_entity)
            await uow.commit()

    @staticmethod
    async def _check_existing_user(user_email: EmailStr, uow: AbstractUnitOfWork) -> None:
        params = {"email": user_email}
        user = await uow.users.search(**params)
        if user:
            raise UserAlreadyExistsError()

    @staticmethod
    def _create_domain_user(data: UserCreate | UserUpdate) -> DomainUser:
        return DomainUser(
            first_name=data.first_name,
            last_name=data.last_name,
            middle_name=data.middle_name,
            email=data.email,
            role=Role.USER,
            number_phone=data.number_phone,
            time_call=data.time_call,
            status=Status.PENDING
        )
