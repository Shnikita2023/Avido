from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, status, Query, Depends

from application.services.ad import AdvertisementService, get_ad_service
from application.services.category_ad import CategoryAdService, get_category_ad_service
from application.services.user import UserService, get_user_service
from application.web.views.ad.schemas import AdvertisementOutput, AdvertisementInput, AdvertisementInputUpdate

router = APIRouter(prefix="/advertisement",
                   tags=["Advertisement"])


@router.get(path="/",
            summary="Получение объявления",
            status_code=status.HTTP_200_OK,
            response_model=AdvertisementOutput)
async def get_advertisement(ad_service: Annotated[AdvertisementService, Depends(get_ad_service)],
                            advertisement_oid: str) -> AdvertisementOutput:
    advertisement = await ad_service.get_advertisement_by_id(advertisement_oid)
    return AdvertisementOutput.to_schema(advertisement)


@router.get(path="/all",
            summary="Получение всех объявлений",
            status_code=status.HTTP_200_OK,
            response_model=list[AdvertisementOutput])
async def get_all_ad(ad_service: Annotated[AdvertisementService, Depends(get_ad_service)]) -> list[AdvertisementOutput]:
    advertisements = await ad_service.get_all_advertisements()
    return [AdvertisementOutput.to_schema(ad) for ad in advertisements]


@router.post(path="/",
             summary="Cоздание объявления",
             status_code=status.HTTP_201_CREATED,
             response_model=AdvertisementOutput)
async def add_advertisement(ad_service: Annotated[AdvertisementService, Depends(get_ad_service)],
                            category_service: Annotated[CategoryAdService, Depends(get_category_ad_service)],
                            user_service: Annotated[UserService, Depends(get_user_service)],
                            advertisement_schema: AdvertisementInput) -> AdvertisementOutput:
    user_service.check_user_role_allowed()
    user = await user_service.get_user_by_id(user_oid=advertisement_schema.author)
    category = await category_service.get_category_by_id(category_oid=advertisement_schema.category)
    updated_advertisement_schema = AdvertisementInput(**advertisement_schema.model_dump(exclude={"author", "category"}),
                                                      author=user,
                                                      category=category)
    advertisement = await ad_service.create_advertisement(advertisement=updated_advertisement_schema.to_domain())
    return AdvertisementOutput.to_schema(advertisement)


@router.patch(path="/",
              summary="Редактирование объявления",
              status_code=status.HTTP_200_OK,
              response_model=AdvertisementOutput)
async def update_partial_advertisement(ad_service: Annotated[AdvertisementService, Depends(get_ad_service)],
                                       user_service: Annotated[UserService, Depends(get_user_service)],
                                       advertisement_oid: str,
                                       updated_schema: AdvertisementInputUpdate) -> AdvertisementOutput:
    user_service.check_user_role_allowed()
    updated_ad = await ad_service.update_advertisement(advertisement_oid=advertisement_oid,
                                                       updated_ad=updated_schema.model_dump(exclude_none=True))

    return AdvertisementOutput.to_schema(updated_ad)


@router.delete(path="/",
               summary="Cнятие объявления",
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_advertisement(advertisement_oid: str,
                               user_service: Annotated[UserService, Depends(get_user_service)],
                               ad_service: Annotated[AdvertisementService, Depends(get_ad_service)]) -> None:
    user_service.check_user_role_allowed()
    return await ad_service.update_advertisement_status_to_removed_by_id(advertisement_oid)


@router.patch(path="/status",
              summary="Изменение статус объявления",
              status_code=status.HTTP_200_OK,
              response_model=AdvertisementOutput)
async def update_status_advertisement(ad_service: Annotated[AdvertisementService, Depends(get_ad_service)],
                                      user_service: Annotated[UserService, Depends(get_user_service)],
                                      advertisement_oid: str,
                                      is_approved: bool) -> AdvertisementOutput:
    user_service.check_user_role_allowed(role=("ADMIN", "MODERATOR"))
    updated_ad = await ad_service.change_ad_status_on_active_or_rejected(advertisement_oid=advertisement_oid,
                                                                         is_approved=is_approved)
    return AdvertisementOutput.to_schema(updated_ad)


@router.get(path="/search",
            summary="Поиск объявлений по фильтрам",
            status_code=status.HTTP_200_OK,
            response_model=list[AdvertisementOutput])
async def search_advertisement(ad_service: Annotated[AdvertisementService, Depends(get_ad_service)],
                               price_from: Decimal = Query(ge=0, default=0, decimal_places=2),
                               price_to: Decimal = Query(ge=0, default=0, decimal_places=2),
                               category: str = Query(default=None),
                               city: str = Query(default=None)) -> list[AdvertisementOutput]:
    search_params = {
        "city": city,
        "category": category,
        "price_to": price_to,
        "price_from": price_from
    }
    advertisements = await ad_service.search_advertisements_by_filters(**search_params)
    return [AdvertisementOutput.to_schema(ad) for ad in advertisements]
