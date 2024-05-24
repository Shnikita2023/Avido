from pydantic import BaseModel, Field as f


class TokenInfo(BaseModel):
    refresh_token: str | None = f(default=None)
    access_token: str
    token_type: str = f(default="Bearer")


class AccessToken(BaseModel):
    sub: str = f(title="Идентификатор токена")
    first_name: str = f(title="Имя пользователя")
    email: str = f(title="Емайл пользователя")
    role: str = f(title="Роль пользователя")
    type: str = f(default="access")


class RefreshToken(BaseModel):
    sub: str = f(title="Идентификатор токена")
    type: str = f(default="refresh")
