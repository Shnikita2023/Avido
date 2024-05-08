import re
from enum import Enum
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, EmailStr, Field as f, field_validator

from application.exceptions.domain import FullNameValidationError, PhoneValidationError


class User(BaseModel):
    class Role(str, Enum):
        ADMIN = "Администратор"
        GUEST = "Гость"
        USER = "Пользователь"
        MODERATOR = "Модератор"

    class Status(str, Enum):
        ACTIVE = "Активный"
        BLOCKED = "Заблокирован"
        PENDING = "Ожидает подтверждение email"

    model_config = ConfigDict(strict=True)

    oid: UUID = f(title="Идентификатор", default_factory=uuid4)
    first_name: str = f(title="Имя")
    last_name: str = f(title="Фамилия")
    middle_name: str | None = f(default=None, title="Отчество")
    role: Role = f(title="Роль", default=Role.USER)
    email: EmailStr = f(title="Емайл")
    number_phone: str = f(title="Номер телефона")
    time_call: str | None = f(
        title="Время звонка",
        description="Когда удобно принимать звонки",
        default=None,
        max_length=50
    )
    status: Status = f(title="Статус", default=Status.PENDING)

    @field_validator("first_name", "last_name", "middle_name")
    @classmethod
    def validate_full_name(cls, value_field: str) -> str:
        username_regex = r"^[А-ЯЁ][а-яё]+$|^[A-Z][a-z]+$"
        if not re.match(username_regex, value_field) or len(value_field) > 50:
            raise FullNameValidationError(value_field)

        return value_field

    @field_validator("number_phone")
    @classmethod
    def validate_phone_number(cls, number_phone: str) -> str:
        if not number_phone.startswith(("7", "8")) or not number_phone.isdigit() or len(number_phone) != 11:
            raise PhoneValidationError(number_phone)

        return number_phone

    @classmethod
    def to_entity(cls, data) -> "User":
        return cls(
                first_name=data.first_name,
                last_name=data.last_name,
                middle_name=data.middle_name,
                email=data.email,
                number_phone=data.number_phone,
                time_call=data.time_call,
            )
