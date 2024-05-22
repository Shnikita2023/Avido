from dataclasses import dataclass
from enum import Enum

from ..value_objects.base import BaseValueObjects
from application.constants import COUNT_PHOTO_ERROR


class Status(str, Enum):
    DRAFT = "Черновик"
    ON_MODERATION = "На модерации"
    REJECTED_FOR_REVISION = "Отклонено, к доработке"
    REMOVED = "Снято/Продано"
    ACTIVE = "Опубликована"


@dataclass(frozen=True, slots=True)
class Photo(BaseValueObjects):
    value: list[str]

    def validate(self) -> None:
        if not 0 < len(self.value) < 11:
            raise ValueError(COUNT_PHOTO_ERROR)
