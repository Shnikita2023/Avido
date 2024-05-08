from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field as f

from application.infrastructure.bus.local import DomainCommand


class Moderation(BaseModel):
    @dataclass
    class ApproveAd(DomainCommand):
        ad_id: UUID = f(default_factory=uuid4)

    @dataclass
    class RejectAd(DomainCommand):
        ad_id: UUID = f(default_factory=uuid4)

    model_config = ConfigDict(strict=True)

    oid: UUID = f(title="Идентификатор", default_factory=uuid4)
    advertisement_id: UUID = f(title="ID объявления")
    moderator_id: UUID = f(title="ID модератора")
    moderation_date: datetime = f(title="Дата модерации", default_factory=datetime.utcnow)
    is_approved: bool = f(title="Решение", description="Опубликовать/Отправить на доработку")
    rejection_reason: str = f(title="Причина отказа", default_factory=str, max_length=250)

    @classmethod
    def from_schema(cls, schema) -> "Moderation":
        return cls(
                advertisement_id=schema.advertisement_id,
                is_approved=schema.is_approved,
                rejection_reason=schema.rejection_reason,
                moderator_id=schema.moderator_id,
            )

