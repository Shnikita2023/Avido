import re
from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel, ConfigDict, EmailStr, Field as f, field_validator


class User(BaseModel):
    class Status(str, Enum):
        ACTIVE = "Активный"
        BLOCKED = "Заблокирован"
        PENDING = "Ожидает подтверждение email"

    class Role(str, Enum):
        ADMIN = "Администратор"
        GUEST = "Гость"
        USER = "Пользователь"
        MODERATOR = "Модератор"

    USERNAME_ERROR = (
        "Поля 'username, last_name, patronymic' должно содержать от 2 до 50 символов, "
        "только латинские буквы и начинаться с большой буквы, затем строчные."
    )
    USERNAME_REGEX = r"^[А-ЯЁ][а-яё]+$|^[A-Z][a-z]+$"

    model_config = ConfigDict(strict=True)

    user_id: int = f(title="Номер пользователя")
    first_name: str = f(title="Имя")
    last_name: str = f(title="Фамилия")
    patronymic: str | None = f(default=None, title="Отчество")
    role: Role = f(title="Роль")
    email: EmailStr = f(title="Емайл")
    phone_number: str = f(title="Номер телефона")
    time_of_the_call: str = f(title="Время звонка", description="Когда удобно принимать звонки")
    status: Status = f(title="Статус")

    @field_validator("first_name", "last_name", "patronymic")
    @classmethod
    def validate_username(cls, value_field: str):
        if not re.match(cls.USERNAME_REGEX, value_field) or len(value_field) > 50:
            #!TODO: Change to custom ValidationError
            raise HTTPException(status_code=400, detail=cls.USERNAME_ERROR)
        return value_field

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, phone_number: str):
        if not phone_number.startswith(("7", "8")) or not phone_number.isdigit() or len(phone_number) != 11:
            # !TODO: Change to custom ValidationError
            raise HTTPException(status_code=400, detail="Некорректный формат номера телефона")
        return phone_number

    @field_validator("status")
    @classmethod
    def validate_status(cls, status: str):
        if status not in ("ACTIVE", "BLOCKED", "PENDING"):
            # !TODO: Change to custom ValidationError
            raise HTTPException(status_code=400, detail="Некорректный статус пользователя")
        return status

    @field_validator("role")
    @classmethod
    def validate_role(cls, role: str):
        if role not in ("ADMIN", "GUEST", "USER", "MODERATOR"):
            # !TODO: Change to custom ValidationError
            raise HTTPException(status_code=400, detail="Некорректная роль пользователя")
        return role
