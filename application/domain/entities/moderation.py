from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field as f
from .user import User


class Moderation(BaseModel):
    model_config = ConfigDict(strict=True)

    oid: UUID = f(title="Идентификатор", default_factory=uuid4)
    advertisement_id: UUID = f(title="ID объявления")
    moderation_date: datetime = f(title="Дата модерации", default_factory=datetime.utcnow)
    is_approved: bool = f(title="Решение", description="Опубликовать/Отправить на доработку")
    rejection_reason: str = f(title="Причина отказа", default_factory=str, max_length=250)
    moderator: User = f(title="Модератор объявления")


