from dataclasses import dataclass

from application.exceptions.base import ApplicationException


@dataclass(eq=False)
class DBError(ApplicationException):
    exception: Exception

    @property
    def message(self) -> str:
        return "Ошибка подключение к базе данных"
