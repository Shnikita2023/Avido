from application.domain.exceptions.base import ApplicationException


class CodeValidationError(ApplicationException):

    @property
    def message(self) -> str:
        return "Неверное указана поля, код должен содержать латинские буквы"
