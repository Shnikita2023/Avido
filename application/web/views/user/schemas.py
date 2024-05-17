import re

from pydantic import BaseModel, field_validator, Field as f

from application.constants import (
    PASSWORD_LENGTH_ERROR, PASSWORD_LOWERCASE_ERROR, PASSWORD_DIGIT_ERROR,
    PASSWORD_SPECIAL_CHAR_ERROR, PASSWORD_UPPERCASE_ERROR, EMAIL_ERROR)
from application.exceptions.domain import (
    FullNameValidationError, PhoneValidationError,
    EmailValidationError, PasswordValidationError
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

    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str) -> str:
        PASSWORD_REGEX = r"[!@#$%^&*()\-_=+{};:,<.>|\[\]\\/?]"
        # Проверка на длину пароля
        if len(password) < 8 or len(password) > 50:
            raise PasswordValidationError(PASSWORD_LENGTH_ERROR)

        # Проверка на наличие хотя бы одной заглавной буквы
        if not any(c.isupper() for c in password):
            raise PasswordValidationError(PASSWORD_UPPERCASE_ERROR)

        # Проверка на наличие хотя бы одной строчной буквы
        if not any(c.islower() for c in password):
            raise PasswordValidationError(PASSWORD_LOWERCASE_ERROR)

        # Проверка на наличие хотя бы одной цифры
        if not any(c.isdigit() for c in password):
            raise PasswordValidationError(PASSWORD_DIGIT_ERROR)

        # Проверка на наличие хотя бы одного специального символа
        if not re.search(PASSWORD_REGEX, password):
            raise PasswordValidationError(PASSWORD_SPECIAL_CHAR_ERROR)

        return password

    def to_domain(self) -> User:
        return User.from_json(**self.model_dump(mode="python"))


class UserOutput(UserBase):
    oid: str
    role: str
    status: str
