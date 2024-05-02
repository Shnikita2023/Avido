from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from application.infrastructure.base import get_async_session
from application.repos.user import SQLAlchemyUserRepository
from application.services.user import UserService

router = APIRouter(prefix="/user",
                   tags=["User"])


@router.get(path="/")
async def get_user(user_oid: UUID,
                   session: Annotated[AsyncSession, Depends(get_async_session)]):
    repo = SQLAlchemyUserRepository(session=session)
    service = UserService(user_repository=repo)
    return await service.get_user_by_id(user_oid=user_oid)
