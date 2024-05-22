from datetime import datetime
from typing import Optional

from application.domain.entities.ad import Advertisement
from application.domain.entities.moderation import Moderation as DomainModeration
from application.exceptions.domain import ModerationNotFoundError, AdvertisementNotFoundError
from application.infrastructure.unit_of_work_manager import get_unit_of_work
from application.repos.uow.unit_of_work import AbstractUnitOfWork
from application.web.views.moderation.schemas import ModerationInput, ModerationOutput


class ModerationService:
    uow: AbstractUnitOfWork

    def __init__(self, uow=None):
        self.uow = uow if uow else get_unit_of_work()

    async def get_moderation_by_id(self, moderation_oid: str) -> ModerationOutput:
        async with self.uow:
            moderation: Optional[DomainModeration] = await self.uow.moderation.get(moderation_oid)
            if moderation:
                return ModerationOutput.to_schema(moderation)

            raise ModerationNotFoundError

    async def create_moderation(self, moderation_schema: ModerationInput) -> ModerationOutput:
        async with self.uow:
            moderation: DomainModeration = moderation_schema.to_domain()
            await self.uow.moderation.add(moderation)
            advertisement: Advertisement | None = await self.uow.advertisement.get(moderation.advertisement_id)
            if advertisement:
                new_status = ("ACTIVE", datetime.utcnow()) if moderation.is_approved else ("REJECTED_FOR_REVISION", None)
                advertisement.status = new_status[0]
                advertisement.approved_at = new_status[1]
                await self.uow.advertisement.update(advertisement)
                # await publish(IsApprovedAd(ad_oid=moderation_schema.advertisement_id,
                #                            is_approved=moderation_schema.is_approved))
                await self.uow.commit()
                return ModerationOutput.to_schema(moderation)

            raise AdvertisementNotFoundError


def get_moderation_service() -> ModerationService:
    return ModerationService()
