from dataclasses import dataclass

from application.exceptions.base import ApplicationException


@dataclass(eq=False)
class PasswordValidationError(ApplicationException):
    text: str
    status_code = 400

    @property
    def message(self) -> str:
        return f"Неверный формат: {self.text}"


@dataclass(eq=False)
class EmailValidationError(ApplicationException):
    text: str
    status_code = 400

    @property
    def message(self) -> str:
        return f"Неверный формат: {self.text}"


@dataclass(eq=False)
class PhotoValidationError(ApplicationException):
    text: int
    status_code = 400

    @property
    def message(self) -> str:
        return f"Неверный лимит в количестве {self.text} фотографий, разрешенный диапазон от 1 до 10"


@dataclass(eq=False)
class FullNameValidationError(ApplicationException):
    text: str
    status_code = 400

    @property
    def message(self) -> str:
        return (f"Неверный формат поля: {self.text}, должно содержать от 2 до 50 символов, "
                f"только латинские буквы и начинаться с большой буквы, затем строчные")


@dataclass(eq=False)
class PhoneValidationError(ApplicationException):
    text: str
    status_code = 400

    @property
    def message(self) -> str:
        return f"Неверный формат поля phone: {self.text}, должно содержать 11 цифр и начинаться с 7 или 8"


class UserNotFoundError(ApplicationException):
    status_code = 400

    @property
    def message(self) -> str:
        return "The user was not found"


class UserAlreadyExistsError(ApplicationException):
    status_code = 400

    @property
    def message(self) -> str:
        return "The user already exists"


class InvalidUserDataError(ApplicationException):
    status_code = 400

    @property
    def message(self) -> str:
        return "Invalid username or password"


class CategoryNotFoundError(ApplicationException):
    status_code = 400

    @property
    def message(self) -> str:
        return "The category ad was not found"


class CategoryAlreadyExistsError(ApplicationException):
    status_code = 400

    @property
    def message(self) -> str:
        return "The category ad already exists"


class AdvertisementNotFoundError(ApplicationException):
    status_code = 400

    @property
    def message(self) -> str:
        return "The ad was not found"


class AdvertisementAlreadyExistsError(ApplicationException):
    status_code = 400

    @property
    def message(self) -> str:
        return "The ad already exists"


class AdvertisementStatusError(ApplicationException):
    status_code = 400

    @property
    def message(self) -> str:
        return "The ad can be edited only in DRAFT or REJECTED_FOR_REVISION"


class ModerationNotFoundError(ApplicationException):
    status_code = 400

    @property
    def message(self) -> str:
        return "The moderation was not found"


class InvalidCookieError(ApplicationException):
    status_code = 401

    @property
    def message(self) -> str:
        return "Invalid cookie"


class InvalidTokenError(ApplicationException):
    status_code = 401

    @property
    def message(self) -> str:
        return "Invalid token"


class AccessDeniedError(ApplicationException):
    status_code = 403

    @property
    def message(self) -> str:
        return "Access denied"

