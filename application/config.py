from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent


class DbSettings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    ECHO: bool
    ECHO_POOL: bool
    POOL_SIZE: int
    MAX_OVERFLOW: int

    @property
    def database_url_asyncpg(self) -> str:
        return (f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@"
                f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")


class SessionCookie(BaseSettings):
    COOKIE_SESSION_KEY: str
    COOKIE_SESSION_TIME: int


class AuthJWT(BaseSettings):
    PRIVATE_KEY: Path = BASE_DIR / "certs" / "jwt-private.pem"
    PUBLIC_KEY: Path = BASE_DIR / "certs" / "jwt-public.pem"
    EXCLUDE_PATHS: str
    ALGORITHM: str = "RS256"
    ACCESS_TOKEN_EXPIRE_MINUTE: int
    REFRESH_TOKEN_EXPIRE_MINUTE: int

    @field_validator('EXCLUDE_PATHS')
    @classmethod
    def split_paths(cls, paths: str) -> tuple[str]:
        paths_list: list[str] = paths.split(',')
        return tuple(paths_list)


class KafkaSettings(BaseSettings):
    KAFKA_HOST: str
    KAFKA_PORT: int
    TOPIC: str
    GROUP_ID: str

    @property
    def url(self):
        return f"{self.KAFKA_HOST}:{self.KAFKA_PORT}"


class Settings:
    db: DbSettings = DbSettings()
    auth_jwt: AuthJWT = AuthJWT()
    session_cookie: SessionCookie = SessionCookie()
    kafka: KafkaSettings = KafkaSettings()


settings = Settings()
