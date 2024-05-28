from typing import Annotated

from fastapi import APIRouter, Depends, status

from application.context import get_payload_current_user
from application.exceptions.domain import AccessDeniedError

from application.services.user import UserService, get_user_service
from application.web.views.user.schemas import UserOutput


router = APIRouter(prefix="/user",
                   tags=["User"])


@router.get(path="/",
            summary="Получение пользователя",
            response_model=UserOutput,
            status_code=status.HTTP_200_OK)
async def get_user(user_service: Annotated[UserService, Depends(get_user_service)],
                   current_user: Annotated[dict, Depends(get_payload_current_user)],
                   user_oid: str) -> UserOutput:
    if current_user.get("sub") == user_oid or current_user.get("role") in ("ADMIN", "MODERATOR"):
        user = await user_service.get_user_by_id(user_oid=user_oid)
        return UserOutput.to_schema(user)

    raise AccessDeniedError


@router.get(path="/me",
            summary="Получение данных текущего пользователя",
            status_code=status.HTTP_200_OK)
async def get_current_auth_user(current_user: Annotated[dict, Depends(get_payload_current_user)]) -> dict:
    return {
        "id": current_user["sub"],
        "first_name": current_user["first_name"],
        "email": current_user["email"],
        "role": current_user["role"]
    }


@router.post(path="/search",
             summary="Поиск пользователей",
             response_model=list[UserOutput],
             status_code=status.HTTP_200_OK)
async def search_users(user_service: Annotated[UserService, Depends(get_user_service)],
                       user_oids: list[str]) -> list[UserOutput]:
    users = await user_service.get_multi_users_by_id(user_oids)
    return [UserOutput.to_schema(user) for user in users]


@router.delete(path="/",
               summary="Удаление пользователя",
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_oid: str,
                      user_service: Annotated[UserService, Depends(get_user_service)],
                      current_user: Annotated[dict, Depends(get_payload_current_user)]) -> None:
    if current_user.get("sub") == user_oid or current_user.get("role") == "ADMIN":
        return await user_service.delete_user_by_id(user_oid)

    raise AccessDeniedError
