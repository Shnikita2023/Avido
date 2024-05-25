from uuid import uuid4

from slugify import slugify
from pydantic import Field as f

from application.domain.entities.base import BaseEntity


class Category(BaseEntity):
    title: str = f(title="Название", min_length=1, max_length=50)
    code: str = f(title="Код")
    description: str = f(title="Описание", default_factory=str, max_length=250)

    @staticmethod
    def _generate_code_from_title(title: str) -> str:
        return slugify(title)

    @classmethod
    def from_json(cls, json: dict[str, str]) -> "Category":
        return cls(
            title=json["title"],
            code=cls._generate_code_from_title(json["title"]),
            description=json["description"],
            oid=json["oid"] if json.get("oid") else str(uuid4())
        )
