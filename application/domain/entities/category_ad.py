from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field as f, field_validator

from application.exceptions.domain.category import CodeValidationError


class Category(BaseModel):
    model_config = ConfigDict(strict=True)

    oid: UUID = f(title="Идентификатор", default_factory=lambda: str(uuid4()))
    title: str = f(title="Название", min_length=1, max_length=50)
    code: str = f(title="Код", min_length=1, max_length=50)
    description: str = f(default_factory=str, title="Описание", max_length=250)

    @field_validator("code")
    @classmethod
    def validate_code(cls, code: str) -> str:
        for char in code:
            if not char.isalpha() or ord(char) > 128:
                raise CodeValidationError()
        return code
