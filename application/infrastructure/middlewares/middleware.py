import logging
from typing import Callable
from datetime import datetime

import jwt
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from application.config import settings
from application.context import user as user_context
from application.services.user.token.token_jwt import token_work
from application.exceptions.domain import InvalidTokenError


logger = logging.getLogger(__name__)


class AuthMiddleware(BaseHTTPMiddleware):
    EXCLUDE_PATHS: tuple[str] = settings.auth_jwt.EXCLUDE_PATHS

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        try:
            if request.url.path.endswith(self.EXCLUDE_PATHS):
                return await call_next(request)

            access_token, refresh_token = await token_work.get_tokens_from_headers(request)
            access_token_payload, refresh_token_payload = token_work.check_active_tokens(access_token, refresh_token)
            user_context.set(access_token_payload)
            response: Response = await call_next(request)
            return response

        except (jwt.PyJWTError, InvalidTokenError) as ex:
            logger.error(f"Token decoding error: {ex}")
            return JSONResponse(
                status_code=401,
                content={"status": "error", "data": f"{datetime.now()}", "detail": "Unauthorized"}
            )
