from application.exceptions.base import ApplicationException


class KafkaError(ApplicationException):
    status_code = 500

    @property
    def message(self) -> str:
        return "Ошибка подключение к брокеру Kafka"
