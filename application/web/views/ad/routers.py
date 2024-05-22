from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, status, Query, Depends

from application.services.ad import AdvertisementService, get_ad_service
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
    return await ad_service.get_advertisement_by_id(advertisement_oid)


@router.get(path="/all",
            summary="Получение всех объявлений",
            status_code=status.HTTP_200_OK)
async def get_all_ad(ad_service: Annotated[AdvertisementService, Depends(get_ad_service)]):
    return await ad_service.get_all_advertisements()


@router.post(path="/",
             summary="Cоздание объявления",
             status_code=status.HTTP_201_CREATED,
             response_model=AdvertisementOutput)
async def add_advertisement(ad_service: Annotated[AdvertisementService, Depends(get_ad_service)],
                            user_service: Annotated[UserService, Depends(get_user_service)],
                            advertisement: AdvertisementInput) -> AdvertisementOutput:
    await user_service.check_role()
    return await ad_service.create_advertisement(advertisement_schema=advertisement)


@router.patch(path="/",
              summary="Редактирование объявления",
              status_code=status.HTTP_200_OK,
              response_model=AdvertisementOutput)
async def update_partial_advertisement(ad_service: Annotated[AdvertisementService, Depends(get_ad_service)],
                                       user_service: Annotated[UserService, Depends(get_user_service)],
                                       advertisement_oid: str,
                                       new_advertisement: AdvertisementInputUpdate) -> AdvertisementOutput:
    await user_service.check_role()
    return await ad_service.update_advertisement(advertisement_oid=advertisement_oid,
                                                 advertisement_schema=new_advertisement)


@router.delete(path="/",
               summary="Cнятие объявления",
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_advertisement(advertisement_oid: str,
                               user_service: Annotated[UserService, Depends(get_user_service)],
                               ad_service: Annotated[AdvertisementService, Depends(get_ad_service)]) -> None:
    await user_service.check_role()
    return await ad_service.update_advertisement_status_to_removed_by_id(advertisement_oid)


@router.patch(path="/status",
              summary="Изменение статус объявления",
              status_code=status.HTTP_200_OK,
              response_model=AdvertisementOutput)
async def update_status_advertisement(ad_service: Annotated[AdvertisementService, Depends(get_ad_service)],
                                      user_service: Annotated[UserService, Depends(get_user_service)],
                                      advertisement_oid: str,
                                      is_approved: bool) -> AdvertisementOutput:
    await user_service.check_role(role=("ADMIN", "MODERATOR"))
    return await ad_service.change_ad_status_on_active_or_rejected(advertisement_oid=advertisement_oid,
                                                                   is_approved=is_approved)


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
    return await ad_service.search_advertisements_by_filters(**search_params)
