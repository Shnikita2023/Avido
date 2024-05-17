from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field as f, field_validator

from application.exceptions.domain import PhotoValidationError
from application.web.views.category_ad.schemas import CategoryOutput
from application.web.views.user.schemas import UserOutput


class BaseAdvertisement(BaseModel):
    title: str = f(title="Название", min_length=1, max_length=50)
    city: str = f(title="Город", min_length=1, max_length=50)
    description: str = f(title="Описание", default_factory=str, max_length=250)
    price: Decimal = f(title="Цена", ge=0, decimal_places=2)
    photo: list[str] = f(default_factory=list, title="Фотки", description="Ссылки на фото")

    @field_validator("photo")
    @classmethod
    def validate_photo(cls, photo: list[str]) -> list[str]:
        if 11 > len(photo) > 0:
            return photo

        raise PhotoValidationError(len(photo))


class AdvertisementInput(BaseAdvertisement):
    author: str | UserOutput = f(title="Идентификатор автора")
    category: str | CategoryOutput = f(title="Идентификатор категории")


class AdvertisementInputUpdate(BaseAdvertisement):
    title: Optional[str] = None
    city: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    photo: Optional[list[str]] = None


class AdvertisementOutput(AdvertisementInput):
    oid: str
    status: str
    approved_at: datetime | None

