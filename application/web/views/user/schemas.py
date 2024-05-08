import re

from pydantic import BaseModel, ConfigDict, EmailStr, field_validator
from pydantic import Field as f

from application.domain.user.user import User
from application.exceptions.domain import FullNameValidationError, PhoneValidationError


class UserInput(BaseModel):
    model_config = ConfigDict(strict=True)

    first_name: str = f(title="Имя")
    last_name: str = f(title="Фамилия")
    middle_name: str | None = f(default=None, title="Отчество")
    email: EmailStr = f(title="Емайл")
    number_phone: str = f(title="Номер телефона")
    time_call: str | None = f(
        title="Время звонка",
        description="Когда удобно принимать звонки",
        default=None,
        max_length=50
    )

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


UserOutput = User


