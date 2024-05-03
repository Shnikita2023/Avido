from application.exceptions.base import ApplicationException


class PhotoValidationError(ApplicationException):

    @property
    def message(self) -> str:
        return "Неверный лимит фотографий, разрешенный диапазон от 1 до 10"
