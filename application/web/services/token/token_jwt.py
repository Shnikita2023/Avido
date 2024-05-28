from abc import ABC, abstractmethod

import jwt
from fastapi import Request

from application.config import settings
from application.exceptions.domain import InvalidTokenError

ACCESS_TOKEN_TYPE = "access"


class TokenAbstractService(ABC):
    @abstractmethod
    def decode_token(self, token: bytes | str) -> dict:
        raise NotImplemented


class TokenJWTService(TokenAbstractService):
    """
    Класс для кодирования/декодирование jwt токена
    """
    PUBLIC_KEY: str = settings.auth_jwt.PUBLIC_KEY.read_text()
    ALGORITHM: str = settings.auth_jwt.ALGORITHM

    @classmethod
    def decode_token(cls, token: bytes | str) -> dict:
        try:
            return jwt.decode(jwt=token, key=cls.PUBLIC_KEY, algorithms=[cls.ALGORITHM])

        except jwt.ExpiredSignatureError:
            raise InvalidTokenError


class TokenManager:
    """
    Класс для работы с токенами пользователей
    """

    def __init__(self, token_service: TokenAbstractService):
        self.token_service = token_service

    async def get_current_token_payload(self, request: Request) -> dict:
        try:
            payload: str | None = request.headers.get('Authorization')
            if not payload:
                raise InvalidTokenError

            token: str = payload.split()[1]
            return self.token_service.decode_token(token=token)

        except jwt.InvalidTokenError:
            raise InvalidTokenError

    @staticmethod
    def validate_token_type(payload: dict, token_type: str) -> bool:
        current_token_type = payload.get("type")
        if current_token_type == token_type:
            return True

        raise InvalidTokenError


token_jwt_service = TokenJWTService()
token_manager = TokenManager(token_jwt_service)
