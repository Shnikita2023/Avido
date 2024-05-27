# import logging
# from typing import Callable
# from datetime import datetime
#
# import jwt
# from fastapi import Request, Response, status as status_code
# from fastapi.responses import JSONResponse
# from starlette.middleware.base import BaseHTTPMiddleware
#
# from application.config import settings
# from application.context import user as user_context
#
# from application.exceptions.domain import InvalidTokenError
# from application.web.services.token.token_jwt import token_manager, ACCESS_TOKEN_TYPE
#
# logger = logging.getLogger(__name__)
#
#
# class AuthMiddleware(BaseHTTPMiddleware):
#     EXCLUDE_PATHS: tuple[str] = settings.auth_jwt.EXCLUDE_PATHS
#
#     async def dispatch(self, request: Request, call_next: Callable) -> Response:
#         try:
#             if request.url.path.endswith(self.EXCLUDE_PATHS):
#                 return await call_next(request)
#
#             access_token_payload: dict = await token_manager.get_current_token_payload(request=request)
#             token_manager.validate_token_type(access_token_payload, ACCESS_TOKEN_TYPE)
#             user_context.set(access_token_payload)
#             response: Response = await call_next(request)
#             return response
#
#         except (jwt.PyJWTError, InvalidTokenError) as ex:
#             logger.error(f"Token decoding error: {ex}")
#             return JSONResponse(
#                 status_code=status_code.HTTP_401_UNAUTHORIZED,
#                 content={"status": "error", "data": f"{datetime.now()}", "detail": "Unauthorized"}
#             )
