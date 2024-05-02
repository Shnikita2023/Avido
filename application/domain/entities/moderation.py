from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field as f
from sqlalchemy import func

from .ad import Advertisement
from .user import User


class Moderation(BaseModel):
    model_config = ConfigDict(strict=True)

    oid: UUID = f(title="Идентификатор", default_factory=lambda: str(uuid4()))
    moderation_date: datetime = f(title="Дата модерации", default_factory=func.utcnow())
    is_approved: bool = f(title="Решение", description="Опубликовать/Отправить на доработку")
    rejection_reason: str = f(title="Причина отказа", min_length=1, max_length=250)
    user: User = f(title="Пользователь")
    advertisement: Advertisement = f(title="Объявление")
