class ApplicationException(Exception):

    @property
    def message(self) -> str:
        return "Произошла ошибка приложение"
