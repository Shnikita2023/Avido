from fastapi import HTTPException
from pydantic import BaseModel, ConfigDict, Field, field_validator


class AdvertisementData(BaseModel):
    model_config = ConfigDict(strict=True)

    title: str = Field(title="Название объявление", min_length=1, max_length=50)
    city: str = Field(title="Город", min_length=1, max_length=50)
    description: str = Field(title="Описание", min_length=1, max_length=250)
    price: float = Field(title="Цена")
    number_of_views: int = Field(title="Количество просмотров")
    photo: str = Field(title="Фотки", description="Ссылки на фото")
    status_ad: str = Field(title="Cтатус объявление")
    user_id: int = Field(title="Номер пользователя")
    category_id: int = Field(title="Номер категории")

    @field_validator("status_ad")
    @classmethod
    def validate_status(cls, status_ad: str):
        if status_ad not in ("DRAFT", "ON_MODERATION", "REJECTED_FOR_REVISION", "REMOVED", "ACTIVE"):
            raise HTTPException(status_code=400, detail="Некорректный статус объявление")
        return status_ad
