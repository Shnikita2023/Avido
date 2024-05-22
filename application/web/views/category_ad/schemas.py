from pydantic import BaseModel, Field as f

from application.domain.entities.category_ad import Category as DomainCategory


class CategoryInput(BaseModel):
    title: str = f(title="Название", min_length=1, max_length=50)
    description: str = f(title="Описание", default_factory=str, max_length=250)

    def to_domain(self) -> DomainCategory:
        return DomainCategory.from_json(self.model_dump())


class CategoryOutput(CategoryInput):
    oid: str
    code: str

    @staticmethod
    def to_schema(category: DomainCategory) -> "CategoryOutput":
        return CategoryOutput(
            oid=category.oid,
            title=category.title,
            code=category.code,
            description=category.description
        )
