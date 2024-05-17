from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Response, Depends, status

from application.exceptions.domain import InvalidCookieError, AccessDeniedError
from application.services.user.token.cookie_token import cookie_helper
from application.services.user.token.schemas import TokenInfo
from application.services.user.token.token_jwt import token_work
from application.services.user.user import user_service
from application.web.views.user.schemas import UserOutput, UserInput


router = APIRouter(prefix="/user",
                   tags=["User"])


@router.get(path="/",
            summary="Получение пользователя",
            response_model=UserOutput,
            status_code=status.HTTP_200_OK)
async def get_user(current_user: Annotated[dict, Depends(user_service.get_current_auth_user)],
                   user_oid: UUID) -> UserOutput:
    if current_user.get("sub") == user_oid or current_user.get("role") in ("ADMIN", "MODERATOR"):
        return await user_service.get_user_by_id(user_oid=user_oid)

    raise AccessDeniedError


@router.post(path="/",
             summary="Регистрация пользователя",
             response_model=UserOutput,
             status_code=status.HTTP_201_CREATED)
async def add_user(user_schema: UserInput) -> UserOutput:
    return await user_service.create_user(user_schema=user_schema)


@router.post(path="/login",
             response_model=TokenInfo,
             summary="Аутентификация пользователя",
             status_code=status.HTTP_200_OK)
async def login_user(response: Response,
                     user: Annotated[UserOutput, Depends(user_service.validate_auth_user)]) -> TokenInfo:
    access_token, refresh_token = token_work.create_tokens(user=user, response=response)
    return TokenInfo(access_token=access_token, refresh_token=refresh_token)


@router.get(path="/me",
            summary="Получение данных о пользователе",
            status_code=status.HTTP_200_OK)
async def get_current_auth_user(response: Response,
                                current_user: Annotated[dict, Depends(user_service.get_current_auth_user)]) -> dict:
    if current_user:
        return {
            "id": current_user["sub"],
            "first_name": current_user["first_name"],
            "email": current_user["email"],
            "role": current_user["role"]
        }
    raise InvalidCookieError


@router.get(path="/logout",
            summary="Выход пользователя",
            status_code=status.HTTP_200_OK)
async def logout_user(response: Response,
                      current_user: Annotated[dict, Depends(cookie_helper.get_cookie_tokens)]) -> dict[str, str]:
    if current_user:
        response.delete_cookie(cookie_helper.COOKIE_SESSION_KEY)
        return {"message": "logout successful"}

    raise InvalidCookieError


@router.post(path="/search",
             summary="Поиск пользователей",
             response_model=list[UserOutput],
             status_code=status.HTTP_200_OK)
async def search_users(user_oids: list[UUID]) -> list[UserOutput]:
    return await user_service.get_multi_users_by_id(user_oids)


@router.delete(path="/",
               summary="Удаление пользователя",
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_oid: UUID,
                      current_user: Annotated[dict, Depends(user_service.get_current_auth_user)]) -> None:
    if current_user.get("sub") == user_oid or current_user.get("role") == "ADMIN":
        return await user_service.delete_user_by_id(user_oid)


