import re
from dataclasses import dataclass
from enum import Enum

from application.constants import (
    EMAIL_ERROR, PHONE_ERROR, FULLNAME_ERROR
)
from application.domain.value_objects.base import BaseValueObjects


@dataclass(frozen=True, slots=True)
class Email(BaseValueObjects):
    value: str

    def validate(self) -> None:
        EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        # Проверка формата email
        if not re.match(EMAIL_REGEX, self.value):
            raise ValueError(EMAIL_ERROR)


@dataclass(frozen=True, slots=True)
class Phone(BaseValueObjects):
    value: str

    def validate(self) -> None:
        if not self.value.startswith(("7", "8")) or not self.value.isdigit() or len(self.value) != 11:
            raise ValueError(PHONE_ERROR)


@dataclass(frozen=True, slots=True)
class FullName(BaseValueObjects):
    value: str

    def validate(self) -> None:
        username_regex = r"^[А-ЯЁ][а-яё]+$|^[A-Z][a-z]+$"
        if not re.match(username_regex, self.value) or len(self.value) > 50:
            raise ValueError(FULLNAME_ERROR)


class Role(str, Enum):
    ADMIN = "Администратор"
    GUEST = "Гость"
    USER = "Пользователь"
    MODERATOR = "Модератор"


class Status(str, Enum):
    ACTIVE = "Активный"
    BLOCKED = "Заблокирован"
    PENDING = "Ожидает подтверждение email"
