from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field as f

from .ad import Advertisement
from .user import User


class Moderation(BaseModel):
    model_config = ConfigDict(strict=True)

    oid: UUID = f(title="Идентификатор", default_factory=lambda: str(uuid4()))
    advertisement_id: UUID = f(title="ID Объявления")
    moderation_date: datetime = f(title="Дата модерации", default_factory=datetime.utcnow)
    is_approved: bool = f(title="Решение", description="Опубликовать/Отправить на доработку")
    rejection_reason: str = f(title="Причина отказа", default_factory=str, max_length=250)
    moderator: User = f(title="Пользователь")


