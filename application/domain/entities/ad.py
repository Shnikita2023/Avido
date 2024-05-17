from datetime import datetime
from decimal import Decimal
from uuid import uuid4

from pydantic import Field as f

from .base import BaseEntity
from .category_ad import Category
from .user import User
from ..value_objects.ad import Status, Photo
from application.web.views.ad.schemas import AdvertisementOutput, AdvertisementInput


class Advertisement(BaseEntity):
    title: str = f(title="Название", min_length=1, max_length=50)
    city: str = f(title="Город", min_length=1, max_length=50)
    description: str = f(title="Описание", default_factory=str, max_length=250)
    price: Decimal = f(title="Цена", ge=0, decimal_places=2)
    approved_at: datetime | None = f(title="Дата публикации", default=None)
    number_of_views: int = f(default=0, title="Количество просмотров", ge=0)
    photo: Photo = f(default_factory=list, title="Фотки", description="Ссылки на фото")
    status: Status = f(title="Cтатус", default=Status.DRAFT)
    author: User = f(title="Автор")
    category: Category = f(title="Категория")

    @classmethod
    def to_entity(cls, schema: AdvertisementInput | AdvertisementOutput) -> "Advertisement":
        author: User = User.to_entity(schema.author)
        category: Category = Category.to_entity(schema.category)
        return cls(
                oid=schema.oid if isinstance(schema, AdvertisementOutput) else str(uuid4()),
                title=schema.title,
                city=schema.city,
                description=schema.description,
                price=schema.price,
                photo=Photo(schema.photo),
                status=Status[schema.status] if isinstance(schema, AdvertisementOutput) else Status.DRAFT,
                author=author,
                category=category
            )

    def to_schema(self) -> AdvertisementOutput:
        return AdvertisementOutput(
            oid=self.oid,
            title=self.title,
            city=self.city,
            description=self.description,
            price=self.price,
            photo=self.photo.value,
            status=self.status.name,
            approved_at=self.approved_at,
            author=self.author.to_schema(),
            category=self.category.to_schema()
        )
