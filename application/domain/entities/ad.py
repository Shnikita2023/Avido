from datetime import datetime
from decimal import Decimal
from uuid import uuid4

from pydantic import Field as f

from .base import BaseEntity
from .category_ad import Category
from .user import User
from ..value_objects.ad import Status, Photo


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
    def from_json(cls, json: dict[str, str]) -> "Advertisement":
        return cls(
            title=json["title"],
            city=json["city"],
            description=json["description"],
            price=json["price"],
            photo=Photo(json["photo"]),
            author=json["author"],
            status=Status[json["status"]] if json.get("status") else Status.DRAFT,
            category=json["category"],
            oid=json["oid"] if json.get("oid") else str(uuid4())
        )

    def to_json(self) -> dict:
        return self.model_dump(exclude_none=True)

    def approve(self):
        self.status = Status.ACTIVE
        self.approved_at = datetime.utcnow()

    def reject(self):
        self.status = Status.REJECTED_FOR_REVISION
