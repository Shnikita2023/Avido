from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer

from application.context import user as user_context
from application.exceptions.domain import AccessDeniedError
from application.services.user.token.schemas import TokenInfo
from application.services.user.token.token_jwt import token_work
from application.services.user import UserService, get_user_service
from application.web.views.user.schemas import UserOutput, UserInput

http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(prefix="/user",
                   tags=["User"],
                   dependencies=[Depends(http_bearer)])


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
async def login_user(user: Annotated[UserOutput, Depends(UserService().validate_auth_user)]) -> TokenInfo:
    access_token, refresh_token = token_work.create_tokens(user=user)
    return TokenInfo(access_token=access_token, refresh_token=refresh_token)


@router.post(path="/refresh",
             response_model=TokenInfo,
             response_model_exclude_none=True,
             summary="Обновление access токена",
             status_code=status.HTTP_200_OK)
async def refresh_access_token(payload: Annotated[dict, Depends(token_work.get_current_token_payload)]) -> TokenInfo:
    access_token = token_work.refresh_access_token(payload)
    return TokenInfo(access_token=access_token)


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
