from typing import Annotated

from fastapi import APIRouter, Response, Depends, status

from application.context import user as user_context
from application.exceptions.domain import AccessDeniedError
from application.services.user.token.schemas import TokenInfo
from application.services.user.token.token_jwt import token_work
from application.services.user import UserService, get_user_service
from application.web.views.user.schemas import UserOutput, UserInput
from application.services.user.token.cookie import create_cookie_for_tokens
from application.config import settings

router = APIRouter(prefix="/user",
                   tags=["User"])


@router.get(path="/",
            summary="Получение пользователя",
            response_model=UserOutput,
            status_code=status.HTTP_200_OK)
async def get_user(user_service: Annotated[UserService, Depends(get_user_service)],
                   user_oid: str) -> UserOutput:
    current_user = user_context.value
    if current_user.get("sub") == user_oid or current_user.get("role") in ("ADMIN", "MODERATOR"):
        return await user_service.get_user_by_id(user_oid=user_oid)

    raise AccessDeniedError


@router.post(path="/sign-up",
             summary="Регистрация пользователя",
             response_model=UserOutput,
             status_code=status.HTTP_201_CREATED)
async def add_user(user_service: Annotated[UserService, Depends(get_user_service)],
                   user_schema: UserInput) -> UserOutput:
    return await user_service.create_user(user_schema=user_schema)


@router.post(path="/login",
             response_model=TokenInfo,
             summary="Аутентификация пользователя",
             status_code=status.HTTP_200_OK)
async def login_user(response: Response,
                     user: Annotated[UserOutput, Depends(UserService().validate_auth_user)]) -> TokenInfo:
    access_token, refresh_token = token_work.create_tokens(user=user)
    await create_cookie_for_tokens(response, access_token, refresh_token)
    return TokenInfo(access_token=access_token, refresh_token=refresh_token)


@router.get(path="/me",
            summary="Получение данных о пользователе",
            status_code=status.HTTP_200_OK)
async def get_current_auth_user() -> dict:
    current_user = user_context.value
    return {
        "id": current_user["sub"],
        "first_name": current_user["first_name"],
        "email": current_user["email"],
        "role": current_user["role"]
    }


@router.get(path="/logout",
            summary="Выход пользователя",
            status_code=status.HTTP_200_OK)
async def logout_user(response: Response) -> dict[str, str]:
    response.delete_cookie(settings.session_cookie.COOKIE_SESSION_KEY)
    return {"message": "logout successful"}


@router.post(path="/search",
             summary="Поиск пользователей",
             response_model=list[UserOutput],
             status_code=status.HTTP_200_OK)
async def search_users(user_service: Annotated[UserService, Depends(get_user_service)],
                       user_oids: list[str]) -> list[UserOutput]:
    return await user_service.get_multi_users_by_id(user_oids)


@router.delete(path="/",
               summary="Удаление пользователя",
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_oid: str,
                      user_service: Annotated[UserService, Depends(get_user_service)]) -> None:
    current_user = user_context.value
    if current_user.get("sub") == user_oid or current_user.get("role") == "ADMIN":
        return await user_service.delete_user_by_id(user_oid)

    raise AccessDeniedError
