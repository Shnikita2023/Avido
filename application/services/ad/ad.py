from datetime import datetime
from typing import Optional, Any

from application.domain.entities.ad import Advertisement as DomainAdvertisement
from application.exceptions.domain import (
    AdvertisementNotFoundError,
    AdvertisementAlreadyExistsError,
    AdvertisementStatusError, AccessDeniedError
)
from application.infrastructure.unit_of_work_manager import get_unit_of_work
from application.repos.uow.unit_of_work import AbstractUnitOfWork
from application.services.category_ad import CategoryAdService
from application.services.user import UserService
from application.web.views.ad.schemas import AdvertisementOutput, AdvertisementInput, AdvertisementInputUpdate
from application.context import user as user_context
from application.web.views.category_ad.schemas import CategoryOutput


class AdvertisementService:
    uow: AbstractUnitOfWork
    user_current: dict

    def __init__(self, uow=None):
        self.uow = uow if uow else get_unit_of_work()
        self.user_current = user_context.value

    async def get_advertisement_by_id(self, advertisement_oid: str) -> AdvertisementOutput:
        async with self.uow:
            advertisement: Optional[DomainAdvertisement] = await self.uow.advertisement.get(advertisement_oid)
            if not advertisement:
                raise AdvertisementNotFoundError

            if advertisement.status.name == "ACTIVE":
                return AdvertisementOutput.to_schema(advertisement)

            if (self.user_current.get("sub") != advertisement.author.oid and
                    self.user_current.get("role") not in ("ADMIN", "MODERATOR")):
                raise AccessDeniedError

            return AdvertisementOutput.to_schema(advertisement)

    async def get_all_advertisements(self) -> list[AdvertisementOutput]:
        async with self.uow:
            advertisements: list[DomainAdvertisement] = await self.uow.advertisement.all()
            if not advertisements:
                raise AdvertisementNotFoundError

            if self.user_current.get("role") in ("ADMIN", "MODERATOR"):
                return [AdvertisementOutput.to_schema(ad) for ad in advertisements]

            return [AdvertisementOutput.to_schema(ad) for ad in advertisements if ad.status.name == "ACTIVE"]

    async def search_advertisements_by_filters(self, **kwargs: dict) -> list[AdvertisementOutput]:
        params = {}

        for name_field, value in kwargs.items():
            if not value:
                continue

            if name_field == "category":
                param_search = {"title": value}
                category_schema: CategoryOutput = await CategoryAdService().check_existing_category(param_search)
                params["category_id"] = category_schema.oid
            else:
                params[name_field] = value

        async with self.uow:
            advertisements: list[DomainAdvertisement] = await self.uow.advertisement.get_all_by_params(params=params,
                                                                                                       offset=0,
                                                                                                       limit=20)
            if advertisements:
                return [AdvertisementOutput.to_schema(ad) for ad in advertisements]

            raise AdvertisementNotFoundError

    async def update_advertisement_status_to_removed_by_id(self, advertisement_oid: str) -> None:
        advertisement: AdvertisementOutput = await self.get_advertisement_by_id(advertisement_oid)
        if self.user_current.get("sub") != advertisement.author.oid:
            raise AccessDeniedError

        advertisement.status = "REMOVED"
        async with self.uow:
            await self.uow.advertisement.update(advertisement.to_domain())
            await self.uow.commit()

    async def create_advertisement(self, advertisement_schema: AdvertisementInput) -> AdvertisementOutput:
        async with self.uow:
            existing_ad = await self._check_existing_advertisement(title=advertisement_schema.title,
                                                                   author_id=advertisement_schema.author)
            if existing_ad:
                raise AdvertisementAlreadyExistsError

            advertisement_schema.author = await UserService().get_user_by_id(advertisement_schema.author)
            advertisement_schema.category = await CategoryAdService().get_category_by_id(advertisement_schema.category)
            advertisement: DomainAdvertisement = advertisement_schema.to_domain()
            await self.uow.advertisement.add(advertisement)
            await self.uow.commit()
            return AdvertisementOutput.to_schema(advertisement)

    async def _check_existing_advertisement(self, title: str, author_id: str) -> Optional[DomainAdvertisement]:
        params_search: dict[str, str] = {"title": title, "author_id": author_id}
        advertisement: DomainAdvertisement | None = await self.uow.advertisement.get_one_by_all_params(params_search)
        return advertisement

    async def update_advertisement(self,
                                   advertisement_oid: str,
                                   advertisement_schema: Optional[AdvertisementInputUpdate] = None
                                   ) -> AdvertisementOutput:
        advertisement: AdvertisementOutput = await self.get_advertisement_by_id(advertisement_oid)
        if self.user_current.get("sub") != advertisement.author.oid:
            raise AccessDeniedError

        if advertisement.status not in ("DRAFT", "REJECTED_FOR_REVISION"):
            raise AdvertisementStatusError

        updated_advertisement: dict[str, Any] = advertisement_schema.dict(exclude_none=True)
        for key, value in updated_advertisement.items():
            setattr(advertisement, key, value)

        async with self.uow:
            await self.uow.advertisement.update(advertisement.to_domain())
            await self.uow.commit()
            return advertisement

    async def change_ad_status_on_active_or_rejected(self,
                                                     advertisement_oid: str,
                                                     is_approved: bool) -> AdvertisementOutput:
        advertisement: AdvertisementOutput = await self.get_advertisement_by_id(advertisement_oid)
        updated_status_and_time = ("ACTIVE", datetime.utcnow()) if is_approved else ("REJECTED_FOR_REVISION", None)
        advertisement.status = updated_status_and_time[0]
        advertisement.approved_at = updated_status_and_time[1]
        async with self.uow:
            await self.uow.advertisement.update(advertisement.to_domain())
            await self.uow.commit()
            return advertisement


def get_ad_service() -> AdvertisementService:
    return AdvertisementService()
