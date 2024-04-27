import re
from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserData(BaseModel):
    USERNAME_ERROR = (
        "Поля 'username, last_name, patronymic' должно содержать от 2 до 50 символов, "
        "только латинские буквы и начинаться с большой буквы, затем строчные."
    )
    USERNAME_REGEX = r"^[А-ЯЁ][а-яё]+$|^[A-Z][a-z]+$"

    model_config = ConfigDict(strict=True)

    user_id: int = Field(title="Номер пользователя")
    first_name: str = Field(title="Имя")
    last_name: str = Field(title="Фамилия")
    patronymic: Optional[str] = Field(default=None, title="Отчество")
    role: str = Field(title="Роль")
    email: EmailStr = Field(title="Емайл")
    phone_number: str = Field(title="Номер телефона")
    time_of_the_call: str = Field(title="Время звонка", description="Когда удобно принимать звонки")
    status: str = Field(title="Статус")

    @field_validator("first_name", "last_name", "patronymic")
    @classmethod
    def validate_username(cls, value_field: str):

        if not re.match(cls.USERNAME_REGEX, value_field) or len(value_field) > 50:
            raise HTTPException(status_code=400, detail=cls.USERNAME_ERROR)
        return value_field

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, phone_number: str):
        if not phone_number.startswith(("7", "8")) or not phone_number.isdigit() or len(phone_number) != 11:
            raise HTTPException(status_code=400, detail="Некорректный формат номера телефона")
        return phone_number

    @field_validator("status")
    @classmethod
    def validate_status(cls, status: str):
        if status not in ("ACTIVE", "BLOCKED", "PENDING"):
            raise HTTPException(status_code=400, detail="Некорректный статус пользователя")
        return status

    @field_validator("role")
    @classmethod
    def validate_role(cls, role: str):
        if role not in ("ADMIN", "GUEST", "USER", "MODERATOR"):
            raise HTTPException(status_code=400, detail="Некорректная роль пользователя")
        return role
