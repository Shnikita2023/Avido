import logging
from typing import Callable
from datetime import datetime

import jwt
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from application.config import settings
from application.context import user as user_context
from application.services.user.token.token_jwt import TokenAbstractService, token_work
from application.exceptions.domain import InvalidTokenError
from application.services.user.token.cookie import get_tokens_from_cookie, create_cookie_for_tokens

logger = logging.getLogger(__name__)


class AuthMiddleware(BaseHTTPMiddleware):
    EXCLUDE_PATHS: tuple[str] = settings.auth_jwt.EXCLUDE_PATHS

    def __init__(self, app: Callable, token_service: TokenAbstractService):
        super().__init__(app)
        self.token_service: TokenAbstractService = token_service

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        try:
            if request.url.path.endswith(self.EXCLUDE_PATHS):
                return await call_next(request)

            access_token, refresh_token = await get_tokens_from_cookie(request)
            payload_access_token: dict = self.token_service.decode_token(access_token)
            payload_refresh_token: dict = self.token_service.decode_token(refresh_token)
            new_access_token: None | str = token_work.check_expires_tokens(payload_access_token, payload_refresh_token)
            if new_access_token:
                payload_access_token = self.token_service.decode_token(new_access_token)

            user_context.set(payload_access_token)
            response: Response = await call_next(request)
            if new_access_token:
                await create_cookie_for_tokens(response, new_access_token, refresh_token)

            return response

        except (jwt.PyJWTError, InvalidTokenError) as ex:
            logger.error(f"Token decoding error: {ex}")
            return JSONResponse(
                status_code=401,
                content={"status": "error", "data": f"{datetime.now()}", "detail": "Unauthorized"}
            )
