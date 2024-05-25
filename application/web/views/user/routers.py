from typing import Annotated

from fastapi import APIRouter, Depends, status

from application.context import get_payload_current_user
from application.domain.entities.user import User as DomainUser
from application.exceptions.domain import AccessDeniedError

from application.services.user import UserService, get_user_service
from application.web.services.token.schemas import TokenInfo
from application.web.services.token.token_jwt import token_manager, ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE
from application.web.views.user.schemas import UserOutput, UserInput


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


@router.post(path="/sign-up",
             summary="Регистрация пользователя",
             response_model=UserOutput,
             status_code=status.HTTP_201_CREATED)
async def add_user(user_service: Annotated[UserService, Depends(get_user_service)],
                   user_schema: UserInput) -> UserOutput:
    user = await user_service.create_user(user=user_schema.to_domain())
    return UserOutput.to_schema(user)


@router.post(path="/login",
             response_model=TokenInfo,
             summary="Аутентификация пользователя",
             status_code=status.HTTP_200_OK)
async def login_user(user: Annotated[DomainUser, Depends(UserService().validate_auth_user)]) -> TokenInfo:
    user_schema = UserOutput.to_schema(user)
    access_token = token_manager.create_token(user_schema=user_schema, type_token=ACCESS_TOKEN_TYPE)
    refresh_token = token_manager.create_token(user_schema=user_schema, type_token=REFRESH_TOKEN_TYPE)
    return TokenInfo(access_token=access_token, refresh_token=refresh_token)


@router.post(path="/refresh",
             response_model=TokenInfo,
             response_model_exclude_none=True,
             summary="Обновление access токена",
             status_code=status.HTTP_200_OK)
async def refresh_access_token(payload: Annotated[dict, Depends(token_manager.get_current_token_payload)]) -> TokenInfo:
    user_schema = await token_manager.get_auth_user_from_token_of_type(payload, REFRESH_TOKEN_TYPE)
    access_token = token_manager.create_token(user_schema=user_schema, type_token=ACCESS_TOKEN_TYPE)
    return TokenInfo(access_token=access_token)


@router.get(path="/me",
            summary="Получение данных о пользователе",
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
