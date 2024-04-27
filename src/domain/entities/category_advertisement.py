from pydantic import BaseModel, ConfigDict, Field


class CategoryData(BaseModel):
    model_config = ConfigDict(strict=True)

    title: str = Field(title="Название категории", min_length=1, max_length=50)
    code: str = Field(title="Код", min_length=1, max_length=50)
    description: str = Field(title="Описание", min_length=1, max_length=250)
    sort_order: int = Field(title="Порядок сортировки")
