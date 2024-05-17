from pydantic import Field as f

from application.domain.entities.base import BaseEntity


class Moderation(BaseEntity):
    advertisement_id: str = f(title="ID объявления")
    moderator_id: str = f(title="ID модератора")
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
