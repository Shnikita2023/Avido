from datetime import datetime
from decimal import Decimal
from enum import Enum
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field as f, field_validator
from sqlalchemy import func

from .category_ad import Category
from .user import User
from application.exceptions.domain.ad import PhotoValidationError


class Status(str, Enum):
    DRAFT = "Черновик"
    ON_MODERATION = "На модерации"
    REJECTED_FOR_REVISION = "Отклонено, к доработке"
    REMOVED = "Снято/Продано"
    ACTIVE = "Опубликована"


class Advertisement(BaseModel):
    model_config = ConfigDict(strict=True)

    oid: UUID = f(title="Идентификатор", default_factory=lambda: str(uuid4()))
    title: str = f(title="Название", min_length=1, max_length=50)
    city: str = f(title="Город", min_length=1, max_length=50)
    description: str = f(title="Описание", min_length=1, max_length=250)
    price: Decimal = f(title="Цена", ge=0)
    created_at: datetime = f(title="Дата создание", default_factory=func.utcnow())
    approved_at: datetime | None = f(title="Дата публикации", default=None)
    number_views: int = f(title="Количество просмотров", ge=0)
    photo: list[str] = f(title="Фотки", description="Ссылки на фото")
    status: Status = f(title="Cтатус")
    user: User = f(title="Пользователь")
    category: Category = f(title="Категория")

    @field_validator("photo")
    @classmethod
    def validate_photo(cls, photo: list[str]) -> list[str]:
        if 11 > len(photo) > 0:
            return photo
        raise PhotoValidationError()
