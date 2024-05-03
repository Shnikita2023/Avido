from application.exceptions.base import ApplicationException


class FullNameValidationError(ApplicationException):
    text: str

    @property
    def message(self) -> str:
        return (f"Неверный формат поля: {self.text}, должно содержать от 2 до 50 символов, "
                f"только латинские буквы и начинаться с большой буквы, затем строчные")


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
