from uuid import UUID

from pydantic import BaseModel, Field as f

from application.domain.moderation.moderation import Moderation


class ModerationInput(BaseModel):

    advertisement_id: UUID = f(title="ID объявления")
    moderator_id: UUID = f(title="Модератор объявления")
    is_approved: bool = f(title="Решение", description="Опубликовать/Отправить на доработку")
    rejection_reason: str = f(title="Причина отказа", default_factory=str, max_length=250)


ModerationOutput = Moderation
