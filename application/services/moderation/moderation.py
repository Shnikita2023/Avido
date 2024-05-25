import asyncio
from typing import Optional

from application.domain.entities.ad import Advertisement
from application.domain.entities.moderation import Moderation as DomainModeration
from application.exceptions.domain import ModerationNotFoundError, AdvertisementNotFoundError
from application.infrastructure.unit_of_work_manager import get_unit_of_work
from application.repos.uow.unit_of_work import AbstractUnitOfWork


class ModerationService:
    uow: AbstractUnitOfWork

    def __init__(self, uow=None):
        self.uow = uow if uow else get_unit_of_work()

    async def get_moderation_by_id(self, moderation_oid: str) -> DomainModeration:
        async with self.uow:
            moderation: Optional[DomainModeration] = await self.uow.moderation.get(moderation_oid)
            if moderation:
                return moderation

            raise ModerationNotFoundError

    async def create_moderation(self, moderation: DomainModeration) -> DomainModeration:
        async with self.uow:
            advertisement: Advertisement | None = await self.uow.advertisement.get(moderation.advertisement_id)
            if not advertisement:
                raise AdvertisementNotFoundError

            if moderation.is_approved:
                advertisement.approve()
            else:
                advertisement.reject()

            await asyncio.gather(
                self.uow.moderation.add(moderation),
                self.uow.advertisement.update(advertisement)
            )
            await self.uow.commit()
        return moderation


def get_moderation_service() -> ModerationService:
    return ModerationService()
