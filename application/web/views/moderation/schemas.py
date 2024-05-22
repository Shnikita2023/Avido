from pydantic import BaseModel, Field as f

from application.domain.entities.moderation import Moderation as DomainModeration


class BaseModeration(BaseModel):
    is_approved: bool = f(title="Решение", description="Опубликовать/Отправить на доработку")
    rejection_reason: str = f(title="Причина отказа", default_factory=str, max_length=250)


class ModerationInput(BaseModeration):
    advertisement_id: str = f(title="ID объявления")
    moderator_id: str = f(title="Модератор объявления")

    def to_domain(self) -> DomainModeration:
        return DomainModeration.from_json(self.model_dump())


class ModerationOutput(BaseModeration):

    @staticmethod
    def to_schema(moderation: DomainModeration) -> "ModerationOutput":
        return ModerationOutput(
            oid=moderation.oid,
            is_approved=moderation.is_approved,
            rejection_reason=moderation.rejection_reason
        )
