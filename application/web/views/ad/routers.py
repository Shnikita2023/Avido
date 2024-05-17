from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, status, Query, Depends

from application.services.ad import advertisement_service
from application.services.user.user import user_service
from application.web.views.ad.schemas import AdvertisementOutput, AdvertisementInput, AdvertisementInputUpdate

router = APIRouter(prefix="/Advertisement",
                   tags=["Advertisement"])


@router.get(path="/",
            summary="Получение объявления",
            status_code=status.HTTP_200_OK,
            response_model=AdvertisementOutput)
async def get_advertisement(user_current: Annotated[dict, Depends(user_service.get_current_auth_user)],
                            advertisement_oid: str) -> AdvertisementOutput:
    return await advertisement_service.get_advertisement_by_id(user_current, advertisement_oid)


@router.get(path="/all",
            summary="Получение всех объявлений",
            status_code=status.HTTP_200_OK)
async def get_all_ad(user_current: Annotated[dict, Depends(user_service.get_current_auth_user)]):
    return await advertisement_service.get_all_advertisements(user_current=user_current)


@router.post(path="/",
             summary="Cоздание объявления",
             status_code=status.HTTP_201_CREATED,
             response_model=AdvertisementOutput)
async def add_advertisement(user_current: Annotated[dict, Depends(user_service.get_current_auth_user)],
                            advertisement: AdvertisementInput) -> AdvertisementOutput:
    await user_service.check_authentication(user_current)
    return await advertisement_service.create_advertisement(advertisement_schema=advertisement)


@router.patch(path="/",
              summary="Редактирование объявления",
              status_code=status.HTTP_200_OK,
              response_model=AdvertisementOutput)
async def update_partial_advertisement(user_current: Annotated[dict, Depends(user_service.get_current_auth_user)],
                                       advertisement_oid: str,
                                       new_advertisement: AdvertisementInputUpdate) -> AdvertisementOutput:
    await user_service.check_authentication(user_current)
    return await advertisement_service.update_advertisement(user_current=user_current,
                                                            advertisement_oid=advertisement_oid,
                                                            advertisement_schema=new_advertisement)


@router.delete(path="/",
               summary="Cнятие объявления",
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_advertisement(user_current: Annotated[dict, Depends(user_service.get_current_auth_user)],
                               advertisement_oid: str) -> None:
    await user_service.check_authentication(user_current)
    return await advertisement_service.update_advertisement_status_to_removed_by_id(user_current,
                                                                                    advertisement_oid)


@router.patch(path="/status",
              summary="Изменение статус объявления",
              status_code=status.HTTP_200_OK,
              response_model=AdvertisementOutput)
async def update_status_advertisement(user_current: Annotated[dict, Depends(user_service.get_current_auth_user)],
                                      advertisement_oid: str,
                                      is_approved: bool) -> AdvertisementOutput:
    await user_service.check_authentication(user_current=user_current, role_required=("ADMIN", "MODERATOR"))
    return await advertisement_service.change_ad_status_on_active_or_rejected(user_current=user_current,
                                                                              advertisement_oid=advertisement_oid,
                                                                              is_approved=is_approved)


@router.get(path="/search",
            summary="Поиск объявлений по фильтрам",
            status_code=status.HTTP_200_OK,
            response_model=list[AdvertisementOutput])
async def search_advertisement(price_from: Decimal = Query(ge=0, default=0, decimal_places=2),
                               price_to: Decimal = Query(ge=0, default=0, decimal_places=2),
                               category: str = Query(default=None),
                               city: str = Query(default=None)) -> list[AdvertisementOutput]:
    return await advertisement_service.search_advertisements_by_filters(city=city,
                                                                        category=category,
                                                                        price_to=price_to,
                                                                        price_from=price_from)

