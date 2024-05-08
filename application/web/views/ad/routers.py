from uuid import UUID

from fastapi import APIRouter, status

from application.services.ad import advertisement_service
from application.web.views.ad.schemas import AdvertisementOutput, AdvertisementInput, AdvertisementInputUpdate

router = APIRouter(prefix="/Advertisement",
                   tags=["Advertisement"])


@router.get(path="/",
            summary="Получение объявления",
            status_code=status.HTTP_200_OK,
            response_model=AdvertisementOutput)
async def get_advertisement(advertisement_oid: UUID) -> AdvertisementOutput:
    return await advertisement_service.get_advertisement_by_id(advertisement_oid=advertisement_oid)


@router.post(path="/",
             summary="Cоздание объявления",
             status_code=status.HTTP_201_CREATED,
             response_model=AdvertisementOutput)
async def add_advertisement(advertisement: AdvertisementInput) -> AdvertisementOutput:
    return await advertisement_service.create_advertisement(data=advertisement)


@router.patch(path="/",
              summary="Редактирование объявления",
              status_code=status.HTTP_200_OK,
              response_model=AdvertisementOutput)
async def update_partial_advertisement(advertisement_oid: UUID,
                                       new_advertisement: AdvertisementInputUpdate) -> AdvertisementOutput:
    return await advertisement_service.update_advertisement(advertisement_oid=advertisement_oid,
                                                            data=new_advertisement)


@router.delete(path="/",
               summary="Cнятие объявления",
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_advertisement(advertisement_oid: UUID) -> None:
    return await advertisement_service.update_advertisement_status_to_removed_by_id(advertisement_oid)


@router.patch(path="/status",
              summary="Изменение статус объявления",
              status_code=status.HTTP_200_OK,
              response_model=AdvertisementOutput)
async def update_status_ad(advertisement_oid: UUID, status_ad: str) -> AdvertisementOutput:
    return await advertisement_service.update_advertisement(advertisement_oid=advertisement_oid,
                                                            status_ad=status_ad)
