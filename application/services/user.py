from uuid import UUID

from application.domain.entities.user import User as DomainUser
from application.repos.user import AbstractUserRepository


class UserService:
    def __init__(self, user_repository: AbstractUserRepository):
        self.user_repository = user_repository

    async def get_user_by_id(self, user_oid: UUID) -> DomainUser:
        user = await self.user_repository.get(user_oid)
        return user
