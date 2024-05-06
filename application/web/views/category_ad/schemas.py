from pydantic import BaseModel, ConfigDict, Field as f

from application.domain.entities.category_ad import Category


class CategoryInput(BaseModel):
    model_config = ConfigDict(strict=True)

    title: str = f(title="Название", min_length=1, max_length=50)
    description: str = f(title="Описание", default_factory=str, max_length=250)


CategoryOutput = Category
