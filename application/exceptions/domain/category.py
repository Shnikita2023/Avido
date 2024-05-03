from application.exceptions.base import ApplicationException


class CodeValidationError(ApplicationException):

    @property
    def message(self) -> str:
        return "Неверный формат поля, код должен содержать латинские буквы"
