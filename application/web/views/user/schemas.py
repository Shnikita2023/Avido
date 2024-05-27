import re

from pydantic import BaseModel, field_validator, Field as f

from application.constants import EMAIL_ERROR
from application.domain.entities.user import User as DomainUser
from application.exceptions.domain import (
    FullNameValidationError, PhoneValidationError,
    EmailValidationError
)


class UserBase(BaseModel):
    first_name: str = f(title="Имя")
    last_name: str = f(title="Фамилия")
    middle_name: str | None = f(default=None, title="Отчество")
    email: str = f(title="Емайл")
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
        if not re.match(username_regex, value_field) or len(value_field) > 100:
            raise FullNameValidationError(value_field)
        return value_field

    @field_validator("number_phone")
    @classmethod
    def validate_phone_number(cls, number_phone: str) -> str:
        if not number_phone.startswith(("7", "8")) or not number_phone.isdigit() or len(number_phone) != 11:
            raise PhoneValidationError(number_phone)
        return number_phone

    @field_validator("email")
    @classmethod
    def validate_email(cls, email):
        EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        # Проверка формата email
        if not re.match(EMAIL_REGEX, email):
            raise EmailValidationError(EMAIL_ERROR)
        return email


class UserInput(UserBase):
    password: str

    def to_domain(self) -> DomainUser:
        return DomainUser.from_json(self.model_dump())


class UserOutput(UserBase):
    oid: str
    role: str
    status: str

    @staticmethod
    def to_schema(user: DomainUser) -> "UserOutput":
        return UserOutput(
            oid=user.oid,
            first_name=user.first_name.value,
            last_name=user.last_name.value,
            middle_name=user.middle_name.value,
            email=user.email.value,
            number_phone=user.number_phone.value,
            time_call=user.time_call,
            role=user.role.name,
            status=user.status.value
        )
