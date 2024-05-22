from uuid import uuid4

from pydantic import Field as f

from application.domain.entities.base import BaseEntity


class Moderation(BaseEntity):
    advertisement_id: str = f(title="ID объявления")
    moderator_id: str = f(title="ID модератора")
    is_approved: bool = f(title="Решение", description="Опубликовать/Отправить на доработку")
    rejection_reason: str = f(title="Причина отказа", default_factory=str, max_length=250)

    @classmethod
    def from_json(cls, json: dict[str, str]) -> "Moderation":
        return cls(
            is_approved=json["is_approved"],
            rejection_reason=json["rejection_reason"],
            advertisement_id=json["advertisement_id"],
            moderator_id=json["moderator_id"],
            oid=json["oid"] if json.get("oid") else str(uuid4())
        )
