from pydantic import BaseModel, Field as f


class CategoryInput(BaseModel):
    title: str = f(title="Название", min_length=1, max_length=50)
    description: str = f(title="Описание", default_factory=str, max_length=250)


class CategoryOutput(CategoryInput):
    oid: str
    code: str
