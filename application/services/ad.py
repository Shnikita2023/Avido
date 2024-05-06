from typing import Optional, Any
from uuid import UUID

from application.domain.entities.ad import Advertisement as DomainAdvertisement
from application.exceptions.domain import (
    AdvertisementNotFoundError,
    AdvertisementAlreadyExistsError,
    AdvertisementStatusError
)
from application.infrastructure.unit_of_work_manager import get_unit_of_work
from application.services.category_ad import category_ad
from application.services.uof.unit_of_work import AbstractUnitOfWork
from application.services.user import user_service
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

    async def delete_advertisement_by_id(self, advertisement_oid: UUID) -> None:
        advertisement: AdvertisementOutput = await self.get_advertisement_by_id(advertisement_oid)
        advertisement.status = advertisement.Status.REMOVED.name
        async with self.uow:
            await self.uow.advertisement.update(advertisement)
            await self.uow.commit()

    async def update_partial_advertisement_by_id(self,
                                                 advertisement_oid: UUID,
                                                 data: AdvertisementInputUpdate) -> AdvertisementOutput:
        advertisement: AdvertisementOutput = await self.get_advertisement_by_id(advertisement_oid)
        if advertisement.status.name in ("DRAFT", "REJECTED_FOR_REVISION"):
            updated_advertisement: dict[str, Any] = data.dict(exclude_none=True)
            for key, value in updated_advertisement.items():
                setattr(advertisement, key, value)

            async with self.uow:
                await self.uow.advertisement.update(advertisement)
                await self.uow.commit()
                return advertisement

        raise AdvertisementStatusError

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
        advertisement = await self.uow.advertisement.get_by_params(params)
        if advertisement:
            raise AdvertisementAlreadyExistsError


advertisement_service = AdvertisementService()
