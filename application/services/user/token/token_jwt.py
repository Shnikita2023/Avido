from abc import ABC, abstractmethod
from datetime import datetime, timedelta

import jwt
from fastapi import Request

from application.config import settings
from application.exceptions.domain import InvalidTokenError
from application.services.user.token.schemas import AccessToken, RefreshToken
from application.web.views.user.schemas import UserOutput


class TokenAbstractService(ABC):
    @abstractmethod
    def encode_token(self, payload: dict) -> str:
        raise NotImplemented

    @abstractmethod
    def decode_token(self, token: bytes | str) -> dict:
        raise NotImplemented


class TokenJWTService(TokenAbstractService):
    """
    Класс для кодирования/декодирование jwt токена
    """

    ACCESS_TOKEN_EXPIRE_MINUTE: int = settings.auth_jwt.ACCESS_TOKEN_EXPIRE_MINUTE
    REFRESH_TOKEN_EXPIRE_MINUTE: int = settings.auth_jwt.REFRESH_TOKEN_EXPIRE_MINUTE
    PRIVATE_KEY: str = settings.auth_jwt.PRIVATE_KEY.read_text()
    PUBLIC_KEY: str = settings.auth_jwt.PUBLIC_KEY.read_text()
    ALGORITHM: str = settings.auth_jwt.ALGORITHM

    @classmethod
    def encode_token(cls, payload: dict) -> str:

        if payload["type"] == "access":
            expire_minutes = cls.ACCESS_TOKEN_EXPIRE_MINUTE
        else:
            expire_minutes = cls.REFRESH_TOKEN_EXPIRE_MINUTE

        to_encode: dict = payload.copy()
        now_time: datetime = datetime.utcnow()
        expire_token: datetime = now_time + timedelta(minutes=expire_minutes)
        to_encode.update(exp=expire_token, iat=now_time)
        encoded: str = jwt.encode(payload=to_encode, key=cls.PRIVATE_KEY, algorithm=cls.ALGORITHM)
        return encoded

    @classmethod
    def decode_token(cls, token: bytes | str) -> dict:
        try:
            return jwt.decode(jwt=token, key=cls.PUBLIC_KEY, algorithms=[cls.ALGORITHM])

        except jwt.ExpiredSignatureError:
            raise InvalidTokenError


class TokenWork:
    """
    Класс для работы с токенами пользователей
    """

    def __init__(self, token_service: TokenAbstractService):
        self.token_service = token_service

    def create_tokens(self, user: UserOutput) -> tuple:
        access_jwt_payload: dict = AccessToken(sub=user.oid,
                                               first_name=user.first_name,
                                               email=user.email,
                                               role=user.role).model_dump()
        refresh_jwt_payload: dict = RefreshToken(sub=user.oid).model_dump()
        access_token = self.token_service.encode_token(payload=access_jwt_payload)
        refresh_token = self.token_service.encode_token(payload=refresh_jwt_payload)
        return access_token, refresh_token

    def refresh_access_token(self, access_token_payload: dict) -> str:
        new_access_token: str = self.token_service.encode_token(payload=access_token_payload)
        return new_access_token

    def get_current_token_payload(self,
                                  request: Request) -> dict:
        try:
            payload = request.headers.get('Authorization')
            token: str = payload.split(" ")[1]
            return self.token_service.decode_token(token=token)

        except jwt.InvalidTokenError:
            raise InvalidTokenError

    @staticmethod
    def validate_token_type(
            payload: dict,
            token_type: str,
    ) -> bool:
        current_token_type = payload.get("type")
        if current_token_type == token_type:
            return True

        raise InvalidTokenError


token_jwt_service = TokenJWTService()
token_work = TokenWork(token_jwt_service)
