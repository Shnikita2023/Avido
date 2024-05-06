class ApplicationException(Exception):
    text: str

    @property
    def message(self) -> str:
        return "Произошла ошибка приложение"
