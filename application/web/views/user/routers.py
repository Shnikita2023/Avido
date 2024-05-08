import logging
from uuid import UUID

from fastapi import APIRouter, status

from application.services.user import user_service
from application.web.views.user.schemas import UserOutput, UserInput

router = APIRouter(prefix="/user",
                   tags=["User"])

logger = logging.getLogger(__name__)


@router.get(path="/",
            summary="Получение пользователя",
            status_code=status.HTTP_200_OK,
            response_model=UserOutput)
async def get_user(user_oid: UUID) -> UserOutput:
    return await user_service.get_user_by_id(user_oid=user_oid)


@router.post(path="/",
             summary="Cоздание пользователя",
             status_code=status.HTTP_201_CREATED,
             response_model=UserOutput)
async def add_user(user: UserInput) -> UserOutput:
    return await user_service.create_user(data=user)


@router.post(path="/search",
             summary="Поиск пользователей",
             status_code=status.HTTP_200_OK,
             response_model=list[UserOutput])
async def search_users(user_oids: list[UUID]) -> list[UserOutput]:
    return await user_service.get_multi_users_by_id(user_oids)


@router.delete(path="/",
               summary="Удаление пользователя",
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_oid: UUID) -> None:
    return await user_service.delete_user_by_id(user_oid)
