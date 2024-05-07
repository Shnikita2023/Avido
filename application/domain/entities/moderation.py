from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field as f


class Moderation(BaseModel):
    model_config = ConfigDict(strict=True)

    oid: UUID = f(title="Идентификатор", default_factory=uuid4)
    advertisement_id: UUID = f(title="ID объявления")
    moderator_id: UUID = f(title="ID модератора")
    moderation_date: datetime = f(title="Дата модерации", default_factory=datetime.utcnow)
    is_approved: bool = f(title="Решение", description="Опубликовать/Отправить на доработку")
    rejection_reason: str = f(title="Причина отказа", default_factory=str, max_length=250)

    @classmethod
    def to_entity(cls, data) -> "Moderation":
        return cls(
                advertisement_id=data.advertisement_id,
                is_approved=data.is_approved,
                rejection_reason=data.rejection_reason,
                moderator_id=data.moderator_id,
            )

