from datetime import datetime
from typing import Optional, Any
from uuid import UUID

from application.domain.ad.ad import Advertisement as DomainAdvertisement
from application.exceptions.domain import (
    AdvertisementNotFoundError,
    AdvertisementAlreadyExistsError,
    AdvertisementStatusError
)
from application.infrastructure.unit_of_work_manager import get_unit_of_work
from .category_ad import category_ad
from application.repos.uow.unit_of_work import AbstractUnitOfWork
from .user import user_service
from application.web.views.ad.schemas import AdvertisementOutput, AdvertisementInput, AdvertisementInputUpdate


class AdvertisementService:
    uow: AbstractUnitOfWork

    def __init__(self, uow=None):
        self.uow = uow if uow else get_unit_of_work()

    async def get_advertisement_by_id(self, advertisement_oid: UUID) -> AdvertisementOutput:
        async with self.uow:
            advertisement: Optional[DomainAdvertisement] = await self.uow.advertisement.get(advertisement_oid)
            if advertisement:
                return advertisement

            raise AdvertisementNotFoundError

    async def get_all_advertisements(self) -> list[AdvertisementOutput]:
        async with self.uow:
            advertisements: list[DomainAdvertisement] = await self.uow.advertisement.all()
            if advertisements:
                return [ad for ad in advertisements if ad.status.name == "ACTIVE"]

            raise AdvertisementNotFoundError

    async def update_advertisement_status_to_removed_by_id(self, advertisement_oid: UUID) -> None:
        advertisement: AdvertisementOutput = await self.get_advertisement_by_id(advertisement_oid)
        advertisement.status = advertisement.Status.REMOVED.name
        async with self.uow:
            await self.uow.advertisement.update(advertisement)
            await self.uow.commit()

    async def create_advertisement(self, data: AdvertisementInput) -> AdvertisementOutput:
        async with self.uow:
            await self._check_existing_advertisement(title=data.title, author_id=data.author_id)
            data.author_id = await user_service.get_user_by_id(data.author_id)
            data.category_id = await category_ad.get_category_by_id(data.category_id)
            advertisement_entity: DomainAdvertisement = DomainAdvertisement.to_entity(data)
            await self.uow.advertisement.add(advertisement_entity)
            await self.uow.commit()
            return advertisement_entity

    async def _check_existing_advertisement(self, title: str, author_id: UUID) -> None:
        params: dict[str, str | UUID] = {"title": title, "author_id": author_id}
        advertisement: list[DomainAdvertisement] = await self.uow.advertisement.get_by_params(params)
        if advertisement:
            raise AdvertisementAlreadyExistsError

    async def update_advertisement(self,
                                   advertisement_oid: UUID,
                                   advertisement_schema: Optional[AdvertisementInputUpdate] = None
                                   ) -> AdvertisementOutput:
        advertisement: AdvertisementOutput = await self.get_advertisement_by_id(advertisement_oid)

        if advertisement.status.name not in ("DRAFT", "REJECTED_FOR_REVISION"):
            raise AdvertisementStatusError

        updated_advertisement: dict[str, Any] = advertisement_schema.dict(exclude_none=True)
        for key, value in updated_advertisement.items():
            if key in {"status", "approved_at"}:
                continue
            setattr(advertisement, key, value)

        async with self.uow:
            await self.uow.advertisement.update(advertisement)
            await self.uow.commit()
            return advertisement


    async def approve(self):
        ...

    async def reject(self):
        ...

advertisement_service = AdvertisementService()
