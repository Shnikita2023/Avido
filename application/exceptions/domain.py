from dataclasses import dataclass

from application.exceptions.base import ApplicationException


class PhotoValidationError(ApplicationException):

    @property
    def message(self) -> str:
        return "Неверный лимит фотографий, разрешенный диапазон от 1 до 10"


class CodeValidationError(ApplicationException):

    @property
    def message(self) -> str:
        return "Неверный формат поля, код должен содержать латинские буквы"


@dataclass(eq=False)
class FullNameValidationError(ApplicationException):
    text: str

    @property
    def message(self) -> str:
        return (f"Неверный формат поля: {self.text}, должно содержать от 2 до 50 символов, "
                f"только латинские буквы и начинаться с большой буквы, затем строчные")


@dataclass(eq=False)
class PhoneValidationError(ApplicationException):
    text: str

    @property
    def message(self) -> str:
        return f"Неверный формат поля: {self.text}, должно содержать 11 цифр и начинаться с 7 или 8"


class UserNotFoundError(ApplicationException):

    @property
    def message(self) -> str:
        return "The user was not found"


class UserAlreadyExistsError(ApplicationException):

    @property
    def message(self) -> str:
        return "The user already exists"


class CategoryNotFoundError(ApplicationException):

    @property
    def message(self) -> str:
        return "The category ad was not found"


class CategoryAlreadyExistsError(ApplicationException):

    @property
    def message(self) -> str:
        return "The category ad already exists"


class AdvertisementNotFoundError(ApplicationException):

    @property
    def message(self) -> str:
        return "The advertisement was not found"


class AdvertisementAlreadyExistsError(ApplicationException):
    @property
    def message(self) -> str:
        return "The advertisement already exists"


class AdvertisementStatusError(ApplicationException):
    @property
    def message(self) -> str:
        return "The ad can be edited only in DRAFT or REJECTED_FOR_REVISION"
