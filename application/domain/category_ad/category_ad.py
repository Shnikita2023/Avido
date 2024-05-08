from uuid import UUID, uuid4

from slugify import slugify

from pydantic import BaseModel, ConfigDict, Field as f


class Category(BaseModel):
    model_config = ConfigDict(strict=True)

    oid: UUID = f(title="Идентификатор", default_factory=uuid4)
    title: str = f(title="Название", min_length=1, max_length=50)
    code: str = f(title="Код")
    description: str = f(title="Описание", default_factory=str, max_length=250)

    @staticmethod
    def _generate_code_from_title(title: str) -> str:
        return slugify(title)

    @classmethod
    def to_entity(cls, data) -> "Category":
        code: str = cls._generate_code_from_title(data.title)
        return cls(
            title=data.title,
            code=code,
            description=data.description
        )

