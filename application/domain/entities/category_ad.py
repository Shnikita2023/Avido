from uuid import uuid4

from slugify import slugify
from pydantic import Field as f

from application.domain.entities.base import BaseEntity
from application.web.views.category_ad.schemas import CategoryOutput, CategoryInput


class Category(BaseEntity):
    title: str = f(title="Название", min_length=1, max_length=50)
    code: str = f(title="Код")
    description: str = f(title="Описание", default_factory=str, max_length=250)

    @staticmethod
    def _generate_code_from_title(title: str) -> str:
        return slugify(title)

    @classmethod
    def to_entity(cls, schema: CategoryOutput | CategoryInput) -> "Category":
        return cls(
            oid=schema.oid if isinstance(schema, CategoryOutput) else str(uuid4()),
            title=schema.title,
            code=cls._generate_code_from_title(schema.title),
            description=schema.description
        )

    def to_schema(self) -> CategoryOutput:
        return CategoryOutput(
            oid=self.oid,
            title=self.title,
            code=self.code,
            description=self.description
        )
