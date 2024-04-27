from fastapi import HTTPException
from pydantic import BaseModel, ConfigDict, Field, field_validator


class ModerationData(BaseModel):
    model_config = ConfigDict(strict=True)

    decision: str = Field(title="Решение")
    rejection_reason: str = Field(title="Причина отказа")
    user_id: int = Field(title="Номер пользователя")
    advertisement_id: int = Field(title="Номер объявление")

    @field_validator("decision")
    @classmethod
    def validate_status(cls, decision: str):
        if decision not in ("PUBLISH", "MODIFICATION"):
            raise HTTPException(status_code=400, detail="Некорректный статус решение модерации")
        return decision
