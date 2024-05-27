from dataclasses import dataclass

from application.config import settings


@dataclass
class ConnectionParamsKafka:
    url: str
    topic: str
    group_id: str


data_connect_kafka = ConnectionParamsKafka(
    url=settings.kafka.url,
    topic=settings.kafka.TOPIC,
    group_id=settings.kafka.GROUP_ID,
)

