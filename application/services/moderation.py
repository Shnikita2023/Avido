from datetime import datetime
from typing import Optional
from uuid import UUID

from application.domain.moderation.moderation import Moderation as DomainModeration, Moderation
from application.exceptions.domain import ModerationNotFoundError
from application.infrastructure.bus.local import publish
from application.infrastructure.unit_of_work_manager import get_unit_of_work
from application.services.ad import advertisement_service
from application.repos.uow import AbstractUnitOfWork
from application.web.views.moderation.schemas import ModerationInput, ModerationOutput


class ModerationService:
    uow: AbstractUnitOfWork

    def __init__(self, uow=None):
        self.uow = uow if uow else get_unit_of_work()

    async def get_moderation_by_id(self, moderation_oid: UUID) -> ModerationOutput:
        async with self.uow:
            moderation_entity: Optional[DomainModeration] = await self.uow.moderation.get(moderation_oid)
            if moderation_entity:
                return moderation_entity

            raise ModerationNotFoundError

    async def create_moderation(self, data: ModerationInput) -> ModerationOutput:
        data_ad = ("ACTIVE", datetime.utcnow()) if data.is_approved else ("REJECTED_FOR_REVISION", None)
        await advertisement_service.update_advertisement(advertisement_oid=data.advertisement_id,
                                                         status_ad=data_ad[0],
                                                         approved_at=data_ad[1])
        async with self.uow:
            moderation_entity: DomainModeration = DomainModeration.to_entity(data)
            await self.uow.moderation.add(moderation_entity)
            await publish(Moderation.ApproveAd(ad_id=data.advertisement_id))
            await self.uow.commit()
            return moderation_entity


moderation_service = ModerationService()
