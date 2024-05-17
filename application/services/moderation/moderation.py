from typing import Optional

from application.domain.entities.moderation import Moderation as DomainModeration
from application.events import IsApprovedAd
from application.exceptions.domain import ModerationNotFoundError
from application.infrastructure.message_bus import publish
from application.infrastructure.unit_of_work_manager import get_unit_of_work
from application.repos.uow.unit_of_work import AbstractUnitOfWork
from application.web.views.moderation.schemas import ModerationInput, ModerationOutput


class ModerationService:
    uow: AbstractUnitOfWork

    def __init__(self, uow=None):
        self.uow = uow if uow else get_unit_of_work()

    async def get_moderation_by_id(self, moderation_oid: str) -> ModerationOutput:
        async with self.uow:
            moderation_entity: Optional[DomainModeration] = await self.uow.moderation.get(moderation_oid)
            if moderation_entity:
                return moderation_entity

            raise ModerationNotFoundError

    async def create_moderation(self, moderation_schema: ModerationInput) -> ModerationOutput:
        async with self.uow:
            moderation_entity: DomainModeration = DomainModeration.from_schema(moderation_schema)
            await self.uow.moderation.add(moderation_entity)
            await publish(IsApprovedAd(ad_oid=moderation_schema.advertisement_id,
                                       is_approved=moderation_schema.is_approved))
            await self.uow.commit()
            return moderation_entity


moderation_service = ModerationService()
