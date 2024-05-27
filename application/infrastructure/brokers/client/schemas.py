from dataclasses import dataclass

from application.config import settings


@dataclass
class ConnectionParamsKafka:
    url: str
    topics: tuple
    group_id: str


data_connect_kafka = ConnectionParamsKafka(
    url=settings.kafka.url,
    topics=(settings.kafka.USER_TOPIC, settings.kafka.TOKEN_TOPIC),
    group_id=settings.kafka.GROUP_ID,
)

